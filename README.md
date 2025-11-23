# ai_service - 房源智能助手

## 项目概述

ai_service 是一个基于 LangChain 和 AI 的房源智能助手系统，主要功能包括：

1. 智能检索房源
2. 拍照识别录入房源信息
3. 房源标题与标签智能生成
4. 房源营销方案生成

目标是帮助房产中介或房产平台：

- 提高房源录入效率
- 提供智能搜索与推荐
- 生成营销内容，辅助运营决策

## 核心业务功能

### 1. 智能检索

- 用户输入查询，如“小区 + 户型 + 装修”
- 系统返回匹配房源，并按相似度排序
- 支持智能提示词（灰色补全）
- 支持多条件检索，如面积、楼层、朝向、价格

### 2. 拍照录入

- 用户拍摄房源信息表格/手写纸质信息
- 系统通过 OCR/文字识别自动提取房源字段：
  - 小区名、楼栋、房号、户型、面积、装修情况
- 数据清洗后存入系统，减少人工录入成本

### 3. 房源标题与标签生成

- 根据房源信息自动生成标准化标题和标签
  - 示例：`“回祥小区 3室2厅 精装修 朝南 满五唯一”`
  - 标签：户型、面积、装修、是否满五、朝向等
- 使用 LLM 或规则+AI 结合生成高质量标题和标签

### 4. 房源营销方案生成

- 根据房源特点生成营销文案/推广方案
  - 示例：“适合年轻家庭，附近配套齐全，交通便利”
- 可生成不同版本：社交媒体文案、海报标题、短文描述

## 技术方案

### 架构概览

### 核心技术

- **LangChain**：管理 Pipeline/Chain，节点组合
- **OpenAI Embeddings**：语义向量生成，支持检索
- **VectorStore**：Chroma / FAISS，向量存储与检索
- **OCR**：拍照文字识别（Tesseract / PaddleOCR / EasyOCR）
- **LLM**：智能生成标题、标签、营销文案
- **Python Web 框架**：FastAPI / Flask 提供接口
- **缓存**：Redis，用于加速热门查询
- **数据处理**：Pandas/Numpy 清洗、处理、构建向量

## 目录结构（简化版）

```bash
domus-ai/
│
├── app/
│   ├── main.py                # FastAPI/Flask 启动入口，配置路由并启动 Pipeline 调度
│   ├── api/
│   │   └── endpoints.py       # 定义 REST API 接口，如 /search，调用 pipeline_runner
│   └── pipeline_runner.py     # Pipeline 调度器，管理节点执行顺序并返回结果
│
├── core/
│   ├── nodes/
│   │   ├── preprocessor.py    # 文本预处理节点：清洗、分词、标准化用户输入
│   │   ├── embedding_node.py  # Embeddings 节点：调用 OpenAIEmbeddings 生成向量
│   │   ├── vectorstore_node.py# 向量检索节点：查询 Chroma/FAISS 并按相似度排序
│   │   └── llm_node.py        # LLM 节点：生成智能提示词或优化搜索结果显示
│   │
│   └── chains/
│       └── search_chain.py    # 搜索 Pipeline：组合 nodes/preprocessor→embedding→vectorstore→llm
│
├── infrastructure/
│   ├── vectorstore/           # 向量库持久化管理，初始化和维护 Chroma/FAISS
│   ├── cache/                 # 可选缓存，如 Redis，加快检索和响应速度
│   └── external_apis.py       # 外部服务封装，如 LLM 或 OCR API，含请求和错误处理
│
├── data/
│   ├── raw/                   # 原始房源数据，CSV/JSON 或数据库导出
│   └── processed/
│       ├── embeddings/        # 已生成向量，用于快速检索
│       └── cleaned/           # 清洗和标准化后的文本数据，供 embeddings/向量库使用
│
├── tests/
│   ├── unit/                  # 单元测试：测试各节点功能
│   └── integration/           # 集成测试：验证完整 Pipeline 从输入到输出
│
├── scripts/
│   ├── data_prep/             # 数据预处理脚本：清洗、去重、格式化
│   └── vectorstore_init/      # 构建向量库脚本：生成 embeddings 并存入 Chroma/FAISS
│
├── config/
│   └── settings.py            # 配置管理类，管理 API Key、模型配置、路径参数等
│
├── requirements.txt           # Python 项目依赖
├── .env.example               # 环境变量示例：API_KEY、VECTORSTORE_PATH 等
└── README.md                  # 项目说明：架构、目录、运行步骤、Pipeline 流程示意
```
