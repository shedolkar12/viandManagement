from .models import *
from .serializers import *
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
import json


@csrf_exempt
def validate_location(request):
    # user's location should be in the radius 15 km from one of the branch location
    # based on requested Location and availability of product fetch the 
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')
    if not lng or not lat:
        print("Not Valid Location. Try Again")
        return redirect('/validate_location/')
    valid_location, branch_id = True, '' # get_valid_branch_location(lng, lat) // should returns Valid branch location
    if valid_location:
        return redirect('/categories/%s/'%(branch_id))
    # Not Valid Location. Try Again
    return redirect('/validate_location/')

def get_categories(branch_id):
    distinct_available_product = Storage.objects.filter(branch_id=branch_id, quantity__gte=1).order_by().values_list('product_id').distinct()
    return ProductCategoryRelation.objects.filter(product_id__in=distinct_available_product).distinct()

@csrf_exempt
def categories(request, branch_id):
    """
    List all categories.
    """
    if request.method == 'GET':
        # check User authentication
        # List of all categories
        if not Branch.objects.filter(id=branch_id).exists():
            return JsonResponse({'msg': "not a valid branch"}, status=400)
        # category_objects = get_categories(branch_id)
        category_objects = Categories.objects.all()
        serializer = CategoriesSerializer(category_objects, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def productList(request, branch_id, category):
    """
    List all products.
    """
    if request.method == 'GET':
        #skiping authentication/authrization
        if not Categories.objects.filter(id=category).exists():
            return JsonResponse({'msg': "not a valid category"}, status=400)
        limit = request.GET.get('limit', 10)
        offset = request.GET.get('offset', 0)
        serializer = get_products(category, branch_id, limit, offset)
        return JsonResponse(serializer.data, safe=False)

def get_products(category, branch_id, limit, offset):
    product_ids = [obj.product_id for obj in ProductCategoryRelation.objects.filter(category=category)]
    products = Product.objects.filter(id__in=product_ids)[offset : offset+limit]
    pricing_obj = Pricing.objects.filter(product__in=products)
    serializer = PricingProcessSerializer(pricing_obj, many=True)
    return serializer


@csrf_exempt
def comboProductsList(request, branch_id):
    """
    List all Combo Products.
    """
    if request.method == 'GET':
        #skiping authentication/authrization
        if not Branch.objects.filter(id=branch_id).exists():
            return JsonResponse({'msg': "not a valid branch"}, status=400)
        limit = request.GET.get('limit', 10)
        offset = request.GET.get('offset', 0)
        response = get_combo_products(branch_id, limit, offset)
        return JsonResponse(response, safe=False)

def get_combo_products(branch_id, limit, offset):
    products = [p.product for p in ComboProductRelation.objects.filter(combo_product__branch_id = branch_id)[offset:offset+limit] ]
    pricing_obj = Pricing.objects.filter(product__in = products)
    combo_products = ComboProductRelation.objects.filter(combo_product__branch_id = branch_id)[offset:offset+limit]
    pricing_serializer = PricingProcessSerializer(pricing_obj, many=True)
    combo_product_serializer = ComboProductRelationSerializer(combo_products, many=True)
    product_price_mapping = get_product_price_mapping(pricing_serializer.data)
    response = get_combo_products_mapping(combo_product_serializer.data, product_price_mapping)
    response = {'combo_products': response, 'branch_id': branch_id, 'limit': limit, 'offset': offset}
    return response

def get_product_price_mapping(pricing_objects):
    response = {}
    for obj in pricing_objects:
        response[obj['product']['id']] = {'price': obj['price'], 'unit': obj['unit']}
    return response

def get_combo_products_mapping(combo_products, product_price_mapping):
    response = []
    res = {}
    description_mapping = {}
    for obj in combo_products:
        product = {**obj['product'], **product_price_mapping[obj['product']['id']]}
        if obj['combo_product']['id'] not in res:            
            res[obj['combo_product']['id']] = [product]
            description_mapping[obj['combo_product']['id']] = obj['combo_product']['description']
        else:
            res[obj['combo_product']['id']].append(product)
    for key in res:
        response.append({'id': key ,'products': res[key], 'description': description_mapping[key]})
    return response


@csrf_exempt
def placeOrder(request):
    """
    request body:
        {  
            "branch_id": 123, 
            "user_id": 34211, 
            "items": [
                {
                    "type": "individual", 
                    "products": [{"product_id": "chicken_curry_cut_small" }], 
                    "quantity": 2
                },
                {
                    "type": "combo", 
                    "products": [{"product_id": "chicken_curry_cut_small" }, {"product_id": "prawns"}], 
                    "quantity": 1
                }
                ], 
            "customer_address_id": 4542
        }
    """
    if request.method == 'POST':
        # Assuming User authentication check is available
        # Assuming validation check 
        request_data = json.loads(request.body.decode('utf-8'))
        user_id = request_data.get("user_id")
        customer_address_id = request_data.get("customer_address_id")
        branch_id = request_data.get('branch_id')
        print(user_id, customer_address_id)
        user = User.objects.filter(id = user_id)
        customer_address = CustomerAddress.objects.filter(id = customer_address_id)
        if not user.exists() or not customer_address.exists():
            return JsonResponse({'msg': "not a valid data"}, status=400)
        customer_address = customer_address.last()
        user = user.last()
        if not customer_address.customer.user_id == user.id:
            return JsonResponse({'msg': "not a valid address or Add new address"}, status=400)
        if not Branch.objects.filter(id=branch_id).exists():
            return JsonResponse({'msg': "not a valid branch"}, status=400)
        # assuming structured data is getting from client side
        # calculating total amount
        # sample data: {'items': [obj1, obj2], net_amount: , 'gst': '', discount: , gross_amount: }
        input_data = request_data.get('items', [])
        order_response = {}
        response = {}
        items = []
        for obj in input_data:
            type = obj.get('type') # individual / combo
            quantity = obj.get('quantity')
            products = obj.get('products', [])
            coupon_code = obj.get('coupon_code')
            # discounting factor is in decimal
            discounting_factor = get_discounting(user, items, type, coupon_code, quantity)
            total_curr_item_amount = 0
            response_items = []
            for product in products:
                product_id = product.get('product_id')
                price = get_price(product_id, branch_id)
                if not price:
                    return JsonResponse({'msg': "Product is not availabe at this moment"}, status=400)
                total_curr_item_amount += price
            total_curr_item_amount = total_curr_item_amount * quantity
            discount = total_curr_item_amount * discounting_factor
            current_item_computation = {
                        'quantity': quantity, 
                        'type': type, 
                        'products': products,
                        'discount': discount, 
                        'discounting_factor': discounting_factor, 
                        'total_amount': total_curr_item_amount
                        }
            items.append(current_item_computation)
        # {'items': [obj1, obj2], net_amount: 123, 'gst': '', discount: 123, gross_amount: 12345}
        total_amount = 0
        net_amount = 0
        net_discount = 0
        amount_after_discount = 0
        for obj in items:
            total_amount += obj['total_amount']
            net_discount += obj['discount']
        total_amount = total_amount - net_discount
        gst = total_amount * 0.18
        net_amount = total_amount - net_discount + gst
        
        response = {
            'items': items,
            'total_amount': total_amount,
            'net_amount': net_amount,
            'discount': net_discount,
            'gst': gst
        }
        payment = True
        if payment is True:
            order_breakup = json.dumps(response)
            order = Order.objects.create(status='COMPLETED', customer_address_id=customer_address_id, 
                branch_id=branch_id, amount=response.get('net_amount'), order_breakup=order_breakup)
            response['order_id'] = order.order_id
            return JsonResponse(response, safe=False)
        else:
            JsonResponse({'msg': 'payment has been failed'}, safe = False)

def get_discounting(user, items, type, coupon_code, quantity):
    # has to be some business logic
    # here simply returning random value
    discounts = [0, 0.1, 0.2, 0.25, 0, 0.15, 0]
    import random
    random_value = int(random.random()*100)
    index = random_value % 7
    return discounts[index]

def get_price(product_id, branch_id):
    price_obj = Pricing.objects.filter(product_id=product_id, unit=0.5, branch_id=branch_id)
    if price_obj:
        return price_obj[0].price
    return None
