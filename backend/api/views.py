from rest_framework import viewsets, status
from recipes.models import Ingredient, Tag, Recipe, Favorite, ShoppingCart
from .serializers import IngredientSerializer, TagSerializer, RecipeCreateSerializer, FavoriteRecipesSerializer, RecipeListSerializer, ShoppingCartSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly
from .filters import TagFilter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import filters


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filterset_class = TagFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeCreateSerializer

    @staticmethod
    def method_to_post(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def method_to_delete(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.method_to_post(
            request=request, pk=pk, serializers=FavoriteRecipesSerializer)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.method_to_post(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.method_to_delete(
            request=request, pk=pk, model=Favorite)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.method_to_delete(
            request=request, pk=pk, model=ShoppingCart)
