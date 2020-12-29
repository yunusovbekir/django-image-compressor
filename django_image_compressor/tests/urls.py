from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from example_app.views import ExampleCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', ExampleCreateView.as_view(), name='create_view')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
