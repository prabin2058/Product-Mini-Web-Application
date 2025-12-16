from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Admin users can do anything, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Products.
    
    - GET /api/products/ - List all products
    - POST /api/products/ - Create product (Admin only)
    - GET /api/products/{id}/ - Retrieve product
    - PUT /api/products/{id}/ - Update product (Admin only)
    - DELETE /api/products/{id}/ - Delete product (Admin only)
    - GET /api/products/search/?q=term - Search products
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get product statistics"""
        products = Product.objects.all()
        return Response({
            'total_products': products.count(),
            'in_stock': products.filter(status='in_stock').count(),
            'low_stock': products.filter(status='low_stock').count(),
            'out_of_stock': products.filter(status='out_of_stock').count(),
        })


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Categories.
    
    - GET /api/categories/ - List all categories
    - POST /api/categories/ - Create category (Admin only)
    - GET /api/categories/{id}/ - Retrieve category
    - PUT /api/categories/{id}/ - Update category (Admin only)
    - DELETE /api/categories/{id}/ - Delete category (Admin only)
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
