import matplotlib.pyplot as plt
import numpy as np

def boxplot_by_category(data,var,catcol,
                        cats=None, tmin=None, 
                        ylabel=None,xlabel=None,title=None,flname=None,
                        markersize_flier=2,
                        markersize_mean=4,widths=None,
                        figsize=None,
                        ylim=None,
                        stats=True,
                        stats_ycoord=None,
                        use_all=True,
                        yscale='linear'):
    '''Univariate. Boxplots by category. Optionally add number and unweighted
    mean to the plot.

    Args:
        data (pd.DataFrame): df with values and a category column
        var(str): column name for variable
        catcol(str): column name for category column
        cats (optional): Categories to consider from catcol
        xlabel(str, optional): x-label 
        ylabel(str, optional): y-label
        figsize(tuple,optional): figsize
        flname(str, optional): path to save file if not None
        stats(bool,optional): Show number and unweighted mean for each box plot
        yscale(str, optional): y-axis scale
        stats_ycoord(float, optional): bottom coordinate to add the stats (count and mean).
            The mean is unweighted. 
        tmin (float, optional): Minumum var value to filter out values
        use_all(bool, optional): If False, plot boxplots only for categories with >0 number
            of data. If True, it shows all boxplots. If tmin is not None, then
            tmin is applied before use_all.

    **Examples:**

	.. plot::

		import resourcegeo as rs
		df = rs.BaseData('assay_geo').data
		_ = rs.boxplot_by_category(data = df,var = 'CUpc',catcol = 'UNIT',
			tmin=0, markersize_flier=0.5,widths=0.7,markersize_mean=4,
			ylim=(-0.2,2), stats_ycoord=-0.15, figsize=(17,6),stats=False, use_all=False)

	'''
    # _ = rs.boxplot_by_category(data = df,var = 'CUpc',catcol = 'UNIT',
    #     tmin=0,markersize_mean=3,markersize_flier=0.1,widths=0.5,
    #     ylim=(0,2),figsize=(10,6),stats=False,use_all=False,ylabel='CUpc')
    #     ylabel (str): fff
    #     xlabel()
    #     use_all (bool,optional): if False, only include boxplots for categories
    #         with >0 data. True shows all. 

	# .. plot::

    # """
    # TODO:
    # - Bug tmin gives errors when None
    # - Justified text for stats
    # - if use_all=False, and there's cats with 0 records, add a notice text
    #     to the plot?
    # - asc/descending sort of the boxplots as option
    # - grouping different variables does not make sense as the axis values are
    #     not different
    # - Add a weighting column
    # - add rationale for fig size depending on number of categories to plot
    # """
    # """
    # Sources:
    # - Grouped boxplots: 
    # https://rowannicholls.github.io/python/graphs/ax_based/boxplots_multiple_groups.html
    # """

    if title is None:
        title = 'Boxplots'
    if xlabel is None:
        xlabel = 'Categories'
    if ylabel is None:
        ylabel = 'Values'

    if cats is not None:
        if not isinstance(cats, list):
            try:
                cats = str(cats)
            except:
                raise ValueError('Could not coerce cats to list')
        data = data.loc[data[catcol].isin(cats)]

    vals, labels = data_by_category(data,var,catcol,tmin,use_all)

    c = 'gray'
    rotation=90

    medianprops = dict(linestyle='-', linewidth=0.8, color='k')
    meanpointprops = dict(marker='s',
                        markeredgecolor='black',
                        markerfacecolor='black',
                        markersize=markersize_mean)
    flierprops = dict(
                    markeredgecolor=c,
                    markersize=markersize_flier,
                    markerfacecolor=c,
                    )

    #outline of boxes
    boxprops = dict(linestyle='-.-', linewidth=0.7, color='k')

    #ending transversal lines
    capprops = dict(color='k',linewidth=0.7)

    #vertical lines from box to cap
    whiskerprops = dict(linestyle='--', linewidth=0.7)
    
    fig, ax = plt.subplots(1,1, figsize=figsize)
    bplot1 = ax.boxplot(vals,
                        vert=True, 
                        boxprops= boxprops,
                        patch_artist=True, 
                        showcaps=True,  
                        showmeans=True, #squared dot
                        capprops=capprops,
                        flierprops=flierprops,
                        medianprops=medianprops,
                        meanprops=meanpointprops,
                        whiskerprops=whiskerprops,
                        widths=widths,
                        labels=labels)  
    
    #global min and max
    mx = np.concatenate(vals).max()
    mn = np.concatenate(vals).min()
    span = mx-mn

    #base coordinate to plot bulk stats
    if stats_ycoord is None:
        stats_ycoord=0
    rotation=90

    if stats:
        fontsize=7
        for i, arr in enumerate(vals,1):
            count = str(len(arr))
            if len(arr)>0:
                mean = str(round(arr.mean(),2))

                ax.text(i-0.4,
                        stats_ycoord,
                        f'n:{count}',
                        color='blue',
                        horizontalalignment='left',
                        rotation=rotation,
                        fontsize=fontsize)

                ax.text(i-0.4+0.4,
                        stats_ycoord,
                        f'm:{mean}',
                        color='blue',
                        horizontalalignment='left',
                        fontsize=fontsize,
                        rotation=rotation
                        )
            else:
                ax.text(i,
                        stats_ycoord,
                        f'n:{count}',
                        color='blue',
                        horizontalalignment='center',
                        rotation=rotation,
                        fontsize=fontsize)
    
    ax.yaxis.grid(True, lw=0.3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)
    ax.set_title(title)
    _ = plt.xticks(rotation=rotation)
    plt.yscale(yscale)

    if flname is not None:
        plt.savefig(flname,bbox_inches='tight')

    return vals

