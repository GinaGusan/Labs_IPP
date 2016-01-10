from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hi')


def login(request):
    return HttpResponse('login')


def register(request):
    return HttpResponse('register')


def get_last_login(request):
    return HttpResponse('get_last_login')


def log_out_from_all_apps(request):
    return HttpResponse('log_out_from_all_apps')
