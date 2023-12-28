<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" height="200px" srcset="https://github.com/slicedPear/noel/assets/153924178/796738d0-4ff9-4268-98da-aa5471da790a">
    <img alt="logo" height="200px" src="https://github.com/slicedPear/noel/assets/153924178/796738d0-4ff9-4268-98da-aa5471da790a">
  </picture>
</div>

# Noel - AI Ability to Pay evaluation model by slicedPear Ltd.

## What is Noel?
**"Noel" is a small Christmas gift / toy from Jez Graham and slicedPear Ltd.**

Provided as-is and for experimentation and to promote discussion, Noel is an AI supported project to assess customer data and determine whether they may be suffering from Financial stress or experiencing difficulty in making/maintaining payments on a credit service provided.

Working, at scale, through a wealth of customer data has traditionally been difficult - significant behavioural and status indicators are often buried in unformatted free-text and notes fields and a meaningful review also needs internal and external characteristics to be considered and understood. This has always been a challenge, requiring high resource and time commitments and as a result, such activities were carried out infrequently or even avoided. 

Through the use of AI agents, Noel can heuristically evaluate datasets, including free text and notes fields and provide a determination on the possibility of ability to pay (ATP) problems - potentially making continual, proactive financially vulnerable customer identification and support a practical reality. This creates the potential to take away a lot of heavy lifting and identify a priority sub-set for direct evaluation and strategic support.

## What does Noel do?
Noel takes user-defined CSV files of customer data, along with user context and acting as a collections agent, evaluates them for potential signs of financial stress or ability to pay (ATP) problems. The agent will provide a view of "Ability to Pay" risk (ATP_Risk - True/False), Reasoning behind the decision (Reasoning - string) and a confidence score (0 - 10 on the decision made)

## Why free?
Why not? 

The possibilities of AI are transforming many industries - let's not let Credit Management, Credit Risk, Debt and Collections get left behind. With economic conditions as they are, many people are feeling the squeeze, lots are in difficulty for the first time and won't necessarily volunteer that to service providers/creditors until it's late and resolution is a lot more challenging. 

Nobody benefits from *"fix on fail"* when it comes to debt.....It's a cliche, but **prevention really is better than cure** - by taking a proactive stance in identifying customers who may be struggling and strategising accordingly, support can be offered, options can be socialised and solutions agreed, leading to less debt emergence, better early stage recovery and longer, more sustainable relationships.

All in all, this is a bit of Christmas fun, a light-touch experiment, a basic proof of concept, but more importantly.....I hope, a conversation starter that hopefully could lead to new approaches, more advanced and refined tools, bespoke trained models and new ways of working with financially vulnerable customers - Let's redefine *"Best in class"*

## The Model(s)
Everyone likes choice, so Noel has one, with multiple AI models and providers supported and hopefully more to come.

## AI Agents
Currently, Noel supports two agents and can be switched between them in code.
```python
model_list = ["gpt","Llama"]                    
active_model = 0                                # selected model (0 = chatGPT 3.5 Turbo, 1 = Llama/Mistral)
selected_model = model_list[active_model]     
```

### chatGPT 3.5 Turbo
Requires a commercial account and API key. This key is pulled from environmental variables - place your API key in a .env file (as shown in ".env.example"). chatGPT charging is on a token-use basis. Make sure you are aware of run costs (though for small/moderate testing these are likely to be low). Evaluation is done server-side at openai.com

### Llama based (specifically Mistral 7b)
Meta's Llama and variants are open-source and can be run locally. For now - this option is Mac only, as it relies on a local ollama server ([ollama.ai](https://ollama.ai) - please support this project). Evaluation is local and needs a fast machine(!), but has the advantage of running 100% locally and is free.

Download and install ollama, if you wish to utilise Llama models or variants. The Noel code is currently configured to use the Mistral 7b model, but ollama supports a range of models - check the website for options and this can be changed in the source, easily. Mistral is (currently) the best-performing for the size and memory footprint.

The ollama server will download any models not already held locally on first run - be aware this can take a while, as a typical 7b parameter model is c4.3GB. This can be avoided by opening a terminal window (with the ollama server running in the background) and running the command

```commandline
ollama run Mistral
```

and waiting for the download to complete.


## Examples
Sample input/output can be found in the [data/samples](../data/samples) folder. Input is flexible and supported by context provided in the driver json file ([formatting](../formatting)). Noel will provide a determination for further examination and reasoning for that outcome.

### Input Example:

|cutomer|ref,dunning_entries|bureau_arrears|bureau_balance|balance,Notes|
|---|---|---|---|---|
|"00001"|4|"Yes"|£300|£250|"Customer is injured and cannot work| Has made promise to pay on 17/12/2023."|
|"00006"|2|"No"|£0|£230|"Vulnerable customer - housebound"|

### Output Example:

|customer_ref|ATP_risk|Risk_confidence|reasoning|
|---|---|---|---|
|00001|True|9|"The customer has a high dunning_entries count and is currently injured and unable to work. Although they have made a promise to pay on a specific date, there is uncertainty about their ability to fulfill this commitment. Therefore, there is a high risk that the customer may struggle to pay."|
|00006|False|8|"The customer has 2 dunning entries, but there are no bureau arrears or balance owed to other creditors. The note states that the customer is a vulnerable customer and is housebound, but there is no indication of financial problems. Therefore, the customer is not considered to be struggling to pay."|

## Batching
Noel can batch-process. To reduce token usage, a max batch size can be set and processing will be handled in rounds - this is faster and lighter than handling each record in sequence. Noel can also start and end as specified points in the dataset - this allows for re-runs of part sets, or for continuation of an aborted run.

## Data
Noel can handle variable datasets, but try to keep the number of variables down - data format, input sources, output locations etc are defined in a json file (eg "inputFormat.json") and also allows context to be added to each data characteristic (what does it represent? how should the agent read it? what does good/bad look like? why is it important?)

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

Point main.py at your chosen inputformat file
```python
input_info = "./formatting/inputFormat1"
```

and specify input and output files/locations within the inputformat json file - this allows for rapid switching between datasets. Output locations will be auto-created under *YYYYMMDD* and an auto-iterating output folder of the for *NNN* (eg 001)

```python
{
    "name": "ExtendedTest",
    "source": "./data/samples/sample2.csv",
    "inputHasHeaders": true,
    "output Filename": "ATPAssessed_Sample2",
    "output Location": "./data/output/",
    "outputHasHeaders": true
}
```

## Installation
Just a few steps to get you up and running with Noel.

**Using an open terminal or command line prompt:**

## Clone this GIT

Navigate to or create a suitable directory for your local install of the project (the Noel subdirectory and structure will be created for you)

```commandline
git clone https://github.com/slicedPear/Noel.git
```

Navigate to the newly created Noel directory 
```commandline
cd Noel
```
We'd advise using a virtual environment to ensure dependency versions remain aligned and do not conflict with your other projects. 

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
Windows (cmd):
```commandline
venv\Scripts\activate.bat
```

Dependencies are captured and can be batch-installed by issuing the command
```commandline
pip install -r requirements.txt
```
from within the Noel directory

## Setup environment variables
Noel pulls from environmental variables for sensitive sources - in this case, your chatGPT key.

Create a ".env" file or rename ".env.example"
You'll see a placeholder for your chatGPT API key in ".env.example" - paste your key between the quotes and you're ready to go. Once you're done, you should have a .env file in the root directory that includes:
```python
'OPENAI_API_KEY = "Your Key Here"'
```

## License
The code in this repository is released under GNU General Public License version 3.0
