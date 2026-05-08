from ..core.base_agent import BaseAgent
from ..core.types import AgentOutput, SubTask


class GenomicAgent(BaseAgent):
    """Analyze genomic biomarkers such as driver mutations and TMB."""

    def process(self, task: SubTask) -> AgentOutput:
        sample_mutations = task.input_data.get("mutations", ["KRAS G12C", "STK11 loss"])
        tmb = task.input_data.get("tmb", 18)

        facts = [
            self._add_fact(
                content=f"Driver mutations: {', '.join(sample_mutations)}",
                confidence=0.95,
                mutations=sample_mutations,
            ),
            self._add_fact(
                content=f"TMB = {tmb} muts/Mb ({'high' if tmb > 10 else 'low'})",
                confidence=0.90,
                tmb=tmb,
            ),
        ]

        if "STK11" in " ".join(sample_mutations).upper():
            facts.append(
                self._add_fact(
                    content="STK11 loss is associated with immune-cold tumors and primary anti-PD-1 resistance.",
                    confidence=0.85,
                )
            )

        return AgentOutput(success=True, facts=facts)
