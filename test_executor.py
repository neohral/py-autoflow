import yaml
import re
import os
from pathlib import Path
from typing import Any, Callable, Dict, List


class TestExecutor:
    """YAMLファイルから関数を順番に実行するテスト自動化ツール"""
    
    def __init__(self, yaml_file: str):
        """
        Args:
            yaml_file: YAMLファイルのパス
        """
        self.yaml_file = yaml_file
        # YAMLファイルが置かれたディレクトリを取得
        self.yaml_dir = os.path.dirname(os.path.abspath(yaml_file))
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
        self.config = self._load_yaml()
    
    def _load_yaml(self) -> Dict[str, Any]:
        """YAMLファイルを読み込む"""
        with open(self.yaml_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    
    def register_function(self, name: str, func: Callable) -> None:
        """
        関数を登録する
        
        Args:
            name: 関数の名前
            func: 実行する関数オブジェクト
        """
        self.functions[name] = func
    
    def _replace_variables(self, value: Any) -> Any:
        """
        値に含まれる変数プレースホルダー（${variable_name}形式）を置換する
        
        Args:
            value: 置換対象の値
            
        Returns:
            置換後の値
        """
        if isinstance(value, str):
            # ${variable_name} の形式で置換
            def replacer(match):
                var_name = match.group(1)
                if var_name in self.variables:
                    return str(self.variables[var_name])
                else:
                    raise ValueError(f"変数 '{var_name}' が定義されていません")
            
            return re.sub(r'\$\{(\w+)\}', replacer, value)
        elif isinstance(value, dict):
            return {k: self._replace_variables(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._replace_variables(v) for v in value]
        else:
            return value
    
    def _load_variables(self) -> None:
        """YAMLファイルから変数を読み込む"""
        if 'variables' in self.config:
            self.variables = self.config['variables'].copy()
    
    def load_file(self, file_path: str) -> str:
        """
        ファイルを読み込んで変数置換を行う
        YAMLファイルが置かれたディレクトリを基準として相対パスを解決
        
        Args:
            file_path: 読み込むファイルのパス（相対パスまたは絶対パス）
            
        Returns:
            変数置換後のファイル内容
        """
        # 相対パスの場合、YAMLファイルのディレクトリを基準とする
        full_path = file_path
        if not os.path.isabs(file_path):
            full_path = os.path.join(self.yaml_dir, file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {full_path}")
        except Exception as e:
            raise Exception(f"ファイル読み込みエラー: {e}")
        
        # 変数置換を実行
        replaced_content = self._replace_variables(content)
        return replaced_content
    
    def _execute_step(self, step: Dict[str, Any]) -> Any:
        """
        ステップを実行する
        
        Args:
            step: ステップの定義
            
        Returns:
            関数の実行結果
        """
        step_name = step.get('name')
        if not step_name:
            raise ValueError("stepには'name'フィールドが必須です")
        
        if step_name not in self.functions:
            raise ValueError(f"関数 '{step_name}' が登録されていません")
        
        # 引数を取得して変数置換を行う
        args = {}
        for key, value in step.items():
            if key not in ['name', 'store_as']:  # メタデータを除外
                args[key] = self._replace_variables(value)
        
        # 関数に_replace_variablesメソッドを渡す
        args['_replace_variables'] = self._replace_variables
        
        # 関数を実行
        func = self.functions[step_name]
        result = func(**args)
        
        # 結果を変数に保存する場合
        if 'store_as' in step:
            var_name = step['store_as']
            self.variables[var_name] = result
            print(f"  結果を変数 '{var_name}' に保存しました: {result}")
        
        return result
    
    def execute(self) -> bool:
        """
        YAMLファイルの設定に従ってテストを実行する
        
        Returns:
            すべてのステップが成功した場合 True
        """
        try:
            # 変数を読み込む
            self._load_variables()
            print(f"変数を読み込みました: {self.variables}\n")
            
            # ステップを実行
            if 'process' in self.config and 'steps' in self.config['process']:
                steps = self.config['process']['steps']
                print(f"合計 {len(steps)} 個のステップを実行します\n")
                
                for i, step in enumerate(steps, 1):
                    step_name = step.get('name', 'unknown')
                    print(f"[ステップ {i}] {step_name} を実行中...")
                    
                    try:
                        result = self._execute_step(step)
                        print(f"  ✓ 完了 (結果: {result})\n")
                    except Exception as e:
                        print(f"  ✗ エラー: {e}\n")
                        return False
            
            print("すべてのステップが正常に完了しました！")
            print(f"最終的な変数の状態: {self.variables}")
            return True
        
        except Exception as e:
            print(f"エラー: {e}")
            return False
