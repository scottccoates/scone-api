from collections import Counter
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.geo_utils.services import geo_location_service
from src.libs.nlp_utils.services import demography_service
from src.libs.python_utils.collections import iter_utils
from src.libs.text_utils.parsers import text_parser


class ProfessionalSocialNetworkingTechStartupRulesEngine(BaseRulesEngine):
  def __init__(self, _demography_service=demography_service):
    super().__init__()
    self._demography_service = _demography_service

  _important_websites = (
    "linkedin",
  )

  _important_bio_keywords = iter_utils.stemmify_iterable((
    "ceo",
    "cto",
    "founder",
    "startup",
    "vp",
    "manager",
    "entrepreneur",
    "networking",
    "director",
    "hustler",
    "professional",
  ))

  _bad_bio_keywods = iter_utils.stemmify_iterable((
    "recruiter",
    "job search",
    "fuck",
    "bitch",
    "cunt",
    "slut",
  ))

  _bad_keywords = iter_utils.stemmify_iterable((
    "fuck",
    "bitch",
    "cunt",
    "slut",
  ))

  _important_locations = (
    "sf",
    "san fran",
    "nyc",
    "new york",
    "atlanta",
    "seattle",
    "philadelphia",
    "chicago",
    "los angeles",
    "dallas",
    "ft worth",
    "boston",
    "boulder",
  )

  _home_countries = (
    "united states",
  )

  def _get_internal_score(self, calculation_data, _iter_utils=iter_utils, _geolocation_service=geo_location_service,
                          _text_parser=text_parser):
    score = 0
    internal_score_attrs = {}
    counter = Counter()

    profile_websites = calculation_data[constants.PROFILE_WEBSITES]
    if profile_websites:
      website_score = 5
      for ws in profile_websites:
        if any(domain in ws.lower() for domain in self._important_websites):
          score += website_score
          counter[constants.PROFILE_WEBSITES] += website_score
      if counter[constants.PROFILE_WEBSITES]: internal_score_attrs[constants.PROFILE_WEBSITES] = counter[
        constants.PROFILE_WEBSITES]

    bio = calculation_data[constants.BIO]
    if bio:
      bio_score = 3
      bio = _iter_utils.stemmify_string(bio)
      for kw in self._important_bio_keywords:
        if kw in bio:
          score += bio_score
          counter[constants.BIO] += bio_score

      for kw in self._bad_bio_keywods:
        if kw in bio:
          bio_score = -5
          score += bio_score
          counter[constants.BIO] += bio_score

      if counter[constants.BIO]: internal_score_attrs[constants.BIO] = counter[constants.BIO]

    text = calculation_data[constants.TEXT]
    if text:
      bad_text_score = -5
      for kw in self._bad_keywords:
        if kw in text:
          score += bad_text_score
          counter[constants.BAD_TEXT] += bad_text_score

      if counter[constants.BAD_TEXT]: internal_score_attrs[constants.BAD_TEXT] = counter[constants.BAD_TEXT]

    birth_date = calculation_data[constants.RELATIVE_DOB]
    if birth_date:
      age_years = relativedelta(timezone.now(), birth_date).years
      if 18 <= age_years <= 35:
        age_score = 3
        score += age_score
        counter[constants.RELATIVE_DOB] += age_score
        if counter[constants.RELATIVE_DOB]: internal_score_attrs[constants.RELATIVE_DOB] = counter[constants.RELATIVE_DOB]

    employment_latest_start_date = calculation_data[constants.ORGANIZATION_LATEST_START_DATE]
    if employment_latest_start_date:
      employment_years = relativedelta(timezone.now(), employment_latest_start_date).years
      if employment_years < 1:
        employment_length_score = 3
        score += employment_length_score
        counter[constants.ORGANIZATION_LATEST_START_DATE] += employment_length_score
        if counter[constants.ORGANIZATION_LATEST_START_DATE]: internal_score_attrs[
          constants.ORGANIZATION_LATEST_START_DATE] = counter[constants.ORGANIZATION_LATEST_START_DATE]

    followers_count = calculation_data[constants.FOLLOWERS_COUNT]
    if followers_count and followers_count >= 2500:
      followers_count_score = 1
      score += followers_count_score
      internal_score_attrs[constants.FOLLOWERS_COUNT] = followers_count_score

    location = calculation_data[constants.LOCATION]
    if location:
      location_score = 2

      country = _geolocation_service.get_country(location)
      if country:
        country = country.lower()

        for home_country in self._home_countries:
          if country in home_country:
            score += location_score
            counter[constants.LOCATION] += location_score

      location = location.lower()
      if any(loc in location for loc in self._important_locations):
        score += location_score
        counter[constants.LOCATION] += location_score

      if counter[constants.LOCATION]: internal_score_attrs[constants.LOCATION] = counter[constants.LOCATION]

    internal_score_attrs[constants.SCORE] = score

    return score, internal_score_attrs

  def get_final_score(self, score_attrs):
    scores = [x['score'] for x in score_attrs]
    return max(scores)
