# Note: 您需要使用OpenAI Python v0.27.0才能使下面的代码正常工作
import openai
import sys
import prompt_toolkit


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



#设置颜色
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
reset = "\033[0m"


Question_length = 1000   #每个问题最大tokens数量
total_tokens_last = 0  #上一次的总tokens
messages=[]    #消息列表
tokens_list=[]    #记录消息列表数量




openai.api_key = "your API"


#由用户设置记忆等级
print(red + "请输入记忆等级\n"
"1:记住最近100个字符\n"
"2:记住最近500个字符\n"
"3:记住最近1000个字符\n"
"4:记住最近2000个字符\n"
"5:记住最近3000个字符\n"
"6:记住最近3500个字符\n")
set_allow_tokens()







#输入场景描述
#user_input = input(red + "请定义本次聊天的主题：",)
print('')
input_message = {"role": "system", "content": "你是一个优秀的助手"}
#输入合法性检查
input_count = len(input_message["content"].encode('utf-8'))
total_tokens = input_count
if input_count > Question_length:
    print("输入太长")
    sys.exit()
#拼接输入的场景
messages.append(input_message)

#回答问题
chatbot_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages
)

#输出答案
response_message = chatbot_response['choices'][0]['message']['content']

#拼接输出的答案
response_message = chatbot_response['choices'][0]['message']
messages.append(response_message)

input_total_tokens = chatbot_response["usage"]["prompt_tokens"]
total_tokens = chatbot_response["usage"]["total_tokens"]


input_tokens = chatbot_response["usage"]["prompt_tokens"]
output_tokens = chatbot_response["usage"]["completion_tokens"]
total_tokens = int(str(total_tokens))


tokens_list.append(input_tokens)
tokens_list.append(output_tokens)


while True:

    #输入问题
    user_input = prompt_toolkit.prompt("[%d]>>"%total_tokens)
    print('')
    input_message = {"role": "user", "content": user_input}
    #输入合法性检查
    input_count = len(input_message["content"].encode('utf-8'))
    if input_count > Question_length:
        print("输入太长")
        sys.exit()
    #拼接输入的问题
    messages.append(input_message)

    #拼接之后合法性检查
    #如果tokens过长
    while total_tokens + input_count > base.Allow_tokens:
        total_tokens_last = total_tokens
        if total_tokens == 0:
            break
        del messages[0]
        del tokens_list[0]
        total_tokens = 0
        for num in tokens_list:
            total_tokens += num

    total_tokens_last = total_tokens

    

        
    #回答问题
    chatbot_response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    #输出答案
    response_message = chatbot_response['choices'][0]['message']['content']
    print(yellow + "ChatGPT:",response_message.strip())
    print('')

    #拼接输出的答案
    response_message = chatbot_response['choices'][0]['message']
    messages.append(response_message)

    #计算tokens值
    total_tokens = chatbot_response["usage"]["total_tokens"]
    input_total_tokens = chatbot_response["usage"]["prompt_tokens"]
    output_tokens = chatbot_response["usage"]["completion_tokens"]

    total_tokens = int(str(total_tokens))
    output_tokens = int(str(output_tokens)) 
    input_tokens = total_tokens - output_tokens - total_tokens_last   
    
    tokens_list.append(input_tokens)
    tokens_list.append(output_tokens)
    





        
