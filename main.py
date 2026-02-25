#!/usr/bin/env python3
"""テスト自動化ツールの実行スクリプト"""

import sys
import os
import questionary
from common.test_executor import TestExecutor
from registerFunctions import register_default_functions

# 設定定数
TESTS_DIR = 'tests'
CONFIG_FILENAME = 'config.yaml'

def run_test_case(yaml_file: str, case_name: str) -> bool:
    """
    テストケースを実行する
    
    Args:
        yaml_file: YAMLファイルのパス
        case_name: テストケース名
        
    Returns:
        テスト成功時 True、失敗時 False
    """
    print(f"\n{'=' * 60}")
    print(f"テストケース: {case_name}")
    print(f"YAML: {yaml_file}")
    print('=' * 60)
    
    try:
        # TestExecutorを初期化
        executor = TestExecutor(yaml_file)
        
        # デフォルト関数を登録
        register_default_functions(executor)
        
        # テストを実行
        success = executor.execute()
        
        return success
    
    except Exception as e:
        print(f"エラー: {e}")
        return False


def list_available_cases():
    """利用可能なテストケースを表示"""
    if not os.path.exists(TESTS_DIR):
        print(f"エラー: {TESTS_DIR} ディレクトリが見つかりません")
        return []
    
    cases = []
    for item in sorted(os.listdir(TESTS_DIR)):
        item_path = os.path.join(TESTS_DIR, item)
        if os.path.isdir(item_path):
            config_file = os.path.join(item_path, CONFIG_FILENAME)
            if os.path.exists(config_file):
                cases.append(item)
    
    return cases

def main():
    """メイン処理"""
    # テストケースを取得（1回だけ）
    available_cases = list_available_cases()
    
    if not available_cases:
        print("エラー: 利用可能なテストケースが見つかりません")
        sys.exit(1)
    
    # コマンドライン引数を取得
    if len(sys.argv) < 2:
        # 引数がない場合は対話的に選択
        choices = available_cases + ['all', '--- キャンセル ---']
        
        print("テスト自動化ツール - テストケース選択")
        test_case = questionary.select(
            'テストケースを選択してください:',
            choices=choices
        ).ask()
        
        # キャンセルされた場合
        if test_case is None or test_case == '--- キャンセル ---':
            print("キャンセルしました")
            sys.exit(0)
    else:
        test_case = sys.argv[1]
    
    # テスト実行
    if test_case == 'all':
        # すべてのテストケースを実行
        print("テスト自動化ツール - マルチケーステスト実行")
        results = {}
        for case in available_cases:
            yaml_file = os.path.join(TESTS_DIR, case, CONFIG_FILENAME)
            results[case] = run_test_case(yaml_file, case)
        
        # 結果サマリー
        print(f"\n{'=' * 60}")
        print("テスト結果サマリー")
        print('=' * 60)
        passed = sum(1 for r in results.values() if r)
        failed = sum(1 for r in results.values() if not r)
        
        for case, success in results.items():
            status = "✓ 成功" if success else "✗ 失敗"
            print(f"  {case}: {status}")
        
        print(f"\n合計: {len(results)}件、成功: {passed}件、失敗: {failed}件")
        print('=' * 60)
        
        # いずれかが失敗した場合は終了コード1で終了
        sys.exit(0 if failed == 0 else 1)
    
    elif test_case in available_cases:
        # 指定されたテストケースを実行
        yaml_file = os.path.join(TESTS_DIR, test_case, CONFIG_FILENAME)
        success = run_test_case(yaml_file, test_case)
        sys.exit(0 if success else 1)
    
    else:
        # テストケースが見つからない
        print(f"エラー: テストケース '{test_case}' が見つかりません")
        print(f"\n利用可能なテストケース:")
        for case in available_cases:
            print(f"  - {case}")
        sys.exit(1)


if __name__ == '__main__':
    main()
