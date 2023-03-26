import openai



Question_length = 1000   #每个问题最大tokens数量
total_tokens_last = 0  #上一次的总tokens
messages=[]    #消息列表
tokens_list=[]    #记录消息列表数量



#设置颜色
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
reset = "\033[0m"


#函数set_allow_tokens设置Allow_tokens
Allow_tokens = 1000
def set_allow_tokens():
    def set_level_tokens(level_tokens):
        global  Allow_tokens
        Allow_tokens = level_tokens
    def switcher(key):
        func_dict = {
            "1": lambda: set_level_tokens(100),
            "2": lambda: set_level_tokens(500),
            "3": lambda: set_level_tokens(1000),
            "4": lambda: set_level_tokens(2000),
            "5": lambda: set_level_tokens(3000),
            "6": lambda: set_level_tokens(3500)
        }
        func = func_dict.get(key, None)
        if func is not None:
            func()
        else:
            print("无效的输入")
            return
    key = input("(1/2/3/4/5/6)：")
    switcher(key)
    return Allow_tokens
    
