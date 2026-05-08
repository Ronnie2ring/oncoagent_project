from typing import Dict, List

from ..core.types import AgentOutput


class DebateConsensusModule:
    """Adjust confidence when low-confidence agent evidence is present."""

    @staticmethod
    def resolve(agents_outputs: List[AgentOutput], reasoner_result: Dict) -> Dict:
        confidence = reasoner_result["confidence"]
        low_confidence_facts = [
            fact.content
            for output in agents_outputs
            for fact in output.facts
            if fact.confidence < 0.7
        ]

        if low_confidence_facts:
            confidence = max(0.5, confidence - 0.1)

        final = reasoner_result.copy()
        final["confidence"] = confidence
        final["consensus_reached"] = True
        final["low_confidence_facts"] = low_confidence_facts
        return final
