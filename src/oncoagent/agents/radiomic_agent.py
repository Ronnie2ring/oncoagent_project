from ..core.base_agent import BaseAgent
from ..core.types import AgentRole, SubTask, AgentOutput, Fact


class RadiomicAgent(BaseAgent):
    """影像学Agent：病理WSI / CT影像特征"""
    def process(self, task: SubTask) -> AgentOutput:
        print(f"[RadiomicAgent] 分析影像数据...")
        sample_data = task.input_data
        facts = []
        if sample_data.get("fibrosis", 60) > 50:
            facts.append(Fact(content="间质纤维化比例>60%，形成物理屏障限制淋巴细胞浸润",
                              source_agent=self.role, confidence=0.78))
        if sample_data.get("pd_l1_pattern") == "stromal":
            facts.append(Fact(content="PD-L1表达呈斑驳状，主要定位于间质巨噬细胞，提示适应性耐药",
                              source_agent=self.role, confidence=0.83))
        return AgentOutput(success=True, facts=facts)