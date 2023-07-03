from tabulate import tabulate

def outputTable(table):
    print(tabulate(table, headers="firstrow", tablefmt="grid"))