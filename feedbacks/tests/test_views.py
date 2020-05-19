# -*- coding: utf-8 -*-
from flask import url_for, session

from common.tests import BaseTestCase
from common.utils import get_signer
from accounts.models import User
from feedbacks.models import Feedback


class ParkingSearchTest(BaseTestCase):

    def setUp(self):
        try:
            self.user = User(
                email='user1@email.com',
                password='123456'
            ).save()
        except:
            pass
        self.login(email='user1@email.com',
                   password='123456', client=self.client)
        self.url = url_for('feedbacks_app.feedback')
        self.redirect_to_search = url_for('parkings_app.search')

    def tearDown(self):
        User.drop_collection()
        Feedback.drop_collection()

    def test_render(self):
        resp = self.client.get(self.url)
        self.assertStatus(resp, 200)

    def test_feedback(self):
        # test form rendering
        with self.captured_templates(self.app) as templates:
            resp = self.client.get(self.url)
            self.assertStatus(resp, 200)
            template, context = templates[0]
            self.assertTrue(context['form'])
            self.assertTrue(context['form'].rating)
            self.assertTrue(context['form'].message)

        # test validation
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(self.url)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                'Number must be between 0 and 5.' in form.errors['rating'])

        # test feedback success
        resp = self.client.post(
            self.url,
            data=dict(
                rating=4,
                message='This is a feedback message'
            ))
        self.assertRedirects(resp, self.redirect_to_search)
