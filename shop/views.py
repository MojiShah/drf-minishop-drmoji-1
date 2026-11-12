# from django.http import HttpResponse , HttpRequest
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer

# def alaki(request : HttpRequest) -> HttpResponse:
#     return HttpResponse("Hello world")

# @api_view(http_method_names=["POST","GET","DELETE"])
# def alaki(request : Request) -> Response:
#     return Response("Hello world")

@api_view()
def getCategory(request):
    category = Category.objects.last()
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view()
def getProduct(request):
    product = Product.objects.last()
    serializer = ProductSerializer(product)
    return Response(serializer.data)