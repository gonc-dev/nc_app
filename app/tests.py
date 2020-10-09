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

    def test_create_product(self):
        obj = models.Product.objects.create(
            name = "some_product",
            description = "something interesting about this product",
            unit = "each",
            unit_price = 123344555.00,
            featured = "",
            discount = 8.00
        )

        self.assertIsInstance(obj, models.Product)

        sku = models.SKU.objects.create(
            sku_id = "gaksjb",
            attribute = "somthe",
            value = "12",
            product = obj,
            quantity = 123
        )

        self.assertEqual(obj.quantity_in_stock, 123)
        self.assertTrue(obj.in_stock)
        self.assertEqual(obj.discounted_price, 113476990.60)
        self.assertFalse(obj.primary_photo_url)
        self.assertTrue(obj.save, 2)


    def test_create_department(self):
        obj = models.Department.objects.create(
            name = "some department",
            description = "about a department",
        )
        prod = models.Product.objects.create(
            name = "some_product",
            description = "something interesting about this product",
            unit = "each",
            unit_price = 123344555.00,
            featured = "",
            discount = 8.00
        )

        self.assertIsInstance(obj, models.Department)
        # self.assertEquals(obj.products, [])
        # how to test the products propert in department

    def test_category(self):
        dept = models.Department.objects.create(
            name = "some depart",
            description = "some description",

        )
        obj = models.Category.objects.create(
            name = "some department",
            description = "something about you",
            department = dept

        )

        self.assertIsInstance(obj, models.Category)


    def test_order(self):
        prod = models.Product.objects.create(
            name = "some_product",
            description = "something interesting about this product",
            unit = "each",
            unit_price = 123344555.00,
            featured = "",
            discount = 8.00
        )

        self.assertIsInstance(prod, models.Product)

        cust = models.Customer.objects.create(
            first_name="Caleb", 
            last_name="Kandoro", 
            email="kandoroc@hotmail.com", 
            password="audacity123"
            )

        curr = models.Currency.objects.create(
            name = "USD",
            symbol = "$"
        )

        sku = models.SKU.objects.create(
            sku_id = "gaksjb",
            attribute = "somthe",
            value = "12",
            product = prod,
            quantity = 123
        )

        obj = models.Order.objects.create(
            date = '2020-09-13',
            shipping_address = "someone's address",
            customer = cust,
            currency = curr,
            shipping_cost = 123.88,
            tax = 5
        )

        orderitem = models.OrderItem.objects.create(
            item = prod,
            sku = sku,
            quantity = 5,
            subtotal = 25,
            discount = 2.00,
            order = obj
        )

        self.assertIsInstance(obj, models.Order)
        self.assertFalse(obj.primary_img)
        self.assertEqual(obj.subtotal, 23.7500)
        self.assertEqual(obj.tax_amount, 1.2500)
        self.assertEqual(obj.total, 25.00)

    def test_payment(self):

        cust = models.Customer.objects.create(
            first_name="Caleb", 
            last_name="Kandoro", 
            email="kandoroc@hotmail.com", 
            password="audacity123"
            )
        curr = models.Currency.objects.create (
            name ="USD",
            symbol ="$"
        )
        orde = models.Order.objects.create(
            date = '2020-09-13',
            shipping_address = "someone's address",
            customer = cust,
            currency = curr,
            shipping_cost = 123.88,
            tax = 5
        )

        obj = models.Payment.objects.create(
            payment_id = 255,
            amount = 352.00,
            method = "card",
            currency = curr,
            order = orde,
        )

        self.assertIsInstance(obj, models.Payment)

    def test_wishlist_item(self):
        
        prod = models.Product.objects.create(
            name = "some_product",
            description = "something interesting about this product",
            unit = "each",
            unit_price = 123344555.00,
            featured = "",
            discount = 8.00
        )

          
        product = prod,
        image = SimpleUploadedFile(name='test_image.jpg',content=open(
        'app/static/app/images/bag.jpg', 'rb').read(), content_type='image/jpeg')
        

        cust = models.Customer.objects.create(
            first_name="Caleb", 
            last_name="Kandoro", 
            email="kandoroc@hotmail.com", 
            password="audacity123"
            )
        
        obj = models.WishlistItem.objects.create(
            product = prod,
            customer = cust,
            date_added = "2020-09-13"
        )
        
        self.assertIsInstance(obj, models.WishlistItem)

    def test_faq_category(self):
        obj = models.FaqCategory.objects.create(
            name = "something about this",
            description = "something even more about this",
            icon = "fa fas"
        )

        self.assertIsInstance(obj, models.FaqCategory)

    def test_faq_item(self):

        faq = models.FaqCategory.objects.create(
            name = "something about this",
            description = "something even more about this",
            icon = "fa fas"
        )
        obj = models.FaqItem.objects.create(
            question = "Paida",
            answer = "The child of SK",
            department = faq
        )

        self.assertIsInstance(obj, models.FaqItem)

    def test_outstanding_email_confirmation(self):
        obj = models.OutstandingEmailConfirmation.objects.create(
            # does this test if it is an email field or if something else is put it wont work?
            user_email = "something", 
            request_id = "55"
        )

        self.assertIsInstance(obj, models.OutstandingEmailConfirmation)

    def test_password_recovery_request(self):
        obj = models.PasswordRecoveryRequest.objects.create(
            user_email = "something", 
            request_id = "55"
        )

        self.assertIsInstance(obj, models.PasswordRecoveryRequest)

    def test_curreny(self):
        obj = models.Currency.objects.create(
            name = "something", 
            symbol = "55"
        )

        self.assertIsInstance(obj, models.Currency)

    def test_currency_exchange(self):
        
        curr = models.Currency.objects.create(
            name = "USD",
            symbol = "$"
        )
    
        obj = models.CurrencyExchange.objects.create(
            from_currency = curr,
            to_currency = curr,
            date = "1990-08-21",
            rate = 123.33
        )

        self.assertIsInstance(obj, models.CurrencyExchange)


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

    def test_get_home_page(self):
        resp = self.client.get(reverse('app:home'))
        self.assertEqual(resp.status_code, 200)

    def test_get_login(self):
        resp = self.client.get(reverse('app:login'))
        self.assertEqual(resp.status_code, 200)
        
    def test_get_shopping_cart_page(self):
        resp = self.client.get(reverse('app:cart'))
        self.assertEqual(resp.status_code, 200)

    def test_get_account_page(self):
        resp = self.client.get(reverse('app:account'))
        self.assertEqual(resp.status_code, 200)

    def test_get_update_account(self):
        resp = self.client.get(reverse('app:update-account'))
        self.assertEqual(resp.status_code, 200)

    def test_get_discount(self):
        resp = self.client.get(reverse('app:discount'))
        self.assertEqual(resp.status_code, 200)

    def test_get_featured(self):
        resp = self.client.get(reverse('app:featured'))
        self.assertEqual(resp.status_code, 200)

    def test_get_wishlist(self):
        resp = self.client.get(reverse('app:wishlist'))
        self.assertEqual(resp.status_code, 200)

    def test_get_about(self):
        resp = self.client.get(reverse('app:about'))
        self.assertEqual(resp.status_code, 200)

    def test_get_login(self):
        resp = self.client.get(reverse('app:login'))
        self.assertEqual(resp.status_code, 200)

    def test_post_login(self):
        resp = self.client.post(reverse('app:login'), data={
            "email":"careea@gmail.com",
            "password":"adfkdhkgadhfyryewri23783"

        })
        self.assertEqual(resp.status_code, 302)


    def test_get_sign_up(self):
        resp = self.client.get(reverse('app:sign-up'))
        self.assertEqual(resp.status_code, 200)

    def test_post_sign_up(self):
        resp = self.client.post(reverse('app:sign-up'), data={
            "first_name":"Caleb",
            "last_name" :"Rejoin",
            "email": "system@gmail.com",
            "password1":"qwertypoipidfggsf123",
            "password2": "qwertypoipidfggsf123"
        })
        # print(resp.context["form"].errors)
        self.assertEqual(resp.status_code, 302)

    def test_get_faq(self):
        resp = self.client.get(reverse('app:faq'))
        self.assertEqual(resp.status_code, 200)


    def test_get_department_page(self):
        resp = self.client.get(reverse('app:department', 
            kwargs={'pk': self.dept.pk}
            ))
        self.assertEqual(resp.status_code, 200)

    def test_get_category_page(self):
        resp = self.client.get(reverse('app:category',
            kwargs={'pk': self.cate.pk}
            ))
        self.assertEqual(resp.status_code, 200)


    def test_get_product_page(self):
        prod = models.Product.objects.create(
            name="hdskfjadhj",
            description="21weqqwe",
            unit="23",
            unit_price=34.5,
            discount=0.3,
            category= self.cate
        )

        prod_img = models.ProductImage.objects.create(
            product = prod,
            image = self.img
        )
        resp = self.client.get(reverse('app:product',
                                       kwargs={'pk': prod.pk}
                                       ))
        self.assertEqual(resp.status_code, 200)

    def test_get_faq_page(self):
        
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


        
    def test_get_payment_success(self):
        resp = self.client.get(reverse('app:payment-success'))
        self.assertEqual(resp.status_code, 302)

    def test_get_pending_payment(self):
        resp = self.client.get(reverse('app:pending-payment'))
        self.assertEqual(resp.status_code, 302)

    def test_get_404_order_view(self):
        
        resp = self.client.get(reverse('app:order-view',
                                                kwargs={'pk':1}
                                                ))
        self.assertEqual(resp.status_code, 404)
    
    def test_get_order_view(self):
        orde = models.Order.objects.create(
            date = '2020-09-13',
            status = "done",
            shipping_address = "shipped tonight",
            shipping_cost = 123.00,
            currency = self.currency
        )
        resp = self.client.get(reverse('app:order-view',
                                                kwargs={'pk':orde.pk}))

    def test_get_password_reset(self):
        resp = self.client.get(reverse('app:password-reset'))
        self.assertEqual(resp.status_code, 302)

    def test_post_password_reset(self):
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

        

    def test_get_password_reset_with_valid_recovery_request(self):
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


    
       


        







