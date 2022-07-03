from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
        )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
        )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
        )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цветовой код'
        )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Slug'
        )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
        )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
        )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
        )
    text = models.TextField(
        verbose_name='Текст рецепта'
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientAmount',
        verbose_name='Ингредиенты'
        )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги'
        )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления в минутах'
        )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientsamount',
        verbose_name='Ингредиент'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientsamount',
        verbose_name='Рецепт'
        )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиента'
        )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количества ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredient_amount')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
        )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name='Пользователь'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name='Рецепт'
        )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]
