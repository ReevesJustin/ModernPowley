"""Promoted M01 geometry, M02 evidence records, and M03 diagnostics."""

from .geometry import (
    WaterConversionConvention,
    barrel_swept_volume,
    barrel_volume_ratio,
    boat_tail_seated_displacement,
    charge_to_bullet_mass_ratio,
    charge_to_estimated_usable_water_capacity_mass_ratio,
    charge_to_gross_water_capacity_mass_ratio,
    charge_to_measured_usable_water_capacity_mass_ratio,
    circle_area,
    compare_usable_powder_spaces,
    conical_frustum_volume,
    cylinder_volume,
    derive_seating_depth,
    estimate_geometric_usable_powder_space,
    flat_base_seated_displacement,
    sectional_density_mass_over_diameter_squared,
    total_expanded_volume,
    total_expansion_ratio,
    water_mass_to_volume,
    water_mass_to_volume_by_convention,
    water_volume_to_mass,
    water_volume_to_mass_by_convention,
)
from .provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from .records import (
    SCHEMA_ID,
    CapacityComparison,
    CapacityFillBoundary,
    CartridgeIdentity,
    CaseCondition,
    DiameterConvention,
    EstimatedUsablePowderSpace,
    FirearmRecord,
    GeometryAdequacy,
    GrossCaseCapacity,
    MeasuredUsablePowderSpace,
    MeasurementConditions,
    PhysicalValue,
    PrimerPocketTreatment,
    PrimerPocketVolume,
    ProjectileRecord,
    ProjectileTravel,
    SeatingDepth,
    SeatingDepthKind,
    UncertaintyTreatment,
)
from .serialization import dumps_record, loads_record, record_from_dict, record_to_dict
from .uncertainty import Uncertainty, UncertaintyKind
from .units import Dimension, Quantity, Unit
from .missing_values import IdentityQualifier, MissingState
from .powder_identity import (
    M02_SCHEMA_ID,
    PowderIdentity,
    PowderIdentityRelationship,
    PowderRelationshipKind,
)
from .powder_properties import (
    CategoricalPropertyValue,
    DimensionalPropertyValue,
    IntervalPropertyValue,
    OrdinalPropertyValue,
    PropertyDefinition,
    PropertyId,
    PropertyValueKind,
    SourceScalarPropertyValue,
    TabularReferencePropertyValue,
    TextualPropertyValue,
    standard_property_definition,
)
from .property_domains import (
    ApplicabilityDomain,
    BoundKind,
    CategoricalDomainConstraint,
    DomainBound,
    DomainMembership,
    DomainMembershipStatus,
    DomainStatus,
    NumericDomainConstraint,
    SourceScalarDomainBound,
    SourceScalarDomainConstraint,
    SourceScalarDomainValue,
    test_domain_membership,
)
from .property_observations import (
    MissingPropertyObservation,
    ObservationContext,
    ObservationTransformation,
    PowderPropertyObservation,
    SourceLocator,
    TranscriptionStatus,
)
from .property_conflicts import (
    ConflictComparison,
    DefinitionComparison,
    DomainComparison,
    IdentityComparison,
    NumericComparison,
    UnitComparison,
    compare_property_observations,
)
from .m02_serialization import (
    dumps_m02_record,
    loads_m02_record,
    m02_record_from_dict,
    m02_record_to_dict,
)
from .input_requirements import (
    M03_SCHEMA_ID,
    ConditionalBranch,
    InputBundle,
    InputCandidate,
    InputCandidateKind,
    InputRequirement,
    RequirementKind,
    RequirementSet,
    m03_design_provenance,
    production_requirement_sets,
)
from .input_completeness import (
    CompletenessDiagnostic,
    CompletenessEvaluation,
    CompletenessStatus,
    evaluate_input_completeness,
)
from .domain_diagnostics import (
    ApplicabilityEvaluation,
    ApplicabilitySummary,
    ConstraintKind,
    DomainConstraintDiagnostic,
    DomainDiagnosticStatus,
    DomainQueryContext,
    DomainQueryKind,
    DomainQueryValue,
    QueryInterval,
    diagnose_observation_applicability,
)
from .m03_serialization import (
    dumps_m03_record,
    loads_m03_record,
    m03_record_from_dict,
    m03_record_to_dict,
)
from .screening_criteria import (
    M04_SCHEMA_ID,
    CriterionDefinition,
    CriterionForm,
    CriterionReference,
    CriterionRole,
    CriterionSetDefinition,
    CriterionStatus,
    FiniteSetThreshold,
    LiteralThreshold,
    MissingStateSetThreshold,
    NumericBoundThreshold,
    NumericIntervalThreshold,
    ThresholdKind,
)
from .screening_contexts import (
    ConflictDeclaration,
    EvaluationContext,
    EvidenceReference,
    EvidenceReferenceKind,
    EvidenceValueKind,
)
from .screening_outcomes import (
    CriterionEvaluationRecord,
    CriterionOutcomeStatus,
    CriterionSetOutcomeRecord,
    CriterionSetSummary,
    EvaluationMethod,
    ManualAssertionDetails,
    ManualReviewStatus,
    OutcomeCounts,
)
from .criterion_evaluation import (
    evaluate_criterion,
    record_manual_assertion,
    summarize_criterion_set,
)
from .m04_serialization import (
    dumps_m04_record,
    loads_m04_record,
    m04_record_from_dict,
    m04_record_to_dict,
)

__all__ = [name for name in globals() if not name.startswith("_")]
