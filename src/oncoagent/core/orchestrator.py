from ..agents import GenomicAgent, TranscriptomicAgent, RadiomicAgent, KnowledgeGraphAgent
from ..reasoning.chain_of_thought import ChainOfThoughtReasoner
from ..reasoning.debate import DebateConsensusModule
from .memory import SharedMemory
from .types import AgentRole, SubTask


class Orchestrator:
    """
    任务分解、调度、管理多Agent协作流程
    """
    def __init__(self, memory: SharedMemory):
        self.memory = memory
        self.agents = self._init_agents(memory)
        self.reasoner = ChainOfThoughtReasoner(memory, use_mock=True)
        self.debate = DebateConsensusModule()

    def _init_agents(self, memory):
        return {
            AgentRole.GENOMIC: GenomicAgent(AgentRole.GENOMIC, memory),
            AgentRole.TRANSCRIPTOMIC: TranscriptomicAgent(AgentRole.TRANSCRIPTOMIC, memory),
            AgentRole.RADIOMIC: RadiomicAgent(AgentRole.RADIOMIC, memory),
            AgentRole.KNOWLEDGE_GRAPH: KnowledgeGraphAgent(AgentRole.KNOWLEDGE_GRAPH, memory),
        }

    def run(self, user_query: str, patient_data: dict) -> dict:
        print("\n" + "="*60)
        print(f"[Orchestrator] 接到任务: {user_query}")
        print("="*60)

        # 1. 分解任务，执行各Agent
        all_outputs = []
        task_gen = SubTask("分析基因组", AgentRole.GENOMIC, patient_data.get("genomic", {}))
        out_gen = self.agents[AgentRole.GENOMIC].process(task_gen)
        all_outputs.append(out_gen)

        task_tran = SubTask("分析转录组", AgentRole.TRANSCRIPTOMIC, patient_data.get("transcriptomic", {}))
        out_tran = self.agents[AgentRole.TRANSCRIPTOMIC].process(task_tran)
        all_outputs.append(out_tran)

        task_rad = SubTask("分析影像", AgentRole.RADIOMIC, patient_data.get("radiomic", {}))
        out_rad = self.agents[AgentRole.RADIOMIC].process(task_rad)
        all_outputs.append(out_rad)

        task_kg = SubTask("知识检索", AgentRole.KNOWLEDGE_GRAPH, {"entity": patient_data.get("kg_query", "")})
        out_kg = self.agents[AgentRole.KNOWLEDGE_GRAPH].process(task_kg)
        all_outputs.append(out_kg)

        # 2. 收集所有事实
        all_facts = []
        for out in all_outputs:
            if out.success:
                all_facts.extend(out.facts)
        print(f"\n[SharedMemory] 当前共存储 {len(all_facts)} 条事实")

        # 3. 长链推理
        reasoning_result = self.reasoner.reason(user_query, all_facts)

        # 4. 辩论与共识
        final_result = self.debate.resolve(all_outputs, reasoning_result)

        # 5. 输出最终决策
        print("\n" + "="*60)
        print("最终决策报告")
        print("="*60)
        print(f"结论: {final_result['conclusion']}")
        print(f"置信度: {final_result['confidence']:.2f}")
        print("\n推理链:")
        for i, step in enumerate(final_result['reasoning_chain'], 1):
            print(f"  {step}")
        if final_result.get('contradictions'):
            print("\n矛盾处理:")
            for c in final_result['contradictions']:
                print(f"  ⚠️ {c}")
        print("\n治疗推荐:")
        for rec in final_result['recommendations']:
            print(f"  ✔ {rec}")

        return final_result