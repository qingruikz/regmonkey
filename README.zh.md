# regmonkey

[English](README.md) | [日本語](README.ja.md) | [中文](README.zh.md)

**regmonkey** 是一个轻量级的 Python 包，旨在简化数据分析和回归建模任务。它简化了描述性统计、虚拟变量创建、回归模型估计和导出带注释的 Excel 文件等任务。

## 功能特点

- 📊 **描述性统计**：轻松从 DataFrame 生成清晰且四舍五入的汇总统计。
- 🧠 **智能变量解析**：自动解释对数变换、多项式项和交互项。
- 📦 **虚拟变量创建**：快速将分类变量转换为虚拟/指示变量。
- 📈 **回归分析**：运行多元线性回归，支持对数、幂和交互项，并导出格式良好的结果表。
- 📄 **Excel 页脚注释**：自动向 Excel 文件添加脚注。
- 🌐 **多语言支持**：使用任何支持的语言（英语、日语或中文）指定变量，并通过 `lang` 参数独立控制输出语言，确保所有结果的一致性格式。

![](https://raw.githubusercontent.com/qingruikz/regmonkey/main/assets/example.png)

## 安装

```bash
pip install regmonkey
```

## 函数

### `add_footer(file_path, value, sheet_name=None)`

在 Excel 工作表的最后一行添加脚注。

**参数**：

- `file_path` (str)：Excel 文件的路径。
- `value` (str)：脚注的内容。
- `sheet_name` (str, 可选)：要修改的工作表名称。默认为第一个工作表。

**示例**：

```python
from regmonkey.stats import add_footer

add_footer("example.xlsx", "注：数据为初步数据。", sheet_name="Sheet1")
```

---

### `get_dummies(df, columns)`

将分类变量转换为虚拟/指示变量。

**参数**：

- `df` (DataFrame)：输入的 DataFrame。
- `columns` (str 列表)：要转换的列名列表。

**返回**：

- 包含虚拟变量的新 DataFrame。

**示例**：

```python
from regmonkey.stats import get_dummies
import pandas as pd

data = pd.DataFrame({"Year": ["2020", "2021", "2022"], "Value": [10, 20, 30]})
dummies = get_dummies(data, columns=["Year"])
print(dummies)
```

---

### `summary(df, var_list, round_digits=2, lang="ja")`

计算指定变量的描述性统计量。

- `df`：包含数据的 DataFrame
- `var_list`：变量名列表
- `round_digits`：小数位数（默认：2）
- `lang`：输出标签的语言代码（"ja"、"en"、"zh"）（默认："ja"）

**注意**：默认情况下（未指定 `lang` 时），输出将为日语。

返回包含以下统计量的 DataFrame：

- 样本数
- 平均值
- 标准差
- 最小值
- 最大值

示例：

```python
# 默认（日语标签）
summary_stats = summary(df, ["X1", "X2"])

# 英语标签
summary_stats = summary(df, ["X1", "X2"], lang="en")

# 日语标签
summary_stats = summary(df, ["X1", "X2"], lang="ja")

# 中文标签
summary_stats = summary(df, ["X1", "X2"], lang="zh")
```

---

### `regress(variables_dicts, df, decimal_places=2, lang="ja", cov_type="HC1")`

执行支持对数、幂和交互项的回归分析。

**参数**：

- `variables_dicts` (字典列表)：指定因变量和自变量的字典列表。
  - **多语言支持**：您可以使用不同语言的变量键：
    - 日语：`{"被説明変数": "Y", "説明変数": ["X1", "X2"]}`
    - 英语：`{"y": "Y", "X": ["X1", "X2"]}`
    - 中文：`{"被解释变量": "Y", "解释变量": ["X1", "X2"]}`
  - **对数项**：使用 `log(X1)` 表示 `X1` 的自然对数。
  - **幂项**：使用 `X2**2` 或 `X2**3` 表示平方或立方项。
  - **虚拟变量**：对于二元变量，直接使用（例如，`['Gender']`）。对于分类变量，使用 `get_dummies` 预处理 DataFrame（例如，`['Year_1990', 'Year_1995']`）。
  - **交互项**：使用 `X1:X2` 表示 `X1` 和 `X2` 之间的交互，或组合变换如 `X1**2:log(X2)`。
- `df` (DataFrame)：输入数据。
- `decimal_places` (int)：结果的小数位数。
- `lang` (str)：输出标签的语言代码（"ja"、"en"、"zh"）（默认："ja"）
- `cov_type` (str)：标准误差的计算方法（默认："HC1"）
  - "HC1"：怀特标准误差（带小样本修正）
  - "HC0"：怀特标准误差
  - "HC2"：麦金农标准误差
  - "HC3"：戴维森-麦金农标准误差
  - "nonrobust"：常规标准误差

**注意**：默认情况下（未指定 `lang` 时），输出将为日语。

**返回**：

- 包含以下内容的元组：
  1. 处理后的 DataFrame。
  2. 使用变量的描述性统计量。
  3. 回归结果表。

**示例**：

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

# 预处理分类变量
data_with_dummies = pd.get_dummies(data, columns=["Category"])

# 定义回归变量（日语）
variables_ja = [
    {"被説明変数": "Y", "説明変数": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 定义回归变量（英语）
variables_en = [
    {"y": "Y", "X": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 定义回归变量（中文）
variables_zh = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 使用默认输出执行回归（日语）
df_processed, summary_result, regression_result = regress(variables_ja, data_with_dummies)

# 使用日语输出执行回归
df_processed, summary_result, regression_result = regress(variables_ja, data_with_dummies, lang="ja")

# 使用英语输出执行回归
df_processed, summary_result, regression_result = regress(variables_en, data_with_dummies, lang="en")

# 使用中文输出执行回归
df_processed, summary_result, regression_result = regress(variables_zh, data_with_dummies, lang="zh")

# 打印结果
print(regression_result)
```

---

### `interpret_result(df_result, lang="ja")`

解释回归结果并生成人类可读的文本描述。

**参数**：

- `df_result` (DataFrame)：由`regress`函数返回的回归结果表
- `lang` (str, 可选)：输出文本的语言代码（"ja"、"en"、"zh"）（默认："ja"）

**返回值**：

- 包含回归结果解释的字符串。包括以下内容：
  - 模型描述（因变量对自变量进行回归）
  - 每个变量的系数估计值和显著性水平
  - 每个模型的调整后决定系数

**注意**：默认情况下（未指定`lang`时），输出将为日语。

**示例**：

```python
from regmonkey.stats import regress, interpret_result
import pandas as pd

# 样本数据
data = pd.DataFrame({
    "X1": [1, 2, 3, 4, 5],
    "X2": [2, 3, 4, 5, 6],
    "Y": [3, 5, 7, 9, 11]
})

# 执行回归
variables = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2"]}
]
df_processed, summary_result, regression_result = regress(variables, data, lang="ja")

# 解释结果
interpretation = interpret_result(regression_result, lang="ja")
print(interpretation)
```

输出将为日语（默认）：

```
モデル（1）ではYをX1、X2に回帰した。
X1の係数の推定値は1.00となり、10％の有意水準でも有意に推定されていない。
X2の係数の推定値は1.00となり、10％の有意水準でも有意に推定されていない。
モデル（1）の自由度修正済み決定係数は0.50である。
```

对于中文输出：

```python
interpretation = interpret_result(regression_result, lang="zh")
print(interpretation)
```

对于英文输出：

```python
interpretation = interpret_result(regression_result, lang="en")
print(interpretation)
```

---

## 使用示例

```python
import pandas as pd
from regmonkey.stats import get_dummies, regress, interpret_result, add_footer

# 加载数据
data = pd.DataFrame({
    "X1": [1, 2, 3, 4, 5],
    "X2": [2, 3, 4, 5, 6],
    "Y": [3, 5, 7, 9, 11],
    "Category": ["A", "B", "A", "B", "A"]
})

# 创建虚拟变量
data_with_dummies = get_dummies(data, columns=["Category"])

# 执行回归分析
variables = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2"]},
    {"被解释变量": "Y", "解释变量": ["X1", "X2", "log(X1)", "X2**2"]}
]
df_processed, summary_result, regression_result = regress(variables, data_with_dummies, lang="zh")

# 解释回归结果
interpretation = interpret_result(regression_result, lang="zh")
print(interpretation)

# 将回归结果保存到 Excel 并添加脚注
regression_result.to_excel("regression_results.xlsx", index=True)
add_footer("regression_results.xlsx", "注：回归结果包括对数、幂和交互项。标准误差显示在括号内。")

# 将汇总统计量保存到 Excel 并添加脚注
summary_result.to_excel("summary_statistics.xlsx", index=True)
add_footer("summary_statistics.xlsx", "注：回归分析中使用的所有变量的汇总统计量。")

# 将解释结果保存到文本文件
with open("interpretation.txt", "w", encoding="utf-8") as f:
    f.write(interpretation)
```

更详细的使用示例，请参阅 `examples` 目录下的 `example.py`。
