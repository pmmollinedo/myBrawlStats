import requests, json

# Constants for BrawlStarsAPI
HOST = "https://api.brawlstars.com/v1/"
BRAWLERS_ENDPOINT = "brawlers/"
PLAYERS_ENDPOINT = "players/"
API_KEY = "Bearer <INSERT_YOUR_API_KEY_HERE>"

class BrawlStarsApiException(Exception):

    def __init__(self, message="", error_code=400) -> None:
        super().__init__(message)
        self.error_code = error_code

    def __str__(self) -> str:
        if self.error_code == 403:
            return "Access denied. Check if your BrawlStarsAPI Token is valid."
        elif self.error_code >= 500:
            return "The request to the Brawl Stars API returned a server error."
        elif self.error_code >= 400:
            return "There is something wrong with your request."

class BrawlStarsApiClient(object):

    player_tag = None

    def __init__(self, player_tag) -> None:
        self.player_tag = player_tag

    def __generate_headers(self):
        headers = {"Authorization": API_KEY}
        return headers

    def __call_api(self, url):
        response = requests.get(url=url,headers=self.__generate_headers())
        json_response = json.loads(response.text)
        if response.status_code == 200:
            return json_response
        else:
            raise BrawlStarsApiException(error_code= response.status_code)

    def get_player_endpoint(self):
        url = HOST + PLAYERS_ENDPOINT + self.player_tag.replace("#","%23")
        try:
            return self.__call_api(url=url)
        except BrawlStarsApiException as apiEx:
            raise apiEx
    
    def get_brawlers_endpoint(self):
        url = HOST + BRAWLERS_ENDPOINT
        try:
            return self.__call_api(url=url)
        except BrawlStarsApiException as apiEx:
            raise apiEx
