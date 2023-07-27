import json, csv
csvPath = './recipes_sf.csv'
itemsJsonPath = 'csv_generation/items.json'

def readJsonFile(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def convertToCSVRow(recipe):
    if(not (
        'id' in recipe and 
        'result' in recipe and 
        'recipeType' in recipe and 
        'recipe' in recipe
    )):
        return None
    
    materials = {}
    row = [recipe['id'], recipe['result'], recipe['recipeType']]

    for item in recipe['recipe']:
        if(not('value' in item and 'amount' in item)):
            continue

        matName = item['value']

        if matName in materials:
            materials[matName] += item['amount']
        else:
            materials[matName] = item['amount']
    row.append(materials)

    return row

def createCSV(jsonData):
    missedRows = 0

    csvData = []
    csvHeader = [
        'Result',
        'Result Count',
        'Machine',
        'Materials'
    ]

    for i in range(len(jsonData)):
        row = convertToCSVRow(jsonData[i])
        if(row):
            csvData.append(row)
        else:
            missedRows += 1

    with open(csvPath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvHeader)
        writer.writerows(csvData)
  
    print(f'{round(100 * len(csvData) / len(jsonData), 2)}% Inclusion Rate')

jsonData = readJsonFile(itemsJsonPath)
createCSV(jsonData)
