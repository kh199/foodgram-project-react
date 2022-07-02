from csv import reader

from django.core.management import BaseCommand

from recipes.models import Ingredient

CSV_PATH = '../data/ingredients.csv'


class Command(BaseCommand):
    help = "Loads data from ingredients.csv"

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print('data already loaded')
            return
        print("Loading data")

        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            ingreader = reader(f, delimiter=',')
            for row in ingreader:
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
