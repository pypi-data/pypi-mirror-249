from pastel_gateway_sdk.api import (LoginApi, AccountApi, ApiKeysApi, UsersApi,
                                CascadeApi, CollectionApi, NftApi, SenseApi)
from pastel_gateway_sdk import ApiClient, Configuration


class GatewayApiClientAsync:
    NETWORKS = {
        "mainnet": "https://gateway-api.pastel.network/",
        "testnet": "https://testnet.gateway-api.pastel.network/"
    }

    def __init__(self, network: str = None, custom_url: str = None):
        self.host = self.get_host(network, custom_url)
        self.api_client = self._initialize_api_client()
        self._token = None
        self._account_api = None
        self._api_keys_api = None
        self._users_api = None
        self._login_api = None
        self._cascade_api = None
        self._collection_api = None
        self._nft_api = None
        self._sense_api = None

    @staticmethod
    def get_host(network, custom_url):
        if custom_url is not None:
            return custom_url
        if network in GatewayApiClientAsync.NETWORKS:
            return GatewayApiClientAsync.NETWORKS[network]
        raise ValueError(f"Invalid network. Choose from {list(GatewayApiClientAsync.NETWORKS.keys())} "
                         f"or provide custom_url")

    def _initialize_api_client(self):
        configuration = Configuration(host=self.host)
        return ApiClient(configuration)

    async def authenticate(self, username: str, password: str):
        login_api = self.login_api
        token = await login_api.login_access_token(username=username, password=password)
        self.api_client.configuration.access_token = token.access_token
        self._token = token.access_token

    async def test_token(self):
        api = self.login_api
        user = await api.login_test_token()
        return user

    def set_auth_api_key(self, api_key):
        self.api_client.configuration.api_key["Authorization"] = api_key

    def clear_auth_api_key(self):
        self.api_client.configuration.api_key.pop("Authorization", None)

    @property
    def login_api(self):
        if self._login_api is None:
            self._login_api = LoginApi(self.api_client)
        return self._login_api

    @property
    def account_api(self):
        if self._token is None:
            raise ValueError("Please authenticate before accessing this API.")
        if self._account_api is None:
            self._account_api = AccountApi(self.api_client)
        return self._account_api

    @property
    def api_keys_api(self):
        if self._token is None:
            raise ValueError("Please authenticate before accessing this API.")
        if self._api_keys_api is None:
            self._api_keys_api = ApiKeysApi(self.api_client)
        return self._api_keys_api

    @property
    def users_api(self):
        if self._token is None:
            raise ValueError("Please authenticate before accessing this API.")
        if self._users_api is None:
            self._users_api = UsersApi(self.api_client)
        return self._users_api

    @property
    def cascade_api(self):
        if self._cascade_api is None:
            self._cascade_api = CascadeApi(self.api_client)
        return self._cascade_api

    @property
    def collection_api(self):
        if self._collection_api is None:
            self._collection_api = CollectionApi(self.api_client)
        return self._collection_api

    @property
    def nft_api(self):
        if self._nft_api is None:
            self._nft_api = NftApi(self.api_client)
        return self._nft_api

    @property
    def sense_api(self):
        if self._sense_api is None:
            self._sense_api = SenseApi(self.api_client)
        return self._sense_api
