# Note: 您需要使用OpenAI Python v0.27.0才能使下面的代码正常工作
import openai
import sys
import prompt_toolkit
from base import red
from base import green
from base import yellow
from base import blue
from base import reset
from base import set_allow_tokens
import base 

openai.api_key = ""


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
if input_count > base.Question_length:
    print("输入太长")
    sys.exit()
#拼接输入的场景
base.messages.append(input_message)

#回答问题
chatbot_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=base.messages
)

#输出答案
response_message = chatbot_response['choices'][0]['message']['content']

#拼接输出的答案
response_message = chatbot_response['choices'][0]['message']
base.messages.append(response_message)

input_total_tokens = chatbot_response["usage"]["prompt_tokens"]
total_tokens = chatbot_response["usage"]["total_tokens"]


input_tokens = chatbot_response["usage"]["prompt_tokens"]
output_tokens = chatbot_response["usage"]["completion_tokens"]
total_tokens = int(str(total_tokens))


base.tokens_list.append(input_tokens)
base.tokens_list.append(output_tokens)


while True:

    #输入问题
    user_input = prompt_toolkit.prompt("[%d]>>"%total_tokens)
    print('')
    input_message = {"role": "user", "content": user_input}
    #输入合法性检查
    input_count = len(input_message["content"].encode('utf-8'))
    if input_count > base.Question_length:
        print("输入太长")
        sys.exit()
    #拼接输入的问题
    base.messages.append(input_message)

    #拼接之后合法性检查
    #如果tokens过长
    while total_tokens + input_count > base.Allow_tokens:
        total_tokens_last = total_tokens
        if total_tokens == 0:
            break
        del base.messages[0]
        del base.tokens_list[0]
        total_tokens = 0
        for num in base.tokens_list:
            total_tokens += num

    total_tokens_last = total_tokens

    

        
    #回答问题
    chatbot_response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=base.messages
    )

    #输出答案
    response_message = chatbot_response['choices'][0]['message']['content']
    print(yellow + "ChatGPT:",response_message.strip())
    print('')

    #拼接输出的答案
    response_message = chatbot_response['choices'][0]['message']
    base.messages.append(response_message)

    #计算tokens值
    total_tokens = chatbot_response["usage"]["total_tokens"]
    input_total_tokens = chatbot_response["usage"]["prompt_tokens"]
    output_tokens = chatbot_response["usage"]["completion_tokens"]

    total_tokens = int(str(total_tokens))
    output_tokens = int(str(output_tokens)) 
    input_tokens = total_tokens - output_tokens - total_tokens_last   
    
    base.tokens_list.append(input_tokens)
    base.tokens_list.append(output_tokens)
    





        
