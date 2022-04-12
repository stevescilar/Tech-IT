from django.http import HttpResponse


def home(request):
    return HttpResponse(' We are at home')