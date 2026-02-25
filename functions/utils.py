"""テスト自動化ツール用のサンプル関数"""

import datetime
import time
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


def wait(seconds: float = None, milliseconds: float = None, _replace_variables=None, **kwargs):
    """
    指定時間だけ待機する関数
    
    Args:
        seconds: 待機時間（秒）
                デフォルト: None
        milliseconds: 待機時間（ミリ秒）
                     デフォルト: None
                     注: secondsとmillisecondsの両方を指定した場合、両者の合計で待機
        _replace_variables: 変数置換関数（自動渡される）
        **kwargs: その他の引数
        
    Returns:
        処理結果メッセージ
        
    Raises:
        Exception: seconds/milliseconds未指定、または無効な値の場合
    """
    try:
        # 待機時間の計算
        wait_time = 0
        
        if seconds is not None:
            wait_time += float(seconds)
        
        if milliseconds is not None:
            wait_time += float(milliseconds) / 1000
        
        # どちらも指定されていない場合はエラー
        if wait_time == 0:
            raise ValueError("secondsまたはmillisecondsを指定してください")
        
        # 負の値はエラー
        if wait_time < 0:
            raise ValueError("待機時間は0以上である必要があります")
        
        # 待機を実行
        print(f"    {wait_time}秒待機します...")
        time.sleep(wait_time)
        
        print(f"    待機完了しました (wait_time={wait_time}秒)")
        return f"wait completed: {wait_time}秒"
    
    except Exception as e:
        raise Exception(f"待機エラー: {e}")


def print_message(message: str, _replace_variables=None, **kwargs):
    """
    指定した文字列をコンソールに出力する関数
    
    Args:
        message: 出力するメッセージ（${variable}での置換可能）
        _replace_variables: 変数置換関数（自動渡される）
        **kwargs: その他の引数
        
    Returns:
        処理結果メッセージ
    """
    try:
        # message に含まれる変数を置換
        if _replace_variables and isinstance(message, str):
            message = _replace_variables(message)
        
        # メッセージを出力
        print(f"    {message}")
        
        return f"print_message completed: {message}"
    
    except Exception as e:
        raise Exception(f"メッセージ出力エラー: {e}")

