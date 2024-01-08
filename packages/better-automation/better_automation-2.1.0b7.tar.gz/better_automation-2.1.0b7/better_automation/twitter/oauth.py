async def get_oauth_auth_tokens(self) -> tuple[str | None, str | None, str | None, ClientResponse]:
    while True:
        # noinspection PyProtectedMember
        headers: dict = self.twitter_client._headers

        if headers.get('content-type'):
            del headers['content-type']
        headers[
            'accept'] = ('text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                         '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')

        if not self.twitter_client.ct0:
            # noinspection PyProtectedMember
            self.twitter_client.set_ct0(await self.twitter_client._request_ct0())

        while True:
            try:
                r = await self.twitter_client.request(url='https://memefarm-api.memecoin.org/user/twitter-auth',
                                                      method='get',
                                                      params={
                                                          'callback': 'https://www.memecoin.org/farming'
                                                      },
                                                      headers=headers)
            except better_automation.twitter.errors.BadRequest as error:
                logger.error(f'{self.account_token} | BadRequest: {error}, пробую еще раз')
            else:
                break
        if BeautifulSoup(await r[0].text(), 'lxml').find('iframe', {
            'id': 'arkose_iframe'
        }):
            logger.info(f'{self.account_token} | Обнаружена капча на аккаунте, пробую решить')
            if not await SolveCaptcha(auth_token=self.twitter_client.auth_token,
                                      ct0=self.twitter_client.ct0).solve_captcha(
                proxy=Proxy.from_str(proxy=self.account_proxy).as_url if self.account_proxy else None):
                raise exceptions.WrongCaptcha()
            continue

        if 'https://www.memecoin.org/farming?oauth_token=' in (await r[0].text()):
            return 'https://www.memecoin.org/farming?oauth_token=' + \
                   (await r[0].text()).split('https://www.memecoin.org/farming?oauth_token=')[-1].split('"')[
                       0].replace('&amp;', '&'), None, None, r[0]

        auth_token_html = BeautifulSoup(await r[0].text(), 'lxml').find('input', {
            'name': 'authenticity_token'
        })
        oauth_token_html = BeautifulSoup(await r[0].text(), 'lxml').find('input', {
            'name': 'oauth_token'
        })

        if not auth_token_html or not oauth_token_html:
            logger.error(f'{self.account_token} | Не удалось обнаружить Auth/OAuth Token на странице, '
                         f'статус: {r[0].status}')
            return None, None, None, r[0]

        auth_token: str = auth_token_html.get('value', '')
        oauth_token: str = oauth_token_html.get('value', '')
        return None, auth_token, oauth_token, r[0]


async def get_auth_location(self,
                            oauth_token: str,
                            auth_token: str) -> tuple[str | bool, str]:
    while True:
        if not self.twitter_client.ct0:
            # noinspection PyProtectedMember
            self.twitter_client.set_ct0(await self.twitter_client._request_ct0())
        # noinspection PyProtectedMember
        r = await self.twitter_client.request(url='https://api.twitter.com/oauth/authorize',
                                              method='post',
                                              data={
                                                  'authenticity_token': auth_token,
                                                  'redirect_after_login': f'https://api.twitter.com/oauth'
                                                                          f'/authorize?oauth_token={oauth_token}',
                                                  'oauth_token': oauth_token
                                              },
                                              headers={
                                                  **self.twitter_client._headers,
                                                  'content-type': 'application/x-www-form-urlencoded'
                                              })
        if 'This account is suspended' in await r[0].text():
            raise AccountSuspended(self.account_token)

        if 'https://www.memecoin.org/farming?oauth_token=' in await r[0].text():
            location: str = 'https://www.memecoin.org/farming?oauth_token=' + \
                            (await r[0].text()).split('https://www.memecoin.org/farming?oauth_token=')[-1].split(
                                '"')[0].replace('&amp;', '&')
            return location, await r[0].text()
        return False, await r[0].text()


async def make_old_auth(self,
                        oauth_token: str,
                        oauth_verifier: str) -> tuple[int, str, Response | ClientResponse]:
    while True:
        r = self.meme_client.post(url='https://memefarm-api.memecoin.org/user/twitter-auth1',
                                  json={
                                      'oauth_token': oauth_token,
                                      'oauth_verifier': oauth_verifier
                                  })

        if r.json().get('error', '') == 'account_too_new':
            return 1, '', r

        elif r.json().get('error', '') == 'Unknown Error':
            if await self.check_captcha():
                logger.info(
                    f'{self.account_token} | Обнаружена капча на аккаунте, пробую решить')

                if not await SolveCaptcha(auth_token=self.twitter_client.auth_token,
                                          ct0=self.twitter_client.ct0).solve_captcha(
                    proxy=Proxy.from_str(
                        proxy=self.account_proxy).as_url if self.account_proxy else None):
                    raise exceptions.WrongCaptcha()
                continue

            if r.json().get('status', 0) and r.json()['status'] == 429:
                logger.error(f'{self.account_token} | Неизвестный ответ при авторизации MEME: {r.text}')
                await asyncio.sleep(delay=5)
                continue

            return 2, '', r

        elif r.json().get('error', '') in ['unauthorized',
                                           'Unauthorized']:
            # noinspection PyTypeHints
            r.status: int = r.status_code
            # noinspection PyTypeHints
            r.reason: str = ''
            raise better_automation.twitter.errors.Unauthorized(r)

        elif r.json().get('accessToken', ''):
            return 0, r.json()['accessToken'], r

        return 2, '', r


async def request_access_token_old(self) -> tuple[int | None, str | None, ClientResponse | None]:
    location, auth_token, oauth_token, r = await self.get_oauth_auth_tokens()

    if not location:
        if not auth_token \
                or not oauth_token:
            logger.error(
                f'{self.account_token} | Ошибка при получении OAuth / Auth Token, '
                f'статус: {r.status}')
            return None, None, r
        location, response_text = await self.get_auth_location(oauth_token=oauth_token,
                                                               auth_token=auth_token)
        if not location:
            logger.error(
                f'{self.account_token} | Ошибка при авторизации через Twitter, '
                f'статус: {r.status}')
            return None, None, r

    if parse_qs(urlparse(location).query).get('redirect_after_login') \
            or not parse_qs(urlparse(location).query).get('oauth_token') \
            or not parse_qs(urlparse(location).query).get('oauth_verifier'):
        logger.error(
            f'{self.account_token} | Не удалось обнаружить OAuth Token / OAuth Verifier в '
            f'ссылке: {location}')
        return None, None, r

    oauth_token: str = parse_qs(urlparse(location).query)['oauth_token'][0]
    oauth_verifier: str = parse_qs(urlparse(location).query)['oauth_verifier'][0]

    return await self.make_old_auth(oauth_token=oauth_token,
                                    oauth_verifier=oauth_verifier)


##################################################################

def login(self):

    response = self.session.get(f"https://api-invite.kuscription.com/v1/info?account={self.address}")

    code = response.json()['data']['code']
    # print(code)

    if response.json()['data']['socials'] == []:
        response = self.session.get("https://api-invite.kuscription.com/v1/login_twitter")
        authUrl = response.json()['data']

        self.session.cookies.update({'auth_token': self.auth_token, 'ct0': self.csrf})
        response = self.session.get(authUrl)

        soup = BeautifulSoup(response.text, 'html.parser')
        authenticity_token = soup.find('input', attrs={'name': 'authenticity_token'}).get('value')

        payload = {'authenticity_token': authenticity_token,
                   'redirect_after_login': authUrl,
                   'oauth_token': authUrl.split("oauth_token=")[-1]}

        response = self.session.post(f'https://api.twitter.com/oauth/authorize', data=payload,
                                     headers={'content-type': 'application/x-www-form-urlencoded'})
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('a', class_='maintain-context').get('href')
        # print(link)

        response = self.session.get(link)

        verifier = link.split("oauth_verifier=")[-1]
        response = self.session.post("https://api-invite.kuscription.com/v1/auth_twitter",
                                     json={"account": self.address,
                                           "token": authUrl.split("oauth_token=")[-1],
                                           "verifier": verifier},
                                     headers={'content-type': 'application/json'})

        # if response.json()['msg'] != "SUCCESS":
        #     raise Exception("Error 1")

        # print(response.text)

    return code