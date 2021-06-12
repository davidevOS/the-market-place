from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .models import Products, Users, Categorys
from .serializers import *


from django.core.serializers.json import DjangoJSONEncoder



# Create your views here.

def index(request):
    return HttpResponse('<h1>martketplace api</h1>')



class UsersList(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    # return HttpResponse('Working')



class CategoriesList(APIView):
    def get(self,request):
        categories = Categorys.objects.all()
        serializer = CategorysSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self,request):
        name_c = CategorysSerializer(data=request.data)        
        if name_c.is_valid():
            name_c.save()
        return Response(name_c,status=status.HTTP_201_CREATED)


class ProductsList(APIView):
    def get(self,request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products,many=True)
        return Response(serializer.data)


    def post(self,request):
        ls = []
        for key in request.data:
            ls.append(key)        

        if ('name_p' and 'description_p'
        and 'sku' and 'price' and 'stock' and 'user_fk' and 'category_fk' in ls):
            
            product = ProductsInsertSerializer(data=request.data)
            if product.is_valid():
                product.save()
                return Response(f"a new product has been created",status=status.HTTP_201_CREATED)
             
            else:
                return Response('a problem has ocurred',status=500)

        else:
            return Response('a problem has ocurred',status=500)    



class CategoryAndProducts(APIView):
    def get(self, request):
        categories = Products.objects.all().order_by('category_fk')
        serializer_class = CategorysAndProducts(categories,many=True)
        
        return Response(serializer_class.data, status=200)
    
