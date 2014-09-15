from collections import namedtuple


CalculationAssignedEntityObject = namedtuple(
  'CalculationAssignedEntityObject',
  'assigned_entity assigned_entity_uid entity_type provider_type prospect'
)

RulesEngineScoredObject = namedtuple(
  'RulesEngineScoredObject',
  'internal_score internal_score_attrs base_score base_score_attrs'
)
