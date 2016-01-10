from django.test import TestCase
from django.core.urlresolvers import resolve

from . import views


class  IndexViewTest(TestCase):
    def test_root(self):
        found = resolve('/')
        self.assertEqual(found.func, views.index)




class RegisterViewTest(TestCase):
    def test_register(self):
        found = resolve('/')
        self.assertEqual(found.func, views.register)



class LoginViewTest(TestCase):
    def test_login(self):
        found = resolve('/')
        self.assertEqual(found.func, views.login)



class Get_last_loginViewTest(TestCase):
    def test_get_last_login(self):
        found = resolve('/')
        self.assertEqual(found.func, views.get_last_login)



class Log_out_from_all_appsViewTest(TestCase):
    def test_log_out_from_all_apps(self):
        found = resolve('/')
        self.assertEqual(found.func, views.log_out_from_all_apps)


class ApplicationModelTest(TestCase):
    def test_application(self):
        pass



class InstanceModelTest(TestCase):
    def test_instance(self):
        pass



class UserModelTest(TestCase):
    def test_user(self):
        pass
