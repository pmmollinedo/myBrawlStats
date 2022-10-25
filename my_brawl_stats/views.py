from django.http import JsonResponse


def home(request):
    return JsonResponse(data={'message': "Welcome to the app."})
