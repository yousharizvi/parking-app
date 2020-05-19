# -*- coding: utf-8 -*-
from flask import url_for, session

from common.tests import BaseTestCase
from common.utils import get_signer
from accounts.models import User
from parkings.models import Parking, ParkingSlot, Booking
from datetime import datetime, timedelta


class ParkingSearchTest(BaseTestCase):

    def setUp(self):
        try:
            self.user = User(
                email='user1@email.com',
                password='123456'
            ).save()
            Parking(
                display_name='Test parking lot',
                address='Plot # 123, XYZ Street, ABC City, B Country'
            ).save().pk
        except:
            pass
        self.login(email='user1@email.com',
                   password='123456', client=self.client)
        self.url = url_for('parkings_app.search')
        self.redirect_to_search = url_for('parkings_app.search')

    def tearDown(self):
        User.drop_collection()
        Parking.drop_collection()

    def test_render(self):
        resp = self.client.get(self.url)
        self.assertStatus(resp, 200)

    # test parking list
    def test_parkings(self):
        with self.captured_templates(self.app) as templates:
            resp = self.client.get(self.url)
            self.assertStatus(resp, 200)
            template, context = templates[0]
            self.assertTrue(context['parkings'])


class ParkingSlotBookingTest(BaseTestCase):

    def setUp(self):
        parking_id = None
        try:
            self.user = User(
                email='user1@email.com',
                password='123456'
            ).save()
            parking_id = Parking(
                display_name='Test parking lot',
                address='Plot # 123, XYZ Street, ABC City, B Country'
            ).save().pk
            for i in range(1, 100):
                self.parkingslot_id = ParkingSlot(
                    display_name=f'A{i}', parking_id=parking_id).save().pk
        except:
            pass
        self.login(email='user1@email.com',
                   password='123456', client=self.client)
        self.url = url_for('parkings_app.book', parking_id=parking_id)
        self.redirect_to_search = url_for('parkings_app.search')
        self.redirect_to_feedback = url_for('feedbacks_app.feedback')
        self.bookings_url = url_for('parkings_app.bookings')

    def tearDown(self):
        User.drop_collection()
        Parking.drop_collection()
        ParkingSlot.drop_collection()
        Booking.drop_collection()

    def test_render(self):
        resp = self.client.get(self.url)
        self.assertStatus(resp, 200)

    def test_parkings(self):
        # test parking slots
        with self.captured_templates(self.app) as templates:
            resp = self.client.get(self.url, data={})
            self.assertStatus(resp, 200)
            template, context = templates[0]
            self.assertTrue(context['parking'])
            self.assertTrue(context['parking_slots'])

        # test validation
        with self.captured_templates(self.app) as templates:
            resp = self.client.post(self.url)
            self.assertStatus(resp, 200)
            template, context = templates[0]
            form = context['form']
            self.assertTrue(
                'This field is required.' in form.errors['parkingslot_id'])

        # test booking
        resp = self.client.post(
            self.url,
            data=dict(
                parkingslot_id=str(self.parkingslot_id),
                date=datetime.now().strftime('%Y-%m-%d'),
                start_time=(datetime.now() + timedelta(hours=1)).strftime('%H:%M'),
                end_time=(datetime.now() +  + timedelta(hours=2)).strftime('%H:%M')
            )
        )
        self.assertRedirects(resp, self.redirect_to_feedback)


        # test booking list
        with self.captured_templates(self.app) as templates:
            self.client.get(self.bookings_url)
            template, context = templates[0]
            self.assertEqual(len(context['bookings']), 1)

