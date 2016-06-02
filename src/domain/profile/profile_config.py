from django.apps import AppConfig

class ProfileConfig(AppConfig):
  name = 'src.domain.profile'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.profile.event_handlers
