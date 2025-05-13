# regmonkey

[English](README.md) | [日本語](README.ja.md) | [中文](README.zh.md)

**regmonkey** is a lightweight Python package designed to streamline data analysis and regression modeling tasks. It simplifies tasks like descriptive statistics, dummy variable creation, regression model estimation, and exporting annotated Excel files.

## Features

- 📊 **Descriptive Statistics**: Easily generate clean and rounded summary statistics from a DataFrame.
- 🧠 **Smart Variable Parsing**: Automatically interpret log transformations, polynomial terms, and interaction terms.
- 📦 **Dummy Variable Creation**: Quickly convert categorical variables into dummy/indicator variables.
- 📈 **Regression Analysis**: Run multiple linear regressions with support for log, power, and interaction terms, and export well-formatted result tables.
- 📄 **Excel Footer Annotation**: Add footnotes to Excel files automatically.
- 🌐 **Multilingual Support**: Specify variables and get results in English, Japanese, or Chinese, with automatic language detection and consistent output formatting.

## Installation

```bash
pip install regmonkey
```

## Functions

### `add_footer(file_path, value, sheet_name=None)`

Adds a footer note to the last row of an Excel sheet.

**Arguments**:

- `file_path` (str): Path to the Excel file.
- `value` (str): The content of the footer note.
- `sheet_name` (str, optional): Name of the sheet to modify. Defaults to the first sheet.

**Example**:

```python
from regmonkey.stats import add_footer

add_footer("example.xlsx", "Note: Data is preliminary.", sheet_name="Sheet1")
```

---

### `get_dummies(df, columns)`

Converts categorical variables into dummy/indicator variables.

**Arguments**:

- `df` (DataFrame): The input DataFrame.
- `columns` (list of str): List of column names to convert.

**Returns**:

- A new DataFrame with dummy variables.

**Example**:

```python
from regmonkey.stats import get_dummies
import pandas as pd

data = pd.DataFrame({"Year": ["2020", "2021", "2022"], "Value": [10, 20, 30]})
dummies = get_dummies(data, columns=["Year"])
print(dummies)
```

---

### `summary(df, var_list)`

Generates descriptive statistics for a list of variables.

**Arguments**:

- `df` (DataFrame): The input DataFrame.
- `var_list` (list of str): List of variable names to summarize.

**Returns**:

- A DataFrame containing descriptive statistics.

**Example**:

```python
from regmonkey.stats import summary
import pandas as pd

data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
stats = summary(data, ["A", "B"])
print(stats)
```

---

### `regression(variables_dicts, df, decimal_places=2)`

Performs regression analysis with support for log, power, and interaction terms.

**Arguments**:

- `variables_dicts` (list of dict): List of dictionaries specifying dependent and independent variables.
  - **Multilingual Support**: You can use different language keys for variables:
    - Japanese: `{"被説明変数": "Y", "説明変数": ["X1", "X2"]}`
    - English: `{"y": "Y", "X": ["X1", "X2"]}`
    - Chinese: `{"被解释变量": "Y", "解释变量": ["X1", "X2"]}`
  - **Log terms**: Use `log(X1)` for the natural logarithm of `X1`.
  - **Power terms**: Use `X2**2` or `X2**3` for squared or cubed terms.
  - **Dummy variables**: For binary variables, use them directly (e.g., `['Gender']`). For categorical variables, preprocess the DataFrame using `get_dummies` (e.g., `['Year_1990', 'Year_1995']`).
  - **Interaction terms**: Use `X1:X2` for the interaction between `X1` and `X2`, or combine transformations like `X1**2:log(X2)`.
- `df` (DataFrame): The input data.
- `decimal_places` (int): Number of decimal places for results.

**Returns**:

- A tuple containing:
  1. Processed DataFrame.
  2. Descriptive statistics for used variables.
  3. Regression results table.

**Example**:

```python
from regmonkey.stats import regression
import pandas as pd

# Sample data
data = pd.DataFrame({
    "X1": [1, 2, 3],
    "X2": [4, 5, 6],
    "Y": [7, 8, 9],
    "Category": ["A", "B", "A"]
})

# Preprocess categorical variables
data_with_dummies = pd.get_dummies(data, columns=["Category"])

# Define regression variables (Japanese)
variables_ja = [
    {"被説明変数": "Y", "説明変数": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# Define regression variables (English)
variables_en = [
    {"y": "Y", "X": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# Define regression variables (Chinese)
variables_zh = [
    {"被解释变量": "Y", "解释变量": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]

# Perform regression (using any of the above variable definitions)
df_processed, summary_result, regression_result = regression(variables_ja, data_with_dummies)

# Print results
print(regression_result)
```

In this example:

- The regression can be specified using any of the supported languages (Japanese, English, or Chinese).
- `log(X1)` computes the natural logarithm of `X1`.
- `X2**2` computes the square of `X2`.
- `X1:X2` computes the interaction between `X1` and `X2`.
- Dummy variables for `Category` are automatically created using `get_dummies`.
- The output labels (e.g., "観測数"/"N"/"样本数") will automatically match the language of the input keys.

---

## Usage Example

```python
import pandas as pd
from regmonkey.stats import get_dummies, regression, add_footer

# Load data
data = pd.DataFrame({
    "X1": [1, 2, 3],
    "X2": [4, 5, 6],
    "Y": [7, 8, 9],
    "Category": ["A", "B", "A"]
})

# Create dummy variables
data_with_dummies = get_dummies(data, columns=["Category"])

# Perform regression with log, power, and interaction terms (using English keys)
variables = [
    {"y": "Y", "X": ["X1", "X2", "log(X1)", "X2**2", "X1:X2"]}
]
df_processed, summary_result, regression_result = regression(variables, data_with_dummies)

# Save regression results to Excel and add a footer
regression_result.to_excel("regression_results.xlsx", index=False)
add_footer("regression_results.xlsx", "Note: Regression results include log, power, and interaction terms.")

# Save summary statistics to Excel and add a footer
summary_result.to_excel("summary_statistics.xlsx", index=False)
add_footer("summary_statistics.xlsx", "Note: Summary statistics for all variables used in the regression analysis.")
```
