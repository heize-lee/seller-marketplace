<<<<<<< HEAD
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from order.models import Order
from seller_product.models import Product,Cart
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home_view(request):
    products = Product.objects.all()
    context = {
        'object_list' : products
    }
    return render(request,'home.html',context)
=======
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from seller_product.models import Product,Category, Cart
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



>>>>>>> ee2883aaeb9b88c14f9b865b323a3adc6827b341
