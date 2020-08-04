from django.urls import path
from products.views import (
    # product_list_view,
    ProdutListView,
    # product_detail_view,
    # ProdutFeaturedListView,
    # ProdutFeaturedDetailView,
    ProdutDetailSlugView
)

app_name = "products"

urlpatterns = [
    path('', ProdutListView.as_view(), name="list"),
    path('<slug>', ProdutDetailSlugView.as_view(), name="detail"),

]

