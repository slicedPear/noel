# noel - A Christmas gift from slicedPear Ltd (Jez Graham) 12/2023 - See License

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import json
from helpers import loadJson, printStamp

# Ollama support
ollama_url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type':'application/json',
}

load_dotenv()

# Base model prompt (both models) - establish role parameters and query conditions for the AI agent
base_prompt = "\nAct as a customer collections agent. Review data for each unique customer and assess whether they may be struggling to pay due to financial problems. " \
    "Explain your reasoning for the decision and provide a confidence score between 0 and 10 where high = high. DO NOT SHARE DATA BETWEEN LINE ITEMS/CUSTOMERS"

# llama additions - currently llama does not support tools/functions and needs to be conditioned to respond in the correct format. GPT outputs defined in ./formatting/gptFunctions.json
llama_add = "Respond in json as an array of 'customers' using ONLY the fields :" \
            "customer_ref (from input source data - (MUST ALIGN)), " \
            "ATP_risk (type boolean), " \
            "Risk_confidence (type number 0 to 10, high = high confidence in decision), " \
            "reasoning (type string, providing an explanation for your decision)"

def askAI(model,question):
    response = ["no response"]
    match model:
        case "gpt":
            response = askGPT(question)
        case _:
            response = askLocalLlama(question)
    try:
        parsed_response = json.loads(response[0])
    except:
        parsed_response = "ERROR"
    return parsed_response
    
def askGPT(question):    # chatGPT 3.5 Turbo
    printStamp('chatGPT model')
    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        )

    completion = client.completions
    tools = loadJson("formatting/gptFunctions")
    # chat_log = None
    # if chat_log is None:
    chat_log = [{
        'role': 'system',
        'content': 'You are a helpful collections service assistant.',
    }]
    chat_log.append({'role': 'user', 'content': question+base_prompt})
 
    # response = completion.create(model='gpt-3.5-turbo', prompt=chat_log, tools = functions, tool_choice = {"name":functions[0]["name"]})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=chat_log,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "evaluate_ATP"}}
        )
    
    answer = response.choices[0].message.tool_calls[0].function.arguments
    chat_log.append({'role': 'assistant', 'content': answer})
    return answer, chat_log

def askLocalLlama(question):    # Mistral 7b (currently config'd below - can be swapped. Hosted locally via ollama)
    printStamp('Mistral/Ollama Model')
    tools = loadJson("formatting/gptFunctions")
    chat_log = None
    data = {
    "model":"mistral",
    "prompt": (question+base_prompt+llama_add),
    "stream": False,
    "format":"json"
    }
    response = requests.post(ollama_url,headers = headers, data = json.dumps(data))
    if response.status_code == 200:
        holding = json.loads(response.text)
        parsed_response = holding["response"]
    else:
        print("Error:",response.status_code,response.text)
    answer = parsed_response.replace('\n', '')
    return answer, chat_log
