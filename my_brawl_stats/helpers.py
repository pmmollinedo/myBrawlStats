from datetime import datetime

from django.utils.timezone import make_aware

from .models import Player, Brawler, Gadget, StarPower, UnlockedBrawler, BrawlerStat
from .services import BrawlStarsApiClient


def fetch_from_api():
    # BRAWL STARS API
    api = BrawlStarsApiClient(player_tag="#9RO2JCJJ")
    brawlers_response = api.get_brawlers_endpoint()
    player_response = api.get_player_endpoint()

    if ("tag" in player_response and "items" in brawlers_response):
        save_date = make_aware(datetime.now())

        # PLAYER
        player = Player(
            tag=player_response["tag"],
            name=player_response["name"],
            name_color=player_response["nameColor"],
            icon=player_response["icon"]["id"],
            trophies=player_response["trophies"],
            highest_trophies=player_response["highestTrophies"],
            highest_power_play_points=player_response["highestPowerPlayPoints"],
            exp_level=player_response["expLevel"],
            exp_points=player_response["expPoints"],
            is_qualified=player_response[
                "isQualifiedFromChampionshipChallenge"],
            solo_victories=player_response["soloVictories"],
            duo_victories=player_response["duoVictories"],
            normal_victories=player_response["3vs3Victories"],
            best_time_robo_rumble=player_response["bestRoboRumbleTime"],
            best_time_big_brawler=player_response["bestTimeAsBigBrawler"],
            club_tag=player_response["club"]["tag"],
            club_name=player_response["club"]["name"]
        )
        player.save()
        # BRAWLERS / GADGETS / STAR POWERS
        for json_brawler in brawlers_response["items"]:
            brawler = Brawler(
                id=json_brawler["id"],
                name=json_brawler["name"]
            )
            brawler.save()
            for json_gadget in json_brawler["gadgets"]:
                gadget = Gadget(
                    id=json_gadget["id"],
                    name=json_gadget["name"],
                    brawler=brawler
                )
                gadget.save()
            for json_star_power in json_brawler["starPowers"]:
                star_power = StarPower(
                    id=json_star_power["id"],
                    name=json_star_power["name"],
                    brawler=brawler
                )
                star_power.save()

        # PLAYER BRAWLERS
        for json_unlocked_brawler in player_response["brawlers"]:
            json_unlocked_brawler_id = json_unlocked_brawler["id"]
            brawler: Brawler = Brawler.objects.get(pk=json_unlocked_brawler_id)
            player.brawlers.add(brawler, through_defaults={
                                'highestTrophies': json_unlocked_brawler["highestTrophies"]})
            unlocked_brawler: UnlockedBrawler = UnlockedBrawler.objects.get(
                player=player,
                brawler=brawler
            )
            for json_unlocked_star_power in json_unlocked_brawler["starPowers"]:
                unlocked_star_power = StarPower.objects.get(
                    pk=json_unlocked_star_power["id"])
                unlocked_brawler.starpowers.add(unlocked_star_power)
            for json_unlocked_gadget in json_unlocked_brawler["gadgets"]:
                unlocked_gadget = Gadget.objects.get(
                    pk=json_unlocked_gadget["id"])
                unlocked_brawler.gadgets.add(unlocked_gadget)
            player.brawlers.add(brawler, through_defaults={})

            brawler_stats = BrawlerStat(
                unlocked_brawler=unlocked_brawler,
                date=save_date,
                power=json_unlocked_brawler["power"],
                rank=json_unlocked_brawler["rank"],
                trophies=json_unlocked_brawler["trophies"]
            )
            brawler_stats.save()
