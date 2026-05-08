from typing import Any, Dict, List

from ..core.memory import SharedMemory
from ..core.types import Fact


class ChainOfThoughtReasoner:
    """Rule-based MVP reasoner with a future-compatible LLM interface."""

    def __init__(self, memory: SharedMemory, use_mock: bool = True):
        self.memory = memory
        self.use_mock = use_mock

    def reason(self, user_query: str, initial_facts: List[Fact]) -> Dict[str, Any]:
        if self.use_mock:
            return self._mock_reasoning(user_query, initial_facts)
        return self._llm_reasoning(user_query, initial_facts)

    def _mock_reasoning(self, query: str, facts: List[Fact]) -> Dict[str, Any]:
        fact_texts = [fact.content for fact in facts]
        normalized = " ".join(fact_texts).upper()

        has_stk11 = "STK11" in normalized
        has_tgf = "TGF-BETA" in normalized or "TGF" in normalized
        has_treg = "TREG" in normalized
        has_cd8_low = "CD8+" in normalized and ("LOW" in normalized or "<3%" in normalized)
        has_high_tmb = "TMB = 18" in normalized or "TMB" in normalized and "HIGH" in normalized
        has_pd_l1_stromal = "PD-L1" in normalized and "STROMAL" in normalized

        reasoning_steps = [
            "Genomic evidence shows STK11 loss or related resistance biomarkers when present.",
        ]
        if has_tgf and has_treg:
            reasoning_steps.append(
                "Transcriptomic evidence supports TGF-beta enrichment and high Treg-mediated immune suppression."
            )
        if has_cd8_low or has_pd_l1_stromal:
            reasoning_steps.append(
                "Radiomic and immune-context signals suggest limited effector T-cell activity."
            )

        contradictions = []
        if has_high_tmb:
            contradictions.append(
                "High TMB can favor immunotherapy response, but STK11 loss and immune exclusion may offset it."
            )

        if has_stk11 or (has_tgf and has_treg):
            conclusion = "The patient is unlikely to respond well to anti-PD-1 monotherapy."
            confidence = 0.85
            recommendations = [
                "Consider a clinical trial combining anti-PD-1 with TGF-beta inhibition.",
                "Consider KRAS G12C targeted therapy such as sotorasib when clinically appropriate.",
            ]
        else:
            conclusion = "The patient may benefit from anti-PD-1 therapy, pending additional validation."
            confidence = 0.60
            recommendations = [
                "Further evaluate PD-L1 IHC, MSI status, and longitudinal response markers."
            ]

        return {
            "conclusion": conclusion,
            "confidence": confidence,
            "reasoning_chain": reasoning_steps,
            "recommendations": recommendations,
            "contradictions": contradictions,
        }

    def _llm_reasoning(self, query: str, facts: List[Fact]) -> Dict[str, Any]:
        raise NotImplementedError("Real LLM integration is not implemented in this MVP.")
