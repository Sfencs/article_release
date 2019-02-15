#__author:"sfencs"
#date:2018/11/25

import random

def random_code():
    """
    生成随机邮箱验证码
    :return:
    """
    code = ''
    for i in range(4):
        current = random.randrange(0,4)
        if current != i:
            temp = chr(random.randint(65,90))
        else:
            temp = random.randint(0,9)
        code += str(temp)
    return code


