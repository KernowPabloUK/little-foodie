from .models import Consistency
from .models import Preparation
from .models import FeedingMethod
from .models import SatisfactionLevel
from .models import FoodLog
from django.contrib import admin

# Register your models here.
admin.site.register(Consistency)
admin.site.register(Preparation)
admin.site.register(FeedingMethod)
admin.site.register(SatisfactionLevel)
admin.site.register(FoodLog)
