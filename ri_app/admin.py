from django.contrib import admin
from ri_app.models import RegulatoryData

@admin.register(RegulatoryData)
class RegulatoryDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency', 'drug_name', 'category', 'date')
    list_filter = ('agency','drug_name', 'category')
    search_fields = ('title', 'summary')
    readonly_fields = ('article_url', 'source_file')