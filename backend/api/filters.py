from django_filters import AllValuesMultipleFilter, FilterSet

from recipes.models import Recipe


class TagFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
