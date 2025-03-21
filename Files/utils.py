import os
import time
import sys

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
    """Show progress with percentage for file operations"""
    if final:
        elapsed = time.time() - start_time
        speed = total_size / elapsed if elapsed > 0 else 0
        print(f"\r100% - Completed in {elapsed:.2f}s ({format_size(speed)}/s)", end='')
    else:
        # Simulate progress for directories (not real-time due to shutil limitations)
        elapsed = time.time() - start_time
        if elapsed > 0:
            processed = os.path.getsize(src) if os.path.isfile(src) else 0  # Simplified for demo
            percent = min(100, int((processed / total_size) * 100) if total_size > 0 else 0)
            print(f"\r{percent}% - Processing...", end='', flush=True)