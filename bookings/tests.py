from django.test import TestCase
from .models import User, Property, Booking
from datetime import date, timedelta


class PropertyTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(
            username="owner1",
            email="o1@test.com",
            password="123"
        )
        self.u2 = User.objects.create_user(
            username="tenant1",
            email="t1@test.com",
            password="123"
        )

        self.p1 = Property.objects.create(
            title="Apartamento Centro",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=100,
            children=2,
            adults=2,
            rooms=2,
            owner=self.u1
        )

        self.p2 = Property.objects.create(
            title="Estudio",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=10,
            children=0,
            adults=1,
            rooms=1,
            owner=self.u1
        )

        self.p_free = Property.objects.create(
            title="Error Precio",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=0,
            children=0,
            adults=1,
            rooms=1,
            owner=self.u1
        )

        self.p_negative = Property.objects.create(
            title="Error Negativo",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=-10,
            children=0,
            adults=1,
            rooms=1,
            owner=self.u1
        )

        self.p_no_adults = Property.objects.create(
            title="Error Adultos",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=50,
            children=0,
            adults=0,
            rooms=1,
            owner=self.u1
        )

        self.p_no_rooms = Property.objects.create(
            title="Error Cuartos",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=50,
            children=0,
            adults=2,
            rooms=0,
            owner=self.u1
        )

    def test_valid_property(self):
        self.assertTrue(self.p1.is_valid_property())
        self.assertTrue(self.p2.is_valid_property())

    def test_invalid_property_free_price(self):
        self.assertFalse(self.p_free.is_valid_property())

    def test_invalid_property_negative_price(self):
        self.assertFalse(self.p_negative.is_valid_property())

    def test_invalid_property_adults(self):
        self.assertFalse(self.p_no_adults.is_valid_property())

    def test_invalid_property_rooms(self):
        self.assertFalse(self.p_no_rooms.is_valid_property())


class BookingTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@test.com",
            password="123"
        )

        self.tenant = User.objects.create_user(
            username="tenant",
            email="tenant@test.com",
            password="123"
        )

        self.property = Property.objects.create(
            title="Casa Rural",
            description="Desc",
            location="Madrid",
            image="test.jpg",
            price_per_night=80,
            children=2,
            adults=2,
            rooms=2,
            owner=self.owner
        )

    def test_valid_booking(self):
        booking = Booking.objects.create(
            tenant=self.tenant,
            property=self.property,
            initial_date=date.today(),
            final_date=date.today() + timedelta(days=3)
        )
        self.assertTrue(booking.is_valid_booking())

    def test_invalid_booking_same_day(self):
        booking = Booking.objects.create(
            tenant=self.tenant,
            property=self.property,
            initial_date=date.today(),
            final_date=date.today()
        )
        self.assertFalse(booking.is_valid_booking())

    def test_invalid_booking_end_before_start(self):
        booking = Booking.objects.create(
            tenant=self.tenant,
            property=self.property,
            initial_date=date.today(),
            final_date=date.today() - timedelta(days=1)
        )
        self.assertFalse(booking.is_valid_booking())