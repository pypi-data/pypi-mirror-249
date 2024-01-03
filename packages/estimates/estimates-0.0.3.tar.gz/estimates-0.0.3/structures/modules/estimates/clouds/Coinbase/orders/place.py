
'''
	https://docs.cloud.coinbase.com/exchange/docs/sandbox
'''

'''
	https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder
'''

'''
	https://exchange.coinbase.com/profile/api
'''

'''
	https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-auth
'''

'''
	https://forums.coinbasecloud.dev/t/python-create-market-order-example/2335
	
	client_order_id = "1"
	
	{
		"client_order_id": "238e4a4e-e4ee-4974-860d-4b98d37d70a1",
		"order_configuration": {
			"marketMarketIoc": {
				"quoteSize": "1"
			}
		},
		"product_id": "SUKU-USD",
		"side": "BUY"
	}
'''	


sandbox = "https://api-public.sandbox.exchange.coinbase.com"

import http.client
import json

def place_market_order ():
	conn = http.client.HTTPSConnection("api.coinbase.com")
	payload = ''
	headers = {
	  'Content-Type': 'application/json'
	}
	conn.request (
		"POST", 
		"/api/v3/brokerage/orders", 
		payload, 
		headers
	)
	
	
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))