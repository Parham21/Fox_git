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

    def createAdvertiser(self):
        area = self.createArea()
        user = User.objects.create_user('fatemeh')
        exp_data = {'first_name': 'Fatemeh', 'last_name': 'Zardbani', 'email': 'F@gmail.com', 'phone': 1234321, 'sex': 'F', 'age': 20, 'area': area, 'user': user}

        advertiser = Advertiser.objects.create(first_name= exp_data['first_name'], last_name= exp_data['last_name'], email= exp_data['email'], phone= exp_data['phone'], sex= exp_data['sex'], age= exp_data['age'], user= exp_data['user'])
        advertiser.save()

        return advertiser
    
    def createCategory(self, name, father):
        if father is not None:
            cat = Category.objects.create(title = name, parent= father)
            cat.save()
            return cat
        cat = Category.objects.create(title=name)
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
    
    def testArea(self):
        count = Area.objects.count()
        city = self.createCity()
        exp_data = {"name": "Niavaran", "city": city, "city_name": "Tehran"}
        area = self.createArea()
        self.assertEqual(Area.objects.count(), count + 1)
        self.assertEqual(area.name, exp_data["name"])
        self.assertEqual(area.city.name, exp_data["city_name"])
    
    def testCategory(self):
        count = Category.objects.count()
        cat = self.createCategory('greetings', None)

        cat2 = self.createCategory('hello', cat)
        cat3 = self.createCategory('bye', cat)

        self.assertEqual(Category.objects.count(), count + 3)
        self.assertEqual(cat.title, "greetings")
        self.assertEqual(cat2.title, "hello")
        self.assertEqual(cat3.title, "bye")
        self.assertEqual(cat2.parent, cat)
        self.assertEqual(cat3.parent, cat)  
        
    def testAdvertiser(self):
        count = Advertiser.objects.count()
        adv = self.createAdvertiser()
        exp_data = {'first_name': 'Fatemeh', 'last_name': 'Zardbani', 'email': 'F@gmail.com', 'phone': 1234321, 'sex': 'F', 'age': 20}

        self.assertEqual(Advertiser.objects.count(), count + 1)
        self.assertEqual(adv.first_name, exp_data['first_name'])
        self.assertEqual(adv.last_name, exp_data['last_name'])
        self.assertEqual(adv.email, exp_data['email'])
        self.assertEqual(adv.phone, exp_data['phone'])
        self.assertEqual(adv.sex, exp_data['sex'])
        self.assertEqual(adv.age, exp_data['age'])
    
    def testAdvertisement(self):
        count = Advertisement.objects.count()
        ad = self.createAdvertisement()
        exp_data = {
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

        self.assertEqual(Advertisement.objects.count(), count + 1)
        self.assertEqual(ad.title, exp_data['title'])
        self.assertEqual(ad.price, exp_data['price'])
        self.assertEqual(ad.phone, exp_data['phone'])
        self.assertEqual(ad.description, exp_data['description'])
        self.assertEqual(ad.category.title, exp_data['category_name'])
        self.assertEqual(ad.immediate, exp_data['immediate'])
        self.assertEqual(ad.area.name, exp_data['area_name'])
        self.assertEqual(ad.area.city.name, exp_data['city_name'])
        self.assertEqual(ad.advertiser.first_name, exp_data['advertiser_name'])
        
