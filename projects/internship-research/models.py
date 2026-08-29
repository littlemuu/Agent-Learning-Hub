from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated,Literal,Generic, TypeVar

class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

class Evidence(StrictModel):
    evidence_id: str = Field(min_length=1)
    source_path: str = Field(min_length=1)
    quote: str = Field(min_length=1)


NonEmptyString = Annotated[str, Field(min_length=1)]
WorkMode = Literal["onsite", "hybrid", "remote"]
PreferenceLevel = Literal["required", "preferred", "not_required"]
PositiveInt = Annotated[int, Field(ge=1)]
OnsiteDaysPerWeek = Annotated[int, Field(ge=0, le=7)]

ValueT = TypeVar("ValueT")

class EvidencedValue(StrictModel, Generic[ValueT]):
    value: ValueT
    evidence_refs: list[NonEmptyString] = Field(min_length=1)

class JobSnapshot(StrictModel):
    company: EvidencedValue[NonEmptyString]
    role: EvidencedValue[NonEmptyString]
    city: EvidencedValue[NonEmptyString]
    work_mode: EvidencedValue[WorkMode]
    minimum_onsite_days_per_week: EvidencedValue[
        OnsiteDaysPerWeek
    ]
    minimum_duration_months: EvidencedValue[PositiveInt]
    responsibilities: list[
        EvidencedValue[NonEmptyString]
    ] = Field(min_length=1)
    required_skills: list[
        EvidencedValue[NonEmptyString]
    ] = Field(min_length=1)
    project_evidence_required: EvidencedValue[bool]
    bonus_skills: list[EvidencedValue[NonEmptyString]]

class ProjectEvidence(StrictModel):
    project_id: NonEmptyString
    summary: NonEmptyString
    skills: list[NonEmptyString] = Field(min_length=1)


class LocationPreferences(StrictModel):
    acceptable_cities: list[NonEmptyString] = Field(min_length=1)
    acceptable_work_modes: list[WorkMode] = Field(min_length=1)
    max_onsite_days_per_week: int = Field(ge=0, le=7)


class Availability(StrictModel):
    days_per_week: int = Field(ge=1, le=7)
    duration_months: int = Field(ge=1)


class WorkPreferences(StrictModel):
    low_overtime: PreferenceLevel
    mentorship: PreferenceLevel


class CandidateProfile(StrictModel):
    candidate_id: NonEmptyString
    target_roles: list[NonEmptyString] = Field(min_length=1)
    skills: list[NonEmptyString] = Field(min_length=1)
    project_evidence: list[ProjectEvidence] = Field(min_length=1)
    location_preferences: LocationPreferences
    availability: Availability
    work_preferences: WorkPreferences

ConstraintStatus = Literal["met", "not_met", "unknown"]
DimensionStatus = Literal["match", "gap", "unknown"]
VerdictStatus = Literal[
    "worth_applying",
    "needs_verification",
    "not_suitable",
]


class ConstraintAssessment(StrictModel):
    name: NonEmptyString
    status: ConstraintStatus
    reason: NonEmptyString


class DimensionAssessment(StrictModel):
    name: NonEmptyString
    status: DimensionStatus
    reason: NonEmptyString


class Verdict(StrictModel):
    status: VerdictStatus
    reason: NonEmptyString
    next_action: NonEmptyString

class DecisionCard(StrictModel):
    candidate_id: NonEmptyString
    source_path: NonEmptyString
    evidence: list[Evidence] = Field(min_length=1)
    job_snapshot: JobSnapshot
    unknown_fields: list[NonEmptyString]
    constraints: list[ConstraintAssessment] = Field(min_length=1)
    dimensions: list[DimensionAssessment] = Field(min_length=1)
    verdict: Verdict