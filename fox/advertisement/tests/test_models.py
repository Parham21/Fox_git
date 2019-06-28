from django.test import TestCase
from ..models import Advertisement, Advertiser, Area, City, Category
from django.contrib.auth.models import User
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TestAdvertisementModels(TestCase):
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

    # def createAdvertiser(self):
    #     area = self.createArea()
    #     user = User.objects.create_user('fatemeh')
    #     exp_data = {'first_name': 'Fatemeh', 'last_name': 'Zardbani', 'email': 'F@gmail.com', 'phone': 1234321, 'sex': 'F', 'age': 20, 'area': area, 'user': user}

    #     advertiser = Advertiser.objects.create('first_name'= exp_data['first_name'], 'last_name'= exp_data['last_name'], 'email'= exp_data['email'], 'phone'= exp_data['phone'], 'sex'= exp_data['sex'], 'age'= exp_data['age'], 'area'= exp_data['area'], 'user'= exp_data['user'])
    #     advertiser.save()

    #     return advertiser
    
    def createCategory(self, name, father):
        if father is not None:
            cat = Category.objects.create(name = name, parent= father)
            cat.save()
            return cat
        cat = Category.objects.create(name=name)
        cat.save()
        return cat

    def createAdvertisement(self):
        area = self.createArea()
        advertiser = self.createAdvertiser()
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

        ad = Advertisement.objects.create(title= exp_data['title'],
            price = exp_data['price'],
            phone = exp_data['phone'],
            description = exp_data['description'],
            profile_image = exp_data['profile_image'],
            category=exp_data['category'],
            immediate = exp_data['immediate'],
            area = exp_data['area'],
            advertiser = exp_data['advertiser'] )
        
        ad.save()
        
        return ad

    def testCity(self):
        exp_data = {"name": "Tehran"}
        count = City.objects.count()
        city = self.createCity()
        self.assertEqual(City.objects.count(), count + 1)
        self.assertEqual(city.name, exp_data["name"])
