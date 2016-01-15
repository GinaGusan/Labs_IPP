from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import hashlib, string, random

from authentication.models import *


def index(request):
    return HttpResponse('Hi')


def register(request):
    if 'POST' == request.method:
        # print('####################', request.POST)
        context_dict = {}
        email = request.POST['email']
        password = request.POST['password']
        name_surname = request.POST['name_surname']
        app_id = request.POST['app_id']
        if check_app_existence(app_id):
            if not check_user_existence(email):
                user = create_new_user(email, name_surname, password)
                app = find_application(app_id)
                token = generate_token()
                create_new_instance(user, app, token)
                context_dict = {'code': 0, 'token': token}
            else:
                context_dict = {'code': 1}
        else:
            context_dict = {'code': 1}
        return JsonResponse(context_dict)
    else:
        return render(request, 'register.html')


def login(request):
    if 'POST' == request.method:
        context_dict = {}
        email = request.POST['email']
        password = request.POST['password']
        app_id = request.POST['app_id']
        if check_app_existence(app_id):
            if check_user_password(email, password):
                user = find_user(email)
                application = find_application(app_id)
                token = generate_token()
                context_dict['token'] = token
                context_dict['code'] = 0
                if check_instance_existence(application, user):
                    update_instance(application, user, token)
                else:
                    create_new_instance(app=application, user=user, token=token)
            else:
                context_dict['code'] = 1
        else:
            context_dict['code'] = 2
        return JsonResponse(context_dict)
    else:
        return render(request, 'login.html')


def get_last_login(request):
    if 'POST' == request.method:
        context_dict = {}
        app_id = request.POST['app_id']
        email = request.POST['email']
        token = request.POST['token']
        if check_app_existence(app_id):
                if check_user_existence(email):
                    app = find_application(app_id)
                    user = find_user(email)
                    if check_instance_existence(app, user):
                        context_dict['code'] = 0
                        context_dict['time'] = Instance.objects.filter(token=token)[0].time.strftime("%H:%M:%S, %B %d, %Y")
                    else:
                        context_dict['code'] = 3
                else:
                    context_dict['code'] = 2
        else:
            context_dict['code'] = 2
        return JsonResponse(context_dict)
    else:
        return HttpResponse('get_last_login')


def log_out_from_all_apps(request):
    if 'POST' == request.method:
        context_dict = {}
        app_id = request.POST['app_id']
        email = request.POST['email']
        token = request.POST['token']
        if check_app_existence(app_id):
                if check_user_existence(email):
                    app = find_application(app_id)
                    user = find_user(email)
                    if check_instance_existence(app, user):
                        context_dict['code'] = 0
                        log_out(user)
                    else:
                        context_dict['code'] = 3
                else:
                    context_dict['code'] = 2
        else:
            context_dict['code'] = 2
        return JsonResponse(context_dict)
    else:
        return HttpResponse('log_out_from_all_apps')


def check_app_existence(app_id):
    return Application.objects.filter(id=app_id).exists()


def check_user_existence(email):
    return User.objects.filter(email=email).exists()


def check_instance_existence(application, user):
    return Instance.objects.filter(app=application, user=user).exists()


def create_new_user(email, name_surname, password):
    user = User()
    user.email = email
    user.name_surname = name_surname
    sha1 = hashlib.sha1()
    sha1.update(password.encode())
    user.password = sha1.hexdigest()
    user.save()
    return user


def generate_token():
    source = string.ascii_letters + string.digits
    rand = random.SystemRandom()
    return ''.join(rand.choice(source) for _ in range(30))


def create_new_instance(user, app, token):
    instance = Instance()
    instance.user = user
    instance.app = app
    instance.token = token
    instance.time = timezone.now()
    instance.save()
    return instance


def check_user_password(email, password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode())
    hashed_password = sha1.hexdigest()
    return User.objects.filter(password=hashed_password, email=email).exists()


def find_user(email):
    try:
        user = User.objects.get(email=email)
        return user
    except ObjectDoesNotExist:
        return None


def find_application(app_id):
    try:
        application = Application.objects.get(id=app_id)
        return application
    except ObjectDoesNotExist:
        return None


def find_instance(application, user):
    try:
        instance = Instance.objects.get(app=application, user=user)
        return instance
    except ObjectDoesNotExist:
        return None


def update_instance(application, user, token):
    instance = find_instance(application, user)
    instance.token = token
    instance.save()


def log_out(user):
    for i in Instance.objects.filter(user=user):
        i.delete()

