from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime


DAYNAME = ["Mo", "Di", "Mit", "Do", "Fr", "Sa", "So"]


def germanslugify(value):
    replacements = [(u'ä', u'ae'), (u'ö', u'oe'), (u'ü', u'ue')]
    for (s, r) in replacements:
        value = value.replace(s, r)
    return slugify(value)


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SupplierItems(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = germanslugify(self.name)
        super(SupplierItems, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)

    def save(self, *args, **kwargs):
        self.slug = germanslugify(self.name)

        super(Ingredient, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class IngredientSupplierItems(models.Model):
    supplier_item = models.ForeignKey(SupplierItems, on_delete=models.PROTECT)
    date_from = models.DateTimeField()
    date_until = models.DateTimeField()
    Ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)


class Measurement(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Measurement, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    version = models.IntegerField()
    temperatur = models.FloatField(blank=True, null=True)
    mixTimeOne = models.CharField(max_length=150, blank=True, null=True)
    mixTimeTwo = models.CharField(max_length=150, blank=True, null=True)
    rest = models.DurationField(blank=True, null=True)
    charge_amount = models.DecimalField(decimal_places=3, max_digits=15)
    charge_unit = models.ForeignKey(Measurement, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
            self.created = datetime.now()
            self.version = 1

        self.modified = datetime.now()
        self.version = self.version + 1
        super(Recipe, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        get_latest_by = 'created'


class RecipeIngredient(models.Model):
    amount = models.DecimalField(decimal_places=3, max_digits=100)
    unit = models.ForeignKey(Measurement, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    temperatur = models.FloatField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name='ingredients')
    slug = models.SlugField()

    def __str__(self):
        return '{} {} {}'.format(self.amount, self.unit, self.ingredient.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ingredient)
        super(RecipeIngredient, self).save(*args, **kwargs)

    class Meta:
        ordering = ['ingredient']


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Orders(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=3, max_digits=20)
    unit = models.ForeignKey(Measurement, on_delete=models.PROTECT)

    def get_day_name(self):
        return '{}'.format(DAYNAME[self.date.weekday()])


class Production(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    orders = models.ManyToManyField(Orders)
    slug = models.SlugField()
    mix_date = models.DateField()
    bake_date = models.DateField()
    created = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    checked = models.BooleanField()
    actual_temperatur = models.DecimalField(decimal_places=2, max_digits=10, null=True, default=0)
    amount = models.DecimalField(decimal_places=3, max_digits=100)
    unit = models.ForeignKey(Measurement, on_delete=models.PROTECT)
    product_list_id = models.CharField(max_length=300, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.id) + '-' + self.recipe.name)
        super(Production, self).save(*args, **kwargs)

    def get_charge(self):
        return '{}-{}'.format(self.id, self.recipe.id)

    def __str__(self):
        return self.recipe.name


class ProductionIngredients(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    # slug = models.SlugField()
    date = models.DateTimeField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=3, max_digits=100)
    unit = models.ForeignKey(Measurement, on_delete=models.PROTECT)
    checked = models.BooleanField()

    class Meta:
        unique_together = (("production", "ingredient"),)

    # def save(self, *args, **kwargs):
    #     super(Production, self).save(*args, **kwargs)
    #     self.slug = slugify(str(self.id) + '-' + self.product.name)

    def __str__(self):
        return self.production_id
