from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import RegulatoryData
from datetime import datetime
from django.db.models import Q

class DashboardView(ListView):
    model = RegulatoryData
    template_name = 'ri_app/dashboard.html'
    context_object_name = 'items'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering
        agency = self.request.GET.get('agency')
        if agency:
            queryset = queryset.filter(agency=agency)
            
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        drug_name = self.request.GET.get('drug_name')
        if drug_name:
            queryset = queryset.filter(drug_name=drug_name)
    
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(summary__icontains=search)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for item in context['items']:
            if isinstance(item.date, str):
                try:
                    item.date = datetime.strptime(item.date, '%Y-%m-%d')
                except ValueError:
                    item.date = None  # or handle invalid format
        context['agencies'] = RegulatoryData.objects.values_list('agency', flat=True).distinct()
        context['drug_names'] = RegulatoryData.objects.values_list('drug_name', flat=True).distinct()
        context['categories'] = RegulatoryData.objects.values_list('category', flat=True).distinct()
        return context

class DetailView(DetailView):
    model = RegulatoryData
    template_name = 'ri_app/detail.html'
    context_object_name = 'item'