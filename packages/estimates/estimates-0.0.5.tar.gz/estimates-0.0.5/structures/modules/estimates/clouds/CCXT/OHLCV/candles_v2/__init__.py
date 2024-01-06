

'''
	import estimates.clouds.CCXT.OHLCV.candles_v2 as CCXT_OHLCV_candles_v2
	chart = candles_v2.show (
		DF = DF
	)
	
	chart.show ()
'''

from datetime import datetime

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


'''
	https://stackoverflow.com/questions/64689342/plotly-how-to-add-volume-to-a-candlestick-chart
'''
def show (
	#
	#	df
	#
	intervals = None,
	DF = None
):
	#
	#	Utilize the intervals as the DF if intervals is provided.
	#
	if (type (intervals) == list):
		df = pd.DataFrame.from_dict (intervals)
	else:
		df = DF;


	figure = go.Figure (
		data = [
			go.Candlestick (
				x = df ['UTC date string'],
				
				open = df ['open'],
				high = df ['high'],
				low = df ['low'],
				close = df ['close']
			)
		]
	)
	

	'''
	candle_stick_chart.add_annotation (
		x = "2024-01-03T03:00:00+00:00",
		y = 45279.3,
		
		text = 'text?',
		showarrow = False,
		yshift = 10
	)
	'''


	# Do not show OHLC's rangeslider plot 
	'''
	candle_stick_chart.update (
		layout_xaxis_rangeslider_visible = False
	)
	'''

	#fig.data[1].increasing.fillcolor = color_hi_fill
	#figure.increasing.line.color = 'rgba (200,0,130,1)'
	
	##fig.data[1].decreasing.fillcolor = 'rgba(0,0,0,0)'
	#figure.decreasing.line.color = 'rgba (200,130,0,1)'

	figure.data[0].increasing.line.color = 'rgba (200,0,130,1)'
	
	#fig.data[1].decreasing.fillcolor = 'rgba(0,0,0,0)'
	figure.data[0].decreasing.line.color = 'rgba (200,130,0,1)'

	#fig.update_layout (height=600, width=600, title_text="Stacked Subplots")
	
	
	return figure;