from abc import ABC, abstractmethod
import logging
from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject

logger = logging.getLogger(__name__)


class BaseProspectRulesEngine(ABC):
  def score_it(self, prospect):
    prospect_internal_score, prospect_internal_score_attrs = self._get_internal_score(prospect)
    prospect_base_score, prospect_base_score_attrs = self._apply_base_score(prospect)

    ret_val = RulesEngineScoredObject(
      prospect_internal_score, prospect_internal_score_attrs,
      prospect_base_score, prospect_base_score_attrs
    )

    return ret_val

  def _apply_base_score(self, prospect):
    return 0, {}

  @abstractmethod
  def _get_internal_score(self, prospect):
    """Get the client-specific rules"""
