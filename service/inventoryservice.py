from numpy import int64
import client.inventoryclient
import json
import csv

def getInventoriesAge():
    start = 0
    furyToken = "9521ccfed890fe8d06a5575289997a990a43941d2c5c68cb51208630f01d555d"
    total = 9999999
    while(start <= total):
        response = client.inventoryclient.getInventoriesAgeAggregator(start,furyToken,True)
        result = json.loads(response.text)
        total = result["total"]
        print("[Total]: " + str(total) + " [from]" + str(start))
        start = start + 1000
        with open('util/dataresult.json', 'w', encoding='utf-8') as f:
            json.dump(result["metadata"], f, ensure_ascii=False, indent=4)

def getInventoriesAgeScope():
    start = 0
    total = 9999999
    contextId = ""
    furyToken = "4506f1b38ed8f4ca88937cb906a7543c8932ded95233e0ccf5780f318ea6b845"
    while(start <= total):
        response = client.inventoryclient.getInventoriesAgeAggregatorScope(contextId, furyToken)
        result = json.loads(response.text)
        total = result["total"]
        contextId = result["search_context_id"]
        print("[Total]: " + str(total) + " [from]" + str(start))
        start = start + 1000
        for document in result["documents"]:
            with open('util/dataResult.txt', 'a') as f:
                f.write('{"inventory_id": "' +document["inventory_id"]+ '"},\n')




def saveInventoryCharges():
    with open('util/inventoriescharges.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                response = client.inventoryclient.saveInventoriesCharges(row)
                result = json.loads(response.text)
                with open('util/pxw_inventories.txt', 'a') as f:
                    f.write('Response[row('+str(row['Id'])+')]: '+str(result)+',\n')
        

