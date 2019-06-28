from django.test import TestCase
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import logging
from ..forms import AddAdvertisementForm, AddAdvertiserForm, SearchForm
from ..models import Advertisement, Advertiser, City, Area, Category
from django.contrib.auth.models import User


class TestForm(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')

    def createCity(self):
        exp_data = {"name": "Tehran"}
        city = City.objects.create(name=exp_data['name'])
        city.save()
        return city

    def createArea(self):
        city = self.createCity()
        exp_data = {"name": "Niavaran", "city": city}
        area = Area.objects.create(name=exp_data['name'], city=exp_data['city'])
        area.save()
        return area

    def createAdvertiser(self, username, email):
        area = self.createArea()
        user = User.objects.create_user(username)
        exp_data = {'first_name': 'Fatemeh', 'last_name': 'Zardbani', 'email': email, 'phone': 1234321, 'sex': 'F',
                    'age': 20, 'area': area, 'user': user}

        advertiser = Advertiser.objects.create(first_name=exp_data['first_name'], last_name=exp_data['last_name'],
                                               email=exp_data['email'], phone=exp_data['phone'], sex=exp_data['sex'],
                                               age=exp_data['age'], user=exp_data['user'])
        advertiser.save()

        return advertiser

    def createCategory(self, name, father):
        if father is not None:
            cat = Category.objects.create(title=name, parent=father)
            cat.save()
            return cat
        cat = Category.objects.create(title=name)
        cat.save()
        return cat

    def createAdvertisement(self):
        area = self.createArea()
        advertiser = self.createAdvertiser('folan', 't@y.com')
        category = self.createCategory('CAT', None)
        exp_data = {
            'title': 'Hello',
            'price': 23,
            'phone': 1234321,
            'description': 'hey hey hey hey',
            'profile_image': self.img,
            'category': category,
            'immediate': True,
            'area': area,
            'advertiser': advertiser
        }

        ad = Advertisement.objects.create(title=exp_data['title'],
                                          price=exp_data['price'],
                                          phone=exp_data['phone'],
                                          description=exp_data['description'],
                                          profile_image=exp_data['profile_image'],
                                          category=exp_data['category'],
                                          immediate=exp_data['immediate'],
                                          area=exp_data['area'],
                                          advertiser=exp_data['advertiser'])

        ad.save()

        return ad

    def test_AddAdvertiserForm(self):
        invalid_data = {'first_name': 'Fatemeh',
                        'last_name': 'Zardbani',
                        'email': 'F@gmail.com',
                        'phone': 1234321,
                        'sex': 'F',
                        'age': 20}

        form = AddAdvertiserForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        invalid_data = {
            'username': 'hey',
            'password': '12werew',
            'first_name': 'Fatemeh',
            'last_name': 'Zardbani',
            'email': 'F@gmail.com',
            'phone': '09127784405',
            'sex': 'F',
            'favorite_ads': [],
            'age': 20}

        form = AddAdvertiserForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        invalid_data = {
            'username': 'hey',
            'password': '12werew',
            'first_name': 'Fatemeh',
            'last_name': 'Zardbani',
            'email': 'F@gmail.com',
            'phone': '09127784405',
            'sex': 'Fdsv',
            'favorite_ads': [],
            'age': 20}

        form = AddAdvertiserForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        invalid_data = {
            'username': 'hey',
            'password': '12werew',
            'first_name': 'Fatemeh',
            'last_name': 'Zardbani',
            'email': 'F@gmail.com',
            'phone': '091277805',
            'sex': 'Fdsv',
            'favorite_ads': [],
            'age': 20}

        form = AddAdvertiserForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        ad1 = self.createAdvertisement()

        invalid_data = {
            'username': 'hey',
            'password': '12werew',
            'first_name': 'Fatemeh',
            'last_name': 'Zardbani',
            'email': 'F@gmail.com',
            'phone': '09127784405',
            'sex': 'F',
            'favorite_ads': [ad1],
            'age': 20}

        form = AddAdvertiserForm(data=invalid_data)
        form.is_valid()
        self.assertFalse(form.errors)

    def test_AddAdvertisementForm(self):
        invalid_data = {
            'title': 'Hello',
            'price': 23,
            'phone': 1234321,
            'description': 'hey hey hey hey',
            'profile_image': self.img,
            'category_name': 'CAT',
            'immediate': True,
            'area_name': 'Niavaran',
            'city_name': 'Tehran',
            'advertiser_name': 'Fatemeh'
        }

        form = AddAdvertisementForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        invalid_data = {
            'title': 'Hello',
            'price': 23,
            'phone': 1234321,
            'description': 'hey hey hey hey',
            'profile_image': self.img,
            # 'category': ,
            'immediate': True,
            'area_name': 'Niavaran',
            'city_name': 'Tehran',
            'advertiser_name': 'Fatemeh'
        }

        form = AddAdvertisementForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)
