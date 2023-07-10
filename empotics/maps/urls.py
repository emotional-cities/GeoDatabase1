from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.landing_page),
    path('london/',views.london_page),
    path('lansing/',views.lansing_page),
    path('lisbon/',views.lisbon_page),
    path('copenhagen/',views.copenhagen_page),
    path('checkbox-page/', views.checkbox_page, name='checkbox_page'),
]
