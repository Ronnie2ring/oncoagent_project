from typing import Dict, List
from ..core.types import AgentOutput


class DebateConsensusModule:
    """多Agent辩论与共识：当LLM检测到高矛盾时触发"""
    @staticmethod
    def resolve(agents_outputs: List[AgentOutput], reasoner_result: Dict) -> Dict:
        print("\n[DebateModule] 检测到潜在矛盾，启动共识协商...")
        conf = reasoner_result["confidence"]
        low_conf_facts = []
        for out in agents_outputs:
            for fact in out.facts:
                if fact.confidence < 0.7:
                    low_conf_facts.append(fact.content)
        if low_conf_facts:
            print(f"  争议事实: {low_conf_facts}")
            conf = max(0.5, conf - 0.1)

        final = reasoner_result.copy()
        final["confidence"] = conf
        final["consensus_reached"] = True
        return final