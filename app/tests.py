from django.test import TestCase, Client
from app import models

from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .forms import *


# Create your tests here.
class ModelTests(TestCase):
    def test_create_shipping_fee(self):
        obj = models.ShippingFee.objects.create(
            city="Harare",
            amount=10.0,
            currency="USD"
        )

        self.assertIsInstance(obj, models.ShippingFee)

    def test_create_customer(self):
        obj = models.Customer.objects.create(
                    first_name="Caleb", 
                    last_name="Kandoro", 
                    email="kandoroc@hotmail.com", 
                    password="audacity123")

        self.assertIsInstance(obj, models.Customer)
        self.assertEqual(obj.full_name, "Caleb Kandoro")


    

class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        return super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = models.Customer.objects.create_superuser('user', 'admin@123.com', '123')
        cls.img = SimpleUploadedFile(name='test_image.jpg', content=open(
            'app/static/app/images/bag.jpg', 'rb').read(), content_type='image/jpeg')
        cls.dept = models.Department.objects.create(
            name='calt',
            description="desc",
            image=cls.img
        )
        cls.cate = models.Category.objects.create(
            name = 'calt',
            description="desc",
            image=cls.img,
            department=cls.dept
        )

        cls.currency = models.Currency.objects.create (
            name = 'USD',
            symbol = '$'
        )

        cls.settings = models.AppSettings.objects.create(
            promo_title = 'buy one for more',
            about_page_text = 'this is more',
            shop_address = 'corner of that street',
            default_currency = cls.currency,
            
        )

    def setUp(self):
        self.client.login(username="user", password='123')

    def test_home_page(self):
        resp = self.client.get(reverse('app:home'))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get(reverse('app:login'))
        self.assertEqual(resp.status_code, 200)
        
    def test_shopping_cart_page(self):
        resp = self.client.get(reverse('app:cart'))
        self.assertEqual(resp.status_code, 200)

    def test_account_page(self):
        resp = self.client.get(reverse('app:account'))
        self.assertEqual(resp.status_code, 200)

    def test_update_account(self):
        resp = self.client.get(reverse('app:update-account'))
        self.assertEqual(resp.status_code, 200)

    def test_discount(self):
        resp = self.client.get(reverse('app:discount'))
        self.assertEqual(resp.status_code, 200)

    def test_featured(self):
        resp = self.client.get(reverse('app:featured'))
        self.assertEqual(resp.status_code, 200)

    def test_wishlist(self):
        resp = self.client.get(reverse('app:wishlist'))
        self.assertEqual(resp.status_code, 200)

    def test_about(self):
        resp = self.client.get(reverse('app:about'))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get(reverse('app:login'))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.post(reverse('app:login'), data={
            "email":"careea@gmail.com",
            "password":"adfkdhkgadhfyryewri23783"

        })
        self.assertEqual(resp.status_code, 302)


    def test_sign_up(self):
        resp = self.client.get(reverse('app:sign-up'))
        self.assertEqual(resp.status_code, 200)

    def test_sign_up(self):
        resp = self.client.post(reverse('app:sign-up'), data={
            "first_name":"Caleb",
            "last_name" :"Rejoin",
            "email": "system@gmail.com",
            "password1":"qwertypoipidfggsf123",
            "password2": "qwertypoipidfggsf123"
        })
        # print(resp.context["form"].errors)
        self.assertEqual(resp.status_code, 302)

    def test_faq(self):
        resp = self.client.get(reverse('app:faq'))
        self.assertEqual(resp.status_code, 200)


    def test_department_page(self):
        resp = self.client.get(reverse('app:department', 
            kwargs={'pk': self.dept.pk}
            ))
        self.assertEqual(resp.status_code, 200)

    def test_category_page(self):
        resp = self.client.get(reverse('app:category',
            kwargs={'pk': self.cate.pk}
            ))
        self.assertEqual(resp.status_code, 200)



    def test_product_page(self):
        prod = models.Product.objects.create(
            name="hdskfjadhj",
            description="21weqqwe",
            unit="23",
            unit_price=34.5,
            discount=0.3,
            category= self.cate
        )
        resp = self.client.get(reverse('app:product',
                                       kwargs={'pk': prod.pk}
                                       ))
        self.assertEqual(resp.status_code, 200)

    def test_faq_page(self):
        
        faq_cat = models.FaqCategory.objects.create(
            name = "some text",
            description = "More text",
            icon = "Even more text"
        )

        faq_detail = models.FaqItem.objects.create(
            question = "is this easy?",
            answer = "supereasy barely an inconvenience",
            department = faq_cat
        )
        resp = self.client.get(reverse('app:faq-detail', 
                                            kwargs={'pk':faq_detail.pk}
                                            ))
        self.assertEqual(resp.status_code, 200)


        
    def test_payment_success(self):
        resp = self.client.get(reverse('app:payment-success'))
        self.assertEqual(resp.status_code, 302)

    def test_pending_payment(self):
        resp = self.client.get(reverse('app:pending-payment'))
        self.assertEqual(resp.status_code, 302)

    # def test_order_view(self):
    #     resp = self.client.get(reverse('app:order-view'))
    #     self.assertEqual(resp.status_code, 200)


    def test_password_reset(self):
        resp = self.client.get(reverse('app:password-reset'))
        self.assertEqual(resp.status_code, 302)

    def test_password_reset(self):
        r_request = models.PasswordRecoveryRequest.objects.create(
            user_email="admin@123.com",
            request_id="123"
        )

        resp = self.client.post(reverse('app:password-reset'), data={
            'email':'admin@123.com',
            'password': 'qwereiurgdfb3443',
            'repeat_password': 'qwereiurgdfb3443'
            
        })
        self.assertEqual(resp.status_code, 302)

        

    def test_password_reset_with_valid_recovery_request(self):
        r_request = models.PasswordRecoveryRequest.objects.create(
            user_email="kandoroc@hotmail.com",
            request_id="123"
        )
        request_count = models.PasswordRecoveryRequest.objects.all().count()
        resp = self.client.get(reverse('app:password-reset'), data={
            'email': r_request.user_email,
            'id': r_request.request_id
        })

        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(request_count, 
                            models.PasswordRecoveryRequest.objects.all().count())


    
       


        







