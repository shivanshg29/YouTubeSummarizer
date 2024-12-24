from django.urls import path
from .views import *

urlpatterns=[
    path('',get_summary,name='get_summary')
]