from django.urls import path
from django.http import HttpResponse

def api_root(request):
    return HttpResponse("API is working", content_type="text/plain")

urlpatterns = [
    path('api/', api_root, name='api_root'),
]