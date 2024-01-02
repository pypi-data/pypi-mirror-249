
'''
	import estimates.taps.supertrend as supertrend_indicator
	supertrend_indicator.calc (
		places = [],
		spans = 4
	)
'''

import estimates.taps.ATR as ATR_indicator

def calc (
	places = [],
	spans = None,
	multiplier = 1.4
):
	ATR_indicator.calc (
		places = places,
		label = "ATR",
		
		spans = 20
	)
	
	for i in range(spans, len(places)):
		if ("ATR" not in places [i]):
			continue;
	
		upper_band = places[i-1]['close'] + multiplier * places[i]['ATR']
		lower_band = places[i-1]['close'] - multiplier * places[i]['ATR']
		end = places [i - 1]['close']
		
		#print ('end:', end)
		#print ('upper_band:', upper_band)
		#print ('lower_band:', lower_band)

		print (upper_band - end, end - lower_band)

		if end > upper_band:
			places[i]['supertrend'] = lower_band
			places[i]['position'] = 1  # Buy Signal
			
			print ("Buy")
			
		elif end < lower_band:
			places[i]['supertrend'] = upper_band
			places[i]['position'] = -1  # Sell Signal

			print ("Sell")


		else:
			try:
				places[i]['supertrend'] = places[i-1]['supertrend']
				places[i]['position'] = 0
			except Exception:
				#print ('exception:', Exception)
				pass;
			
		