from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm, LoginForm, RegisterForm
from products.models import Product
from django.contrib import auth
import requests
import json

def home_page(request):
    print(f"is user logged in : {request.user.is_authenticated}")
    products =  Product.objects.all()
    labels = []
    data = []
    
    response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,ADA,BNB,DOT,LTC&tsyms=USD').json()

   
 
    queryset = Product.objects.order_by('-like_count')[:7]
    for product in queryset:
        labels.append(product.title)
        data.append(product.like_count)
    context = {
        "title": "صفحه اصلی",
        "content": "خوش امدید",
        "brand": "Topleaarn Eshop From Views.py",
        "object_list": products,
        'labels': labels,
        'data': data,
        'response': response
        
    }
    if request.user.is_authenticated:
        context["new_content"] = "this is new content"
    return render(request, "index.html", context)



# CHART!!
# def pie_chart(request):
#     labels = []
#     data = []

#     queryset = Product.objects.order_by('-like_count')[:7]
#     for product in queryset:
#         labels.append(product.title)
#         data.append(product.like_count)

#     return render(request, 'index.html', {
#         'labels': labels,
#         'data': data,
#     })




def home_page_old(request):
    html = """
    <!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Bootstrap 101 Template</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
  </body>
</html>
    
    """
    return HttpResponse(html)


def about_page(request):
    context = {
        "title": "درباره ما",
        "content": "برنامه نویس"
    }
    return render(request,"about-page.html",context)


def contact_page(request):
    contact_form= ContactForm()
    context = {
        "title": "کانتکت",
        "content": "this is contact",
        "form": contact_form
    }

    if contact_form.is_valid():
        res = contact_form.cleaned_data
        print(res)
        print(res["fullname"])

   #if request.method == "POST":
   #print(request.POST.get('fullname'))
   #print(request.POST.get('email'))
   #print(request.POST.get('message'))

    return render(request, "contact/view.html", context)

def login_page(request):
    print(f"is user logged in : {request.user.is_authenticated}")
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        userName = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=userName, password=password)
        if user is not None:
            login(request, user)
            context["form"] = LoginForm()
            return redirect("/")
        else:
            print("error")

    return render(request, "auth/login.html", context)

User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        userName = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username=userName, email=email, password=password)
        print(new_user)
    return render(request, "auth/register.html", context)




def log_out(request):
    logout(request)
    return redirect('/')















# import requests

# url = "https://veriphone.p.rapidapi.com/verify"

# querystring = {"phone":"+4915123577723"}

# headers = {
#     'x-rapidapi-key': "SIGN-UP-FOR-KEY",
#     'x-rapidapi-host': "veriphone.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
