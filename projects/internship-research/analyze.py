from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
import json
import argparse

from models import (
    CandidateProfile,
    ConstraintAssessment,
    DimensionAssessment,
    Evidence,
    JobSnapshot,
    Verdict,
    DecisionCard,
)



@dataclass(frozen=True)
class ExtractedJob:
    evidence: list[Evidence]
    job_snapshot: JobSnapshot
    unknown_fields: list[str]

@dataclass(frozen=True)
class CandidateAssessment:
    constraints: list[ConstraintAssessment]
    dimensions: list[DimensionAssessment]
    verdict: Verdict

def require_evidence(
    job_text: str,
    evidence_id: str,
    quote: str,
    source_path: str,
) -> Evidence:
    if quote not in job_text:
        raise ValueError(
            f"{evidence_id} quote was not found in job.txt"
        )

    return Evidence(
        evidence_id=evidence_id,
        source_path=source_path,
        quote=quote,
    )

def require_full_match(
    pattern: str,
    text: str,
    field_name: str,
) -> re.Match[str]:
    match = re.fullmatch(pattern, text)

    if match is None:
        raise ValueError(
            f"could not parse {field_name}: {text}"
        )

    return match


def extract_job(job_text: str,source_path:str,) -> ExtractedJob:
    quotes = {
        "ev_heading": (
            "星桥智能（虚构公司）— Agent 工程实习生"
        ),
        "ev_workplace": (
            "工作地点：上海，混合办公，每周至少到岗 3 天。"
        ),
        "ev_duration": "实习周期：至少 4 个月。",
        "ev_agent_work": (
            "- 使用 Python 开发带工具调用能力的 Agent。"
        ),
        "ev_eval_work": (
            "- 为 Agent 输出设计可重复运行的评测。"
        ),
        "ev_failure_work": (
            "- 记录失败案例并改进提示词与工具契约。"
        ),
        "ev_python_git": "- 熟悉 Python 和 Git。",
        "ev_llm_api": (
            "- 理解大语言模型 API 的基本调用方式。"
        ),
        "ev_project": (
            "- 能清楚说明自己参与过的一个软件项目。"
        ),
        "ev_cpp": "- 有 C++ 项目经验。",
    }

    evidence_by_id = {
        evidence_id: require_evidence(
            job_text,
            evidence_id,
            quote,
            source_path,
        )
        for evidence_id, quote in quotes.items()
    }

    heading_match = require_full_match(
        (
            r"(?P<company>.+?)（虚构公司）"
            r"—\s*(?P<role>.+)"
        ),
        quotes["ev_heading"],
        "heading",
    )

    workplace_match = require_full_match(
        (
            r"工作地点：(?P<city>[^，]+)，"
            r"混合办公，每周至少到岗 "
            r"(?P<days>\d+) 天。"
        ),
        quotes["ev_workplace"],
        "workplace",
    )

    duration_match = require_full_match(
        r"实习周期：至少 (?P<months>\d+) 个月。",
        quotes["ev_duration"],
        "duration",
    )

    job_snapshot = JobSnapshot.model_validate(
        {
            "company": {
                "value": heading_match["company"],
                "evidence_refs": ["ev_heading"],
            },
            "role": {
                "value": heading_match["role"],
                "evidence_refs": ["ev_heading"],
            },
            "city": {
                "value": workplace_match["city"],
                "evidence_refs": ["ev_workplace"],
            },
            "work_mode": {
                "value": "hybrid",
                "evidence_refs": ["ev_workplace"],
            },
            "minimum_onsite_days_per_week": {
                "value": int(workplace_match["days"]),
                "evidence_refs": ["ev_workplace"],
            },
            "minimum_duration_months": {
                "value": int(duration_match["months"]),
                "evidence_refs": ["ev_duration"],
            },
            "responsibilities": [
                {
                    "value": (
                        "使用 Python 开发带工具调用能力的 Agent"
                    ),
                    "evidence_refs": ["ev_agent_work"],
                },
                {
                    "value": (
                        "为 Agent 输出设计可重复运行的评测"
                    ),
                    "evidence_refs": ["ev_eval_work"],
                },
                {
                    "value": (
                        "记录失败案例并改进提示词与工具契约"
                    ),
                    "evidence_refs": ["ev_failure_work"],
                },
            ],
            "required_skills": [
                {
                    "value": "Python",
                    "evidence_refs": ["ev_python_git"],
                },
                {
                    "value": "Git",
                    "evidence_refs": ["ev_python_git"],
                },
                {
                    "value": "LLM API",
                    "evidence_refs": ["ev_llm_api"],
                },
            ],
            "project_evidence_required": {
                "value": True,
                "evidence_refs": ["ev_project"],
            },
            "bonus_skills": [
                {
                    "value": "C++",
                    "evidence_refs": ["ev_cpp"],
                }
            ],
        }
    )

    unknown_markers = {
        "salary": ("工资", "薪资", "薪酬"),
        "education_requirement": ("学历", "本科", "硕士"),
        "overtime": ("加班", "996", "工作时长"),
        "mentorship": ("导师", "带教", "mentor"),
        "application_deadline": ("截止日期", "申请截止"),
    }

    unknown_fields = [
        field_name
        for field_name, markers in unknown_markers.items()
        if not any(marker in job_text for marker in markers)
    ]

    return ExtractedJob(
        evidence=list(evidence_by_id.values()),
        job_snapshot=job_snapshot,
        unknown_fields=unknown_fields,
    )

