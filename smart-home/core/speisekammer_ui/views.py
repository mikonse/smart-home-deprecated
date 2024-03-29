from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from speisekammer.models import Product, ShoppingList
from .forms import ProductForm


class Index(TemplateView):
    template_name = 'speisekammer_ui/index.html'


class ProductList(FormView, ContextMixin):
    template_name = 'speisekammer_ui/product_list.html'
    form_class = ProductForm
    success_url = reverse_lazy('speisekammer_ui:product-list')

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)

        products = Product.objects.all()
        context.update({'products': products})
        return context

    def form_valid(self, form):
        form.save()
        return super(ProductList, self).form_valid(form)


class ProductDetail(TemplateView):
    template_name = 'speisekammer_ui/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context.update({'product': Product.objects.get(pk=self.kwargs['pk'])})

        return context


class ShoppingLists(TemplateView):
    template_name = 'speisekammer_ui/shopping_lists.html'

    def get_context_data(self, **kwargs):
        context = super(ShoppingLists, self).get_context_data(**kwargs)
        context.update({
            'shopping_lists': ShoppingList.objects.all()
        })

        return context


class ShoppingListDetail(TemplateView):
    template_name = 'speisekammer_ui/shopping_list_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShoppingListDetail, self).get_context_data(**kwargs)
        context.update({
            'shopping_list': ShoppingList.objects.get(pk=self.kwargs['pk'])
        })

        return context
