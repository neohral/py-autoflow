# Python テスト自動化ツール

YAML設定ファイルから関数を順番に実行するテスト自動化ツールです。

## 特徴

- ✅ YAMLファイルからテスト設定を読み込み
- ✅ 複数の関数を順番に実行
- ✅ グローバル変数の管理
- ✅ 引数での変数置換（`${variable_name}`形式）
- ✅ 実行結果を変数として保存可能
- ✅ 関数内から変数置換メソッドにアクセス可能

## インストール

```bash
pip install pyyaml
```

## ファイル構成

```
.
├── test_executor.py       # メインツール（YAML読み込み、関数実行エンジン）
├── core_functions.py      # コア機能（ファイル処理など）
├── sample_functions.py    # ユーザー定義関数
├── main.py                # 関数登録・実行スクリプト
├── README.md              # このファイル
└── tests/
    ├── test_case_001/
    │   ├── config.yaml
    │   └── report_template.txt
    └── test_case_002/
        ├── config.yaml
        └── log_template.txt
```

## 基本的な使用方法

### コマンド

```bash
# 特定のテストケースを実行
python3 main.py test_case_001

# すべてのテストケースを実行
python3 main.py all

# 使用方法を表示
python3 main.py
```

## 機能追加ガイド

**新しい関数をテストに追加する場合は、以下の手順を実行してください：**

### ステップ1：sample_functions.py に関数を定義

```python
def my_function(arg1: str, arg2: str = None, _replace_variables=None, **kwargs):
    """
    カスタム関数
    
    Args:
        arg1: 引数1
        arg2: 引数2
        _replace_variables: 変数置換関数（自動渡される）
        **kwargs: その他の引数
    """
    return f"result: {arg1}"
```

### ステップ2：main.py で関数を登録

```python
from sample_functions import my_function

executor.register_function('my_function', my_function)
```

### ステップ3：YAML で関数を使用

```yaml
- name: my_function
  arg1: value1
  arg2: ${some_variable}
  store_as: result
```

## 推奨パターン

### ファイルを読み込んで処理する関数の実装方法

ファイルを読み込んで加工・変換する必要がある場合は、以下のパターンを推奨します：

**理由：** 
- ファイル処理と変数置換を分離できる
- YAML設定でテンプレートとロジックを分けやすい
- 再利用性が高い

**推奨パターン：**

1. **load_template を使ってファイル読み込み**  
   テンプレートファイルを読み込んで変数置換を実行

2. **カスタム関数で処理**  
   読み込んだ内容を加工・変換

```python
# sample_functions.py での実装例
def process_template(file_path: str, _replace_variables=None, **kwargs):
    """
    テンプレートファイルを読み込んで処理する関数
    
    推奨：直接ファイルを読むのではなく、
    load_templateを経由して変数置換済みの内容を取得
    """
    # この関数では処理ロジックに専念
    # ファイル読み込みはcore.py内のload_templateに任せる

    return processed_result
```

**YAML での使用例：**

```yaml
process:
  steps:
    # ステップ1: テンプレートファイルを読み込み＆変数置換
    - name: load_template
      file_path: template.txt
      store_as: template_content
    
    # ステップ2: 読み込んだ内容を処理
    - name: process_template
      content: ${template_content}
      store_as: final_result
    
    # ステップ3: 結果をファイルに出力
    - name: write_output
      output_file: output.txt
      content: ${final_result}
      mode: w
```

このパターンにより、各関数の責務が明確になり、テストの保守性が向上します。

## YAML設定の詳細

### variables（変数定義）

```yaml
variables:
  varA: 1234
  name: TestUser
```

### process.steps（ステップ定義）

```yaml
process:
  steps:
    - name: function_name
      param1: value1
      param2: ${variable}
      store_as: result_var
```

## 関数のシグネチャ

```python
def my_function(
    param1: str,
    param2: str = None,
    _replace_variables=None,
    **kwargs
):
    return result
```

パラメータ説明：
- `_replace_variables`: テスト実行エンジンから自動的に渡される変数置換関数
- `**kwargs`: `store_as` などのメタデータが含まれる
