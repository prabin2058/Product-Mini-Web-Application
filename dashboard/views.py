from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Sum, Count
from django.utils import timezone
import io

from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductSearchForm
from .utils import generate_product_pdf, generate_single_product_pdf

@login_required
def dashboard_index(request):
    """Dashboard home page with stats"""
    user = request.user
    products = Product.objects.filter(created_by=user)
    categories = Category.objects.all().order_by('name')
    
    # Statistics
    stats = {
        'total_products': products.count(),
        'total_value': products.aggregate(total=Sum('price'))['total'] or 0,
        'in_stock': products.filter(status='in_stock').count(),
        'low_stock': products.filter(status='low_stock').count(),
        'out_of_stock': products.filter(status='out_of_stock').count(),
    }
    
    # Products list for table
    products_list = products.order_by('-created_at')
    
    context = {
        'stats': stats,
        'products': products_list,
        'categories': categories,
        'user': user,
    }
    return render(request, 'dashboard/dashboard.html', context)

# ===== PRODUCT CRUD OPERATIONS =====

@login_required
def product_list(request):
    """List all products"""
    user = request.user
    products = Product.objects.filter(created_by=user)
    
    # Search and filter
    form = ProductSearchForm(request.GET or None)
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        
        if search:
            products = products.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        if category:
            products = products.filter(category=category)
        if status:
            products = products.filter(status=status)
    
    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'form': form,
        'total_products': products.count(),
    }
    return render(request, 'dashboard/product_list.html', context)

@login_required
def product_create(request):
    """Create new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('dashboard:product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
    }
    return render(request, 'dashboard/product_form.html', context)

@login_required
def product_detail(request, pk):
    """View product details"""
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    return render(request, 'dashboard/product_detail.html', {'product': product})

@login_required
def product_update(request, pk):
    """Update existing product"""
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard:product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'title': 'Edit Product',
        'product': product,
    }
    return render(request, 'dashboard/product_form.html', context)

@login_required
def product_delete(request, pk):
    """Delete product"""
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('dashboard:product_list')
    
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

# ===== CATEGORY CRUD OPERATIONS =====

@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': page_obj,
        'total_categories': categories.count(),
    }
    return render(request, 'dashboard/category_list.html', context)

@login_required
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('dashboard:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('dashboard:category_list')

    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})

# ===== PDF EXPORT OPERATIONS =====

@login_required
def export_products_pdf(request):
    """Export all products to PDF"""
    user = request.user
    products = Product.objects.filter(created_by=user)
    
    # Apply same filters as product_list
    form = ProductSearchForm(request.GET or None)
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        
        if search:
            products = products.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        if category:
            products = products.filter(category=category)
        if status:
            products = products.filter(status=status)
    
    # Generate PDF
    pdf_buffer = generate_product_pdf(products, "Products Report")
    
    # Create HTTP response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"products_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
def export_product_pdf(request, pk):
    """Export single product to PDF"""
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    
    # Generate PDF
    pdf_buffer = generate_single_product_pdf(product)
    
    # Create HTTP response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"product_{product.id}_{product.name.replace(' ', '_')}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response