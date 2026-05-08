from ..core.base_agent import BaseAgent
from ..core.types import AgentOutput, SubTask


class KnowledgeGraphAgent(BaseAgent):
    """Retrieve biomarker, drug, and phenotype associations."""

    def process(self, task: SubTask) -> AgentOutput:
        query_entity = task.input_data.get("entity", "KRAS G12C")
        normalized_query = query_entity.upper()
        facts = []

        if "KRAS G12C" in normalized_query:
            facts.append(
                self._add_fact(
                    content="KRAS G12C mutation is sensitive to sotorasib (evidence level A).",
                    confidence=0.95,
                )
            )
        if "STK11" in normalized_query:
            facts.append(
                self._add_fact(
                    content="STK11 mutation is strongly associated with primary resistance to anti-PD-1 therapy.",
                    confidence=0.92,
                )
            )
        if "TGF" in normalized_query:
            facts.append(
                self._add_fact(
                    content="High TGF-beta activity can mediate immune exclusion; TGF-beta inhibition may reverse resistance.",
                    confidence=0.89,
                )
            )

        return AgentOutput(success=True, facts=facts)
