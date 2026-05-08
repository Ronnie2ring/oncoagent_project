from typing import Dict, List, Any
from ..core.memory import SharedMemory
from ..core.types import Fact


class ChainOfThoughtReasoner:
    """
    长链推理引擎：基于LLM或规则，显式生成因果推理链。
    MVP中使用模拟LLM响应，但接口兼容真实LLM调用。
    """
    def __init__(self, memory: SharedMemory, use_mock=True):
        self.memory = memory
        self.use_mock = use_mock
        if not use_mock:
            # 可在此初始化真实LLM，如 OpenAI / LLaMA
            pass

    def reason(self, user_query: str, initial_facts: List[Fact]) -> Dict[str, Any]:
        """
        执行长链推理，返回：
        {
          "conclusion": str,
          "confidence": float,
          "reasoning_chain": List[str],
          "recommendations": List[str],
          "contradictions": List[str]
        }
        """
        print("\n[Reasoner] 启动长链推理 (Chain-of-Thought)...")
        if self.use_mock:
            return self._mock_reasoning(user_query, initial_facts)
        else:
            return self._llm_reasoning(user_query, initial_facts)

    def _mock_reasoning(self, query: str, facts: List[Fact]) -> Dict[str, Any]:
        fact_texts = [f.content for f in facts]
        has_stk11 = any("STK11" in t for t in fact_texts)
        has_tgf = any("TGF-β" in t for t in fact_texts)
        has_treg = any("Treg" in t for t in fact_texts)
        has_cd8_low = any("CD8+" in t and "低" in t for t in fact_texts)
        has_high_tmb = any("TMB = 18" in t for t in fact_texts)
        has_pd_l1_stromal = any("PD-L1" in t and "间质" in t for t in fact_texts)

        reasoning_steps = []
        reasoning_steps.append("Step1: 基因组层发现 STK11 失活突变 → 已知该突变驱动 TGF-β 上调并诱导免疫排斥微环境。")
        if has_tgf and has_treg:
            reasoning_steps.append("Step2: 转录组层证实 TGF-β 通路富集且 Treg 比例升高 → 介导 CD8+ T 细胞抑制。")
        reasoning_steps.append("Step3: 影像学层显示间质纤维化及间质 PD-L1 表达 → 物理屏障 + 非肿瘤细胞的 PD-L1 不参与效应 T 细胞杀伤。")

        contradictions = []
        if has_high_tmb:
            contradictions.append("高 TMB 通常提示免疫治疗敏感，但 STK11 突变可完全抵消其预测价值 (Rizvi et al. 2020)。")

        if has_stk11 or (has_tgf and has_treg):
            conclusion = "患者对抗 PD-1 单药治疗预期无响应（耐药）"
            confidence = 0.85
            recommendations = [
                "考虑联合 TGF-β 抑制剂（如 galunisertib）的临床试验 (NCT02423343)",
                "转向 KRAS G12C 靶向治疗：索托拉西布 (sotorasib) 960mg 每日一次"
            ]
        else:
            conclusion = "患者可能从抗 PD-1 治疗中获益"
            confidence = 0.60
            recommendations = ["建议进一步检测 PD-L1 IHC 及 MSI 状态"]

        return {
            "conclusion": conclusion,
            "confidence": confidence,
            "reasoning_chain": reasoning_steps,
            "recommendations": recommendations,
            "contradictions": contradictions
        }

    def _llm_reasoning(self, query: str, facts: List[Fact]) -> Dict[str, Any]:
        raise NotImplementedError("Real LLM integration not implemented in MVP")