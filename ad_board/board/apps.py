from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = 'board'

  # нам надо переопределить метод ready для сигналов
    def ready(self):
        import board.signals
