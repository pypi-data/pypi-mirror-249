msgDic = {
    1000: "词法错误",
    1001: "语法错误",
    1002: "语义错误",
    2000: "输入语言错误",
    3000: "编译成功",
    4000: "参数错误",
    5000: "模拟成功",
    6000: "模拟失败",
    7000: "isq核错误",
    404: "编译失败",
    9999: "编译器内部错误"
}

class isq_env:
    
    __env_dict = {
        'jax': False,
        'torch': False,
        'aws': False,
        'qcis': False,
        'scq': False,
    }

    @staticmethod
    def set_env(key, val):
        isq_env.__env_dict[key] = val
    @staticmethod
    def get_env(key):
        return isq_env.__env_dict[key]
