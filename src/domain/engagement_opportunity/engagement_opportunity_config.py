from django.apps import AppConfig

class EngagementOpportunityConfig(AppConfig):
  name = 'src.domain.engagement_opportunity'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.engagement_opportunity.event_handlers
