from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import hashlib, string, random

from authentication.models import *


def index(request):
    return HttpResponse('Hi')


def register(request):
    return HttpResponse('Register')


def login(request):
    return HttpResponse('Login')


def get_last_login(request):
    return HttpResponse('Get Last Login')


def log_out_from_all_apps(request):
    return HttpResponse('Log out from all apps')
