from django.db import connection
SQL = """
WITH RECURSIVE plan as (
    SELECT p.name as product,
           o.date as lieferdatum,
           r.name as name,
           i.name as ingredient,
           ROUND((ri.amount /
                  ( SELECT sum(ri.amount)
                  FROM production_recipeingredient ri
                  WHERE ri.recipe_id = r.id
                  )) * o.amount, 2) as menge,
           r.rest as rest,
           DATE(o.date, -IFNULL(r.rest/1000, 0) || ' seconds') as produktionsdatum
    FROM production_orders o, production_product p, production_recipe r, production_recipeingredient ri, production_ingredient i
    WHERE r.id = ri.recipe_id AND
          ri.ingredient_id = i.id AND
          o.product_id = p.id AND
          p.recipe_id = r.id

    UNION ALL

    SELECT plan.product,
           plan.lieferdatum,
           plan.name || '-' || r.name,
           i.name,
           ROUND((ri.amount /
                  ( SELECT sum(ri.amount)
                  FROM production_recipeingredient ri
                  WHERE ri.recipe_id = r.id
                  )) * plan.menge, 2) as Menge,
           r.rest,
           DATE(plan.lieferdatum, -IFNULL((plan.rest+r.rest)/1000000, 0) || ' seconds') as produktionsdatum
    FROM plan, production_recipe r, production_ingredient i, production_recipeingredient ri
    WHERE plan.ingredient = r.name AND
          r.id = ri.recipe_id AND
          ri.ingredient_id = i.id

)
SELECT * FROM plan
ORDER BY plan.produktionsdatum DESC"""

cursor = connection.cursor()