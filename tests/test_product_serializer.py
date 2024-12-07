import pytest

from product.serializers import ProductSerializer


@pytest.mark.django_db
def test_product_serializer():
    # Criando o dict que será passado no atributo 'data' como referência pros testes.
    data = {
        "title": "Teste serializer",
        "description": "Testando o serializer",
        "price": 999
    }

    # Testando a deserialização:
    # Criando a instância do ProductSerializer e passando os dados que serão deserealizados.
    serializer = ProductSerializer(data=data)

    # Verificando se os dados fornecidos estão de acordo com o modelo Product(que o serializer se baseia)
    assert serializer.is_valid(), f"Erros: {serializer.errors}"

    # Caso não estoure nenhuma exceção, iremos criar uma instância de Product, com os dados deserializados.
    product = serializer.save()

    # Verificando os dados da instância criada acima:
    assert product.title == data["title"]  # Teste serializer
    assert product.description == data["description"]  # Testando o serializer
    assert product.price == data["price"]  # 999

    # Testando a serialização:
    # Testando a onversão da instância em dados serializados:
    serializer = ProductSerializer(product)
    serialized_data = serializer.data

    # Conferindo os dados serializados:
    assert serialized_data["title"] == data["title"]
    assert serialized_data["description"] == data["description"]
    assert serialized_data["price"] == data["price"]