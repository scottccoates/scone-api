from django.apps import AppConfig

class ClientConfig(AppConfig):
  name = 'src.domain.client'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.client.event_handlers
