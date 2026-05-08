from ..core.base_agent import BaseAgent
from ..core.types import AgentRole, SubTask, AgentOutput, Fact


class TranscriptomicAgent(BaseAgent):
    """转录组Agent：通路活性、免疫浸润"""
    def process(self, task: SubTask) -> AgentOutput:
        print(f"[TranscriptomicAgent] 分析转录组数据...")
        sample_data = task.input_data
        facts = []
        if sample_data.get("tgf_beta_enriched", True):
            facts.append(Fact(content="TGF-β通路显著富集 (NES=2.1, FDR<0.01)",
                              source_agent=self.role, confidence=0.88))
        if sample_data.get("treg_high", True):
            facts.append(Fact(content="调节性T细胞(Treg)比例升高(15%)，提示免疫抑制微环境",
                              source_agent=self.role, confidence=0.82))
        if sample_data.get("cd8_low", True):
            facts.append(Fact(content="CD8+ T细胞浸润比例低(3%)，效应免疫应答不足",
                              source_agent=self.role, confidence=0.85))
        return AgentOutput(success=True, facts=facts)