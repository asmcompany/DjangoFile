from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404

from .models import Product

# Create your views here.

class ProdutFeaturedListView(ListView):
    template_name = "products/product_list.html"

    def get_queryset(self):
        return Product.objects.all().get_featured()


class ProdutFeaturedDetailView(DetailView):
    template_name = "products/product_featured_detail.html"

    def get_queryset(self):
        return Product.objects.get_featured()




# raveshe kotah
class ProdutListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/product_list.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProdutListView, self).get_context_data(*args, **kwargs)
        context['brand'] = 'products brand'
        print(context)
        return context

    def get_queryset(self):
        return Product.objects.all()


# raveshe dovom
def product_list_view(request):
    products = Product.objects.all()
    context = {
        "object_list": products
    }

    return render(request, "products/product_list.html", context)


class ProdutDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            product = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("product doesnt Exists")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            product = qs.first()
        except:
            raise Http404("not found ...")

        return product


class ProdutDetailView(DetailView):
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super (ProdutDetailView, self).get_context_data(*args, **kwargs)
        context['abc'] = "this is data in context test"
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        productId = self.kwargs.get('pk')
        product = Product.objects.get_by_id(productId)
        if product is None:
            raise Http404("product does not found from custom model manager")
        return product

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     productId = self.kwargs.get('pk')
    #     return Product.objects.filter(id=productId)

# raveshe dovom
def product_detail_view(request, productId=None, *args, **kwargs):
  # try:
  #     product = Product.objects.get(id=productId)
  # except Product.DoesNotExist:
  #     raise Http404("product does not found")
  # except:
  #     print("what?")

  #qs = Product.objects.filter(id=productId)
  #if qs.exists() and qs.count() == 1:
  #    product = qs.first()
  #else:
  #    raise Http404("product does not found")
  #product = get_object_or_404(Product, id=productId)
    product = Product.objects.get_by_id(productId)
    if product is None:
        raise Http404("product does not found from custom model manager")

    context = {
        "object": product
    }

    return render(request, "products/product_detail.html", context)