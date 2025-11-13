from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group 
from rest_framework.test import APITestCase
from django.utils.text import slugify
from account.models import CustomUser 
from .models import Invoice, Payment
from datetime import date, timedelta 
from rest_framework import status
from django.urls import reverse
import uuid 



User = get_user_model()

class CreateInvoiceViewAPITest(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            username="testalireza@1", email="testalireza1@email.com",
            national_id="1987987864", phone="+989051066658", slug="test-alireza"
        )
        self.superuser=User.objects.create_user(
            username="testadmin@22", email="testadmin22@email.com",
            national_id="1987987863", phone="+989051566658", slug="test-admin"
        )
        superuser_group = Group.objects.create(name="SuperUser")
        self.superuser.groups.add(superuser_group)

        self.url = reverse("create-invoice-for-user-by-admin")

        self.valid_payload = {
            "client": self.user.username,
            "amount": "1234.567",
            "deadline": (date.today() + timedelta(days=30)).isoformat(),
            "description": "Test invoice",
            "slug":slugify("testalireza") + "-" +str(uuid.uuid4())[:8]
        }

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


    def test_create_invoice_unauthenticated(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def authorize_client_as(self, user):
        token = self.get_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")



    def test_create_invoice_without_permission(self):
        self.authorize_client_as(self.user)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_create_invoice_with_permission(self):
        self.authorize_client_as(self.superuser)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Invoice.objects.filter(client=self.user).exists())



    def test_create_invoice_invalid_amount(self):
        self.authorize_client_as(self.superuser)
        invalid_payload = self.valid_payload.copy()
        invalid_payload["amount"] = "not-a-number"
        response = self.client.post(self.url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)






class CreatePaymentViewAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="payeruser@12",email="payeruser12@email.com",
        national_id="8769053412", phone="+989191278865", slug="payer-test")

        self.invoice = Invoice.objects.create(
            client=self.user,
            amount=1000.00,
            deadline=date.today() + timedelta(days=10),
            description="Test invoice",
            slug="test-invoice"
        )


        self.url = reverse("create-payment", kwargs={"slug": self.invoice.slug}) 


        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        
        self.payload = {
            "method":"online",
            "amount": "500.00",
        }


    def test_create_valid_online_payment(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(str(payment.amount), "500.00")
        self.assertEqual(payment.invoice, self.invoice)
        self.assertEqual(payment.user, self.user)





class DetailPaymentViewTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser@15",email="payeruser15@email.com",
        national_id="8769053419", phone="+989191278875", slug="user1-test"
        )

        self.user2 = User.objects.create_user(username="testuser@17",email="payeruser17@email.com",
        national_id="8769053429", phone="+989191278878", slug="user2-test"
        )


        self.invoice1 = Invoice.objects.create(
            client=self.user1,
            amount=1000,
            deadline=date.today() + timedelta(days=10),
            description="Invoice for user1",
            slug="invoice-user1"
        )

        self.payment = Payment.objects.create(
            user=self.user1,
            invoice=self.invoice1,
            amount=500,
            method="online",
            slug="payment-user2"
        )

        self.url = reverse("detail-payment-user", kwargs={"slug": self.payment.slug}) 

    def get_token(self, user):
        return str(RefreshToken.for_user(user).access_token)
    

    def test_get_payment_detail_authenticated_owner(self):
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], self.payment.slug)


    def test_get_payment_detail_authenticated_not_owner(self):
        token = self.get_token(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_get_payment_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)







class ListInvoiceUserViewTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser@17",email="payeruser17@email.com",
        national_id="8769253419", phone="+989191278845", slug="user5-test"
        )

        self.user2 = User.objects.create_user(username="testuser@18",email="payeruser18@email.com",
        national_id="8769253219", phone="+989191274845", slug="user6-test"
        )



        Invoice.objects.create(
            client=self.user1,
            amount=500,
            deadline=date.today() + timedelta(days=5),
            description="Invoice 1",
            slug="invoice-1"
        )  

        Invoice.objects.create(
            client=self.user1,
            amount=300,
            deadline=date.today() + timedelta(days=10),
            description="Invoice 2",
            slug="invoice-2"
        )  

        Invoice.objects.create(
            client=self.user2,
            amount=800,
            deadline=date.today() + timedelta(days=3),
            description="Invoice other",
            slug="invoice-3"
        )

        self.url = reverse("list-invoices-user")


    def get_token(self, user):
        return str(RefreshToken.for_user(user).access_token)    
    


    def test_list_invoices_authenticated(self):
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # چون فقط دو فاکتور متعلق به user1 است
        self.assertTrue(all(invoice["description"].startswith("Invoice") for invoice in response.data["results"]))



    def test_list_invoices_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    

