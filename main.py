import service.inventoryservice

def showMenu():
	print("-------")
	print("Utilities")
	print("-------")
	print("1 - Get Inventories Age Agregator")
	print("2 - Save inventoriesCharges in fbm-fee-warehousing")
	print("0 - Exit")

while True:
	showMenu()

	op = int(input("Option: "))
	if op == 0:
		break

	switcher = {
		1: service.inventoryservice.getInventoriesAgeScope,
		2: service.inventoryservice.saveInventoryCharges,
	}


	func = switcher.get(op, lambda: "Invalid Option")
	func()


