import inquirer

def validate_number(gt, lt=0):
    def v(answers, current):
        try:
            # 尝试将输入值转换为整数
            validate_input(answers, current)
            if lt >= int(current) or int(current) > gt:
                raise inquirer.errors.ValidationError("", reason="输入内容有误，请查证")
            int(current)
            return True
        except ValueError:
            raise inquirer.errors.ValidationError("", reason="请输入数字")
    return v


def validate_input(answers, current):
    if not current:
        raise inquirer.errors.ValidationError('', reason='该项为必填项')
    return True

def validate_exist(eg = None):
    def v(answers, current):
        try:
            # 尝试将输入值转换为整数
            validate_input(answers, current)
            if current not in eg:
                raise inquirer.errors.ValidationError("", reason="输入内容有误，请查证")
            int(current)
            return True
        except ValueError:
            raise inquirer.errors.ValidationError("", reason="请输入数字")
    return v