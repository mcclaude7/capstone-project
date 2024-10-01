#from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# ViewSet for Category
class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Category instances.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSet for Product
class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Product instances.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Optional: override the create method to add custom behavior (if needed)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Optional: override the update method to add custom behavior (if needed)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # Optional: Override the destroy method to add custom behavior (if needed)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



# Create your views here.
