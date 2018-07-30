'''Utility functions for interacting with SQL Server and Geth'''
import pymssql

'''
some constants about the database
'''
DB_SERVER = 'localhost\SQ2'
DB_NAME = 'Ethe'
DB_USER = 'sa'
DB_PASSWD = '123456'

def decodeBlock(block):
	'''
	Decode various pieces of information for a block and return the parsed data
	Note that the return is of the format
	
	{
	"id":1,
	"jsonrpc":"2.0",
	"result": 
	{
		"number": "0x1b4", // 436
		"hash": "0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331",
		"parentHash": "0x9646252be9520f6e71339a8df9c55e4d7619deeb018d2a3f2d21fc165dde5eb5",
		"nonce": "0xe04d296d2460cfb8472af2c5fd05b5a214109c25688d3704aed5484f9a7792f2",
		"sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
		"logsBloom": "0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331",
		"transactionsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
		"stateRoot": "0xd5855eb08b3387c0af375e9cdb6acfc05eb8f519e419b874b6ff2ffda7ed1dff",
		"miner": "0x4e65fda2159562a496f9f3522f89122a3088497a",
		"difficulty": "0x027f07", // 163591
		"totalDifficulty":  "0x027f07", // 163591
		"extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
		"size":  "0x027f07", // 163591
		"gasLimit": "0x9f759", // 653145
		"gasUsed": "0x9f759", // 653145
		"timestamp": "0x54e34e8e" // 1424182926
		"transactions": [{...},{ ... }] 
		"uncles": ["0x1606e5...", "0xd5145a9..."]
	}
	}

	and the transaction is of the format
	the example is the 1000000th block data
	"transaction": 
	{
		'gasPrice': '0x12bfb19e60', 
		'from': '0x39fa8c5f2793459d6622857e7d9fbb4bd91766d3', 
		'gas': '0x1f8dc', 
		'transactionIndex': '0x0', 
		'r': '0xa254fe085f721c2abe00a2cd244110bfc0df5f4f25461c85d8ab75ebac11eb10', 
		's': '0x30b7835ba481955b20193a703ebc5fdffeab081d63117199040cdf5a91c68765', 
		'v': '0x1c', 
		'blockNumber': '0xf4240', 
		'to': '0xc083e9947cf02b8ffc7d3090ae9aea72df98fd47', 
		'hash': '0xea1093d492a1dcb1bef708f771a99a96ff05dcab81ca76c31940300177fcf49f', 
		'blockHash': '0x8e38b4dbf6b11fcc3b9dee84fb7986e29ca0a02cecd8977c161ff7333329681e',
		'input': '0x', 
		'nonce': '0x15', 
		'value': '0x56bc75e2d63100000'
	}
	
	the datas what we need is:
		block.number	:int
		block.hash		:str
		block.timestamp	:int
		transaction.hash :str
		transaction.from :str
		transaction.to   :str
		transaction.value :float
	'''
	try:
		b = block
		if 'result' in block:
			b = block['result']
		new_block = {
			'height': int(b['number'], 16),
			'blockhash': b['hash'],
			'timestamp': int(b['timestamp'], 16),
			'transactions': []
		}
		for t in b['transactions']:
			new_transaction = {
				'transactionhash': t['hash'],
				'from': t['from'],
				'to': t['to'],
				'value': float(int(t["value"], 16))/1000000000000000000.
			}
			new_block['transactions'].append(new_transaction)
		return new_block
	except:
		print('decode error')
		return None
		
def initSqlServer():
	'''
	this function is used to init the SQL Server,
	if the database scheme is not exits, then create a new database scheme
	return the connection of the database
	
	The related SQL statement is 
	1. judge the DB scheme 	whether exists
		SELECT CASE WHEN EXISTS (SELECT * FROM EtheSetting) THEN 1 ELSE 0 END AS DBEXIST
	2. create the database table 
			CREATE TABLE EtheTransactions(
		TxId BIGINT IDENTITY(1, 1) PRIMARY KEY,
		BlockHeight BIGINT NOT NULL,
		BlockHash VARCHAR(300) NOT NULL,
		BlockTimeStamp SMALLDATETIME NOT NULL,
		TransactionHash VARCHAR(300) NOT NULL,
		AddressFrom VARCHAR(300) NOT NULL,
		AddressTo VARCHAR(300) NOT NULL,
		TransactionValue FLOAT(6) NOT NULL
		)
	'''
	print('init the Sql Server......')
	try:
		conn = pymssql.connect(DB_SERVER, DB_USER, DB_PASSWD, DB_NAME)
		cursor = conn.cursor()
		cursor.execute('''SELECT CASE WHEN EXISTS (SELECT * FROM EtheSetting) THEN 1 ELSE 0 END AS DBEXIST''')
		is_database_exists = cursor.fetchone()[0]	# if the databasescheme exists then it return 1 else return 0
		if is_database_exists != 1:
			cursor.execute('''
			CREATE TABLE EtheTransactions(
				TxId BIGINT IDENTITY(1, 1) PRIMARY KEY,
				BlockHeight BIGINT NOT NULL,
				BlockHash VARCHAR(300) NOT NULL,
				BlockTimeStamp SMALLDATETIME NOT NULL,
				TransactionHash VARCHAR(300) NOT NULL,
				AddressFrom VARCHAR(300) NOT NULL,
				AddressTo VARCHAR(300) NOT NULL,
				TransactionValue FLOAT(6) NOT NULL
			)'''
			)
			cursor.execute('''CREATE TABLE EtheSetting(DBVersion SMALLINT NOT NULL, Author VARCHAR(20) NOT NULL)''')
			cursor.execute('''INSERT INTO EtheSetting VALUES (1, 'jiangxin') ''')
			cursor.execute('''CREATE INDEX ETHE_TX_BLKHEIGHT EtheTransactions(BlockHeight)''')
		conn.commit()	
		conn.close()
	except:
		print('database operate error')

		
	
	
