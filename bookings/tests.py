from django.test import TestCase
from .models import User, Property, Booking
from datetime import date, timedelta
from django.core.exceptions import ValidationError


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

        self.p1 = Property(
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

        self.p2 = Property(
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

        self.p_free = Property(
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

        self.p_negative = Property(
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

        self.p_no_adults = Property(
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

        self.p_no_rooms = Property(
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
        try:
            self.p1.full_clean()
            self.p2.full_clean()
        except ValidationError:
            self.fail("Should not raise ValidationError")

    def test_invalid_property_free_price(self):
        try:
            self.p_free.full_clean()
            self.fail("Should raise ValidationError")
        except ValidationError:
            pass

    def test_invalid_property_negative_price(self):
        try:
            self.p_negative.full_clean()
            self.fail("Should raise ValidationError")
        except ValidationError:
            pass

    def test_invalid_property_adults(self):
        try:
            self.p_no_adults.full_clean()
            self.fail("Should raise ValidationError")
        except ValidationError:
            pass

    def test_invalid_property_rooms(self):
        try:
            self.p_no_rooms.full_clean()
            self.fail("Should raise ValidationError")
        except ValidationError:
            pass

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

        self.booking1 = Booking(
            tenant=self.tenant,
            property=self.property,
            initial_date=date.today(),
            final_date=date.today() + timedelta(days=3)
        )
        self.booking2 = Booking(
            tenant=self.tenant,
            property=self.property,
            initial_date=date.today(),
            final_date=date.today() + timedelta(days=3)
        )

    def test_valid_booking(self):
        try:
            self.booking1.full_clean()
        except ValidationError:
            self.fail("Should not raise ValidationError")

    def test_overlap_booking(self):
        # Repito el código anterior para que me de error de solapamiento
        try:
            self.booking1.full_clean()
            self.booking1.save()
            self.booking2.full_clean()
            self.fail("Should raise ValidationError")
        except ValidationError:
            pass