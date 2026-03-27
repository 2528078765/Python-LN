import os
from openai import OpenAI
from openai import APIError, APIConnectionError, AuthenticationError



assistant_reply = ""
messages = []

try:
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    # 多轮对话需要把完整的对话历史传给模型，让模型记住上下文
    system_input = input("系统Prompt：")
    messages.append({
        "role": "system",
        "content": system_input
    })
    while(True):
        user_input = input("\n用户输入（输入N结束对话）：")
        if user_input.upper().__eq__("N"):
            break
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages = messages,
        stream=True  # 开启流式模式
        )
        assistant_reply = ""
        # 遍历流式的返回块，逐字打印
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                assistant_reply+=chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
        messages.append ({"role": "assistant", "content": assistant_reply})

        


except AuthenticationError:
    print("错误：API Key无效，请检查你的密钥是否正确")
except APIConnectionError:
    print("错误：网络连接失败，请检查网络或代理设置")
except APIError as e:
    print(f"错误：API调用失败: {e}")