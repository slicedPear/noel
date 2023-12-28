# noel - A Christmas gift from slicedPear Ltd (Jez Graham) 12/2023 - See Licence

import json
import os
import csv
import datetime


##### printStamp
def printStamp(thread,end = ''):
    # Extended console print - date and timestamps output
    print(datetime.datetime.now().strftime('%Y/%m/%d - %H:%M:%S // '+thread),end)
    return
    
###### loadData
def loadJson(source_string):
    # Json import
    print('Loading Data (',source_string,')')
    file_to_find = os.path.join(source_string+'.json')
    jfile=open(file_to_find)
    parsed_data = json.load(jfile)
    jfile.close
    return parsed_data

def importData(source):
    # CSV import
    with open(source, 'r') as raw_input:
        reader = csv.reader(raw_input, delimiter=',')
        data = list(reader)
    return data

###### writeOutput
def writeOutput(out_data, outfile_location,outfile_name,outfile_hasHeaders,model_header,selected_model,receipt_name):
    # Simple post-processed list to CSV
    # Auto-creates organised output folders for multiple runs.
    pathString = outfile_location+datetime.datetime.now().strftime("%Y%m%d/")
    counter = 1
    satisfied = False
    finalPath = ''
    printStamp('Testing possible output package locations...')
    while not satisfied:
        holding = '000'+str(counter)
        holding = holding[-3:]
        thisPath = pathString+holding
        if not os.path.exists(thisPath):
            printStamp(f'found suitable location @: {thisPath}')
            satisfied = True
            try:
                os.makedirs(thisPath)
            except OSError as error:
                print(f'failed to create directory: {error}')
        counter +=1
        finalPath = thisPath

    # Write Data to CSV
    try:
        with open(finalPath+"/"+outfile_name+'.csv', 'w') as f:
                write = csv.writer(f)
                if outfile_hasHeaders:
                    write.writerow(['customer_ref','ATP_risk','Risk_confidence','reasoning'])
                write.writerows(out_data)
                f.close()
    except OSError as error:
        printStamp(f'CSV Output write error - {error}')

    # Write a run-receipt
    receipt_string = model_header+f"\nRun : {datetime.datetime.now().strftime('%Y/%m/%d - %H:%M:%S')}" \
        f"\nModel Deployed : {selected_model}" 

    try:  
        with open(finalPath+"/"+receipt_name, 'w') as f:
            f.write(receipt_string)
            f.close()
    except OSError as error:
        printStamp(f'Receipt Write Error - {error}')
