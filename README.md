# 🌌 QuantumAI 助教 | QuantumAI Assistant

> 量子计算教育 × 人工智能交互 —— 一个结合 FastAPI 与 Bloch 球可视化的智能教学演示系统。  
> “让量子世界可视化，让 AI 学会教学。”

---

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?logo=fastapi)
![HTML](https://img.shields.io/badge/Frontend-HTML%20%7C%20JS-orange?logo=javascript)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🧠 项目简介

**QuantumAI 助教** 是为人工智能创新类赛事与教学演示场景设计的本地运行系统，  
融合了 **量子态可视化** 与 **AI 智能对话** 模块，帮助学习者以直观、交互的方式理解量子计算的核心概念。

系统包括：

- 🧩 **AI 助手模块**：支持「追问 → 学习 → 回答 → 记忆」的循环；
- ⚛️ **Bloch 球可视化**：展示量子比特的状态变化、门操作与测量过程；
- 📚 **本地知识增强 (RAG)**：基于 JSONL 知识库与 Sentence Transformer 的语义检索；
- 💻 **一键运行**：Mac / Windows 环境直接启动，无需联网。

---

## 🛠 技术栈总览

| 模块 | 技术 |
|------|------|
| 后端 | FastAPI · Python 3.9.6 · Uvicorn |
| 前端 | HTML · JavaScript · TailwindCSS |
| 向量检索 | Sentence Transformers · FAISS |
| 知识库 | JSONL 文件结构（Base / Persona / Memory / Growth） |
| 可视化 | Bloch 球动画（量子态动态渲染） |
| 环境管理 | `uv` · `pyenv` · `venv` |

---

## ⚙️ 快速启动

### 🚀 Mac / Linux
```bash
uv run python app.py
```

### 🪟 Windows
```bash
run_win.bat
```

打开浏览器访问：  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

> 💡 点击「Bloch 球」按钮即可进入量子态可视化页面。

---

## 📂 项目结构

```bash
QuantumAI-Assistant/
├── app.py                         # FastAPI 主入口
├── bloch.html                     # Bloch 球可视化页面
├── web/
│   ├── templates/
│   │   ├── chat.html              # 对话界面
│   │   └── bloch.html             # 量子态展示页面
│   └── static/
│       ├── style.css              # 前端样式
│       └── script.js              # 前端逻辑
├── model/
│   └── paraphrase-multilingual-MiniLM-L12-v2/
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer.json
│       └── ...                    # 模型配置与权重
├── data/
│   ├── base_knowledge.jsonl       # 基础知识
│   ├── user_knowledge.jsonl       # 用户个性知识
│   ├── memory.jsonl               # 对话长期记忆
│   ├── persona.json               # AI 人格定义
│   ├── growth.json                # 成长日志
│   └── stopwords.txt              # 停用词表
├── fetch_and_split.py             # 文本切分脚本
├── merge_parts.py                 # 向量合并脚本
├── hybrid_index.py                # 混合检索逻辑
├── run_mac.sh                     # Mac 启动脚本
├── run_win.bat                    # Windows 启动脚本
├── pyproject.toml                 # uv 环境配置
├── uv.lock                        # 依赖锁定文件
└── README.md                      # 项目说明文档
```

---

## 💾 模型文件下载说明

本项目使用的语义检索模型为：

> [**paraphrase-multilingual-MiniLM-L12-v2**](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)  
> 作者：`sentence-transformers`  
> 模型类型：`SentenceTransformer`  
> 大小：约 450 MB  

⚠️ **注意：**
- 由于 GitHub 对单文件（>100MB）有限制，本仓库未上传模型权重文件。  
- 若需在本地完整运行，请手动下载模型至以下目录：  
  ```
  QuantumAI-Assistant/model/paraphrase-multilingual-MiniLM-L12-v2/
  ```
- 运行后系统会自动加载该模型进行文本嵌入与语义检索。

> ✅ 建议通过 Hugging Face Hub 或手动下载：
> ```
> https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
> ```

---

## 🧩 应用价值

- 🌍 教育创新：可在量子计算课程、AI 教学演示中使用；
- 💡 智能交互：展示 AI 助教在本地知识学习中的应用；
- 🧠 可扩展性：支持进一步集成 OpenAI API 或量子 SDK；
- 🏫 比赛展示：适用于人工智能创新类竞赛 Demo。

---

## 🏆 项目背景

本项目为 **人工智能创新杯 · 决赛作品**  
主题：「**AI + 量子计算教育助手**」  
目标是打造一个融合 **教育性 + 交互性 + 可视化性** 的智能学习平台，  
让量子计算不再是抽象概念，而是能被“看见、提问、理解”的知识体系。

---

## 📜 License

Distributed under the **MIT License**.  
See [`LICENSE`](./LICENSE) for more information.

---

## 👩‍💻 作者信息

**赵艺竹 (Yizhu Zhao)**  
📍 Southwest University (SWU) · 智能科学与技术专业  
🎯 研究方向：AI 助手 / 知识检索 / 智能教育系统  
💬 GitHub: [@zhaoyizhu6-pixel](https://github.com/zhaoyizhu6-pixel)

**徐熙曈 (Xv Xitong)**  
📍 Southwest University (SWU) · 智能科学与技术专业  
💬 GitHub: [@xxt7104](https://github.com/xxt7104)

---

> 🌟 *“Educating the machine that teaches quantum.”*  
> —— QuantumAI Team
