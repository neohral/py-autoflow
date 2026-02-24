#!/usr/bin/env python3
"""テスト自動化ツールの実行スクリプト"""

import sys
import os
from functools import partial
from test_executor import TestExecutor
from sample_functions import write_output, get_datetime, generate_uuid
from core_functions import load_template


def run_test_case(yaml_file: str, case_name: str):
    """
    テストケースを実行する
    
    Args:
        yaml_file: YAMLファイルのパス
        case_name: テストケース名
    """
    print(f"\n{'=' * 60}")
    print(f"テストケース: {case_name}")
    print(f"YAML: {yaml_file}")
    print('=' * 60)
    
    try:
        # TestExecutorを初期化
        executor = TestExecutor(yaml_file)
        
        # 関数を登録
        executor.register_function('write_output', write_output)
        executor.register_function('get_datetime', get_datetime)
        executor.register_function('generate_uuid', generate_uuid)
        
        # ファイル置換用の関数を登録（executorを束縛）
        executor.register_function('load_template', partial(load_template, executor=executor))
        
        # テストを実行
        executor.execute()
        
        # ファイル読み込みの結果を表示
        if 'report_content' in executor.variables:
            print(f"\n【{case_name}】のファイル読み込み結果 (report_content)")
            print('-' * 60)
            print(executor.variables['report_content'])
    
    except Exception as e:
        print(f"エラー: {e}")


def list_available_cases():
    """利用可能なテストケースを表示"""
    test_dir = 'tests'
    if not os.path.exists(test_dir):
        print(f"エラー: {test_dir} ディレクトリが見つかりません")
        return []
    
    cases = []
    for item in sorted(os.listdir(test_dir)):
        item_path = os.path.join(test_dir, item)
        if os.path.isdir(item_path):
            config_file = os.path.join(item_path, 'config.yaml')
            if os.path.exists(config_file):
                cases.append(item)
    
    return cases


def print_usage():
    """使用方法を表示"""
    available_cases = list_available_cases()
    
    print("使用方法: python3 run_test_suite.py [テストケース名]")
    print()
    print("利用可能なテストケース:")
    for case in available_cases:
        print(f"  - {case}")
    print()
    print("例:")
    print("  python3 run_test_suite.py test_case_001    # test_case_001を実行")
    print("  python3 run_test_suite.py test_case_002    # test_case_002を実行")
    print("  python3 run_test_suite.py all              # すべてのテストケースを実行")
    print("  python3 run_test_suite.py                  # 使用方法を表示")


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    if len(sys.argv) < 2:
        print_usage()
        return
    
    test_case = sys.argv[1]
    available_cases = list_available_cases()
    
    if test_case == 'all':
        # すべてのテストケースを実行
        print("テスト自動化ツール - マルチケーステスト実行")
        for case in available_cases:
            yaml_file = f'tests/{case}/config.yaml'
            run_test_case(yaml_file, case)
        
        print(f"\n{'=' * 60}")
        print("すべてのテストケースが完了しました！")
        print('=' * 60)
    
    elif test_case in available_cases:
        # 指定されたテストケースを実行
        yaml_file = f'tests/{test_case}/config.yaml'
        run_test_case(yaml_file, test_case)
    
    else:
        # テストケースが見つからない
        print(f"エラー: テストケース '{test_case}' が見つかりません")
        print()
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
