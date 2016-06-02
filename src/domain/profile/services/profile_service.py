from django.db.utils import IntegrityError
from src.domain.profile import factories
from src.domain.profile.models import Profile
from src.domain.profile.providers.linkedin.services import linkedin_profile_service
from src.domain.profile.providers.reddit.services import reddit_profile_service
from src.domain.profile.providers.twitter.services import twitter_profile_service
from src.apps.engagement_discovery.enums import ProviderEnum
from src.libs.web_utils.url import url_utils
from src.domain.profile import constants


def get_profile_from_provider_info(profile_external_id, provider_type):
  return Profile.objects.get(profile_external_id=profile_external_id, provider_type=provider_type)


def clean_profile_attrs(profile_attrs, _url_utils=url_utils):
  websites = profile_attrs.get(constants.WEBSITES)

  if websites:
    websites = _url_utils.get_unique_urls_from_iterable(websites)
    profile_attrs[constants.WEBSITES] = websites

  return profile_attrs


def save_profile_from_provider_info(prospect_id, profile_external_id, provider_type, **kwargs):
  try:
    profile = get_profile_from_provider_info(
      profile_external_id,
      provider_type
    )
  # this should be specific: profile.DoesNotExist
  except Profile.DoesNotExist:
    if provider_type == ProviderEnum.twitter:
      profile_attrs = twitter_profile_service.get_twitter_profile_attrs(profile_external_id, **kwargs)
    elif provider_type == ProviderEnum.reddit:
      profile_attrs = reddit_profile_service.get_reddit_profile_attrs(profile_external_id, **kwargs)
    elif provider_type == ProviderEnum.linkedin:
      profile_attrs = linkedin_profile_service.get_linkedin_profile_attrs(profile_external_id, **kwargs)
    else:
      raise Exception('Invalid provider type')

    profile_attrs = clean_profile_attrs(profile_attrs)

    profile = factories.construct_profile_from_provider_info_and_profile_attrs(
      prospect_id, profile_external_id, provider_type, profile_attrs
    )

    try:
      save_or_update(profile)
    except IntegrityError:
      # This can happen when two identical profiles are saved at almost the exact same time. Ex: One user with
      # multiple comments in a reddit submission.
      profile = get_profile_from_provider_info(
        profile_external_id,
        provider_type
      )

  return profile


def save_or_update(profile):
  profile.save(internal=True)


def get_profile(profile_id):
  return Profile.objects.get(pk=profile_id)

def get_profile_from_uid(profile_uid):
  return Profile.objects.get(profile_uid=profile_uid)
