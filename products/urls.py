from django.urls import path
from django.conf.urls import url
from products.views import ProdutListView, ProdutDetailSlugView, like
    


app_name = "products"

urlpatterns = [
    path('', ProdutListView.as_view(), name="list"),
    path('<slug>', ProdutDetailSlugView.as_view(), name="detail"),
    path('like/',like , name='like'),

]

