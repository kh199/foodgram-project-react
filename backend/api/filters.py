from django.contrib.auth import get_user_model
from django_filters import (AllValuesMultipleFilter, FilterSet,
                            ModelChoiceFilter, NumberFilter)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    author = ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = NumberFilter(method='filter_favorites')
    is_in_shopping_cart = NumberFilter(
        method='filter_shopping_cart')

    def filter_favorites(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shoppingcarts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
