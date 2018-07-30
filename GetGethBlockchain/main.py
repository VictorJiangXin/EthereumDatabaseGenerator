from GetGethBlockchain import GetGethBlockchain

def generateBlockchain(start_number,
					   end_number,
					   host='http://localhost', 
					   port=8545
					   ):
	g = GetGethBlockchain(port, host)
	g.storeBlocksToDb(start_number, end_number)
