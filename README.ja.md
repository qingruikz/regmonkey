# regmonkey

[English](README.md) | [日本語](README.ja.md) | [中文](README.zh.md)

**regmonkey** は、データ分析と回帰モデリングのタスクを効率化するための軽量な Python パッケージです。記述統計、ダミー変数の作成、回帰モデルの推定、注釈付き Excel ファイルのエクスポートなどのタスクを簡素化します。

## 機能

- 📊 **記述統計**：DataFrame からクリーンで丸められた要約統計を簡単に生成。
- 🧠 **スマート変数解析**：対数変換、多項式項、交互作用項を自動的に解釈。
- 📦 **ダミー変数作成**：カテゴリカル変数をダミー/指標変数に素早く変換。
- 📈 **回帰分析**：対数、べき乗、交互作用項をサポートする複数の線形回帰を実行し、フォーマットされた結果表をエクスポート。
- 📄 **Excel フッター注釈**：Excel ファイルに自動的に脚注を追加。
- 🌐 **多言語サポート**：サポートされている言語（英語、日本語、中国語）で変数を指定し、`lang` パラメータを使用して出力言語を独立して制御し、すべての結果で一貫したフォーマットを維持。

![](https://raw.githubusercontent.com/qingruikz/regmonkey/main/assets/example.png)

## インストール

```bash
pip install regmonkey
```

## 関数

### `add_footer(file_path, value, sheet_name=None)`

Excel シートの最後の行に脚注を追加します。

**引数**：

- `file_path` (str)：Excel ファイルのパス。
- `value` (str)：脚注の内容。
- `sheet_name` (str, オプション)：修正するシート名。デフォルトは最初のシート。

**例**：

```python
from regmonkey.stats import add_footer

add_footer("example.xlsx", "注：データは暫定値です。", sheet_name="Sheet1")
```

---

### `get_dummies(df, columns)`

カテゴリカル変数をダミー/指標変数に変換します。

**引数**：

- `df` (DataFrame)：入力 DataFrame。
- `columns` (str のリスト)：変換する列名のリスト。

**戻り値**：

- ダミー変数を含む新しい DataFrame。

**例**：

```python
from regmonkey.stats import get_dummies
import pandas as pd

data = pd.DataFrame({"Year": ["2020", "2021", "2022"], "Value": [10, 20, 30]})
dummies = get_dummies(data, columns=["Year"])
print(dummies)
```

---

### `summary(df, var_list, round_digits=2, lang="ja")`

指定された変数の記述統計量を計算します。

- `df`：データを含む DataFrame
- `var_list`：変数名のリスト
- `round_digits`：小数点以下の桁数（デフォルト：2）
- `lang`：出力ラベルの言語コード（"ja"、"en"、"zh"）（デフォルト："ja"）

**注意**：デフォルト（`lang` が指定されていない場合）では、出力は日本語になります。

以下の統計量を含む DataFrame を返します：

- 観測数
- 平均値
- 標準偏差
- 最小値
- 最大値

例：

```python
# デフォルト（日本語ラベル）
summary_stats = summary(df, ["X1", "X2"])

# 英語ラベル
summary_stats = summary(df, ["X1", "X2"], lang="en")

# 日本語ラベル
summary_stats = summary(df, ["X1", "X2"], lang="ja")

# 中国語ラベル
summary_stats = summary(df, ["X1", "X2"], lang="zh")
```

---

### `regress(variables_dicts, df, decimal_places=2, lang="ja", cov_type="HC1", dynamic_format=True)`

対数、べき乗、交互作用項をサポートする回帰分析を実行します。

**引数**：

- `variables_dicts` (辞書のリスト)：従属変数と独立変数を指定する辞書のリスト。
  - **多言語サポート**：異なる言語の変数キーを使用できます：
    - 日本語：`{"被説明変数": "Y", "説明変数": ["X1", "X2"]}`
    - 英語：`{"y": "Y", "X": ["X1", "X2"]}`
    - 中国語：`{"被解释变量": "Y", "解释变量": ["X1", "X2"]}`
  - **対数項**：`X1` の自然対数には `log(X1)` を使用。
  - **べき乗項**：2 乗または 3 乗項には `X2**2` または `X2**3` を使用。
  - **ダミー変数**：二値変数の場合は直接使用（例：`['Gender']`）。カテゴリカル変数の場合は、`get_dummies` で DataFrame を前処理（例：`['Year_1990', 'Year_1995']`）。
  - **交互作用項**：`X1` と `X2` の交互作用には `X1:X2` を使用、または `X1**2:log(X2)` のような変換を組み合わせる。
- `df` (DataFrame)：入力データ。
- `decimal_places` (int)：結果の小数点以下の桁数。
- `lang` (str)：出力ラベルの言語コード（"ja"、"en"、"zh"）（デフォルト："ja"）
- `cov_type` (str)：標準誤差の計算方法（デフォルト："HC1"）
  - "HC1"：ホワイトの標準誤差（小標本補正付き）
  - "HC0"：ホワイトの標準誤差
  - "HC2"：マックイナンの標準誤差
  - "HC3"：デビッドソン・マックキノンの標準誤差
  - "nonrobust"：通常の標準誤差
- `dynamic_format` (bool)：`True` の場合、有効数字を保持するために小数点以下の桁数を動的に調整します（デフォルト：`True`）。変数のスケールが大きく異なる場合に有用です。例：`decimal_places=2` のとき、係数 0.000234 は "0.00" ではなく "0.00023" と表示されます。固定小数桁数にしたい場合は `False` に設定します。

**注意**：デフォルト（`lang` が指定されていない場合）では、出力は日本語になります。

**戻り値**：

- 以下の内容を含むタプル：
  1. 処理済みの DataFrame。
  2. 使用した変数の記述統計量。
  3. 回帰結果表。

**例**：

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

# デフォルト出力で回帰を実行（日本語）
df_processed, summary_result, regression_result = regress(variables_ja, data_with_dummies)

# 日本語出力で回帰を実行
df_processed, summary_result, regression_result = regress(variables_ja, data_with_dummies, lang="ja")

# 英語出力で回帰を実行
df_processed, summary_result, regression_result = regress(variables_en, data_with_dummies, lang="en")

# 中国語出力で回帰を実行
df_processed, summary_result, regression_result = regress(variables_zh, data_with_dummies, lang="zh")

# 固定小数桁数で回帰を実行（動的フォーマットを無効化）
df_processed, summary_result, regression_result = regress(variables_ja, data_with_dummies, dynamic_format=False)

# 結果を表示
print(regression_result)
```

---

### `interpret_result(df_result, lang="ja")`

推定結果を解釈し、人間が読みやすいテキスト形式の説明を生成します。

**引数**：

- `df_result` (DataFrame)：`regress`関数から返される回帰結果テーブル
- `lang` (str, オプション)：出力テキストの言語コード（"ja"、"en"、"zh"）（デフォルト："ja"）

**戻り値**：

- 回帰結果の解釈を含む文字列。以下の内容を含みます：
  - モデルの説明（被説明変数を説明変数に回帰）
  - 各変数の係数の推定値と有意水準
  - 各モデルの自由度修正済み決定係数

**注意**：デフォルト（`lang` が指定されていない場合）では、出力は日本語になります。

**例**：

```python
from regmonkey.stats import regress, interpret_result
import pandas as pd

# サンプルデータ
data = pd.DataFrame({
    "X1": [1, 2, 3, 4, 5],
    "X2": [2, 3, 4, 5, 6],
    "Y": [3, 5, 7, 9, 11]
})

# 回帰を実行
variables = [
    {"被説明変数": "Y", "説明変数": ["X1", "X2"]}
]
df_processed, summary_result, regression_result = regress(variables, data, lang="ja")

# 結果を解釈
interpretation = interpret_result(regression_result, lang="ja")
print(interpretation)
```

出力は日本語（デフォルト）になります：

```
モデル（1）ではYをX1、X2に回帰した。
X1の係数の推定値は1.00となり、10％の有意水準でも有意に推定されていない。
X2の係数の推定値は1.00となり、10％の有意水準でも有意に推定されていない。
モデル（1）の自由度修正済み決定係数は0.50である。
```

英語出力の場合：

```python
interpretation = interpret_result(regression_result, lang="en")
print(interpretation)
```

中国語出力の場合：

```python
interpretation = interpret_result(regression_result, lang="zh")
print(interpretation)
```

---

## 使用例

```python
import pandas as pd
from regmonkey.stats import get_dummies, regress, interpret_result, add_footer

# データの読み込み
data = pd.DataFrame({
    "X1": [1, 2, 3, 4, 5],
    "X2": [2, 3, 4, 5, 6],
    "Y": [3, 5, 7, 9, 11],
    "Category": ["A", "B", "A", "B", "A"]
})

# ダミー変数の作成
data_with_dummies = get_dummies(data, columns=["Category"])

# 回帰分析を実行
variables = [
    {"被説明変数": "Y", "説明変数": ["X1", "X2"]},
    {"被説明変数": "Y", "説明変数": ["X1", "X2", "log(X1)", "X2**2"]}
]
df_processed, summary_result, regression_result = regress(variables, data_with_dummies, lang="ja")

# 推定結果を解釈
interpretation = interpret_result(regression_result, lang="ja")
print(interpretation)

# 回帰結果を Excel に保存し、脚注を追加
regression_result.to_excel("regression_results.xlsx", index=True)
add_footer("regression_results.xlsx", "注：回帰結果には対数、べき乗、交互作用項が含まれています。標準誤差は括弧内に表示されています。")

# 要約統計量を Excel に保存し、脚注を追加
summary_result.to_excel("summary_statistics.xlsx", index=True)
add_footer("summary_statistics.xlsx", "注：回帰分析で使用したすべての変数の要約統計量。")

# 解釈結果をテキストファイルに保存
with open("interpretation.txt", "w", encoding="utf-8") as f:
    f.write(interpretation)
```

より詳細な使用例については、`examples` フォルダにある `example.py` を参照してください。
