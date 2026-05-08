
#### `run_demo.py`

```python
#!/usr/bin/env python3
"""
OncoAgent 演示入口
"""

import sys
import os

# 将src目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from oncoagent.core.orchestrator import Orchestrator
from oncoagent.core.memory import SharedMemory


def demo_patient():
    """模拟一个晚期非小细胞肺癌患者的数据"""
    return {
        "genomic": {
            "mutations": ["KRAS G12C", "STK11 loss"],
            "tmb": 18   # 高突变负荷
        },
        "transcriptomic": {
            "tgf_beta_enriched": True,
            "treg_high": True,
            "cd8_low": True
        },
        "radiomic": {
            "fibrosis": 60,
            "pd_l1_pattern": "stromal"
        },
        "kg_query": "KRAS G12C, STK11, TGF-β"
    }


if __name__ == "__main__":
    memory = SharedMemory()
    orchestrator = Orchestrator(memory)

    query = "该晚期非小细胞肺癌患者是否应对帕博利珠单抗（抗PD-1）产生客观缓解？"
    result = orchestrator.run(query, demo_patient())

    print("\n✅ 演示执行完毕。实际系统中可将 mock 替换为真实模型调用。")