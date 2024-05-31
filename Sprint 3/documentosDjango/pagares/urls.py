from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('pagares/', views.pagare_list),
    path('firma/', csrf_exempt(views.firma), name='firma'),
    path('pagareCreate/', csrf_exempt(views.pagare_create), name='pagareCreate'),
]