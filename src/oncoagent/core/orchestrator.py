from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

from ..agents import GenomicAgent, KnowledgeGraphAgent, RadiomicAgent, TranscriptomicAgent
from ..reasoning.chain_of_thought import ChainOfThoughtReasoner
from ..reasoning.debate import DebateConsensusModule
from .memory import SharedMemory
from .types import AgentOutput, AgentRole, SubTask


class Orchestrator:
    """Coordinate task decomposition, agent execution, reasoning, and consensus."""

    def __init__(
        self,
        memory: SharedMemory,
        max_workers: int | None = None,
        verbose: bool = True,
        retain_memory: bool = False,
    ):
        self.memory = memory
        self.agents = self._init_agents(memory)
        self.reasoner = ChainOfThoughtReasoner(memory, use_mock=True)
        self.debate = DebateConsensusModule()
        self.max_workers = max_workers or len(self.agents)
        self.verbose = verbose
        self.retain_memory = retain_memory

    def _init_agents(self, memory: SharedMemory):
        return {
            AgentRole.GENOMIC: GenomicAgent(AgentRole.GENOMIC, memory),
            AgentRole.TRANSCRIPTOMIC: TranscriptomicAgent(AgentRole.TRANSCRIPTOMIC, memory),
            AgentRole.RADIOMIC: RadiomicAgent(AgentRole.RADIOMIC, memory),
            AgentRole.KNOWLEDGE_GRAPH: KnowledgeGraphAgent(AgentRole.KNOWLEDGE_GRAPH, memory),
        }

    def _build_tasks(self, patient_data: dict) -> List[SubTask]:
        return [
            SubTask("Analyze genomic biomarkers", AgentRole.GENOMIC, patient_data.get("genomic", {})),
            SubTask(
                "Analyze transcriptomic immune context",
                AgentRole.TRANSCRIPTOMIC,
                patient_data.get("transcriptomic", {}),
            ),
            SubTask("Analyze radiomic features", AgentRole.RADIOMIC, patient_data.get("radiomic", {})),
            SubTask(
                "Retrieve knowledge graph evidence",
                AgentRole.KNOWLEDGE_GRAPH,
                {"entity": patient_data.get("kg_query", "")},
            ),
        ]

    @staticmethod
    def _run_agent(agents, task: SubTask) -> Tuple[AgentRole, AgentOutput]:
        return task.target_agent, agents[task.target_agent].process(task)

    def run(self, user_query: str, patient_data: dict) -> dict:
        if self.verbose:
            print("\n" + "=" * 60)
            print(f"[Orchestrator] Received task: {user_query}")
            print("=" * 60)

        tasks = self._build_tasks(patient_data)
        request_memory = self.memory if self.retain_memory else SharedMemory()
        agents = self.agents if self.retain_memory else self._init_agents(request_memory)
        reasoner = self.reasoner if self.retain_memory else ChainOfThoughtReasoner(request_memory, use_mock=True)
        outputs_by_role: Dict[AgentRole, AgentOutput] = {}
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(tasks))) as executor:
            futures = {executor.submit(self._run_agent, agents, task): task for task in tasks}
            for future in as_completed(futures):
                role, output = future.result()
                outputs_by_role[role] = output

        all_outputs = [outputs_by_role[task.target_agent] for task in tasks]
        all_facts = [fact for output in all_outputs if output.success for fact in output.facts]

        if self.verbose:
            print(f"\n[SharedMemory] Collected {len(all_facts)} facts.")

        reasoning_result = reasoner.reason(user_query, all_facts)
        final_result = self.debate.resolve(all_outputs, reasoning_result)

        if self.verbose:
            self._print_final_result(final_result)

        return final_result

    @staticmethod
    def _print_final_result(final_result: dict) -> None:
        print("\n" + "=" * 60)
        print("Final decision report")
        print("=" * 60)
        print(f"Conclusion: {final_result['conclusion']}")
        print(f"Confidence: {final_result['confidence']:.2f}")
        print("\nReasoning chain:")
        for step in final_result["reasoning_chain"]:
            print(f"  {step}")
        if final_result.get("contradictions"):
            print("\nContradictions:")
            for contradiction in final_result["contradictions"]:
                print(f"  - {contradiction}")
        print("\nRecommendations:")
        for recommendation in final_result["recommendations"]:
            print(f"  - {recommendation}")
