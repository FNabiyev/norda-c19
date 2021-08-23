from django.urls import path
from .views import *

urlpatterns = [
    path('', Home),
    path('about/', AboutUs),
    path('category/<int:id>/', Category),
    path('blog/', Blog),
    path('contact/', Contact),
    path('send-msg/', SendMsg),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('addtocart/<int:pk>/', AddToCart),
]
