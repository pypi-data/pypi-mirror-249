
'''
	import estimates.gadgets.pandas.df.from_list as df_from_list
	list = list_from_df.calc (
		df = df
	)
'''

import pandas

def calc (
	list = None
):
	df = pandas.DataFrame (list)

	return df