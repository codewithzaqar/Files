import os
import time

def clear_screen():
    print("\033[H\033[J", end="")

def format_size(size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

class COLOR:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    RESET = '\033[0m'

def color_text(text, color):
    """Apply color to text"""
    return f"{color}{text}{COLOR.RESET}"

def show_progress(src, dst, total_size, start_time, final=False):
    """Show progress for file operations"""
    if final:
        elapsed = time.time() - start_time
        speed = total_size / elapsed if elapsed > 0 else 0
        print(f"\rCompleted in {elapsed:.2f}s ({format_size(speed)}/s)", end='')
    else:
        # For simplicity, we'll just show completion for now
        pass