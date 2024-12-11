import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import OrderFactory, UserFactory
from product.models import Product
from order.models import Order


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        # Criação do usuário e autenticação
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        # Dados de teste
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(title="mouse", price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product], user=self.user)

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(order_data["results"][0]["product"][0]["title"], self.product.title)  # inclusão do results para correção dos testes
        self.assertEqual(order_data["results"][0]["product"][0]["price"], self.product.price)  # inclusão do results para correção dos testes
        self.assertEqual(order_data["results"][0]["product"][0]["active"], self.product.active)  # inclusão do results para correção dos testes
        self.assertEqual(order_data["results"][0]["product"][0]["category"][0]["title"], self.category.title)  # inclusão do results para correção dos testes

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({
            "products_id": [product.id],
            "user": user.id
        })

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}), 
            data=data, 
            content_type="application/json"
        )

        # Verificar resposta
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Garantir que apenas um pedido foi criado
        self.assertEqual(Order.objects.filter(user=user).count(), 1)
        created_order = Order.objects.get(user=user)

        # Validar os dados do pedido
        self.assertEqual(created_order.user, user)
        self.assertIn(product, created_order.product.all())
