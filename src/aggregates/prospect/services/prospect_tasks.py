from celery import shared_task
from src.aggregates.profile.services import profile_service

from src.aggregates.prospect.services import prospect_service


@shared_task
def save_prospect_from_provider_info_task(profile_external_id, provider_type):
  return prospect_service.save_prospect_from_provider_info(profile_external_id, provider_type).id


@shared_task
def manage_prospect_profiles_task(prospect_id):
  prospect = prospect_service.get_prospect(prospect_id)
  return prospect_service.manage_prospect_profiles(prospect).id


@shared_task
def manage_prospect_attrs_task(profile_uid):
  profile = profile_service.get_profile_from_uid(profile_uid)
  prospect = profile.prospect
  return prospect_service.manage_prospect_attrs(prospect, profile).id
