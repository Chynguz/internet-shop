"""electronics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.main.views import add_to_cart, remove, MainListView, AboutUsView, CardView, InfoView, CategoryView, search

urlpatterns = [
    # path('', main, name='main'),
    path('', MainListView.as_view(), name='main'),
    path('info/<int:id>', InfoView.as_view(), name='info'),
    path('add_to_cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('cart/', login_required(CardView.as_view()), name='cart'),
    path('remove/<int:id>', remove, name='remove'),
    path('search/', search, name='search'),
    path('category/<slug:slug>', CategoryView.as_view(), name='category'),
    path('about/', AboutUsView.as_view(), name='about'),

]
