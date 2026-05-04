
import sys


class CustomException(Exception):
    '''
    Enriches standard Python exceptions with the exact file and line
    number where the original error was raised. Pass the caught
    exception as `error_detail` so the traceback can be inspected.
    '''

    def __init__(self, message: str, error_detail: Exception = None):
        self.error_message = self._build_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def _build_message(message: str, error_detail: Exception) -> str:
        if error_detail is not None:
            # Walk to the innermost frame of the traceback
            tb = error_detail.__traceback__
            while tb and tb.tb_next:
                tb = tb.tb_next
            file_name   = tb.tb_frame.f_code.co_filename if tb else "Unknown"
            line_number = tb.tb_lineno if tb else "Unknown"
            error_msg   = str(error_detail)
        else:
            file_name, line_number, error_msg = "Unknown", "Unknown", "No underlying exception"

        return (
            f"{message} | "
            f"Error: {error_msg} | "
            f"File: {file_name} | "
            f"Line: {line_number}"
        )

    def __str__(self) -> str:
        return self.error_message
