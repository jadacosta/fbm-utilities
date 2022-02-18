import requests
import urllib3
import enums.enumstatusstock
import math

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getInventoriesAgeAggregator(startScroll, furyToken, secundarySearch):
	body = { "query": {
					"and": [
						{
							"date_range": {
								"field": "last_indexed",
								"gte": "now-23d",
								"lte": "now-6d",
								"precision": "days"
							}
						}
					]
				},
				"secondary_search": secundarySearch,
				"size":1000,
				"from":startScroll
			}
	headers = {"x-auth-token":furyToken}
	return requests.post("https://web-legacy.furycloud.io/api/proxy/services_proxy/applications/fbm-age-aggregator/ds/services/aging-inventories-ds/dsclient",json = body,headers=headers)

def getInventoriesAgeAggregatorScope(contextId, furyToken):
	context = ""
	headers = {"x-auth-token":furyToken}
	if(contextId != ""):
		context = "?contextId=" + contextId
	return requests.get("https://getinventories-production_fbm-age-aggregator.furyapps.io/messages/inventories" + context, headers=headers)

def getDecimalTrunc(value):
	fvalue = float(value.replace(",","."))
	posiciones = pow(10.0, 4)
	return math.trunc(posiciones * fvalue) / posiciones


def saveInventoriesCharges(rowCSV):
		
	body = {
                "date": rowCSV['date'],
                "inventory_id": rowCSV['seller_product_id'],
                "rule": {
                    "rules_version": "version_1",
                    "rules": [
                        "regla_1"
                    ]
                },
                "unit_price": getDecimalTrunc(rowCSV['unit_price']),
                "location_id": rowCSV['location_id'],
                "tags": [],
                "is_excluded_from_charge": False,
                "size":  rowCSV['size'],
                "site_id": "MLB",
                "total_fee_amount": getDecimalTrunc(rowCSV['total_fee_amount']),
                "source_id": "",
                "seller_id": int(rowCSV['seller_id']),
                "currency_id": "BLR"
            }
	
	stockdetails={}
	for status in enums.enumstatusstock.estatusStock:
		if(rowCSV[status.name + '_fee_amount']!= 'null'):
			stockdetails[status.name] = {
                        "fee_amount": getDecimalTrunc(rowCSV[status.name + '_fee_amount']),
                        "quantity": int(rowCSV[status.name + '_quantity'])
                    }
		else:
			stockdetails[status.name] = None
	
	body['stock_details']= stockdetails

	return requests.post("https://internal-api.mercadolibre.com/fbm-fee-warehousing-test/fulfillment/fbm-fee-warehousing/inventory-charge",json = body)