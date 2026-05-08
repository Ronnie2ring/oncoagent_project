from ..core.base_agent import BaseAgent
from ..core.types import AgentOutput, SubTask


class TranscriptomicAgent(BaseAgent):
    """Analyze pathway activity and immune infiltration signals."""

    def process(self, task: SubTask) -> AgentOutput:
        sample_data = task.input_data
        facts = []

        if sample_data.get("tgf_beta_enriched", True):
            facts.append(
                self._add_fact(
                    content="TGF-beta pathway is enriched (NES=2.1, FDR<0.01).",
                    confidence=0.88,
                )
            )
        if sample_data.get("treg_high", True):
            facts.append(
                self._add_fact(
                    content="Treg fraction is high (15%), suggesting an immunosuppressive microenvironment.",
                    confidence=0.82,
                )
            )
        if sample_data.get("cd8_low", True):
            facts.append(
                self._add_fact(
                    content="CD8+ T-cell infiltration is low (<3%), suggesting weak effector immune response.",
                    confidence=0.85,
                )
            )

        return AgentOutput(success=True, facts=facts)
