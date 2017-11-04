from django.conf.urls import url

from . import views

app_name = 'speisekammer'
url_regex = r'^speisekammer/'

urlpatterns = [
    url(r'^products/$', views.ProductList.as_view(), name='product_list'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product_detail'),

    url(r'^instances/$', views.ProductInstanceList.as_view(), name='product_instance_list'),
    url(r'^instances/(?P<pk>[0-9]+)/$', views.ProductInstanceDetail.as_view(), name='product_instance_detail'),
    url(r'^instances/(?P<pk>[0-9]+)/item_count$', views.ProductItemCount.as_view()),

    url(r'^shopping-lists/$', views.ShoppingLists.as_view(), name='shopping_lists'),
    url(r'^shopping-lists/(?P<pk>[0-9]+)/$', views.ShoppingListDetail.as_view(), name='shopping_list_detail')
]
