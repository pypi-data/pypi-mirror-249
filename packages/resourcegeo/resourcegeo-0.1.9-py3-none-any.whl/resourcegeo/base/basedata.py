
import pandas as pd
import os

class TabularData: 
    """This class handles tabular data.
    """
    
    def __init__(self, flname=None):
        """
        Args:
            flname (str): Path to read file
            data (pd.DataFrame): values of data
        """
        
        if isinstance(flname,str):
            self.flname = flname
            
        self.data = pd.read_csv(filepath_or_buffer=self.flname)
        # if isinstance(data,pd.DataFrame):
            # self.data = data
            
        # else:
            # if (data is not None) and (not isinstace(data, pd.DataFrame)):
                # try:
                    # self.data = pd.DataFrame(data=data,columns=columns)
                # except:
                    # raise ValueError("Arg data could not be coerced into pd.DataFrame")

def BaseData(fl, griddef=None, **kwargs):
	"""
	Get an example data

	Args:
		testfile (str): available example files below:

		- "assay_geo": assay and lithology 
        - "collar": collar
    Return
	"""
	"""
    Generate bm.csv data
    import pandas as pd
	from random import choices
	import numpy as np
    k = 500
	dx = choices([25,50], k=k)
	dy = choices([25,50], k=k)
	dz = choices([10,5,2.5], k=k)
	otype = choices(['Oxide','Sulfide','Overburden'], k=k)
	mined = choices(['mined','unmined'], k=k)
	classif = choices([1,2,3], k=k)

	grade1 = np.random.normal(10,3,k)
	grade2 = np.random.uniform(low=10,high=25,size=k)
	density = np.random.uniform(low=2.2,high=3,size=k)

	table = {'dx':dx, 'dy':dy, 'dz':dz, 'otype':otype,
			'mined':mined, 'classification':classif,
			'grade1':grade1, 'grade2': grade2,'density':density}

	bm = pd.DataFrame.from_dict(table)
	bm.to_csv('bm.csv',index=False)
	"""

	files = {
		'assay_geo': "assay_geo.csv",
        'collar':"collar.csv",
        'bm':"bm.csv"
	}
	if fl not in files:
		raise ValueError(f"{fl} does not exist in database.")

	data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), r'base_data'))
	return TabularData(os.path.join(data_dir, files[fl]), **kwargs)


