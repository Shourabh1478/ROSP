"""befit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from Login.views import *
from store.views import *
from chatbot.views import chat_view, postchat_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Signup_view),
    path('landing', Landing_page),
    path('store/',store, name="store"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),

    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
    path('chat',chat_view,name="chat"),
    path("postchat/",postchat_view,name="postchat"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)