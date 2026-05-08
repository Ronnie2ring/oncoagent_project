# OncoAgent

> 多 Agent 协作与长链推理驱动的肿瘤精准决策系统

OncoAgent 是一个面向生物医学领域（肿瘤学）的智能决策系统，通过**多领域专业 Agent**（基因组、转录组、影像学、知识图谱）协作与**显式长链因果推理**，将患者的多组学、病理影像等多模态数据转化为可解释的治疗响应预测与个性化方案推荐。它模拟分子肿瘤专家委员会（Molecular Tumor Board）的认知流程，旨在提升精准肿瘤决策的效率与可解释性。

---

## ✨ 核心特性

- **多 Agent 协作**：基因组、转录组、影像学、知识图谱 Agent 各司其职，通过协调器动态调度，模拟专家会诊。
- **长链因果推理**：基于 Chain-of-Thought，显式建模从分子改变到表型的多步生物学逻辑（如：STK11突变 → TGF-β上调 → Treg增加 → 免疫耐药）。
- **可解释决策**：输出包含完整推理链、证据引用、置信度及治疗推荐，支持临床验证与干预。
- **矛盾检测与共识**：内置辩论模块，当 Agent 结论冲突时自动触发证据权重协商，输出共识结果。
- **即插即用**：模块化设计，可替换真实 LLM（如 GPT-4、BioMed-LLM）或对接实际生物信息学工具（PyEnsembl、GSEAPY 等）。

---

## 🏗️ 系统架构

```
患者数据（多组学 + 影像）
         ↓
┌─────────────────────────────────┐
│        Orchestrator Agent       │  ← 任务分解、调度
└────────────┬────────────────────┘
     ┌───────┼───────┬──────────────┐
     ↓       ↓       ↓              ↓
┌─────────┐┌─────────┐┌─────────┐┌─────────────┐
│ Genomic ││Transcript││Radiomic ││ Knowledge   │
│ Agent   ││ Agent   ││ Agent   ││ Graph Agent │
└────┬────┘└────┬────┘└────┬────┘└──────┬──────┘
     └──────────┴──────────┴─────────────┘
                     ↓
         ┌─────────────────────┐
         │   Shared Memory     │  ← 中间事实存储
         │  (工作记忆池)        │
         └──────────┬──────────┘
                    ↓
         ┌─────────────────────┐
         │ Chain-of-Thought     │  ← 长链推理引擎
         │    Reasoner          │
         └──────────┬──────────┘
                    ↓
         ┌─────────────────────┐
         │  Debate & Consensus │  ← 矛盾解决
         └──────────┬──────────┘
                    ↓
         最终决策 + 可解释推理链
```

---

## 📦 安装

### 环境要求
- Python 3.9+
- 建议使用虚拟环境

### 克隆与安装
```bash
git clone https://github.com/yourlab/oncoagent.git
cd oncoagent
pip install -r requirements.txt
```

依赖说明：
- `pydantic`：数据校验与类型管理
- `pyyaml`：配置文件解析（可选）

---

## 🚀 快速开始

### 运行演示（Mock 模式）
```bash
python run_demo.py
```
该命令使用内置模拟数据（非小细胞肺癌患者：KRAS G12C/STK11突变、高TMB、TGF-β富集、间质纤维化等），执行完整的 Agent 协作与推理流程，输出类似以下报告：

```
============================================================
最终决策报告
============================================================
结论: 患者对抗 PD-1 单药治疗预期无响应（耐药）
置信度: 0.85

推理链:
  Step1: 基因组层发现 STK11 失活突变 → 已知该突变驱动 TGF-β 上调并诱导免疫排斥微环境。
  Step2: 转录组层证实 TGF-β 通路富集且 Treg 比例升高 → 介导 CD8+ T 细胞抑制。
  Step3: 影像学层显示间质纤维化及间质 PD-L1 表达 → 物理屏障 + 非肿瘤细胞的 PD-L1 不参与效应 T 细胞杀伤。

矛盾处理:
  ⚠️ 高 TMB 通常提示免疫治疗敏感，但 STK11 突变可完全抵消其预测价值 (Rizvi et al. 2020)。

治疗推荐:
  ✔ 考虑联合 TGF-β 抑制剂（如 galunisertib）的临床试验 (NCT02423343)
  ✔ 转向 KRAS G12C 靶向治疗：索托拉西布 (sotorasib) 960mg 每日一次
```

