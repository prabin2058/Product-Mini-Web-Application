from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "stock_quantity",
        "status",
        "category",
        "is_active",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "is_active", "category")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
