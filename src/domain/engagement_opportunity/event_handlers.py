from django.dispatch import receiver

from src.domain.engagement_opportunity.services import engagement_opportunity_tasks
from src.domain.profile.services import profile_tasks
from src.domain.prospect.services import prospect_tasks
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered


@receiver(engagement_opportunity_discovered)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  engagement_opportunity_discovery_object = kwargs['engagement_opportunity_discovery_object']
  (
    prospect_tasks.save_prospect_from_provider_info_task.s(
      engagement_opportunity_discovery_object.profile_external_id,
      engagement_opportunity_discovery_object.provider_type
    )
    |
    profile_tasks.save_profile_from_provider_info_task.s(
      engagement_opportunity_discovery_object.profile_external_id,
      engagement_opportunity_discovery_object.provider_type
    )
    |
    engagement_opportunity_tasks.create_engagement_opportunity_task.s(engagement_opportunity_discovery_object)
    |
    engagement_opportunity_tasks.add_topic_to_engagement_opportunity_task.s(
      engagement_opportunity_discovery_object.topic_type
    )
  ).delay()
