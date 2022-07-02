from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through


class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInRecipeInline,
    ]
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-empty-'


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInRecipeInline,
    ]
    exclude = ('ingredients',)
    list_display = ('id', 'author', 'name', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'

    def count_favorites(self, obj):
        return obj.favorites.count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(IngredientAmount)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
