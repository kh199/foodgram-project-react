import io

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from .filters import IngredientSearchFilter, RecipesFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (FavoriteRecipesSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, TagSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeCreateSerializer

    @staticmethod
    def method_to_post(request, pk, serializers):
        serializer = serializers(data={'user': request.user.id, 'recipe': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def method_to_delete(model, request, pk):
        obj = model.objects.filter(user=request.user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Такого рецепта нет'},
            status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        page = canvas.Canvas(buffer)
        ingredients = IngredientAmount.objects.filter(
            recipe__shoppingcarts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(sum_amount=Sum('amount'))
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        page.setFont('DejaVuSans', size=24)
        page.drawString(200, 750, 'Список покупок:')
        page.setFont('DejaVuSans', size=16)
        height = 700
        for i, item in enumerate(ingredients, start=1):
            page.drawString(50, height,
                            (f'{i}. {item[0]} {item[2]} {item[1]}'))
            height -= 25
        page.showPage()
        page.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping_list.pdf')
