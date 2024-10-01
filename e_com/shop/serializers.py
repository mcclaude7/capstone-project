

'''from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #fields = ['name']
        fields = ['id', 'name']  # Specify fields to serialize

class ProductSerializer(serializers.ModelSerializer):
    # Using a nested serializer for the category
    category = CategorySerializer(read_only=True)
    
    # Allow clients to provide the category ID when creating or updating products
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        #fields = ['id', 'name', 'description', 'price', 'category', 'stock_quantity', 'image_url', 'created_date']
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 'stock_quantity', 'image_url', 'created_date']  # Add 'category_id' here

    def update(self, instance, validated_data):
        # Example of overriding update to include custom logic
        category_data = validated_data.pop('category', None)
        if category_data:
            instance.category = Category.objects.get(id=category_data['id'])

        return super().update(instance, validated_data)'''

from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    
    # Add a custom field to reduce stock
    reduced_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 'stock_quantity', 'image_url', 'created_date', 'reduced_stock']

    # Method to return reduced stock (just an example)
    def get_reduced_stock(self, obj):
        # This method doesn't change the stock; it only shows the current stock quantity.
        # To actually reduce stock, a custom view should be used.
        return obj.stock_quantity

    # Custom method to handle stock reduction when a request is made
    def reduce_stock(self, product, quantity):
        product.reduce_stock(quantity)
        return product.stock_quantity  # Return the updated stock quantity



