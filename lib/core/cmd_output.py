from tabulate import tabulate

def outputTable(table):
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def get_yellow_font(text):
    return f"\033[01;33m{text}\033[0m"

def get_green_font(text):
    return f"\033[32m{text}\033[0m"

def get_link_text(text):
    return f"\033]8;;{text}\033\\{get_green_font('[')}{get_yellow_font(text)}\033]8;;\033\\{get_green_font(']')}"