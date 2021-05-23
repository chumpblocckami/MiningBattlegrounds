import requests
import json
import pandas as pd

class Api:
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = None

        self._api_url = "https://{0}.api.blizzard.com{1}"
        self._api_url_cn = "https://gateway.battlenet.com.cn{0}"

        self._oauth_url = "https://{0}.battle.net{1}"
        self._oauth_url_cn = "https://www.battlenet.com.cn{0}"

        self._session = requests.Session()

    def _get_client_token(self, region):
        url = self._format_oauth_url("/oauth/token", region)
        query_params = {"grant_type": "client_credentials"}

        response = self._session.post(
            url,
            params=query_params,
            auth=(self._client_id, self._client_secret),
        )

        return self._response_handler(response)

    def _response_handler(self, response):
        return response.json()

    def _request_handler(self, url, region, query_params):
        if self._access_token is None:
            json = self._get_client_token(region)
            self._access_token = json["access_token"]

        if query_params.get("access_token") is None:
            query_params["access_token"] = self._access_token

        response = self._session.get(url, params=query_params)

        return self._response_handler(response)

    def _format_api_url(self, resource, region):
        if region == "cn":
            url = self._api_url_cn.format(resource)
        else:
            url = self._api_url.format(region, resource)

        return url

    def get_resource(self, resource, region, query_params={}):
        url = self._format_api_url(resource, region)
        return self._request_handler(url, region, query_params)

    def _format_oauth_url(self, resource, region):
        if region == "cn":
            url = self._oauth_url_cn.format(resource)
        else:
            url = self._oauth_url.format(region, resource)

        return url

    def get_oauth_resource(self, resource, region, query_params={}):
        url = self._format_oauth_url(resource, region)
        return self._request_handler(url, region, query_params)

class  BG(Api):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
    def get_card(self, region, locale, id_or_slug, game_mode="constructed",**kwargs):
        if id_or_slug == "*":
            resource = f"/hearthstone/cards?"
        else:
            resource = f"/hearthstone/cards/{id_or_slug}"
        if game_mode == "battlegrounds":
            try:
                tier = kwargs["tier"]
                query_params = {"locale": locale, "game_mode": game_mode,"tier":tier}
            except:
                query_params = {"locale": locale, "game_mode": game_mode}
        return super().get_resource(resource, region, query_params)

if __name__ == "__main__":
    api_client = BG(client_id="6419ff17133b43a4bb323e5ce7f9f7c2",
                    client_secret="3Nx5SdKzdX8NtmpezdoBlfd2LQtNfort")
    for tier in range(1,7):
        cards = api_client.get_card(region="us",
                                locale="en_US",
                                id_or_slug="*",
                                game_mode="battlegrounds",
                                tier=tier)
        minion = pd.DataFrame(cards["cards"])[["name","attack","health","manaCost","text"]].set_index("name").T.to_dict()
        minion.T.to_json("./data/"+str(1)+".json")
        del minion
