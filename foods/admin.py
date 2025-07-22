from django.contrib import admin
from django.db.models import Q
from .models import Food


class HasImageFilter(admin.SimpleListFilter):
    """
    Custom admin filter to filter Food objects by whether they have an image.

    Provides two options:
        - 'Has Image': Shows foods with an image.
        - 'No Image': Shows foods without an image.
    """

    title = 'has image'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        """
        Return the filter options for the admin sidebar.

        Args:
            request: The current admin request.
            model_admin: The current model admin instance.

        Returns:
            tuple: A tuple of filter options.
        """
        return (
            ('yes', 'Has Image'),
            ('no', 'No Image'),
        )

    def queryset(self, request, queryset):
        """
        Filter the queryset based on the selected filter value.

        Args:
            request: The current admin request.
            queryset: The original queryset.

        Returns:
            QuerySet: The filtered queryset.
        """
        if self.value() == 'yes':
            return (
                queryset.exclude(image__exact='').exclude(image__isnull=True)
            )
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
