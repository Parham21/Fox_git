from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse
from ..models import Advertisement, Advertiser, Area, City, Category
from ..views import *
from django.contrib.auth.models import User
import os


class TestAdvertisementViews(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')

    def createDummyCity(self):
        exp_data = {"name": "Tehran"}
        city = City.objects.create(name=exp_data['name'])
        city.save()
        return city

    def createDummyArea(self):
        city = self.createDummyCity()
        exp_data = {"name": "Tarasht", "city": city}
        area = Area.objects.create(name=exp_data['name'], city=exp_data['city'])
        area.save()
        return area

    def createDummyAdvertiser(self, name="ali", family="hatami", email="ahatami@gmail.com", phone=1234567, sex="M",
                              age=50):
        area = self.createDummyArea()
        user = User.objects.create_user(name)
        exp_data = {'first_name': name, 'last_name': family, 'email': email, 'phone': phone,
                    'sex': sex, 'age': age, 'area': area, 'user': user}
        advertiser = Advertiser.objects.create(first_name=exp_data['first_name'], last_name=exp_data['last_name'],
                                               email=exp_data['email'], phone=exp_data['phone'], sex=exp_data['sex'],
                                               age=exp_data['age'], user=exp_data['user'])
        advertiser.save()
        return advertiser

    def createDummyCategory(self, name, father):
        if father is not None:
            cat = Category.objects.create(title=name, parent=father)
            cat.save()
            return cat
        cat = Category.objects.create(title=name)
        cat.save()
        return cat

    def createDummyAdvertisement(self):
        area = self.createDummyArea()
        advertiser = self.createDummyAdvertiser()
        category = self.createDummyCategory('CAT', None)
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

    def test_view_urls_by_name(self):
        # search
        self.assertEqual(self.client.get(reverse("search")).status_code, 200)

        # advertisement search
        self.assertEqual(self.client.get(reverse("adv_search")).status_code, 200)

        # favorite ads display
        dummy_advertiser = self.createDummyAdvertiser(name="Leila", family="Hatami", email="lhatami@gmail.com",
                                                      phone=10293847, sex="F", age=40)
        dummy_advertiser.save()
        dummy_ad = self.createDummyAdvertisement()
        dummy_advertiser.favorite_ads.add(dummy_ad)
        self.client.force_login(dummy_advertiser.user)

        url = reverse("favorite_advertisement")
        rf = RequestFactory()
        req = rf.get(url)
        req.user = dummy_advertiser.user
        target_view = favorite_advertisement
        response = target_view(req)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(my_advertisements(req).status_code, 200)
        self.assertEqual(add_favorite_advertisement(req, 1).status_code, 302)
        self.assertEqual(advertisement_detail(req, 1).status_code, 200)
        self.assertEqual(home(req).status_code, 200)
        self.assertEqual(get_categories(req)[0], [1, 13, 20])
        subject = 'Report Advertisement'
        body = render_to_string('report_template', context={
            'advertisement_title': 'aaa',
            'description': 'bbbbb'
        })
        email = EmailMessage(subject=subject, body=body, to=ADMIN_MAILS)
        send_email_async(email)
        generate_random_token()
        request = RequestFactory().post(reverse('report_advertisement', args=[1]),
                                        {'description': 'A test message'})
        self.assertEqual(report_advertisement(request, 1).status_code, 302)

        request = RequestFactory().post(reverse('adv_search'),
                                        {'immediate': True,
                                         'area': self.createDummyArea(),
                                         'title': 'aaa',
                                         'minimum_price': 10,
                                         'has_image': True})
        self.assertEqual(adv_search(request).status_code, 200)


