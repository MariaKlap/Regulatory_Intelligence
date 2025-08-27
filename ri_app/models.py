# ri_app/models.py
from django.db import models

class RegulatoryData(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    article_url = models.URLField(max_length=1000)
    Product_Type = models.CharField(max_length=200, blank=True, null=True)  # Uppercase
    Document_Type = models.CharField(max_length=200, blank=True, null=True)  # Uppercase
    Drug_names = models.CharField(max_length=200, blank=True, null=True)  # Uppercase
    source_file = models.CharField(max_length=255, blank=True, null=True)
    agency = models.CharField(max_length=100, blank=True, null=True, default='Unknown')  # Added null/blank
    category = models.CharField(max_length=100, blank=True, null=True, default='General')  # Added null/blank
    viewed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Regulatory Intelligence Data"
        verbose_name_plural = "Regulatory Intelligence Data"
        ordering = ['-date']
    
    def __str__(self):
        return self.title