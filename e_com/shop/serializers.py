from rest_framework import serializers
from .models import Category, Product

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # Specify the fields you want to serialize

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)  # Nested serializer for the related Category

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock_quantity', 'image_url', 'created_date']
    
    # Optionally, if you want to allow category creation or updates via ID
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
        
    def validate_price(self, value):
       if value <= 0:
           raise serializers.ValidationError('Price must be greater than Zero')
       return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock quantity cannot be negative.')
        return value 
