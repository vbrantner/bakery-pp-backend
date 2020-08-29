from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = DefaultRouter()
router.register(r"employee", views.EmployeeViewSet)
router.register(r"attandance", views.AttandanceViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'attandanceDate/<int:id>/<slug:date>/', views.ListAttandanceWithDate.as_view())
]
