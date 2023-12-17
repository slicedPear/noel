# noel

## What is noel?
**"noel" is small Christmas gift / toy from Jez Graham and slicedPear Ltd.**

Provided as-is and for experimentation and to promote discussion, "noel" is small AI supported project to assess customer information and determine whether they may be suffering from Financial stress or making difficulty making payments on a credit service provided.

Working, at scale, through a wealth of customer data, where significant behavioural and status indicators are often burried in free-text and notes fields and where internal and external characteristics also need to be considered has been a challenge requiring high resource and time commitments, making such activities infrequent of even avoided. 

Through the use of AI agents, "noel" is able to heuristically evaluate datasets, including free text and notes fields and provide a determination on the possibility of ability to pay (ATP) problems - potentially making continual, pro-active financially vulnerable customer identification and support a practical reality.

## What does noel do?

# Why free?
Why not? 

The possibilities of AI are transforming many industries - let's not let Credit Management, Credit Risk, Debt and Collections get left behind. With economic conditions as they are, many people are feeling the squeeze, lots are in difficulty for the first time and won't necessarily volunteer that to service providers/creditors until it's late and resolution is a lot more challenging. It's a cliche, but prevention really is better than cure - by taking a pro-active stance in identifying customers who may be struggling and strategising accordingly, support can be offered, options can be socialised and solutions agreed, leading to less debt emergence, better early stage recovery and longer, more sustainable relationships.

All in all, this is a bit of Christmas fun, a light-touch experiment, a basic proof of concept, but more importantly.....I hope, a conversation starter that hopefully could lead to new approaches, more advanced and refined tools, bespoke trained models and new ways of working with financially vulnerable customers

# AI Agents
Currently noel supports two agents and can be switched between them in code.

## chatGPT 3.5 Turbo
Requires a commercial account and API key. This key is pulled from environmental variables - place your API key in a .env file (as show in .env.example). chatGPT charging is on a token-use basis. Make sure you are aware of run costs (though for small/moderate testing these are likely to be low). Evaluation is done server-side at openai.com

## llama (specifically Mistral 7b)
Meta's llama is open-source and can be run locally. For now - this model is Mac only, as it moel relieas on a local ollama server (ollama.ai - please support this project). Evaluation is local and needs a fast machine(!), but has the advantage of running 100% locally and is free.

# Batching
noel can batch-process. To reduce token usage, a max batch size can be set and processing will be handled in rounds - this is faster and lighter than handling each record in sequence. noel can also start and end as specified points in the dataset - this allows for re-runs of part sets, or for continuation of an aborted run.

# Sample Data
noel can handle variable datasets, but try to keep the number of variables down - data format, input sources, output locations etc are defined in a json file (eg "inputFormat.json") and also allows context to be added to each data characteristic (what does it represent?, how should the agent read it?, what does good/bad look like?, why is it important?)

Two simple sample files are provided to illustrate usage and get you started.

# Installation

Open terminal.

## Clone this GIT
Navigate to or create a suitable directory.

'git clone https://github.com/slicedPear/noel.git'

Create and activate a virtual environment
Create:
'python -m venv venv'
Activate:
Mac:
'source venv/bin/activate'
Windows:
'venv\Scripts\activate.bat

Install the required python libs
'pip install -r requirements.txt'

# Setup environment variables
Create a ".env" file or rename ".env.example"
You'll see a placeholder for your chatGPT API key - paste this between the quotes and you're ready to go. It should look something like:

'OPENAI_API_KEY = "Your Key Here"'



