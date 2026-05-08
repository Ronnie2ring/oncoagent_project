from ..core.base_agent import BaseAgent
from ..core.types import AgentRole, SubTask, AgentOutput, Fact


class KnowledgeGraphAgent(BaseAgent):
    """知识图谱检索Agent：查询基因-药物-表型关联"""
    def process(self, task: SubTask) -> AgentOutput:
        print(f"[KnowledgeGraphAgent] 检索知识库...")
        query_entity = task.input_data.get("entity", "KRAS G12C")
        facts = []
        if "KRAS G12C" in query_entity:
            facts.append(Fact(content="KRAS G12C突变对索托拉西布(sotorasib)敏感 (证据等级A)",
                              source_agent=self.role, confidence=0.95))
        if "STK11" in query_entity:
            facts.append(Fact(content="STK11突变与抗PD-1治疗原发性耐药强相关 (Skoulidis et al. 2018)",
                              source_agent=self.role, confidence=0.92))
        if "TGF-β" in query_entity:
            facts.append(Fact(content="TGF-β高活性可介导免疫排斥微环境，联合TGF-β抑制剂可能逆转耐药",
                              source_agent=self.role, confidence=0.89))
        return AgentOutput(success=True, facts=facts)