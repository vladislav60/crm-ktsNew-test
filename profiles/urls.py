from django.urls import path
from . import views

urlpatterns = [
    # other URL patterns
    path('edit/', views.edit_profile, name='edit_profile'),
]