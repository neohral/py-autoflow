"""テスト自動化ツール用のサンプル関数"""

def write_output(output_file: str, content: str, mode: str = 'w', _replace_variables=None, **kwargs):
    """
    引数の内容をファイルに出力する関数
    
    Args:
        output_file: 出力ファイルパス
        content: 出力する内容
        mode: ファイルモード ('w': 上書き, 'a': 追記) デフォルト: 'w'
        _replace_variables: 変数置換関数（content内の変数を置換）
        **kwargs: その他の引数
        
    Returns:
        処理結果メッセージ
    """
    # content に含まれる変数を置換
    if _replace_variables and isinstance(content, str):
        content = _replace_variables(content)
    
    try:
        # ファイルに書き込み
        with open(output_file, mode, encoding='utf-8') as f:
            f.write(content)
        
        mode_str = '上書き' if mode == 'w' else '追記'
        print(f"    ファイルに{mode_str}しました (file={output_file})")
        return f"write_output completed: {output_file} ({mode_str})"
    
    except Exception as e:
        raise Exception(f"ファイル出力エラー: {e}")

