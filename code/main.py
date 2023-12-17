# noel - A little Festive gift/toy from Jez Graham / slicedPear Ltd - December 2023
# A small project leveraging AI agents in the role of Debt/Collections advisors
# to support the identification of customers in debt, or not yet in debt
# who may be experiencing financial difficulty or stress
# With the view to providing pro-active insight to direct support strategy

# Nothing fancy - this is an experiment to provoke collective conversation. Enjoy and discuss.
# Error trapping is minimal!

from aiAssistants import askAI
from helpers import *

# Setup
model_header = "noel - A little Festive Toy from Jez Graham / slicedPear Ltd - December 2023\n" \
    "AI supported, 'agent-style' evaluation of customer data for potential financial difficulties/Ability to pay problems\n"
receipt_name = "noelRunReceipt.txt"

input_info = "./formatting/inputFormat5"        # Source input controls. Describe data-file contents and provide context to the agent here. (JSON format)

# List of model variations (chatGPT - hosted, Llama - local)
# 2 model interfaces implemented:
# 1. ChatGPT 3.5 Turbo - Requires premium subscription and API key. Processing is openai server-side
# 2. llama (Mistral 7b) - Local processing with support from ollama (ollama.ai - please support!) - Mac only for now.
model_list = ["gpt","llama"]                    
active_model = 1                                # selected model (1 = chatGPT 3.5 Turbo, 2 = llama/Mistral)
selected_model = model_list[active_model]       
max_batch = 5                                   # Query batching - to avoid token limits, queries are batched to a max-size and auto-compiled at endpoint

# Manual controls to allow for processing of sub-batches, or continuation of activity previously suspended
start_record = 0                                # First record in batch.
end_record = 0                                  # Last record in batch (0 will run to end of dataset)

# Import Data
source_format = loadJson(input_info)
infile_source = source_format["source"]  
infile_hasHeaders = source_format["inputHasHeaders"]
outfile_name = source_format["output Filename"]
outfile_location = source_format["output Location"]    
outfile_hasHeaders = source_format["outputHasHeaders"]

# Date and instance sub-directories will be auto-created on completion. 
printStamp(f'Importing Data ({infile_source})')
source_data = importData(infile_source)

# Unspecified endpoint
if end_record == 0:
    end_record = len(source_data)-1

# Step over headers 
if infile_hasHeaders and start_record == 0:
    start_record += 1

# Batch process
# n batches of size (max_batch)
# clustering avoids token limits on models, while reducing token usage on header and footer over processing as individual calls.

# Initialise output var.
output = []
header_string = ''
fieldCount = len(source_data[0])

# Create re-usable field info for AI agent
for field in source_format['fields']:
    header_string += f"{field['name']} = {field['desc']}\n"

# batch handle/
model_success = True
for i in range(0,int((end_record-start_record)/max_batch)+1):
    parse_string = header_string
    thisStart = start_record+i*max_batch
    thisEnd = min((i+1)*max_batch,end_record)
    printStamp(f'Batch {i} - {thisStart} to {thisEnd} :',end='')

    # Parsing source records to text strings.
    for j in range(thisStart,thisEnd+1):
        for k in range(fieldCount):
            parse_string += f"{source_format['fields'][k]['name']}: {source_data[j][k]},"
        parse_string = parse_string[0:len(parse_string)-1]+".\n"
        print('.',end='')
    print('')

    # IA Call (using selected model)
    try:
        batch_out = askAI(selected_model,parse_string)

        # Output formatting
        for item in batch_out['customers']:
                output.append([item['customer_ref'],item['ATP_risk'],item['Risk_confidence'],item['reasoning']])
    except:
        printStamp('General Model Failure Error - Perhaps retry')
        model_success = False

if model_success:
    printStamp('Model ran and completed. Writing outputs...')
    # Save output to CSV at location and filename specified in the input formatter
    writeOutput(output, outfile_location,outfile_name,outfile_hasHeaders,model_header,selected_model,receipt_name)

