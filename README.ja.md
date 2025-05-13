# regmonkey

[English](README.md) | [日本語](README.ja.md) | [中文](README.zh.md)

**regmonkey** は、データ分析と回帰モデリングのタスクを効率化するための軽量な Python パッケージです。記述統計、ダミー変数の作成、回帰モデルの推定、注釈付き Excel ファイルのエクスポートなどのタスクを簡素化します。

## 特徴

- 📊 **記述統計**: DataFrame から見やすく丸められた要約統計量を簡単に生成できます。
- 🧠 **スマートな変数解析**: 対数変換、多項式項、交互作用項を自動的に解釈します。
- 📦 **ダミー変数の作成**: カテゴリカル変数をダミー/指標変数に素早く変換します。
- 📈 **回帰分析**: 対数、べき乗、交互作用項をサポートする複数の線形回帰を実行し、整形された結果テーブルをエクスポートします。
- 📄 **Excel フッター注釈**: Excel ファイルに自動的に注釈を追加します。
- 🌐 **多言語対応**: 日本語、英語、中国語で変数を指定でき、入力キーに応じて自動的に言語を検出し、一貫した形式で結果を出力します。

![](https://raw.githubusercontent.com/qingruikz/regmonkey/main/assets/example.png)

## インストール

```bash
pip install regmonkey
```

## 関数

### `add_footer(file_path, value, sheet_name=None)`

Excel シートの最終行に注釈を追加します。

**引数**:

- `file_path` (str): Excel ファイルのパス。
- `value` (str): 注釈の内容。
- `sheet_name` (str, オプション): 修正するシートの名前。デフォルトは最初のシート。

**使用例**:

```python
from regmonkey.stats import add_footer

add_footer("example.xlsx", "注: データは暫定版です。", sheet_name="Sheet1")
```

---

### `get_dummies(df, columns)`

カテゴリカル変数をダミー/指標変数に変換します。

**引数**:

- `df` (DataFrame): 入力 DataFrame。
- `columns` (str のリスト): 変換する列名のリスト。

**戻り値**:

- ダミー変数を含む新しい DataFrame。

**使用例**:

```python
from regmonkey.stats import get_dummies
import pandas as pd

data = pd.DataFrame({"Year": ["2020", "2021", "2022"], "Value": [10, 20, 30]})
dummies = get_dummies(data, columns=["Year"])
print(dummies)
```

---

### `summary(df, var_list)`

変数リストの記述統計量を生成します。

**引数**:

- `df` (DataFrame): 入力 DataFrame。
- `var_list` (str のリスト): 要約する変数名のリスト。

**戻り値**:

- 記述統計量を含む DataFrame。

**使用例**:

```python
from regmonkey.stats import summary
import pandas as pd

data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
stats = summary(data, ["A", "B"])
print(stats)
```

---

### `regression(variables_dicts, df, decimal_places=2)`

対数、べき乗、交互作用項をサポートする回帰分析を実行します。

**引数**:

- `variables_dicts` (dict のリスト): 被説明変数と説明変数を指定する辞書のリスト。
  - **多言語対応**: 変数に異なる言語のキーを使用できます：
    - 日本語: `{"被説明変数": "Y", "説明変数": ["X1", "X2"]}`
    - 英語: `{"y": "Y", "X": ["X1", "X2"]}`
    - 中国語: `{"被解释变量": "Y", "解释变量": ["X1", "X2"]}`
  - **対数項**: `X1`の自然対数には`log(X1)`を使用。
  - **べき乗項**: `X2`の 2 乗や 3 乗には`X2**2`や`X2**3`を使用。
  - **ダミー変数**: 2 値変数の場合は直接使用（例：`['性別']`）。カテゴリカル変数の場合は`get_dummies`で前処理（例：`['調査年_1990', '調査年_1995']`）。
  - **交互作用項**: `X1`と`X2`の交互作用には`X1:X2`を使用。変換を組み合わせることも可能（例：`X1**2:log(X2)`）。
- `df` (DataFrame): 入力データ。
- `decimal_places` (int): 結果の小数点以下の桁数。

**戻り値**:

- 以下の要素を含むタプル：
  1. 処理済み DataFrame。
  2. 使用変数の記述統計量。
  3. 回帰結果テーブル。

**使用例**:

```python
from regmonkey.stats import regression
import pandas as pd

# サンプルデータ
data = pd.DataFrame({
    "X1": [1, 2, 3],
    "X2": [4, 5, 6],
    "Y": [7, 8, 9],
    "Category": ["A", "B", "A"]
})

# カテゴリカル変数の前処理
data_with_dummies = pd.get_dummies(data, columns=["Category"])

# 回帰変数の定義（日本語）
variables_ja = [
    {"被説明変数": "Y", "説明変数": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 回帰変数の定義（英語）
variables_en = [
    {"y": "Y", "X": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 回帰変数の定義（中国語）
variables_zh = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# 回帰分析の実行（上記の変数定義のいずれかを使用）
df_processed, summary_result, regression_result = regression(variables_ja, data_with_dummies)

# 結果の表示
print(regression_result)
```

この例では：

- 回帰はサポートされている言語（日本語、英語、中国語）のいずれかで指定できます。
- `log(X1)`は`X1`の自然対数を計算します。
- `X2**2`は`X2`の 2 乗を計算します。
- `X1:X2`は`X1`と`X2`の交互作用を計算します。
- `Category`のダミー変数は`get_dummies`で自動的に作成されます。
- 出力ラベル（例：「観測数」/「N」/「样本数」）は入力キーの言語に自動的に合わせられます。

---

## 使用例

```python
import pandas as pd
from regmonkey.stats import get_dummies, regression, add_footer

# データの読み込み
data = pd.DataFrame({
    "X1": [1, 2, 3],
    "X2": [4, 5, 6],
    "Y": [7, 8, 9],
    "Category": ["A", "B", "A"]
})

# ダミー変数の作成
data_with_dummies = get_dummies(data, columns=["Category"])

# 対数、べき乗、交互作用項を含む回帰分析の実行（英語のキーを使用）
variables = [
    {"y": "Y", "X": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]
df_processed, summary_result, regression_result = regression(variables, data_with_dummies)

# 回帰結果をExcelに保存し、注釈を追加
regression_result.to_excel("regression_results.xlsx", index=False)
add_footer("regression_results.xlsx", "注: 回帰結果には対数、べき乗、交互作用項が含まれています。")

# 記述統計量をExcelに保存し、注釈を追加
summary_result.to_excel("summary_statistics.xlsx", index=False)
add_footer("summary_statistics.xlsx", "注: 回帰分析で使用したすべての変数の記述統計量。")
```
