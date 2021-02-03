from django.contrib import admin

from .models import Company, Site, Keyword


@admin.register(Site)
class PositionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company)
admin.site.register(Keyword)
