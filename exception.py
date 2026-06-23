import sys
import traceback

def error_msg_details(error: Exception):
    _, _, exc_tb = sys.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in python script [{file_name}] "
        f"at line number [{line_number}] "
        f"with message [{str(error)}]"
    )
    return error_message
    
class CustomException(Exception):
    def __init__(self, error: Exception):
        super().__init__(str(error))
        self.error_message = error_msg_details(error)

    def __str__(self):
        return self.error_message