def data_by_category(data,var,catcol,tmin=None,use_all=True):
    '''Convert df with category to list of arrays vals + labels.

    Return:
    df_values (list[np.array]): array-values for each category
    df_labels (list[str]) : Categorical labels
    '''
    x =  data.assign(index=data.groupby(catcol).cumcount()).pivot(
        index='index',columns=catcol,values=var)
    df_columns = list(x.columns)
    df_array = x.to_numpy()

    df_values = []
    df_labels = []
    for i,j in enumerate(df_columns):
        slice = df_array[:,i]
        slice = slice[np.logical_not(np.isnan(slice))]
        #filter by tmin values
        if tmin is not None: slice = slice[slice>tmin]

        if use_all==True:
            df_values.append(slice)
            df_labels.append(j)
        else:
            if len(slice)>0:
                df_values.append(slice)
                df_labels.append(j)
    #df_values = [el[el>tmin] for el in df_values if tmin is not None]
    return df_values, df_labels


def boxplot_by_category_sensitivity(dfs,var,catcol,
    yscale = 'linear',markersize_flier=2,markersize_mean=4,flname=None,
    figsize=None,title=None,xlabel=None,ylabel=None,bulkstats=True,
    coverage=0.75,stats_ycoord=0,ylim=None):
    '''
    Univariate. Grouped boxplots by categories. It can be used to
    analyze sensitivity results.

    Args:
        dfs(list[pd.DataFrame]): list of DataFrame(s)
        var(str): shared variable column-name in all df in dfs
        catcol(str): shared category column in all df in dfs
        title(str, optional): title of the graph
        xlabel(str, optional): x-label
        ylabel(str, optional): y-label
        flname(str., optional): path to save file if not None
        figsize(tuple, optional): figsize
        bulkstats(bool, optional): show number and unweighted mean
        ylim(tuple, optional): y-axis coordinate limits. If bulkstats is True,
            you may need to use a lower y-minimum coordinate.
        stats_ycoord(float): bottom coordinate to add the stats (count and mean).
            The mean is unweighted.
        coverage(float, optional): width of boxes expresed as fraction from 0 to 1.

    **Examples:**

	.. plot::

		import resourcegeo as rs
		df = rs.BaseData('assay_geo').data
		df2 = df.loc[df['UNIT'].isin([f'{i}' for i in range(1,9)]  + ['OVB'])].copy()
		df3 = df2.copy()
		df3['CUpc'] = df3['CUpc'] +0.1
		df4 = df2.copy()
		df4['CUpc'] = df3['CUpc'] +0.2
		dfs = [df2,df3,df4]
		rs.boxplot_by_category_sensitivity(dfs,'CUpc','UNIT',figsize=(14,4),
			coverage=0.9,ylim=(-0.7,2), bulkstats=True,stats_ycoord=-0.6)
    '''
    '''
    TODO:
    https://stackoverflow.com/questions/63710448/how-to
    -specify-label-colors-for-box-plots-based-on-pandas-df-column-name-label-n

    - What if not all dfs contains all categories?
    - How to manage the dfs not necessarily have same column names
    '''

    if title is None:
        title = 'Boxplots for variable sensitivity by domain'
    if xlabel is None:
        xlabel = 'Categories'
    if ylabel is None:
        ylabel = var
    c = 'gray'

    #Box properties
    medianprops = dict(linestyle='-', linewidth=0.8, color='k')
    meanpointprops = dict(marker='s',
                        markeredgecolor='black',
                        markerfacecolor='black',
                        markersize=markersize_mean)
    flierprops = dict(
                    markeredgecolor=c,
                    markersize=markersize_flier,
                    markerfacecolor=c,
                    )
    #outline of boxes
    boxprops = dict(linestyle='-.-', linewidth=0.7, color='k')
    #ending transversal lines
    capprops = dict(color='k',linewidth=0.7)
    #vertical lines from box to cap
    whiskerprops = dict(linestyle='--', linewidth=0.7)

    datasets = []
    for df in dfs:
        vals,b_labels = data_by_category(df,var,catcol,
                                            tmin=0,use_all=False)
        datasets.append(vals)

    # - Sensitivity/Compare one variable by-domain from multiple dfs
    fig, ax = plt.subplots(1,1,figsize=figsize)

    labels = b_labels
    ncats = len(labels)
    width = coverage / len(datasets)

    #Global min/max values:
    mn = 1E10
    mx = -1E10
    for arrs in datasets:
        if mn > np.concatenate(arrs).min():
            mn = np.concatenate(arrs).min()
        if mx < np.concatenate(arrs).max():
            mx = np.concatenate(arrs).max()

    text_coords=[]
    x_sens = []
    for i, arrs in enumerate(datasets,1):
        baseleft =  (1 - 0.5*coverage  + width*0.5) 
        leftmosts = baseleft + width*(i-1)

        #coords for one df, all-cats, plotted on different groups. 1meter
        xcoords = [leftmosts+ 1*j for j in range(ncats)]
        x_sens += [f'S{i}' for j in xcoords]

        _ = ax.boxplot(arrs,
                        widths= width,
                        positions= xcoords,
                        boxprops= boxprops,
                        patch_artist=True, 
                        showcaps=True,  
                        showmeans=True, #squared dot
                        capprops=capprops,
                        flierprops=flierprops,
                        medianprops=medianprops,
                        meanprops=meanpointprops,
                        whiskerprops=whiskerprops,
            )

        text_coords += xcoords
        #plot stats using arr maximum at each iteration
        if bulkstats:
            fontsize = 9
            for xcoord, arr in zip(xcoords,arrs):
                count = str(len(arr))
                if len(arr)>0:
                    mean = str(round(arr.mean(),2))

                    ax.text(xcoord,
                            #arr.max() + (0.05*mx),
                            stats_ycoord,
                            f'n:{count}',
                            color='blue',
                            horizontalalignment='right',
                            verticalalignment='bottom',
                            fontsize=fontsize,
                            rotation=90
                            )

                    ax.text(xcoord,
                            #arr.max()+  (0.05*mx), 
                            stats_ycoord,
                            f'm:{mean}',
                            color='blue',
                            horizontalalignment='left',
                            verticalalignment='bottom',
                            fontsize=fontsize,
                            rotation=90
                            )

    #Use these two lines, instead of labels=labels in set_xticks
    ax.set_xticks(np.arange(ncats) + 1)
    ax.set_xticklabels(labels)
    # space below xticks
    ax.xaxis.set_tick_params(pad=20)
    
    xlim = ax.set_xlim([baseleft-2*width, xcoords[-1]+2*width ])

    text_offset = abs(mx-mn)*0.35
    offset_below = abs(mx-mn)*0.05
    #ax.set_ylim([-7,mx+text_offset]) #mn-offset_below

    if ylim is None:    
        ylim=(mn,mx)
    ax.set_ylim(ylim)

    for x,text in zip(text_coords,x_sens):
        ax.text(x,ylim[0],text,rotation=90,
        verticalalignment='top',
        horizontalalignment='center',)

    _ = ax.set_ylabel(ylabel)
    _ = ax.set_title(title)
    #space (pad) below xticklabels
    _ = ax.set_xlabel(xlabel,labelpad=5)
    _ = plt.axhline(y = 0,color='k',lw='0.5')
    plt.yscale(yscale)

    ax.yaxis.grid(False)
    if flname is not None:
        plt.savefig(flname,bbox_inches='tight')



#add grid to sensitivity
#add separating hor line between df number and category xlabel
#add flag to do category labels vertical aswell for long ones

#implement sorted by var, by ndata, some other stat?
#stats should be on bottom? and use relative position not calculated
#there was a cat with nans so it was not shown

#perhaps for boxplots the deulta ylabel should be the variable name
#but you still can set it up to other

#boxplots sensitivity error dfs must have same lentgh and statistics 
# track these

#better add the list of variable in order for each df. and for the cat
#also add a list of cats that for this should be equal in all dfs

#there is some filtering above zero but made sensitivity plot to go nan in some df
#add a message error to point out wich df does not have data

#sensitivity plot does not have ylim? and also put stats on the bottom please

#ensure that in sensitivity plots, the dfs does not require to have the same length
#also perhaps even not the same cats but still plot the cats that exists in
#the given list