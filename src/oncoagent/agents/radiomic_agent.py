from ..core.base_agent import BaseAgent
from ..core.types import AgentOutput, SubTask


class RadiomicAgent(BaseAgent):
    """Analyze radiology-derived tumor microenvironment features."""

    def process(self, task: SubTask) -> AgentOutput:
        sample_data = task.input_data
        facts = []
        fibrosis = sample_data.get("fibrosis", 60)

        if fibrosis > 50:
            facts.append(
                self._add_fact(
                    content=f"Stromal fibrosis ratio is high ({fibrosis}%), creating a physical barrier to T-cell infiltration.",
                    confidence=0.78,
                    fibrosis=fibrosis,
                )
            )
        if sample_data.get("pd_l1_pattern") == "stromal":
            facts.append(
                self._add_fact(
                    content="PD-L1 expression is stromal rather than tumor-cell dominant, suggesting adaptive resistance.",
                    confidence=0.83,
                )
            )

        return AgentOutput(success=True, facts=facts)
