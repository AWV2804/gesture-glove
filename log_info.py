import inspect
import os

def log_info(*messages):
    stack = inspect.stack()
    if len(stack) > 2:
        caller_frame = stack[2]
        file_path = caller_frame.filename
        line_number = caller_frame.lineno
        file_name = os.path.basename(file_path)
        # ANSI escape code for green text
        green_file_name = f"\033[92m{file_name}\033[0m"
        print(f"[{green_file_name}:{line_number}]", *messages)
    else:
        print(*messages)