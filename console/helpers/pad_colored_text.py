import re

def pad_colored_text(text, width):
    # Remove ANSI escape sequences using a regex
    visible_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
    # Calculate padding and center the text
    padding = width - len(visible_text)
    left_padding = padding // 2
    right_padding = padding - left_padding
    return " " * left_padding + text + " " * right_padding