
def validate_number(_, value):
    try:
        # 尝试将输入值转换为整数
        int(value)
        return True
    except ValueError:
        return False

def validate_input(value):
    if not value:
        raise inquirer.errors.ValidationError('', reason='该项为必填项')
    return True