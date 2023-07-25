from django.contrib import admin
from .models import User
from .models import Subordination


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Subordination)
class SubordinationAdmin(admin.ModelAdmin):
    pass
