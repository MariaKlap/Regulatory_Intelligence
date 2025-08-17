import json 
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import RegulatoryData
from datetime import datetime
from django.db.models import Q
from django.utils.timezone import make_aware
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


class DashboardView(ListView):
    model = RegulatoryData
    template_name = 'ri_app/dashboard.html'
    context_object_name = 'items'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # Viewed status filter
        viewed_status = self.request.GET.get('viewed')
        if viewed_status == 'read':
            queryset = queryset.filter(viewed=True)
        elif viewed_status == 'unread':
            queryset = queryset.filter(viewed=False)

        # Date Filtering
        date_range = self.request.GET.get('date_range')
        if date_range and 'to' in date_range:
            try:
                date_from_str, date_to_str = date_range.split(' to ')
                # Parse as YYYY-MM-DD (matches database storage)
                date_from = datetime.strptime(date_from_str.strip(), '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to_str.strip(), '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=date_from, date__lte=date_to)
            except (ValueError, AttributeError) as e:
                print(f"Date filter error: {e}")
        
        # Filtering
        product_type = self.request.GET.get('product_type')
        if product_type:
            queryset = queryset.filter(Product_Type=product_type)
            
        document_type = self.request.GET.get('document_type')
        if document_type:
            queryset = queryset.filter(Document_Type=document_type)
            
        drug_name = self.request.GET.get('drug_name')
        if drug_name:
            queryset = queryset.filter(Drug_names=drug_name)
    
    
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
        product_types = RegulatoryData.objects.values_list('Product_Type', flat=True).distinct()
        document_types = RegulatoryData.objects.values_list('Document_Type', flat=True).distinct()
        drug_names = RegulatoryData.objects.values_list('Drug_names', flat=True).distinct()
        

        def get_filter_values(field_name):
            # Get all distinct values including empty/None
            values = RegulatoryData.objects.exclude(
                **{f"{field_name}__isnull": True}
            ).order_by(field_name).values_list(field_name, flat=True).distinct()
            
            # Clean and prepare values
            cleaned = set()
            for value in values:
                if value:  # Only process non-empty values
                    if isinstance(value, str):
                        value = value.strip()
                        # Skip obviously placeholder values
                        if value.lower() not in ['none', 'other', 'other type', '']:
                            # Handle comma-separated values (for drug names)
                            if field_name == 'Drug_names' and ',' in value:
                                for drug in value.split(','):
                                    cleaned.add(drug.strip())
                            else:
                                cleaned.add(value)
            return sorted(cleaned) if cleaned else []
        
        context.update({
            'product_types': get_filter_values('Product_Type'),
            'document_types': get_filter_values('Document_Type'),
            'drug_names': get_filter_values('Drug_names'),
            'selected_product_type': self.request.GET.get('product_type', ''),
            'selected_document_type': self.request.GET.get('document_type', ''),
            'selected_drug_name': self.request.GET.get('drug_name', ''),
            'current_search': self.request.GET.get('search', ''),
            'current_date_range': self.request.GET.get('date_range', ''),
            'selected_viewed': self.request.GET.get('viewed', '')
        })
        return context


class DetailView(DetailView):
    model = RegulatoryData
    template_name = 'ri_app/detail.html'
    context_object_name = 'item'

# Add the new function-based view here
@csrf_exempt
@require_POST
def update_viewed(request, item_id):
    """
    AJAX endpoint to toggle viewed status of an item.
    Called from JavaScript in the detail template.
    """
    try:
        item = RegulatoryData.objects.get(id=item_id)
        data = json.loads(request.body)
        item.viewed = data.get('viewed', False)
        item.save()
        return JsonResponse({'success': True})
    except RegulatoryData.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)