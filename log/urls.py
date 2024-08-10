from django.urls import path, include

from log.views import *

urlpatterns = [
    path('', UserLoginView.as_view(), name='auth'),
    path('regi/', UserRegisterView.as_view(), name='regi'),
    path('main/', include('main.urls')),

]