def assess_candidate(
    candidate: CandidateProfile,
    extracted: ExtractedJob,
) -> CandidateAssessment:
    job = extracted.job_snapshot
    location = candidate.location_preferences
    availability = candidate.availability

    city_met = (
        job.city.value in location.acceptable_cities
    )
    work_mode_met = (
        job.work_mode.value
        in location.acceptable_work_modes
    )
    onsite_met = (
        job.minimum_onsite_days_per_week.value
        <= location.max_onsite_days_per_week
    )
    duration_met = (
        availability.duration_months
        >= job.minimum_duration_months.value
    )

    constraints = [
        ConstraintAssessment(
            name="city",
            status="met" if city_met else "not_met",
            reason=(
                f"{job.city.value}在候选人的可接受城市中。"
                if city_met
                else (
                    f"{job.city.value}不在候选人的"
                    "可接受城市中。"
                )
            ),
        ),
        ConstraintAssessment(
            name="work_mode",
            status=(
                "met" if work_mode_met else "not_met"
            ),
            reason=(
                f"{job.work_mode.value} 在候选人的"
                "可接受办公方式中。"
                if work_mode_met
                else (
                    f"{job.work_mode.value} 不在候选人的"
                    "可接受办公方式中。"
                )
            ),
        ),
        ConstraintAssessment(
            name="onsite_days",
            status="met" if onsite_met else "not_met",
            reason=(
                "岗位最低到岗 "
                f"{job.minimum_onsite_days_per_week.value} 天，"
                "候选人最多接受到岗 "
                f"{location.max_onsite_days_per_week} 天。"
                if onsite_met
                else (
                    "岗位每周至少到岗 "
                    f"{job.minimum_onsite_days_per_week.value} 天，"
                    "超过候选人最多接受的 "
                    f"{location.max_onsite_days_per_week} 天。"
                )
            ),
        ),
        ConstraintAssessment(
            name="duration",
            status="met" if duration_met else "not_met",
            reason=(
                "候选人可实习 "
                f"{availability.duration_months} 个月，"
                "满足岗位至少 "
                f"{job.minimum_duration_months.value} "
                "个月的要求。"
                if duration_met
                else (
                    "候选人只能实习 "
                    f"{availability.duration_months} 个月，"
                    "不满足岗位至少 "
                    f"{job.minimum_duration_months.value} "
                    "个月的要求。"
                )
            ),
        ),
    ]

    if (
        candidate.work_preferences.low_overtime
        == "not_required"
    ):
        constraints.append(
            ConstraintAssessment(
                name="low_overtime",
                status="met",
                reason="候选人未将低加班作为必要条件。",
            )
        )
    else:
        constraints.append(
            ConstraintAssessment(
                name="low_overtime",
                status="unknown",
                reason="JD 未说明加班情况。",
            )
        )

    if (
        candidate.work_preferences.mentorship
        == "not_required"
    ):
        constraints.append(
            ConstraintAssessment(
                name="mentorship",
                status="met",
                reason="候选人未将导师制度作为要求。",
            )
        )
    else:
        constraints.append(
            ConstraintAssessment(
                name="mentorship",
                status="unknown",
                reason="JD 未说明导师制度。",
            )
        )

    supported_skills = set(candidate.skills)

    for project in candidate.project_evidence:
        supported_skills.update(project.skills)

    required_skills = {
        item.value
        for item in job.required_skills
    }
    bonus_skills = {
        item.value
        for item in job.bonus_skills
    }

    role_matches = (
        "Agent" in job.role.value
        and "agent_engineering_intern"
        in candidate.target_roles
    )

    required_skills_match = (
        required_skills.issubset(supported_skills)
        and (
            not job.project_evidence_required.value
            or bool(candidate.project_evidence)
        )
    )

    bonus_skills_match = (
        bonus_skills.issubset(supported_skills)
    )

    location_matches = (
        city_met and work_mode_met and onsite_met
    )

    sustainability_constraints = constraints[4:]

    if any(
        item.status == "not_met"
        for item in sustainability_constraints
    ):
        sustainability_status = "gap"
        sustainability_reason = (
            "候选人的可持续工作要求存在明确冲突。"
        )
    elif any(
        item.status == "unknown"
        for item in sustainability_constraints
    ):
        sustainability_status = "unknown"
        sustainability_reason = (
            "JD 未说明加班情况和导师制度。"
        )
    else:
        sustainability_status = "match"
        sustainability_reason = (
            "岗位满足候选人的可持续工作要求。"
        )

    dimensions = [
        DimensionAssessment(
            name="role_direction",
            status="match" if role_matches else "gap",
            reason=(
                "候选人的目标岗位包含 Agent 工程实习方向。"
                if role_matches
                else "岗位方向与候选人的目标方向不一致。"
            ),
        ),
        DimensionAssessment(
            name="required_skills",
            status=(
                "match"
                if required_skills_match
                else "gap"
            ),
            reason=(
                "候选人的技能与项目证据覆盖 "
                "Python、Git 和 LLM API。"
                if required_skills_match
                else "候选人缺少岗位要求的核心技能证据。"
            ),
        ),
        DimensionAssessment(
            name="bonus_skills",
            status=(
                "match" if bonus_skills_match else "gap"
            ),
            reason=(
                "候选人具有 C++ 项目经验，"
                "满足岗位加分项。"
                if bonus_skills_match
                else "候选人未覆盖岗位加分技能。"
            ),
        ),
        DimensionAssessment(
            name="location_and_work_mode",
            status=(
                "match" if location_matches else "gap"
            ),
            reason=(
                "上海和 hybrid 均在候选人的"
                "可接受范围内，且到岗天数边界一致。"
                if location_matches
                else "地点、办公方式或到岗天数不匹配。"
            ),
        ),
        DimensionAssessment(
            name="sustainability",
            status=sustainability_status,
            reason=sustainability_reason,
        ),
    ]

    hard_constraint_failed = any(
        item.status == "not_met"
        for item in constraints[:4]
    )
    core_dimension_failed = any(
        item.name in {
            "role_direction",
            "required_skills",
        }
        and item.status == "gap"
        for item in dimensions
    )

    low_overtime_unknown = any(
        item.name == "low_overtime"
        and item.status == "unknown"
        for item in constraints
    )

    if hard_constraint_failed or core_dimension_failed:
        verdict = Verdict(
            status="not_suitable",
            reason=(
                "存在不满足的硬性条件或岗位核心能力缺口。"
            ),
            next_action="暂不投递，优先寻找更匹配的岗位。",
        )
    elif (
        candidate.work_preferences.low_overtime
        == "required"
        and low_overtime_unknown
    ):
        verdict = Verdict(
            status="needs_verification",
            reason=(
                "地点、办公方式、实习周期和技能要求均匹配，"
                "但低加班是候选人的必要条件，"
                "而 JD 没有提供加班信息。"
            ),
            next_action=(
                "向招聘方确认常规工作时长、"
                "加班情况和导师安排。"
            ),
        )
    else:
        verdict = Verdict(
            status="worth_applying",
            reason="已知硬性条件与核心能力均匹配。",
            next_action="准备针对该岗位的简历并投递。",
        )

    return CandidateAssessment(
        constraints=constraints,
        dimensions=dimensions,
        verdict=verdict,
    )

