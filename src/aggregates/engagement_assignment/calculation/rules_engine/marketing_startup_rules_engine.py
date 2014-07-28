from collections import Counter
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.geo_utils.services import geo_location_service
from src.libs.nlp_utils.services import demography_service
from src.libs.nlp_utils.services.enums import GenderEnum
from src.libs.python_utils.collections import iter_utils
from src.libs.text_utils.parsers import text_parser


class MarketingTechStartupRulesEngine(BaseRulesEngine):
  def __init__(self, _demography_service=demography_service):
    super().__init__()
    self._demography_service = _demography_service

  _important_websites = (
    "linkedin",
    "wordpress",
    "blogspot",
    "about.me",
    "ycombinator",
    "stackoverflow",
    ".io",
  )

  # todo iter_utils should be passed in the constructor (like demography service)
  _important_bio_keywords = iter_utils.stemmify_iterable((
    "community",
    "marketing",
    "planning",
    "events",
    "social media",
    "engagement",
    "outreach",
  ))

  _important_industries = iter_utils.stemmify_iterable((
    "computer software",
    "marketing",
    "advertising",
    "internet",
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
    "bend",
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
      website_score = 1
      for ws in profile_websites:
        if any(domain in ws.lower() for domain in self._important_websites):
          score += website_score
          counter[constants.PROFILE_WEBSITES] += website_score
      if counter[constants.PROFILE_WEBSITES]: internal_score_attrs[constants.PROFILE_WEBSITES] = counter[
        constants.PROFILE_WEBSITES]

    # todo use a diff constant - constants.BIO_IMPORTANT_KEYWORD.....
    bio = calculation_data[constants.BIO]
    if bio:
      bio_score = 1
      bio = _iter_utils.stemmify_string(bio)
      for kw in self._important_bio_keywords:
        if kw in bio:
          score += bio_score
          counter[constants.BIO] += bio_score
      if counter[constants.BIO]: internal_score_attrs[constants.BIO] = counter[constants.BIO]

    gender = calculation_data[constants.GENDER]
    if gender:
      if gender == GenderEnum.female:
        gender_score = 1
        score += gender_score
        internal_score_attrs[constants.GENDER] = gender_score

    age = calculation_data[constants.RELATIVE_DOB]
    if age:
      age_years = relativedelta(timezone.now(), age).years
      if 20 <= age_years <= 35:
        age_score = 1
        score += age_score
        counter[constants.RELATIVE_DOB] += age_score
        if counter[constants.RELATIVE_DOB]: internal_score_attrs[constants.RELATIVE_DOB] = counter[constants.RELATIVE_DOB]

    followers_count = calculation_data[constants.FOLLOWERS_COUNT]
    if followers_count and followers_count >= 2500:
      followers_count_score = 1
      score += followers_count_score
      internal_score_attrs[constants.FOLLOWERS_COUNT] = followers_count_score

    location = calculation_data[constants.LOCATION]
    if location:
      location_score = 1

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

    company = calculation_data[constants.COMPANY]
    if company:

      company_industries = company[constants.COMPANY_INDUSTRIES]
      if company_industries:
        industry_score = 1
        stemmed_industry = " ".join(iter_utils.stemmify_iterable(company_industries))
        for ind in self._important_industries:
          if ind in stemmed_industry:
            score += industry_score
            counter[constants.COMPANY_INDUSTRY_SCORE] += industry_score

        if counter[constants.COMPANY_INDUSTRY_SCORE]:
          internal_score_attrs[constants.COMPANY_INDUSTRY_SCORE] = counter[constants.COMPANY_INDUSTRY_SCORE]

      company_size = company[constants.COMPANY_EMPLOYEE_COUNT]
      if company_size:
        company_size_score = 1
        if company_size > 100:
          score += company_size_score
          counter[constants.COMPANY_EMPLOYEE_COUNT_SCORE] += company_size_score

        if counter[constants.COMPANY_EMPLOYEE_COUNT_SCORE]:
          internal_score_attrs[constants.COMPANY_EMPLOYEE_COUNT_SCORE] = counter[constants.COMPANY_EMPLOYEE_COUNT_SCORE]

    internal_score_attrs[constants.SCORE] = score

    return score, internal_score_attrs

  def get_final_score(self, score_attrs):
    scores = [x['score'] for x in score_attrs]
    return max(scores)
