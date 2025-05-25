from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Subscription, Order
from profiles.models import Profile


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='foo',
            email='foo@test.com',
            password='bar'
        )
        # Tạo profile cho user
        Profile.objects.create(user=self.user, is_premium=False)

    # Kiểm tra gửi form đến trang subscribe và chuyển hướng đến bank_info
    def test_post_subscribe_page(self):
        self.client.login(username='foo', password='bar')
        response = self.client.post(reverse('subscribe'), {
            'plans': 'plan_F5eyGdYCvZPtON',
            'full_name': 'foo bar',
            'phone_number': '0123456789',
            'country': 'foo',
            'postcode': 'foo',
            'town_or_city': 'foo',
            'street_address1': 'foo',
            'street_address2': 'foo',
            'county': 'foo'
        })
        self.assertRedirects(response, reverse('bank_info'), status_code=302)
        # Kiểm tra order đã được tạo
        self.assertEqual(Order.objects.count(), 1)
        # Kiểm tra order_id trong session
        self.assertIn('order_id', self.client.session)

    # Kiểm tra xác nhận thanh toán trên trang bank_info
    def test_post_bank_info_page(self):
        self.client.login(username='foo', password='bar')
        # Tạo order trước
        order = Order.objects.create(
            plans='plan_F5eyGdYCvZPtON',
            full_name='foo bar',
            phone_number='0123456789',
            country='foo',
            postcode='foo',
            town_or_city='foo',
            street_address1='foo',
            street_address2='foo',
            county='foo'
        )
        # Lưu order_id vào session
        session = self.client.session
        session['order_id'] = order.id
        session.save()

        response = self.client.post(reverse('bank_info'))
        self.assertRedirects(response, reverse('index'), status_code=302)
        # Kiểm tra subscription đã được tạo
        self.assertEqual(Subscription.objects.count(), 1)
        # Kiểm tra trạng thái premium
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(profile.is_premium)