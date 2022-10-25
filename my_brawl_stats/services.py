import requests, json
from datetime import datetime
from django.utils.timezone import make_aware

from .models import Player, Brawler, Gadget, StarPower, BrawlersHistory, UnlockedGadget, UnlockedStarPower

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

class BrawlStarsApiMapper(object):

    save_date = None

    def __save_brawler(self, brawler_item={}):
        brawler_item_id = brawler_item["id"]
        brawler = Brawler(
            id = brawler_item_id,
            name = brawler_item["name"]
        )
        brawler.save()
        for star_power_item in brawler_item["starPowers"]:
            star_power = StarPower(
                id = star_power_item["id"],
                name = star_power_item["name"],
                brawler = Brawler.objects.get(pk=brawler_item_id)
            )
            star_power.save()
        for gadget_item in brawler_item["gadgets"]:
            gadget = Gadget(
                id = gadget_item["id"],
                name = gadget_item["name"],
                brawler = Brawler.objects.get(pk=brawler_item_id)
            )
            gadget.save()

    def __save_player(self, player_item):
        player = Player(
            tag = player_item["tag"],
            name = player_item["name"],
            name_color = player_item["nameColor"],
            icon = player_item["icon"]["id"],
            trophies = player_item["trophies"],
            highest_trophies = player_item["highestTrophies"],
            highest_power_play_points = player_item["highestPowerPlayPoints"],
            exp_level = player_item["expLevel"],
            exp_points = player_item["expPoints"],
            is_qualified_from_championship_challenge = player_item["isQualifiedFromChampionshipChallenge"],
            solo_victories = player_item["soloVictories"],
            duo_victories = player_item["duoVictories"],
            normal_victories = player_item["3vs3Victories"],
            best_time_robo_rumble = player_item["bestRoboRumbleTime"],
            best_time_big_brawler = player_item["bestTimeAsBigBrawler"],
            club_tag = player_item["club"]["tag"],
            club_name = player_item["club"]["name"]
        )
        player.save()

    def __save_unlocked_brawler(self, player_tag, unlocked_brawler_item={}):
        brawler_id = unlocked_brawler_item["id"]
        brawler_history = BrawlersHistory()
        if self.__is_brawler_history_exists(player_id= player_tag, brawler_id= brawler_id):
            brawler_history = BrawlersHistory.objects.filter(brawler = brawler_id).filter(player = player_tag).first()
        brawler_history.date = self.save_date
        brawler_history.brawler = Brawler.objects.get(pk=brawler_id)
        brawler_history.player = Player.objects.get(pk=player_tag)
        brawler_history.power = unlocked_brawler_item["power"]
        brawler_history.rank = unlocked_brawler_item["rank"]
        brawler_history.trophies = unlocked_brawler_item["trophies"]
        brawler_history.highestTrophies = unlocked_brawler_item["highestTrophies"]
        brawler_history.save()
        for star_power_item in unlocked_brawler_item["starPowers"]:
            star_power_id = star_power_item["id"]
            if not self.__is_starpower_unlocked(player_tag, brawler_id, star_power_id):
                star_power = UnlockedStarPower(
                    player = Player.objects.get(pk=player_tag),
                    brawler = Brawler.objects.get(pk=brawler_id),
                    star_power = StarPower.objects.get(pk=star_power_id)
                )
                star_power.save()
        for gadget_item in unlocked_brawler_item["gadgets"]:
            gadget_id = gadget_item["id"]
            gadget = UnlockedGadget()
            if not self.__is_gadget_unlocked(player_tag, brawler_id, gadget_id):
                gadget = UnlockedGadget(
                    player = Player.objects.get(pk=player_tag),
                    brawler = Brawler.objects.get(pk=brawler_id),
                    gadget = Gadget.objects.get(pk=gadget_id)
                )
            gadget.save()

    def save_brawl_stars_data(self, brawlers_json, player_json):
        self.save_date = make_aware(datetime.now())
        if "items" in brawlers_json and "tag" in player_json and "brawlers" in player_json:
            for brawler_item in brawlers_json["items"]:
                self.__save_brawler(brawler_item= brawler_item)
            self.__save_player(player_item= player_json)
            for unlocked_brawler in player_json["brawlers"]:
                self.__save_unlocked_brawler(player_tag=player_json["tag"], unlocked_brawler_item=unlocked_brawler)
        else:
            raise BrawlStarsApiException()
    
    def __is_brawler_history_exists(self, player_id, brawler_id):
        return BrawlersHistory.objects.filter(player = player_id).filter(brawler = brawler_id).exists()
    
    def __is_starpower_unlocked(self, player_id, brawler_id, star_power_id):
        return UnlockedStarPower.objects.filter(player = player_id).filter(brawler = brawler_id).filter(star_power = star_power_id).exists()
    
    def __is_gadget_unlocked(self, player_id, brawler_id, gadget_id):
        return UnlockedGadget.objects.filter(player = player_id).filter(brawler = brawler_id).filter(gadget = gadget_id).exists()
