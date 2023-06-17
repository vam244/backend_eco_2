from django.shortcuts import render
from django.http import response
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializer import productserializer,cartserializer,RegisterSerializer, UserSerializer
from .models import product,cart_product
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView
# from django.views.decorators.csrf import csrf_exempt
from knox.models import AuthToken
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        # ... other routes ...
    ]
    return Response(routes)


@api_view(['GET'])
def getproducts(request):
    # data_transfer()
    products = product.objects.all()
    serializer = productserializer(products, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def getproduct(request, x):
    product_instance = product.objects.get(id=x)
    serializer = productserializer(product_instance, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
# @csrf_exempt
def update_product(request, x):
 
    data = request.data
    # print(data)
    product_instance = product.objects.get(id=x)
    # print(product_instance)
    serializer = productserializer(instance=product_instance, data=data)

    if serializer.is_valid():
        # product_instance.incart=serializer.data.get('incart')
        serializer.save()

    return Response(serializer.data)

#cart views begin here
@api_view(['GET'])
def getcart_products(request):
    # data_transfer()
    products = cart_product.objects.all()
    serializer = cartserializer(products, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @csrf_exempt
def update_cart_product(request, x):
    data = request.data
    # print(data)
    cart_product_instance = cart_product.objects.get(id=x)
    # print(product_instance)
    serializer = cartserializer(instance=cart_product_instance, data=data)

    if serializer.is_valid():
        # product_instance.incart=serializer.data.get('incart')
        serializer.save()

    return Response(serializer.data)


# def data_transfer():
#     all_obj=product.objects.all()
#   
    
              
#     incart_products=filter(check,all_obj)
#     for obj in incart_products:
#      new_obj = cart_product()
#     #  new_obj.id=obj.id
#      new_obj.img= obj.img # Map field1 of MyModel to field3 of NewModel
#      new_obj.name = obj.name # Map field2 of MyModel to field4 of NewModel
#      new_obj.price = obj.price # Map field2 of MyModel to field4 of NewModel
#      new_obj.discount = obj.discount# Map field2 of MyModel to field4 of NewModel
#      new_obj.p_key= obj.p_key

#      new_obj.save()

#adding items in cart by post request from mai site


def check(data):
    obj_id=data.get('p_key')
    # print(obj_id)
    current_obj=cart_product.objects.all()
    a=True
    for cu_obj in current_obj:
        if(obj_id==cu_obj.p_key):
                # print(cu_obj.id)
                a=False
                break
    return a
    


@api_view(['DELETE'])
def deleteitem(request,x):
    item=cart_product.objects.get(id=x)
    item.delete()
    return Response({'message':'product removed from cart'})


@api_view(['POST'])
def register_api(request):
    print(request.data)
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # token = Token.objects.create(user=user)
    
    return Response({
        "user": UserSerializer(user, context={'request': request}).data,
        "token": AuthToken.objects.create(user)[1]
    })

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request, format=None):
   
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # a=user
        # product.customer.set(a) 
        # print(user)
        login(request, user)
        knox_login_view = KnoxLoginView()
        # print(knox_login_view.post(request, format=None).data)
        return knox_login_view.post(request, format=None)

@api_view(['POST'])
def addtocart(request):
   data=request.data
#    print(data)
   if(check(data)):
     p_key=data.get('p_key')
     name=data.get('name')
     price=data.get('price')
     discount=data.get('discount')
     img=data.get('img')
     cart_item=cart_product.objects.create(  
      
      name=name,
      price=price,
      discount=discount,
      img=img,
      p_key= p_key

    )
     serializer=productserializer(cart_item)
     return Response(serializer.data)
   else:
       return Response({'message': 'Item already exists in the cart'})