from src.domain.engagement_opportunity.models import EngagementOpportunity
from src.apps.assignment_delivery import constants
from src.apps.assignment_delivery.delivery_data_providers.base_delivery_data_provider import BaseDeliveryDataProvider


class TwitterDeliveryDataProvider(BaseDeliveryDataProvider):
  def _provide_internal_delivery_data(self, assigned_entity):

    if not isinstance(assigned_entity, EngagementOpportunity):
      raise ValueError("This data provider only works with EO's")
    else:
      engagement_opportunity = assigned_entity
    ret_val = {}

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.USERNAME] = profile_attrs[constants.PROFILE_URL]
    ret_val[constants.NAME] = profile_attrs[constants.NAME]
    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs[constants.FOLLOWERS_COUNT]
    ret_val[constants.FOLLOWING_COUNT] = profile_attrs[constants.FOLLOWING_COUNT]
    ret_val[constants.URL] = eo_attrs[constants.URL]
    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)

    return ret_val
