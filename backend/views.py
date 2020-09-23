from .models import Categories, Branch, Storage
from .serializers import CategoriesSerializer
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser

class CategoriesList(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    def as_view(cls, **initkwargs):
        v = generics.View()

@csrf_exempt
def validate_location(request):
    # user's location should be in the radius 15 km from one of the branch location
    # based on requested Location and availability of meat fetch the 
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
    distinct_available_meat = Storage.objects.filter(branch_id=branch_id, quantity__gte=1).order_by().values_list('meat_id').distinct()
    return MeatCategoryRelationShip.objects.filter(meat_id__in=distinct_available_meat).distinct()
    


@csrf_exempt
def categories(request, branch_id):
    """
    List all categories.
    """
    if request.method == 'GET':
        # check User authentication
        # List of all categories
        if not Branch.objects.filter(id=branch_id).exist():
            return JsonResponse({'msg': "not a valid branch"}, status=400)
        category_objects = get_categories(branch_id)
        serializer = CategoriesSerializer(category_objects, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def product(request, category):
    """
    List all product.
    """


