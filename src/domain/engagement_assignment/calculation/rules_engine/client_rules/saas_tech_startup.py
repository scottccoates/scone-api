from src.domain.engagement_assignment.calculation.rules_engine.base_engagement_opportunity_rules_engine import \
  BaseTwitterEngagementOpportunityRulesEngine, BaseRedditEngagementOpportunityRulesEngine, \
  BaseLinkedInEngagementOpportunityRulesEngine
from src.domain.engagement_assignment.calculation.rules_engine.base_profile_rules_engine import \
  BaseTwitterProfileRulesEngine, BaseLinkedInProfileRulesEngine, BaseRedditProfileRulesEngine
from src.domain.engagement_assignment.calculation.rules_engine.base_prospect_rules_engine import \
  BaseProspectRulesEngine
from src.libs.nlp_utils.services.enums import GenderEnum


class ProspectRulesEngine(BaseProspectRulesEngine):
  @property
  def _important_locations(self):
    return (
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


  @property
  def _important_home_countries(self):
    return (
      "united states",
    )

  @property
  def _age_range(self):
    return 20, 40

  @property
  def _preferred_gender(self):
    return GenderEnum.male

  @property
  def _important_bio_keywords(self):
    return (
      "ceo",
      "cto",
      "software",
      "developer",
      "engineer",
      "programmer",
      "writer",
      "founder",
      "startup",
    )

  @property
  def _important_websites(self):
    return (
      "linkedin",
      "wordpress",
      "blogspot",
      "about.me",
      "ycombinator",
      "stackoverflow",
      ".io",
    )

  def _get_internal_score(self):
    return 0, {}


class TwitterProfileRulesEngine(BaseTwitterProfileRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class RedditProfileRulesEngine(BaseRedditProfileRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class LinkedInProfileRulesEngine(BaseLinkedInProfileRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class TwitterEngagementOpportunityRulesEngine(BaseTwitterEngagementOpportunityRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class RedditEngagementOpportunityRulesEngine(BaseRedditEngagementOpportunityRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class LinkedInEngagementOpportunityRulesEngine(BaseLinkedInEngagementOpportunityRulesEngine):
  def _get_internal_score(self):
    return 0, {}

    #
    # class SaaSTechStartupRulesEngine(BaseRulesEngine):
    # def __init__(self, _demography_service=demography_service):
    # super().__init__()
    # self._demography_service = _demography_service
    #

    #
    #
    #
    #
    # def _get_internal_score(self, calculation_data, _iter_utils=iter_utils,
    # _geolocation_service=geo_location_service,
    # _text_parser=text_parser):
    # score = 0
    #     internal_score_attrs = {}
    #     counter = Counter()
    #
    #     profile_websites = calculation_data[constants.PROFILE_WEBSITES]
    #     if profile_websites:

    #


# followers_count = calculation_data[constants.FOLLOWERS_COUNT]
# if followers_count and followers_count >= 2500:
# followers_count_score = 1
# score += followers_count_score
# internal_score_attrs[constants.FOLLOWERS_COUNT] = followers_count_score

#
# internal_score_attrs[constants.SCORE] = score
#
# return score, internal_score_attrs
#
# def get_final_score(self, score_attrs):
#     scores = [x['score'] for x in score_attrs]
#     return max(scores)