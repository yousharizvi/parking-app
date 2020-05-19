# -*- coding: utf-8 -*-
from flask import url_for, session

from common.tests import BaseTestCase
from common.utils import get_signer
from accounts.models import User


class LoginViewTest(BaseTestCase):

    def setUp(self):
        self.user = User(
            email='user1@email.com',
            password='123456'
        ).save()
        self.url = url_for('accounts_app.login')
        self.redirect_to = url_for('pages_app.index')
        self.redirect_to_search = url_for('parkings_app.search')

    def tearDown(self):
        User.drop_collection()

    def test_render(self):
        resp = self.client.get(self.url)
        self.assertStatus(resp, 200)

    def test_form(self):
        # test empty form
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(self.url)
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                u'This field is required.' in form.errors['email']
            )
            self.assertTrue(
                u'This field is required.' in form.errors['password']
            )

        # test validate email
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(
                self.url,
                data=dict(email='user2@email.com')
            )
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                u'Email not found.' in form.errors['email']
            )

        # test validate password
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(
                self.url,
                data=dict(email='user1@email.com', password='1234567')
            )
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                u'Incorrect password.' in form.errors['password']
            )

        # test valid form
        with self.app.test_client() as c:
            self.assertFalse('user_id' in session)
            resp = c.post(
                self.url,
                data=dict(email='user1@email.com', password='123456')
            )
            self.assertRedirects(resp, self.redirect_to)
            self.assertTrue('user_id' in session)

        # test valid form redirect
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(
                self.url,
                data=dict(email='user1@email.com', password='123456'),
                follow_redirects=True
            )
            self.assertStatus(resp, 200)
            template, context = templates[0]
            self.assertTrue(context['g'].user)

        # test valid form redirect with next parameter
        resp = self.client.post(
            self.url,
            data=dict(
                email='user1@email.com',
                password='123456',
                next=self.redirect_to_search
            )
        )
        self.assertRedirects(resp, self.redirect_to_search)


class LogoutViewTest(BaseTestCase):

    def setUp(self):
        self.user = User(
            email='user1@email.com',
            password='123456'
        ).save()
        self.url = url_for('accounts_app.logout')
        self.redirect_to = url_for('pages_app.index')
        self.redirect_to_search = url_for('parkings_app.search')

    def tearDown(self):
        User.drop_collection()

    def test_render(self):
        # test logout
        with self.app.test_client() as c:
            self.login(email='user1@email.com', password='123456', client=c)
            self.assertTrue('user_id' in session)
            resp = c.get(self.url)
            self.assertRedirects(resp, self.redirect_to)
            self.assertFalse('user_id' in session)

        # test logout with next parameter
        with self.app.test_client() as c:
            self.login(email='user1@email.com', password='123456', client=c)
            self.assertTrue('user_id' in session)
            resp = c.get(self.url + '?next=' + self.redirect_to_search)
            self.assertRedirects(resp, self.redirect_to_search)
            self.assertFalse('user_id' in session)


class SignupViewTest(BaseTestCase):

    def setUp(self):
        self.user = User(
            name='User 1',
            email='user1@email.com',
            password='123456'
        ).save()
        self.url = url_for('accounts_app.signup')
        self.redirect_to = url_for('accounts_app.login')

    def tearDown(self):
        User.drop_collection()

    def test_render(self):
        resp = self.client.get(self.url)
        self.assertStatus(resp, 200)

    def test_form(self):
        # test empty form
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(self.url)
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                u'This field is required.' in form.errors['email']
            )
            self.assertTrue(
                u'This field is required.' in form.errors['name']
            )
            self.assertTrue(
                u'This field is required.' in form.errors['password']
            )
            self.assertTrue(
                u'This field is required.' in form.errors['password_confirm']
            )

        # test validate email
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(
                self.url,
                data=dict(email='user1@email.com', password='123456', password_confirm='123456', name='User 1')
            )
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                u'E-mail in use.' in form.errors['email']
            )

        # test validate password_confirm
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(
                self.url,
                data=dict(password='123456', password_confirm='1234567')
            )
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                u'Incorrect password.' in form.errors['password_confirm']
            )
