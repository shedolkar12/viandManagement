from rest_framework import serializers
from .models import *

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'description', 'is_active')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'description')


class ProductCategoryRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryRelation
        fields = ('id', 'product_id', 'category_id')


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id')

class PricingProcessSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    class Meta:
        model = Pricing
        fields = ('branch', 'product', 'price', 'unit', 'version')

class ComboProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboProduct
        fields = ('id', 'branch', 'description')

class ComboProductRelationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    combo_product = ComboProductSerializer(read_only = True)
    class Meta:
        model = ComboProductRelation
        fields = ('product', 'combo_product')