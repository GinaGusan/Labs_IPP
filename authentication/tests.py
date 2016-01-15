from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone

from . import views
from authentication.models import *

import json
import string
import datetime
import hashlib


class IndexViewTest(TestCase):
    def test_root_function(self):
        found = resolve('/')
        self.assertEqual(found.func, views.index)


class RegisterViewTest(TestCase):
    def test_register_function(self):
        found = resolve('/register/')
        self.assertEqual(found.func, views.register)

    def test_user_registration(self):
        user1 = User()
        user1.email = 'email1'
        user1.name_surname = 'name_surname'
        sha1 = hashlib.sha1()
        sha1.update(b'password1')
        user1.password = sha1.hexdigest()

        request = self.return_request()

        response = views.register(request)
        response_dict = json.loads(response.content.decode())

        user2 = User.objects.last()

        self.assertTrue(isinstance(response, JsonResponse))
        self.assertEqual(response_dict['code'], 0)
        self.assertEqual(user1, user2)

    def test_user_password_is_hashed(self):
        user1 = User()
        user1.email = 'email1'
        user1.name_surname = 'name_surname'
        sha1 = hashlib.sha1()
        sha1.update(b'password1')
        user1.password = sha1.hexdigest()

        request = self.return_request()

        response = views.register(request)
        response_dict = json.loads(response.content.decode())

        user = User.objects.last()

        self.assertNotEqual(user.password, 'password1')

    def test_user_multiple_registration(self):
        request = self.return_request()

        response = views.register(request)
        response_dict_1 = json.loads(response.content.decode())

        response = views.register(request)
        response_dict_2 = json.loads(response.content.decode())

        self.assertEqual(response_dict_1['code'], 0)
        self.assertNotEqual(response_dict_2['code'], 0)

    def return_request(self):
        application = Application()
        application.id = 1
        application.save()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['email'] = 'email1'
        request.POST['password'] = 'password1'
        request.POST['name_surname'] = 'name_surname'
        request.POST['app_id'] = 1

        return request


class LoginViewTest(TestCase):
    def test_login_function(self):
        found = resolve('/login/')
        self.assertEqual(found.func, views.login)

    def test_empty_request_return_HttpResponse(self):
        request = HttpRequest()
        response = views.login(request)

        self.assertTrue(isinstance(response, HttpResponse))

    def test_user_multiple_login_from_different_apps(self):
        request = self.return_request()

        response = views.login(request)
        response_dict_1 = json.loads(response.content.decode())

        application = Application()
        application.id = 2
        application.save()

        request.POST['app_id'] = 2

        response = views.login(request)
        response_dict_2 = json.loads(response.content.decode())

        self.assertEqual(response_dict_1['code'], 0)
        self.assertEqual(response_dict_2['code'], 0)
        self.assertNotEqual(response_dict_1['token'], response_dict_2['token'])

    def test_user_multiple_login_without_log_out_from_same_app(self):
        request = self.return_request()

        response = views.login(request)
        response_dict_1 = json.loads(response.content.decode())

        response = views.login(request)
        response_dict_2 = json.loads(response.content.decode())

        self.assertEqual(response_dict_1['code'], 0)
        self.assertEqual(response_dict_2['code'], 0)

    def return_request(self):
        application = Application()
        application.id = 1
        application.save()

        user = User()
        user.name_surname = 'name1'
        user.email = 'email1'
        sha1 = hashlib.sha1()
        sha1.update(b'password1')
        user.password = sha1.hexdigest()
        user.save()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['email'] = 'email1'
        request.POST['password'] = 'password1'
        request.POST['app_id'] = 1

        return request


class GetLastLoginViewTest(TestCase):
    def test_get_last_login_function(self):
        found = resolve('/get_last_login/')
        self.assertEqual(found.func, views.get_last_login)

    def test_get_last_login_time(self):
        application = Application()
        application.id = 1
        application.save()

        user = User()
        user.name_surname = 'name1'
        user.email = 'email1'
        sha1 = hashlib.sha1()
        sha1.update(b'password1')
        user.password = sha1.hexdigest()
        user.save()

        instance = Instance()
        instance.user = user
        instance.token = 'token1'
        instance.app = application
        instance.time = timezone.now()
        instance.save()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['email'] = 'email1'
        request.POST['token'] = 'token1'
        request.POST['app_id'] = 1

        time_begin = timezone.now()
        response = views.get_last_login(request)
        response_dict = json.loads(response.content.decode())
        time_end = timezone.now()

        response_time = datetime.datetime.strptime(response_dict['time'], "%H:%M:%S, %B %d, %Y")
        response_time = timezone.make_aware(response_time, timezone.get_current_timezone())

        self.assertEqual(response_dict['code'], 0)
        self.assertGreaterEqual((response_time - time_begin).seconds, 0)
        self.assertGreaterEqual((time_end - response_time).seconds, 0)


class LogOutFromAllAppsViewTest(TestCase):
    def test_log_out_from_all_apps_funtion(self):
        found = resolve('/log_out_from_all_apps/')
        self.assertEqual(found.func, views.log_out_from_all_apps)

    def test_log_out_from_all_apps(self):
        application = Application()
        application.id = 1
        application.save()

        user = User()
        user.name_surname = 'name1'
        user.email = 'email1'
        sha1 = hashlib.sha1()
        sha1.update(b'password1')
        user.password = sha1.hexdigest()
        user.save()

        instance1 = Instance()
        instance1.user = user
        instance1.token = 'token1'
        instance1.app = application
        instance1.time = timezone.now()
        instance1.save()

        application.id = 2
        application.save()

        instance2 = Instance()
        instance2.user = user
        instance2.app = application
        instance2.time = timezone.now()
        instance2.token = 'token2'
        instance2.save()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['email'] = 'email1'
        request.POST['token'] = 'token1'
        request.POST['app_id'] = 1

        response = views.log_out_from_all_apps(request)
        response_dict = json.loads(response.content.decode())

        self.assertEqual(response_dict['code'], 0)
        self.assertNotIn(instance1, Instance.objects.all())
        self.assertNotIn(instance2, Instance.objects.all())


class ApplicationModelTest(TestCase):
    def test_application_saving(self):
        for app in Application.objects.all():
            app.delete()

        app = Application()
        app.id = 1
        app.save()

        self.assertIn(app, Application.objects.all())


class InstanceModelTest(TestCase):
    def test_instance_saving(self):
        ApplicationModelTest().test_application_saving()
        UserModelTest().test_user_saving()

        app = Application.objects.last()
        user = User.objects.last()

        instance = Instance()
        instance.token = 'dsadsadsadas'
        instance.app = app
        instance.user = user
        instance.time = timezone.now()
        instance.save()

        self.assertIn(instance, Instance.objects.all())


class UserModelTest(TestCase):
    def test_user_saving(self):
        for user in User.objects.all():
            user.delete()

        user = User()
        user.email = 'email1'
        user.name = 'name1'
        user.password = 'password1'
        user.save()

        self.assertIn(user, User.objects.all())
