# regmonkey

[English](README.md) | [日本語](README.ja.md) | [中文](README.zh.md)

**regmonkey** 是一个轻量级的 Python 包，旨在简化数据分析和回归建模任务。它简化了描述性统计、虚拟变量创建、回归模型估计和带注释的 Excel 文件导出等任务。

## 特点

- 📊 **描述性统计**: 轻松从 DataFrame 生成清晰且四舍五入的汇总统计。
- 🧠 **智能变量解析**: 自动解释对数转换、多项式项和交互项。
- 📦 **虚拟变量创建**: 快速将分类变量转换为虚拟/指标变量。
- 📈 **回归分析**: 运行支持对数、幂和交互项的多元线性回归，并导出格式良好的结果表。
- 📄 **Excel 页脚注释**: 自动向 Excel 文件添加注释。
- 🌐 **多语言支持**: 支持使用日语、英语或中文指定变量，自动检测语言并提供一致的结果输出格式。

## 安装

```bash
pip install regmonkey
```

## 函数

### `add_footer(file_path, value, sheet_name=None)`

向 Excel 工作表的最后一行添加注释。

**参数**:

- `file_path` (str): Excel 文件的路径。
- `value` (str): 注释的内容。
- `sheet_name` (str, 可选): 要修改的工作表名称。默认为第一个工作表。

**示例**:

```python
from regmonkey.stats import add_footer

add_footer("example.xlsx", "注：数据为初步版本。", sheet_name="Sheet1")
```

---

### `get_dummies(df, columns)`

将分类变量转换为虚拟/指标变量。

**参数**:

- `df` (DataFrame): 输入 DataFrame。
- `columns` (str 列表): 要转换的列名列表。

**返回值**:

- 包含虚拟变量的新 DataFrame。

**示例**:

```python
from regmonkey.stats import get_dummies
import pandas as pd

data = pd.DataFrame({"Year": ["2020", "2021", "2022"], "Value": [10, 20, 30]})
dummies = get_dummies(data, columns=["Year"])
print(dummies)
```

---

### `summary(df, var_list)`

生成变量列表的描述性统计。

**参数**:

- `df` (DataFrame): 输入 DataFrame。
- `var_list` (str 列表): 要汇总的变量名列表。

**返回值**:

- 包含描述性统计的 DataFrame。

**示例**:

```python
from regmonkey.stats import summary
import pandas as pd

data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
stats = summary(data, ["A", "B"])
print(stats)
```

---

### `regression(variables_dicts, df, decimal_places=2)`

执行支持对数、幂和交互项的回归分析。

**参数**:

- `variables_dicts` (dict 列表): 指定因变量和自变量的字典列表。
  - **多语言支持**: 可以使用不同语言的变量键：
    - 日语: `{"被説明変数": "Y", "説明変数": ["X1", "X2"]}`
    - 英语: `{"y": "Y", "X": ["X1", "X2"]}`
    - 中文: `{"被解释变量": "Y", "解释变量": ["X1", "X2"]}`
  - **对数项**: 使用`log(X1)`表示`X1`的自然对数。
  - **幂项**: 使用`X2**2`或`X2**3`表示`X2`的平方或立方。
  - **虚拟变量**: 对于二元变量，直接使用（如`['性别']`）。对于分类变量，使用`get_dummies`预处理（如`['年份_1990', '年份_1995']`）。
  - **交互项**: 使用`X1:X2`表示`X1`和`X2`的交互作用，或组合转换如`X1**2:log(X2)`。
- `df` (DataFrame): 输入数据。
- `decimal_places` (int): 结果的小数位数。

**返回值**:

- 包含以下内容的元组：
  1. 处理后的 DataFrame。
  2. 使用变量的描述性统计。
  3. 回归结果表。

**示例**:

```python
from regmonkey.stats import regression
import pandas as pd

# 示例数据
data = pd.DataFrame({
    "X1": [1, 2, 3],
    "X2": [4, 5, 6],
    "Y": [7, 8, 9],
    "Category": ["A", "B", "A"]
})

# 分类变量预处理
data_with_dummies = pd.get_dummies(data, columns=["Category"])

# 定义回归变量（中文）
variables_zh = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 定义回归变量（英语）
variables_en = [
    {"y": "Y", "X": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 定义回归变量（日语）
variables_ja = [
    {"被説明変数": "Y", "説明変数": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 执行回归分析（使用上述任一变量定义）
df_processed, summary_result, regression_result = regression(variables_zh, data_with_dummies)

# 打印结果
print(regression_result)
```

在此示例中：

- 回归可以使用支持的语言（中文、英语、日语）中的任何一种来指定。
- `log(X1)`计算`X1`的自然对数。
- `X2**2`计算`X2`的平方。
- `X1:X2`计算`X1`和`X2`的交互作用。
- `Category`的虚拟变量使用`get_dummies`自动创建。
- 输出标签（如"样本数"/"N"/"観測数"）会自动匹配输入键的语言。

---

## 使用示例

```python
import pandas as pd
from regmonkey.stats import get_dummies, regression, add_footer

# 加载数据
data = pd.DataFrame({
    "X1": [1, 2, 3],
    "X2": [4, 5, 6],
    "Y": [7, 8, 9],
    "Category": ["A", "B", "A"]
})

# 创建虚拟变量
data_with_dummies = get_dummies(data, columns=["Category"])

# 执行包含对数、幂和交互项的回归分析（使用中文键）
variables = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]
df_processed, summary_result, regression_result = regression(variables, data_with_dummies)

# 将回归结果保存到Excel并添加注释
regression_result.to_excel("regression_results.xlsx", index=False)
add_footer("regression_results.xlsx", "注：回归结果包含对数、幂和交互项。")

# 将描述性统计保存到Excel并添加注释
summary_result.to_excel("summary_statistics.xlsx", index=False)
add_footer("summary_statistics.xlsx", "注：回归分析中使用的所有变量的描述性统计。")
```
