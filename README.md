# noel

## What is noel?
**"noel" is small Christmas gift / toy from Jez Graham and slicedPear Ltd.**

Provided as-is and for experimentation and to promote discussion, noel is small AI supported project to assess customer data and determine whether they may be suffering from Financial stress or experiencing difficulty in making/maintaining payments on a credit service provided.

Working, at scale, through a wealth of customer data has traditionally been difficult - significant behavioural and status indicators are often burried in unformatted free-text and notes fields and a meaningful review also needs internal and external characteristics to be considered and understood. This has always been a challenge, requiring high resource and time commitments and as a result such activities were carried out infrequently or even avoided. 

Through the use of AI agents, noel is able to heuristically evaluate datasets, including free text and notes fields and provide a determination on the possibility of ability to pay (ATP) problems - potentially making continual, pro-active financially vulnerable customer identification and support a practical reality. This has potential to take away a lot of heavy lifting and identify a priority sub-set for direct evaluation and strategic support.

## What does noel do?
noel takes user defined CSV files of customer data, with user supplied context and acting as a collections agent and evaluates them for potential signs of financial stress or ability to pay (ATP) problems. The agent will provide a view of Ability to pay risk (ATP_Risk - True/False), Reasoning behind the decision (Reasoning - string) and a confidence score (0 - 10 on the decision made)

# Why free?
Why not? 

The possibilities of AI are transforming many industries - let's not let Credit Management, Credit Risk, Debt and Collections get left behind. With economic conditions as they are, many people are feeling the squeeze, lots are in difficulty for the first time and won't necessarily volunteer that to service providers/creditors until it's late and resolution is a lot more challenging. 

Nobody wants *"fix on fail"* when it comes to debt, it benefits no-one.....It's a cliche, but **prevention really is better than cure** - by taking a pro-active stance in identifying customers who may be struggling and strategising accordingly, support can be offered, options can be socialised and solutions agreed, leading to less debt emergence, better early stage recovery and longer, more sustainable relationships.

All in all, this is a bit of Christmas fun, a light-touch experiment, a basic proof of concept, but more importantly.....I hope, a conversation starter that hopefully could lead to new approaches, more advanced and refined tools, bespoke trained models and new ways of working with financially vulnerable customers - Let's redefine *"Best in class"*

## The Model(s)
Everyone like choice, so noel has one, with multiple AI models and providers supported and hopefully more to come.

## AI Agents
Currently noel supports two agents and can be switched between them in code.
```python
model_list = ["gpt","llama"]                    
active_model = 0                                # selected model (0 = chatGPT 3.5 Turbo, 1 = llama/Mistral)
selected_model = model_list[active_model]     
```

## chatGPT 3.5 Turbo
Requires a commercial account and API key. This key is pulled from environmental variables - place your API key in a .env file (as show in .env.example). chatGPT charging is on a token-use basis. Make sure you are aware of run costs (though for small/moderate testing these are likely to be low). Evaluation is done server-side at openai.com

## llama (specifically Mistral 7b)
Meta's llama is open-source and can be run locally. For now - this model is Mac only, as it moel relieas on a local ollama server (ollama.ai - please support this project). Evaluation is local and needs a fast machine(!), but has the advantage of running 100% locally and is free.

# Batching
noel can batch-process. To reduce token usage, a max batch size can be set and processing will be handled in rounds - this is faster and lighter than handling each record in sequence. noel can also start and end as specified points in the dataset - this allows for re-runs of part sets, or for continuation of an aborted run.

# Data
noel can handle variable datasets, but try to keep the number of variables down - data format, input sources, output locations etc are defined in a json file (eg "inputFormat.json") and also allows context to be added to each data characteristic (what does it represent?, how should the agent read it?, what does good/bad look like?, why is it important?)

```json
        {
            "name": "customer_ref",
            "type": "string",
            "desc": "5 digit unique customer reference number which must remain with the customer and is used to identify them"
        },
        {
            "name": "notes",
            "type": "string",
            "desc": "notes made by agents relating to the customer and their account including any recent interactions"
        }
```

As a minimum, customer information must include a unique reference identifier.

Two simple sample files are provided to illustrate usage and get you started.

# Installation

Open terminal.

## Clone this GIT
Navigate to or create a suitable directory.

```commandline
git clone https://github.com/slicedPear/noel.git
```

Create and activate a virtual environment
Create:
```commandline
python -m venv venv
```
Activate:
Mac:
```commandline
source venv/bin/activate
```
Windows:
```commandline
venv\Scripts\activate.bat
```
Install the required python libs
```commandline
'pip install -r requirements.txt'
```
# Setup environment variables
Create a ".env" file or rename ".env.example"
You'll see a placeholder for your chatGPT API key - paste this between the quotes and you're ready to go. It should look something like:
```python
'OPENAI_API_KEY = "Your Key Here"'
```


