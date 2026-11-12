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
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view()
def getCategory(request,pk):
    # category = Category.objects.last()
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view()
def getProducts(request):
    products = Product.objects.select_related("category").all()  # for less query in db
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view()
def getProduct(request,pk):
    # product = Product.objects.last()
    # product = Product.objects.first()
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

