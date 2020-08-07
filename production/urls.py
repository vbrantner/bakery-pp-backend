from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'temperaturesensor', views.TemperatureSensorViewSet)
router.register(r'measurements', views.MeasurementViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'recipeingredient', views.RecipeIngredientViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'production', views.ProductionViewSet)
router.register(r'productioningredient', views.ProductionIngredientViewSet)
router.register(r'orders', views.OrdersViewSet)
# router.register(r'productmaking', views.ProductMakingViewSet)
# router.register(r'productmakingconsumption',
#                 views.ProductMakingConsumptionViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'orderoverviewList/', views.orderOverviewList.as_view()),
    path(r'make/<int:production_id>/', views.makeRecipe.as_view()),
    path(r'mixinglist/', views.MixingList.as_view()),
    # path(r'temperaturesensor/', views.ListTemperatureSensor.as_view())
#    path(r'recipes/<slug:recipe>/<slug:ingredient>/', views.RecipeIngredientSpecificRecipe.as_view(), name='recipe-ingredient-detail'),
]
