from django.http import JsonResponse

from .services import BrawlStarsApiClient, BrawlStarsApiException


def home(request):
    return JsonResponse(data={'message': "Welcome to the app."})

def api(request):
    try:
        api = BrawlStarsApiClient(player_tag="#9RO2JCJJ")
        brawlers_response = api.get_brawlers_endpoint()
        player_response = api.get_player_endpoint()
    except BrawlStarsApiException as ex:
        return JsonResponse(status= ex.error_code, data={'message': str(ex)})
    return JsonResponse(data={'brawlers': brawlers_response, 'player': player_response})