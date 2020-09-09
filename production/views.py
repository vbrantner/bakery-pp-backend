# Create your views here.
from datetime import datetime, timedelta
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import action
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Measurement.objects.all()
    serializer_class = serializers.MeasurementSerializer
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This endpoint provides access to categories.
    retrieve:
    Retrieves a category
    list:
    Retrieves all possible categories
    """
    permission_classes = [IsAuthenticated]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    detail_serializer_class = serializers.RecipeDetailSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super(viewsets.ModelViewSet, self).get_serializer_class()


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.RecipeIngredient.objects.all()
    serializer_class = serializers.RecipeIngredientSerializer


class TemperatureSensorViewSet(viewsets.ModelViewSet):
    queryset = models.TemperaturSensor.objects.all().order_by('date_time')[:6]
    serializer_class = serializers.TemperaturSensorSearializer


class orderOverviewList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        sql = """
 WITH RECURSIVE plan as (
        SELECT p.name as Produkt,
               1 as depth,
               o.id as OrderID,
               o.date as Backdatum,
               r.name as Rezept,
               r.id as RezeptID,
               r.charge_amount as ChargeMenge,
               i.name as ingredient,
               ROUND((ri.amount /
                      ( SELECT sum(ri.amount)
                      FROM production_recipeingredient ri
                      WHERE ri.recipe_id = r.id
                      )) * o.amount, 3) as Menge,
               m.name as Einheit,
               m.id as EinheitID,
               r.rest as rest,
               o.date - r.rest as Mischdatum
        FROM production_orders o, production_product p, production_measurement m, production_recipe r, production_recipeingredient ri, production_ingredient i
        WHERE r.id = ri.recipe_id AND
              ri.unit_id = m.id AND
              ri.ingredient_id = i.id AND
              o.product_id = p.id AND
              p.recipe_id = r.id AND
              o.date > NOW() - INTERVAL '1 DAY' AND
              o.date <= NOW() + INTERVAL '4 DAY'

        UNION ALL

        SELECT plan.Produkt,
               plan.depth + 1,
               plan.OrderID,
               plan.Backdatum as Backdatum,
               r.name,
               r.id as RezeptID,
               r.charge_amount as ChargeMenge,
               i.name,
               ROUND((ri.amount /
                      ( SELECT sum(ri.amount)
                      FROM production_recipeingredient ri
                      WHERE ri.recipe_id = r.id
                      )) * plan.menge, 3) as Menge,
               m.name as Einheit,
               m.id as EinheitID,
               plan.rest + r.rest,
               plan.Mischdatum - r.rest as Mischdatum
        FROM plan, production_recipe r, production_ingredient i, production_recipeingredient ri, production_measurement m
        WHERE plan.ingredient = r.name AND
              r.id = ri.recipe_id AND
              ri.unit_id = m.id AND
              ri.ingredient_id = i.id AND
              plan.Menge > 0.2
    )
    SELECT
           ChargeMenge,
           array_agg(DISTINCT OrderID) as OrderID,
           case cast (to_char(Mischdatum, 'd') as integer)
               when 0 then to_char(Mischdatum, 'dd-mm') || ' Sa'
               when 1 then to_char(Mischdatum, 'dd-mm') || ' So'
               when 2 then to_char(Mischdatum, 'dd-mm') || ' Mo'
               when 3 then to_char(Mischdatum, 'dd-mm') || ' Di'
               when 4 then to_char(Mischdatum, 'dd-mm') || ' Mi'
               when 5 then to_char(Mischdatum, 'dd-mm') || ' Do'
               else to_char(Mischdatum, 'dd-mm') || ' Fr' end as Mischdatum_tag,
           to_char(plan.Mischdatum, 'yyyy-mm-dd') as Mischdatum,
           max(to_char(plan.Backdatum, 'yyyy-mm-dd')) as Backdatum,
           Rezept,
           RezeptID,
           replace(TO_CHAR(round(sum(Menge), 3), '9990D999'), '.', ',') as Menge,
           Einheit,
           EinheitID
    FROM plan
    WHERE NOT EXISTS(SELECT p.recipe_id rid,
                            p.mix_date,
                            o.id as oid
                    FROM production_production p, production_production_orders p_o, production_orders o
                    WHERE p_o.orders_id = o.id AND
                          p_o.production_id = p.id AND
                          p.recipe_id = RezeptID AND
                          p.mix_date = plan.Mischdatum AND
                          o.id = OrderID)
    GROUP BY ChargeMenge, plan.Mischdatum, Rezept, RezeptID, plan.Einheit, plan.einheitid
    ORDER BY plan.Mischdatum DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = dictfetchall(cursor)
        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Production.objects.all()
    serializer_class = serializers.Production
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['checked', 'recipe', 'finished']
    ordering_fields = ['finished']


class MixingList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        sql = """
SELECT r.name as rezeptname,
       to_char(p.mix_date, 'dd-mm-yyyy') as mischdatum,
       p.id as production_id,
       replace(TO_CHAR(p.amount, '9999D999'),'.',',') as menge,
       BOOL_OR(pi.checked) as misch_status,
       p.checked as teig_status,
       r.id || '-' || p.id as charge,
       m.name as einheit
FROM production_production p
LEFT JOIN production_productioningredients pi on p.id = pi.production_id
LEFT JOIN production_measurement m ON p.unit_id = m.id
LEFT JOIN production_recipe r on p.recipe_id = r.id
WHERE p.mix_date > NOW() - INTERVAL '2 DAY' AND
      p.mix_date <= NOW() + INTERVAL '2 DAY'
GROUP BY p.id, r.id, m.name;;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            mixing_list = dictfetchall(cursor)
        return Response(mixing_list)


class ProductionIngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.ProductionIngredients.objects.all()
    serializer_class = serializers.ProductionIngredientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['production']


class OrdersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Orders.objects.all()
    serializer_class = serializers.OrdersSerializer


class makeRecipe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, production_id, format=None):
        sql = """
SELECT ri.id as id,
       r.id as rezept_id,
       r.name as rezept_name,
       r.slug as slug,
       TO_CHAR(p.amount, '9999D999') as gesamt_menge,
       pi.id as production_ingredient_id,
       i.name as rohstoff_name,
       i.id as rohstoff_id,
       ri.id,
       ri.temperatur,
       pi.checked as checked,
       m.name as einheit,
       m.id as einheit_id,
       replace(TO_CHAR(ROUND(p.amount * ri.amount / (SELECT sum(ri_h.amount) FROM production_recipeingredient ri_h WHERE ri_h.recipe_id = r.id), 3), '9990D999'), '.', ',') as menge
FROM production_production p
LEFT JOIN production_recipeingredient ri ON ri.recipe_id = p.recipe_id
LEFT JOIN production_productioningredients pi ON p.id = pi.production_id AND pi.ingredient_id = ri.ingredient_id
INNER JOIN production_recipe r ON p.recipe_id = r.id
INNER JOIN production_ingredient i ON ri.ingredient_id = i.id
INNER JOIN production_measurement m ON ri.unit_id = m.id
WHERE p.id = {};
        """.format(production_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            recipe = dictfetchall(cursor)
        return Response(recipe)
