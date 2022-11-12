from django.http import JsonResponse
from django.shortcuts import render

from my_brawl_stats.services import BrawlStarsApiException

from .helpers import fetch_from_api


def home(request):
    template = 'my_brawl_stats/page_home.html'
    context = {}
    return render(request, template, context)


def brawler(request, brawlerId):
    template = 'my_brawl_stats/page_stats.html'
    context = {}
    return render(request, template, context)


def settings(request):
    template = 'my_brawl_stats/page_settings.html'
    context = {}
    return render(request, template, context)


def api(request):
    try:
        fetch_from_api()
    except BrawlStarsApiException as ex:
        return JsonResponse(status= ex.error_code, data={'message': str(ex)})
    except Exception as error:
        #TODO: Change Exception message in JsonResponse
        return JsonResponse(status= 500, data={'message': str(error)})
    return JsonResponse(data={'message': "Successfully updated."})
