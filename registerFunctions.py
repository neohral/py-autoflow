from functools import partial
from common.test_executor import TestExecutor
from common.core import load_template
from functions.utils import write_output, get_datetime, generate_uuid, print_message, wait

def register_default_functions(executor: TestExecutor):
    """
    デフォルトの関数をExecutorに登録する
    
    Args:
        executor: TestExecutor インスタンス
    """
    
    # core関数の登録
    executor.register_function('load_template', partial(load_template, executor=executor))
    
    # 追加関数の登録
    executor.register_function('write_output', write_output)
    executor.register_function('get_datetime', get_datetime)
    executor.register_function('generate_uuid', generate_uuid)
    executor.register_function('print_message', print_message)
    executor.register_function('wait', wait)