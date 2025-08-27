from django.contrib import admin
from ri_app.models import RegulatoryData

@admin.register(RegulatoryData)
class RegulatoryDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'Drug_names', 'Product_Type', 'Document_Type')
    list_filter = ('Product_Type', 'Document_Type', 'Drug_names')
    search_fields = ('title', 'summary', 'Drug_names', 'Product_Type', 'Document_Type')
    readonly_fields = ('article_url', 'source_file')