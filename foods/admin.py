from django.contrib import admin
from django.db.models import Q
from .models import Food


class HasImageFilter(admin.SimpleListFilter):
    title = 'has image'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Has Image'),
            ('no', 'No Image'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image__exact='').exclude(image__isnull=True)
        if self.value() == 'no':
            return queryset.filter(Q(image__exact='') | Q(image__isnull=True))
        return queryset


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

    list_display = (
        'name',
        'category',
        'min_age_months',
        'is_allergen',
        'is_authorised',
        'has_image',
        'created_by_user',
    )
    list_filter = (
        'is_authorised',
        'category',
        'is_allergen',
        HasImageFilter,
    )
