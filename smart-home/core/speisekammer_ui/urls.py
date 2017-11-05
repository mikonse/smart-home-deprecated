from django.conf.urls import url

from . import views

app_name = 'speisekammer_ui'
urlpatterns = [
    url(r'^index/$', views.Index, name='index'),

    url(r'^products/$', views.ProductList.as_view(), name='product-list'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),

    url(r'^shopping-lists/$', views.ShoppingLists.as_view(), name='shopping-lists'),
    url(r'^shopping-lists/(?P<pk>[0-9]+)/$', views.ShoppingListDetail.as_view(), name='shopping-list-detail'),
]
