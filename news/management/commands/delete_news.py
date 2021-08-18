from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление всех новостей'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи? yes/no' '\n')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = str(options['category'])
                print(category)
                Post.objects.filter(post_category__category = category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Succesfully deleted all news'))  # в случае неправильного подтверждения, говорим что в доступе отказано
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category'))