### 自定义输入
修改 `run_demo.py` 中的 `demo_patient()` 函数，传入实际患者数据（格式见下文“数据格式”），即可进行预测。

---

## 📂 数据格式示例

```python
patient_data = {
    "genomic": {
        "mutations": ["KRAS G12C", "STK11 loss"],   # 驱动突变列表
        "tmb": 18                                   # 肿瘤突变负荷 (muts/Mb)
    },
    "transcriptomic": {
        "tgf_beta_enriched": True,                  # TGF-β通路是否富集
        "treg_high": True,                          # Treg比例是否升高
        "cd8_low": True                             # CD8+ T细胞是否低浸润
    },
    "radiomic": {
        "fibrosis": 60,                             # 间质纤维化比例(%)
        "pd_l1_pattern": "stromal"                  # PD-L1表达模式: "stromal"/"tumor"
    },
    "kg_query": "KRAS G12C, STK11, TGF-β"           # 知识图谱检索实体
}
```

> 注：Mock 模式下仅使用了上述字段。实际部署时可扩展字段对接真实数据源。

---

## 🧩 扩展与定制

### 1. 接入真实生物信息学工具
- **基因组 Agent**：替换为调用 `PyEnsembl`、`VEP` 或 `maftools`。
- **转录组 Agent**：集成 `GSEAPY`（通路富集）、`CIBERSORTx`（免疫浸润）。
- **影像学 Agent**：使用预训练的视觉 Transformer（如 `CONCH`、`UNI`）提取病理特征。

### 2. 使用真实 LLM 进行长链推理
在 `src/oncoagent/core/orchestrator.py` 中修改：
```python
self.reasoner = ChainOfThoughtReasoner(memory, use_mock=False)
```
并在 `src/oncoagent/reasoning/chain_of_thought.py` 中实现 `_llm_reasoning()` 方法，调用 OpenAI API 或本地部署的 BioMed-LLM。

### 3. 扩展 Agent 角色
继承 `BaseAgent` 类，添加新 Agent（如“代谢组Agent”、“微生物组Agent”），并在 `Orchestrator._init_agents()` 中注册。

### 4. 持久化记忆与向量检索
将 `SharedMemory` 后端更换为 Chroma、Qdrant 等向量数据库，实现语义级事实检索。

---

## 🧪 测试

运行单元测试（目前包含基因组Agent的简单测试）：
```bash
python -m pytest tests/
```
或直接执行：
```bash
python tests/test_agents.py
```

---

## 🗂️ 项目结构

```
oncoagent/
├── README.md
├── requirements.txt
├── run_demo.py
├── config/
│   └── default.yaml                 # 配置文件（可选）
├── src/
│   └── oncoagent/
│       ├── __init__.py
│       ├── core/                    # 核心组件
│       │   ├── types.py             # 数据结构（Fact, SubTask等）
│       │   ├── memory.py            # 共享工作记忆池
│       │   ├── base_agent.py        # Agent基类
│       │   └── orchestrator.py      # 协调器
│       ├── agents/                  # 专业Agent实现
│       │   ├── genomic_agent.py
│       │   ├── transcriptomic_agent.py
│       │   ├── radiomic_agent.py
│       │   └── knowledge_graph_agent.py
│       ├── reasoning/               # 推理与辩论模块
│       │   ├── chain_of_thought.py
│       │   └── debate.py
│       └── utils/                   # 辅助工具（待扩展）
└── tests/                           # 单元测试
```

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)。

---

## 📚 引用

如果您在研究中使用了 OncoAgent，请引用：
```
@software{oncoagent2025,
  author = {Ronnie Zhang},
  title = {OncoAgent: Multi-Agent Collaborative System for Precision Oncology},
  year = {2026},
  url = {https://github.com/Ronnie2ring/oncoagent_project}
}
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。请确保代码通过现有测试，并为新功能添加相应测试。

---

## 📧 联系方式

如有任何问题或合作意向，请联系：`943830787@qq.com`

---

**OncoAgent —— 让肿瘤决策从“黑箱预测”走向“透明因果推理”。**