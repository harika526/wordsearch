from django.urls import path, re_path
# from rest_framework_swagger.views import get_swagger_view
from . import views

# schema_view = get_swagger_view(title='Word Search API')

urlpatterns = [
    path('', views.home, name='home'),
    # path('api/docs/', schema_view, name='api_docs'),
    path('search/', views.get_word, name='get_word'),
]
