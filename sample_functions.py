"""テスト自動化ツール用のサンプル関数"""

import datetime
import uuid


def get_datetime(format_str: str = "%Y-%m-%d %H:%M:%S", timezone: str = "UTC", _replace_variables=None, **kwargs):
    """
    現在の日付時間を指定フォーマットで返す関数
    
    Args:
        format_str: 日時フォーマット文字列（Python strftime形式）
                   デフォルト: "%Y-%m-%d %H:%M:%S"
                   例: "%Y/%m/%d", "%Y%m%d_%H%M%S", "%Y-W%W"
        timezone: タイムゾーン指定（現在はUTCのみ対応）
        _replace_variables: 変数置換関数（自動渡される）
        **kwargs: その他の引数
        
    Returns:
        フォーマットされた日時文字列
    """
    try:
        # 現在時刻を取得
        now = datetime.datetime.utcnow() if timezone == "UTC" else datetime.datetime.now()
        result = now.strftime(format_str)
        
        print(f"    日時を生成しました (format={format_str}, result={result})")
        return result
    
    except Exception as e:
        raise Exception(f"日時生成エラー: {e}")


def generate_uuid(version: int = 4, _replace_variables=None, **kwargs):
    """
    UUIDを生成する関数
    
    Args:
        version: UUID バージョン指定
                - 4: ランダムUUID（デフォルト）
                - その他のバージョンは拡張可能
        _replace_variables: 変数置換関数（自動渡される）
        **kwargs: その他の引数
        
    Returns:
        生成されたUUID文字列
    """
    try:
        if version == 4:
            result = str(uuid.uuid4())
        else:
            raise ValueError(f"UUID version {version} は未サポート")
        
        print(f"    UUIDを生成しました (version={version}, uuid={result})")
        return result
    
    except Exception as e:
        raise Exception(f"UUID生成エラー: {e}")


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

