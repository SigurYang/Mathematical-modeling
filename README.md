# 兰州大学 2024 数模校赛

### 项目文档结构

**data**: 存放原始数据文件。

**images**: 包含用于报告或 Notebook 中的图像文件。

**outputs**: 保存模型输出、结果文件和中间过程文件。

**赛题**: 比赛问题描述文档，详细说明了比赛任务和标准。

**notebooks**: 包含多个 Jupyter Notebooks，用于数据分析和模型构建。

- **illness_analysis.ipynb**: 分析病情数据，进行特征工程和可视化。
- **op_analysis.ipynb**: 手术数据的分析，包括预处理步骤和转换方法和可视化。
- **time_series_analysis.ipynb**: 时间序列数据的分析及处理和可视化。
- **model_build.ipynb**: 模型构建及训练，包括特征选择和参数调优评估模型性能。
- **result_analysis.ipynb**: 分析模型结果和评估模型性能。

**Analysis.md**: 简要分析报告，包含项目的分析过程和结果。

**data_utils.py**: 数据处理工具代码，包括数据清洗、预处理和特征工程函数。

**requirements.txt**: 项目所需的 python 库和依赖项

### 如何使用

1. **安装依赖**: 请在项目运行前安装必要的 Python 库和依赖项。

```bash
pip install -r requirements.txt
```

2. **运行 Notebooks**: 请按上述顺序运行 Jupyter Notebooks，进行数据分析、模型构建和结果分析。
3. **查看结果**: 所有分析结果和模型输出保存在`outputs`文件夹中。
