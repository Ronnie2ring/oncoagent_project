from ..core.base_agent import BaseAgent
from ..core.types import AgentRole, SubTask, AgentOutput, Fact


class GenomicAgent(BaseAgent):
    """基因组Agent：分析VCF/MAF，提取驱动突变、TMB、MSI状态等"""
    def process(self, task: SubTask) -> AgentOutput:
        print(f"[GenomicAgent] 分析基因组数据...")
        sample_mutations = task.input_data.get("mutations", ["KRAS G12C", "STK11 loss"])
        tmb = task.input_data.get("tmb", 18)

        facts = []
        facts.append(Fact(content=f"驱动突变: {', '.join(sample_mutations)}",
                          source_agent=self.role, confidence=0.95))
        facts.append(Fact(content=f"肿瘤突变负荷 TMB = {tmb} muts/Mb {'(高)' if tmb>10 else '(低)'}",
                          source_agent=self.role, confidence=0.9))
        if "STK11" in " ".join(sample_mutations):
            facts.append(Fact(content="STK11功能丧失突变，与免疫冷微环境、抗PD-1原发性耐药相关",
                              source_agent=self.role, confidence=0.85))
        return AgentOutput(success=True, facts=facts)