from  gemini.gemini_connector import *
import chainlit as cl
import os
import time

# # settings.request_timeout = 10

def async_func(message, message_history):
    collector = GeminiConnector(input=message, message_history=message_history)
    collector.run()
    return collector

@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_message
async def main(message: cl.Message):   
    message = message.content.strip() 

    # Chat history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message})

    async_callable = lambda: async_func(message, message_history)
    collector = await cl.make_async(async_callable)()

    try:
           
        if collector.response != "Report generated":
            msg = cl.Message(content=collector.response)
            message_history.append({"role": "assistant", "content": msg.content})
            await cl.Message(content=collector.response).send()

        else:
            elements = [
            cl.Pdf(name="report", display="inline", path="./report.pdf", page=1)
            ]
            # Reminder: The name of the pdf must be in the content of the message
            await cl.Message(content="Report generated!", elements=elements).send()

    except Exception as e:        
        print(f"Error: {str(e)}")
    
# @cl.on_chat_start
# async def start():
#     print("START")
#     time.sleep(50)
#     print("DONE")
#     await cl.Message(content="Ok").send()