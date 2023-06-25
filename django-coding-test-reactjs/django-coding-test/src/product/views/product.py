from typing import Any, Dict
from django.db.models.query import QuerySet
from django.views import generic

from product.models import Variant, Product, ProductVariantPrice, ProductVariant
from django.core.paginator import Paginator

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        filter_string = {}
        filter_mappings = {
            'title': 'title',
            'variant': 'productvariant__variant_title',
            'price_from': 'productvariantprice__price__gte',
            'price_to': 'productvariantprice__price__lte',
            'date': 'created_at__date'
        }
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string = {
                    filter_mappings[key]: value
                    for key, value in self.request.GET.items()
                    if key in filter_mappings and value
                }
        
        products_qs = Product.objects.prefetch_related('productvariantprice_set').filter(**filter_string)
        products = []
        for product in products_qs:
            varients = product.productvariantprice_set.all()
            products.append({
                'product': product,
                'varients': varients
            })
        return products


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page', '1')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['total_items'] = paginator.count
        context['start_number'] = (page_obj.number - 1) * self.paginate_by + 1
        context['end_number'] = page_obj.number * self.paginate_by

        variants_qs = Variant.objects.prefetch_related('productvariant_set').all()
        varients = []
        for variant in variants_qs:
            product_variants = variant.productvariant_set.all()
            varients.append({
                'title': variant.title,
                'prod_varient': product_variants
            })
        context['varients'] = varients
        return context

