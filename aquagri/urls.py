#the urls will get accepted from the app directory
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),

]
