"""
regmonkey パッケージの使用例

このスクリプトは、regmonkeyパッケージの主要な機能を使用する例を示しています。
"""

import pandas as pd
import numpy as np
from regmonkey.stats import (
    get_dummies,
    regress,
    interpret_result,
    add_footer,
    summary,
)

# ============================================================================
# 1. データの準備
# ============================================================================

# サンプルデータの作成
np.random.seed(42)
n = 100

data = pd.DataFrame(
    {
        "総人口": np.random.randint(100000, 1000000, n),
        "一戸建住宅比率": np.random.uniform(0.3, 0.8, n),
        "県民所得": np.random.uniform(200, 500, n),
        "発電電力量": np.random.uniform(1000, 5000, n),
        "地域": np.random.choice(["A", "B", "C"], n),
        "年度": np.random.choice([2010, 2015, 2020], n),
    }
)

# ダミー変数の作成
data_with_dummies = get_dummies(data, columns=["地域", "年度"])

# ============================================================================
# 2. 記述統計量の計算
# ============================================================================

print("=" * 80)
print("記述統計量")
print("=" * 80)

var_list = ["総人口", "一戸建住宅比率", "県民所得", "発電電力量"]
summary_stats = summary(data, var_list, round_digits=2, lang="ja")
print(summary_stats)
print()

# ============================================================================
# 3. 回帰分析の実行
# ============================================================================

print("=" * 80)
print("回帰分析の実行")
print("=" * 80)

# 複数のモデルを定義
variables = [
    {"被説明変数": "発電電力量", "説明変数": ["総人口", "一戸建住宅比率"]},
    {"被説明変数": "発電電力量", "説明変数": ["総人口", "一戸建住宅比率", "県民所得"]},
    {
        "被説明変数": "発電電力量",
        "説明変数": ["総人口", "一戸建住宅比率", "県民所得", "総人口**2"],
    },
    {
        "被説明変数": "発電電力量",
        "説明変数": ["総人口", "一戸建住宅比率", "県民所得", "log(総人口)"],
    },
    {
        "被説明変数": "発電電力量",
        "説明変数": [
            "総人口",
            "一戸建住宅比率",
            "県民所得",
            "総人口**2",
            "総人口:県民所得",
        ],
    },
]

# 回帰分析を実行
df_processed, summary_result, regression_result = regress(
    variables, data_with_dummies, decimal_places=2, lang="ja", cov_type="HC1"
)

# 回帰結果を表示
print(regression_result)
print()

# ============================================================================
# 4. 推定結果の解釈
# ============================================================================

print("=" * 80)
print("推定結果の解釈")
print("=" * 80)

# 推定結果を解釈
interpretation = interpret_result(regression_result, lang="ja")
print(interpretation)
print()

# ============================================================================
# 5. 結果をExcelファイルに保存
# ============================================================================

print("=" * 80)
print("結果をExcelファイルに保存")
print("=" * 80)

# 回帰結果をExcelに保存
regression_result.to_excel("regression_results.xlsx", index=True)
add_footer(
    "regression_results.xlsx",
    "注：回帰結果には対数、べき乗、交互作用項が含まれています。標準誤差は括弧内に表示されています。",
)

# 記述統計量をExcelに保存
summary_result.to_excel("summary_statistics.xlsx", index=True)
add_footer(
    "summary_statistics.xlsx", "注：回帰分析で使用したすべての変数の記述統計量。"
)

# 解釈結果をテキストファイルに保存
with open("interpretation.txt", "w", encoding="utf-8") as f:
    f.write(interpretation)

print("以下のファイルが作成されました：")
print("  - regression_results.xlsx")
print("  - summary_statistics.xlsx")
print("  - interpretation.txt")
print()

# ============================================================================
# 6. 動的小数フォーマットの使用例
# ============================================================================

print("=" * 80)
print("固定小数桁数の使用例（動的フォーマットを無効化）")
print("=" * 80)

# dynamic_format=False を指定すると、固定の小数桁数で表示される
# デフォルトでは dynamic_format=True（有効数字を保持する動的フォーマット）
df_processed_dyn, summary_result_dyn, regression_result_dyn = regress(
    variables, data_with_dummies, decimal_places=2, lang="ja", dynamic_format=False
)

print(regression_result_dyn)
print()

# ============================================================================
# 7. 英語での使用例
# ============================================================================

print("=" * 80)
print("英語での使用例")
print("=" * 80)

# 英語キーを使用した回帰分析
variables_en = [{"y": "発電電力量", "X": ["総人口", "一戸建住宅比率", "県民所得"]}]

df_processed_en, summary_result_en, regression_result_en = regress(
    variables_en, data_with_dummies, decimal_places=2, lang="en", cov_type="HC1"
)

# 英語での解釈
interpretation_en = interpret_result(regression_result_en, lang="en")
print(interpretation_en)
print()

# ============================================================================
# 8. 中国語での使用例
# ============================================================================

print("=" * 80)
print("中国語での使用例")
print("=" * 80)

# 中国語キーを使用した回帰分析
variables_zh = [
    {"被解释变量": "発電電力量", "解释变量": ["総人口", "一戸建住宅比率", "県民所得"]}
]

df_processed_zh, summary_result_zh, regression_result_zh = regress(
    variables_zh, data_with_dummies, decimal_places=2, lang="zh", cov_type="HC1"
)

# 中国語での解釈
interpretation_zh = interpret_result(regression_result_zh, lang="zh")
print(interpretation_zh)
print()

print("=" * 80)
print("完了")
print("=" * 80)
