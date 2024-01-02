




'''
import estimates.climate as climate
climate.change ("ports", {
	"driver": 18871,
	"cluster": 0,
	"http": 0	
})
'''

'''
import estimates.climate as climate
Tradier = climate.find ("Tradier")
'''

import copy

import json
fp = open ("/online ellipsis/tradier.com/ellipse.json", "r")
Tradier_authorization = json.loads (fp.read ()) ["API"]
fp.close ()

climate = {
	"Tradier": {
		"authorization": Tradier_authorization
	}
}

def change (field, plant):
	#global CLIMATE;
	climate [ field ] = plant


def find (field):
	return copy.deepcopy (climate) [ field ]