def build_decision_card(
    candidate: CandidateProfile,
    extracted: ExtractedJob,
    assessment: CandidateAssessment,
    source_path: str,
) -> DecisionCard:
    return DecisionCard(
        candidate_id=candidate.candidate_id,
        source_path=source_path,
        evidence=extracted.evidence,
        job_snapshot=extracted.job_snapshot,
        unknown_fields=extracted.unknown_fields,
        constraints=assessment.constraints,
        dimensions=assessment.dimensions,
        verdict=assessment.verdict,
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build an evidence-backed internship "
            "decision card."
        )
    )
    parser.add_argument(
        "--job",
        type=Path,
        required=True,
        help="Path to the original job description.",
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Path to the candidate profile JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the generated decision card.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    job_text = args.job.read_text(encoding="utf-8")
    candidate_data = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    candidate = CandidateProfile.model_validate(
        candidate_data
    )

    source_path = args.job.name
    extracted = extract_job(
        job_text,
        source_path=source_path,
    )
    assessment = assess_candidate(
        candidate,
        extracted,
    )
    decision_card = build_decision_card(
        candidate,
        extracted,
        assessment,
        source_path=source_path,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.output.write_text(
        decision_card.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"WROTE output={args.output} "
        f"candidate={decision_card.candidate_id} "
        f"evidence={len(decision_card.evidence)} "
        f"constraints={len(decision_card.constraints)} "
        f"dimensions={len(decision_card.dimensions)} "
        f"verdict={decision_card.verdict.status}"
    )

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"ANALYSIS_FAILED: {error}")
        raise SystemExit(1)