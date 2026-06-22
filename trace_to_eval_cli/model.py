"""Compatibility model surface for the active-MVP factory contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapexPlan:
    scenario_id: str
    queue_projects: int = 1


@dataclass(frozen=True)
class FactorScore:
    name: str
    score: float


def rank_constraints(plan: CapexPlan) -> list[FactorScore]:
    return [FactorScore(f"trace-case:{plan.scenario_id}", 1.0)]
