
def validate_number(_, value):
    try:
        # 尝试将输入值转换为整数
        int(value)
        return True
    except ValueError:
        return False