''' A class to interact with node and to save data to spl server'''
import GetGethBlockchainUtility
import requests
import pymssql
import json
import time
import datetime

class GetGethBlockchain:
	'''
	a class to interact with node and to save data to sql server
	
	Description:
	----------------
	Before starting, make sure geth is running in rpc
	eg the config of geth is (geth --rpc --rpcaddr 127.0.0.1 --rpcport 8545) 
	You can use this class to store blocks into database
	for example you can use storeBlocksToDb(start_num, end_num)
	
	Parameters:
	Default behavior:
		getGethBlockchain = GetGethBlockchain()
		
	Get  the data from a particular number
		block = getGethBlockchain.grtBlock(block_number)
	Save the blocks to db
		getGethBlockchain.storeBlocksToDb(start_number, end_number)
	'''
	
	def __init__(self,
				 rpc_port=8545, 
				 host='http://localhost'
	):
	
		''' Initialize the class'''
		print('start the class')
		self.url = '{}:{}'.format(host, rpc_port)
		self.headers = {'content-type': 'application/json'}
	
		#Initialize tbe db
		GetGethBlockchainUtility.initSqlServer()
	
	def rpcRequest(self, method, params, key):
		'''make the request to geth rpcport'''
		payload = {
			'jsonrpc': '2.0',
			'method': method,
			'params': params,
			'id': 0
		}
		
		res = requests.post(self.url, 
					  data=json.dumps(payload),
					  headers=self.headers).json()
		return res[key]
		
	def getOneBlock(self, n):
		'''
			get one block data
			param: n the number of the block
		'''
		data = self.rpcRequest('eth_getBlockByNumber', [hex(n), True], 'result')
		block = GetGethBlockchainUtility.decodeBlock(data)
		return block
		
	def storeOneBlock(self, block, cursor):
		'''
			store a block to db
		'''
		tm = datetime.datetime.fromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
		for t in block['transactions']:
			execute_statement = '''
					INSERT
					INTO EtheTransactions (BlockHeight, BlockHash, BlockTimeStamp,
						TransactionHash, AddressFrom, AddressTo, TransactionValue)
					VALUES (%d, '%s', '%s', '%s', '%s', '%s', %f)''' % (
						block['height'], block['blockhash'], tm,
						t['transactionhash'], t['from'], t['to'], t['value'])
			cursor.execute(execute_statement)
	
	def storeBlocksToDb(self, start_number, end_number):
		'''store the block between start_number to end_number to db'''
		print("starting storing.......")
		try:
			conn = pymssql.connect(GetGethBlockchainUtility.DB_SERVER, GetGethBlockchainUtility.DB_USER, 
			GetGethBlockchainUtility.DB_PASSWD, GetGethBlockchainUtility.DB_NAME)
			cursor = conn.cursor()
			print("disable index...")
			cursor.execute(''' ALTER INDEX ETHE_TX_BLKHEIGHT ON EtheTransactions DISABLE''')
			for i in range(start_number, end_number):
				if (i-start_number)%10000 == 0:
					print('complete %d ...' % (100*(i-start_number)/(end_number-start_number)))
					conn.commit()
				block = self.getOneBlock(i)
				self.storeOneBlock(block, cursor)
				
			print("rebuild index...")
			cursor.execute(''' ALTER INDEX ETHE_TX_BLKHEIGHT ON EtheTransactions REBUILD''')
			conn.commit()
			conn.close()
			print('completed')
		except:
			print('store error!')
			cursor.execute(''' ALTER INDEX ETHE_TX_BLKHEIGHT ON EtheTransactions REBUILD''')
			conn.commit()
			conn.close()
			
	
			
	