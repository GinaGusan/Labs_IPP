from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse

from . import views
from authentication.models import *

import json
import time


class  IndexViewTest(TestCase):
    def test_root_function(self):
        found = resolve('/')
        self.assertEqual(found.func, views.index)


class RegisterViewTest(TestCase):
    def test_register_function(self):
        found = resolve('/register/')
        self.assertEqual(found.func, views.register)

    def test_user_password_is_encrypted(self):
        request = HttpRequest()
        password = 'password1'
        email = 'email1'
        request.method = 'POST'
        request.POST['email'] = email
        request.POST['password'] = password

        response = views.register(request)
        response_dict = json.loads(response)

        self.assertNotEqual(password, response_dict['password'])

    def test_user_multiple_registration(self):
        request = HttpRequest()
        password = 'password1'
        email = 'email1'
        request.method = 'POST'
        request.POST['email'] = email
        request.POST['password'] = password

        response = views.register(request)
        response_dict_1 = json.loads(response)

        response = views.register(request)
        response_dict_2 = json.loads(response)

        self.assertEqual(response_dict_1['code'], 0)
        self.assertNotEqual(response_dict_2['code'], 0)


class LoginViewTest(TestCase):
    def test_login_function(self):
        found = resolve('/login/')
        self.assertEqual(found.func, views.login)

    def test_empty_request_return_HttpResponse(self):
        request = HttpRequest()
        response = views.login(request)

        self.assertTrue(isinstance(response, HttpResponse))

    def test_user_multiple_login_from_different_apps(self):
        request = HttpRequest()
        password = 'password1'
        email = 'email1'
        app_id_1 = '1'
        app_id_2 = '2'
        request.method = 'POST'
        request.POST['email'] = email
        request.POST['password'] = password
        request.POST['app_id'] = app_id_1

        response = views.register(request)
        response_dict_1 = json.loads(response)

        request.POST['app_id'] = app_id_2

        response = views.register(request)
        response_dict_2 = json.loads(response)

        self.assertEqual(response_dict_1['code'], 0)
        self.assertEqual(response_dict_2['code'], 0)
        self.assertNotEqual(response_dict_1['token'], response_dict_2['token'])

    def test_user_multiple_login_without_log_out_from_same_app(self):
        request = HttpRequest()
        password = 'password1'
        email = 'email1'
        app_id_1 = '1'
        request.method = 'POST'
        request.POST['email'] = email
        request.POST['password'] = password
        request.POST['app_id'] = app_id_1

        response = views.register(request)
        response_dict_1 = json.loads(response)

        response = views.register(request)
        response_dict_2 = json.loads(response)

        self.assertEqual(response_dict_1['code'], 0)
        self.assertNotEqual(response_dict_2['code'], 0)


class GetLastLoginViewTest(TestCase):
    def test_get_last_login_function(self):
        found = resolve('/get_last_login/')
        self.assertEqual(found.func, views.get_last_login)

    def test_get_last_login_time(self):
        request = HttpRequest()
        token = 'token1'
        email = 'email1'
        app_id = '1'
        request.method = 'POST'
        request.POST['email'] = email
        request.POST['token'] = token
        request.POST['app_id'] = app_id

        time_begin = time.strftime("%H:%M:%S, %B %d, %Y")
        response = views.register(request)
        response_dict = json.loads(response)
        time_end = time.time("%H:%M:%S, %B %d, %Y")

        self.assertLessEqual(time_begin, response_dict['time'])
        self.assertGreaterEqual(time_end, response_dict['time'])

    def test_response_code_of_wrong_request(self):
        request = HttpRequest()
        token = 'token1'
        email = 'email1'
        app_id = '1'
        request.method = 'GET'
        request.GET['email'] = email
        request.GET['token'] = token
        request.GET['app_id'] = app_id

        response = views.register(request)
        response_dict = json.loads(response)

        self.assertNotEqual(response_dict['code'], 0)


class LogOutFromAllAppsViewTest(TestCase):
    def test_log_out_from_all_apps_funtion(self):
        found = resolve('/log_out_from_all_apps/')
        self.assertEqual(found.func, views.log_out_from_all_apps)

    def test_log_out_from_all_apps(self):
        pass


class ApplicationModelTest(TestCase):
    def test_application_saving(self):
        app = Application()
        app.id = 1
        app.save()

        self.assertIn(app, Application.objects.all())


class InstanceModelTest(TestCase):
    def test_instance_saving(self):
        instance = Instance()
        instance.token = 'dsadsadsadas'
        instance.app_id = 1
        instance.email = 'email1'
        instance.save()

        self.assertIn(instance, Instance.objects.all())


class UserModelTest(TestCase):
    def test_user_saving(self):
        user = User()
        user.email = 'email1'
        user.name = 'name1'
        user.password = 'password1'
        user.save()

        self.assertIn(user, User.objects.all())
