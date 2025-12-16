from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'stock_quantity', 'status', 'status_display', 'image', 'rating',
            'created_by', 'created_by_name', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'status']


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Product"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category',
            'stock_quantity', 'image', 'rating', 'is_active'
        ]
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
