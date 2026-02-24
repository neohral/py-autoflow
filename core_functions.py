def load_template(executor, file_path: str, _replace_variables=None, **kwargs):
    """
    ファイルを読み込んで変数置換する
    YAML内で関数の引数として指定可能な関数
    
    Args:
        executor: TestExecutorインスタンス
        file_path: 読み込むファイルのパス（相対パス）
        _replace_variables: 変数置換関数（TestExecutorから自動渡される）
        **kwargs: その他の引数
        
    Returns:
        変数置換後のファイル内容
    """
    print(f"    テンプレートファイルを読み込みました (file_path={file_path})")
    return executor.load_file(file_path)