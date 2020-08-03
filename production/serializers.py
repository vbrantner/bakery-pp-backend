from rest_framework import serializers
from . import models
from django.utils.timezone import now


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')
    recipe_name = serializers.ReadOnlyField(source='recipe.name')
    unit_name = serializers.ReadOnlyField(source='unit.name')

    class Meta:
        model = models.RecipeIngredient
        read_only_fields = [
            'slug', ]
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Measurement
        fields = '__all__'
        read_only_fields = ['slug']
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        lookup_field = 'slug'
        read_only_fields = ['slug']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = ('id', 'url', 'name', 'slug')
        read_only_fields = ['slug']


class RecipeSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='recipe-detail',
    #     lookup_field='slug'
    # )

    class Meta:
        model = models.Recipe
        fields = '__all__'
        read_only_fields = ['modified', 'version', 'slug', 'created']
        # extra_kwargs = {
        #     'url': {'loojkup_field': 'slug'},
        # }


class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    # url = serializers.HyperlinkedIdentityField(
        # view_name='recipe-detail',
        # lookup_field='slug'
    # )

    class Meta:
        model = models.Recipe
        fields = '__all__'
        read_only_fields = ['modified', 'version', 'slug', 'created']
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'},
        # }


class ProductSerializer(serializers.ModelSerializer):
    recipe_name = serializers.ReadOnlyField(source='recipe.name')

    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = ['slug']


class Production(serializers.ModelSerializer):
    unit_name = serializers.ReadOnlyField(source='unit.name')
    recipe_name = serializers.ReadOnlyField(source='recipe.name')
    charge = serializers.ReadOnlyField(source='get_charge')

    class Meta:
        model = models.Production
        fields = '__all__'
        read_only_fields = ['slug', 'recipe_name', 'charge']


class ProductionIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductionIngredients
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    unit_name = serializers.ReadOnlyField(source="unit.name")
    day_name = serializers.ReadOnlyField(source="get_day_name")

    class Meta:
        model = models.Orders
        fields = '__all__'


class ProductionListSerializer(serializers.Serializer):
    product = serializers.CharField(read_only=True)
    # lieferdatum = serializers.DateField(read_only=True)
    # recipe = serializers.CharField(read_only=True)
    # ingredient = serializers.CharField(read_only=True)
    # menge = serializers.FloatField(read_only=True)
    # rest = serializers.DurationField(read_only=True)
    # productiondate = serializers.DateField(read_only=True)
