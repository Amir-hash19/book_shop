from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from bootcamp.models import Bootcamp
from rest_framework import status
from django.urls import reverse
from .models import Ticket, TicketMessage
from django.utils.text import slugify
import uuid

User = get_user_model()



class CreateTicketAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testali@12", email="testali1@email.com"
            ,phone="+989122345431",national_id="9187435619", slug="test-ali"
        )
        self.url = reverse("create-tickect")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)


    def test_create_ticket_authenticated(self):

        data = {
            "title":"test ticket1",
            "description":"test description1",
        }    
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response=self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], 'test ticket1')
        self.assertEqual(response.data["user"], "testali@12")


    def test_create_ticket_unauthenticated(self):
        data = {
            "title":"test ticket2",
            "description":"test description2"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)






class CreateTicketMessageAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testali2@12", email="testali2@email.com",
            national_id="8765439212", phone="+989953214365", slug="test-ali2"
        )
        self.user2 = User.objects.create_user(
            username="test-ali3", email="testali3@email.com",
            national_id="8767896548",phone="+989123398896", slug="test-ali3"
        )

        
        self.ticket_user1 = Ticket.objects.create(
            title="user1 ticket",
            description="description user1",
            user=self.user1,
            slug=slugify("user1 ticket") + "-" + str(uuid.uuid4())[:8]
        )
        
        self.ticket_user2 = Ticket.objects.create(
            title="user2 ticket",
            description="description user2",
            user=self.user2,
            slug=slugify("user2 ticket") + "-" + str(uuid.uuid4())[:8]
            
        )

        refresh = RefreshToken.for_user(self.user1)
        self.access_token_user1 = str(refresh.access_token)


        self.url = lambda slug: reverse("create-ticket-message", kwargs={"slug":slug})



    def test_create_message_on_own_tikcet(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token_user1}")
        data = {
            "message":"hi fuck you",
            "title":"requested to fuck you",
        }
        response = self.client.post(self.url(self.ticket_user1.slug), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "hi fuck you")
        self.assertEqual(response.data["title"], "requested to fuck you")
        self.assertEqual(response.data["message_status"], "pending")
        self.assertTrue("slug" in response.data)
        self.assertEqual(TicketMessage.objects.count(), 1)




    def test_cannot_create_message_for_other_users_ticket(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token_user1}")
        data={
            "message":"trying to log in",
            "title":"bad access"
        }
        response = self.client.post(self.url(self.ticket_user2.slug), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(TicketMessage.objects.count(), 0)

        


    def test_unauthenticated_cannot_create_message(self):    
        data = {
            "message":"no token access",
            "title":"unauth"
        }
        response = self.client.post(self.url(self.ticket_user1.slug), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)






class AdminResponseMessageAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testusernormal@12", email="normalusertest@email.com",
            national_id="9821342561", phone="+989956572134", slug="user-test"
        )
        self.admin = User.objects.create_user(
            username="testadmin@12", email="admintest@email.com",
            national_id="9821142561", phone="+989956572034", slug="admin-test"
        )
        group = Group.objects.create(name="SupportPanel")
        self.admin.groups.add(group)

        self.ticket = Ticket.objects.create(
            title="test user5",
            description="test desc",
            user=self.user,
            slug=slugify("test user5") + "-" + str(uuid.uuid4())[:8]
        )

        self.message = TicketMessage.objects.create(
            ticket=self.ticket,
            sender=self.user,
            message='Need help!',
            title='Problem',
            slug=slugify("Problem") + "-" + str(uuid.uuid4())[:8],
        )

        refresh = RefreshToken.for_user(self.admin)
        self.access_token = str(refresh.access_token)

        self.url = reverse("response-messages", kwargs={"slug":self.message.slug})



    def test_admin_can_respond_to_ticket_message(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        data = {
            "admin_response":"We are checking your issue.",
            "message_status": "answered"
        }

        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["admin_response"], "We are checking your issue.")
        self.assertEqual(response.data["message_status"], "answered")
        self.assertEqual(response.data["admin"], str(self.admin)) 



