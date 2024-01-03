import pkg_resources
import pandas as pd
import numpy as np
from json import loads
import matplotlib.pyplot as plt
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
import logging
import warnings
warnings.simplefilter(action = "ignore") 
pd.set_option('display.max_colwidth', None)
pd.options.display.float_format = '{:.3f}'.format

logger = logging.getLogger()

#distributions = get_common_distributions()
default_distributions = [ 'norm','expon','uniform','triang','lognorm','gamma' ]

start_time = 'start_time'
end_time = 'end_time'
case_id =  'case_id' 
interval = 'interval'
timeout = 120


class EventLog:
  
  def __init__( self, log, timestamp_format = '%Y-%m-%d %H:%M:%S.%f', verbose = False ):
    #df = pd.read_csv( BytesIO( log ), sep="," )
    self.data = log
    self.distributions = default_distributions
    columns = list( self.data.columns )   
    new_columns = [ case_id if c.lower().startswith('case') else c for c in columns ]
    new_columns = [ start_time if c.lower().startswith('start') else c for c in new_columns ]
    new_columns = [ end_time if c.lower().startswith('end') else c for c in new_columns ]
    self.data[new_columns] = self.data[ columns ] 
    self.data[ start_time ] = pd.to_datetime(self.data[ start_time ], format = timestamp_format )
    self.data[ end_time ] = pd.to_datetime(self.data[ end_time ], format = timestamp_format )

    if verbose:  
      msg = "Using piops version: " + pkg_resources.get_distribution("piops").version
      print(msg)
      print( "Log with the following columns: ", new_columns )
      print( "Testing the following distributions by default: ", self.distributions )

    self.data[ 'duration' ] =   self.data[ end_time ].sub(self.data[ start_time ]).dt.total_seconds().div(60)
    self.data = self.data.sort_values(by= start_time )


  def __str__( self ):
    return self.data.to_csv( index = False )

  def metadata( self ):
    return pd.DataFrame( np.array([[ 'With ' + str(self.data.shape[0]) + ' Rows, ' + str(self.data.shape[1]) + ' Columns and ' + str( self.data.memory_usage(index=True).sum()/1024 ) + 'KB of Total Memory used', 
                                    self.data['start_time'].min(), self.data['end_time'].max(), self.data.shape[0] , self.data[ case_id ].nunique() , self.data[ 'Activity' ].nunique() , self.data[ 'Role' ].nunique() , self.data[ 'Resource' ].nunique(), ', '.join(self.data.columns) ]]) ,  
                                    columns = [ 'Event Log', 'Start', 'End', 'Events', 'Cases', 'Activities', 'Roles', 'Resources','Column Names']).set_index('Event Log')

  def intervalDistribution( self ):
    df = self.data.copy()
    df = df.drop_duplicates(subset=[ case_id ])
    df[ interval ] = df[ start_time ].diff()
    df[ interval ] = df[ interval ].dt.total_seconds().div(60)
    df.drop(0,axis=0, inplace=True)
    f = Fitter( df[  interval  ], timeout = timeout, distributions = self.distributions )
    f.fit()
    results= {"Cases Interval": {"distribution": list(f.get_best().keys())[0], "parameters" : list(f.get_best().values())[0] }}
    dist = pd.DataFrame.from_dict( results, orient='index' )
    return dist
  

  def intervalStatistics( self ):
    df = self.data.copy()
    df = df.drop_duplicates(subset=[ case_id ])
    df['Cases Interval'] = df[ start_time ].diff()
    df['Cases Interval'] = df['Cases Interval'].dt.total_seconds().div(60)
    df.drop(0,axis=0, inplace=True)
    interval = df['Cases Interval']
    stats = interval.describe().to_frame().T
    stats.insert(loc = 3, column = 'var', value = interval.var() )
    stats.insert(loc = 4, column = 'skew', value = interval.skew() )
    stats.insert(loc = 5, column = 'kurt', value = interval.kurt() )
    return stats
  

  def activitiesDistribution( self ):
    activities_list = list(self.data[ 'Activity' ].unique())
    results = {}
    for activity in activities_list:
        act = self.data[self.data[ 'Activity' ] == activity ]
        f = Fitter( act[ 'duration' ], timeout = timeout, distributions = self.distributions )
        f.fit()
        results[activity] = {"distribution": list(f.get_best().keys())[0], "parameters" : list(f.get_best().values())[0] }
        dist = pd.DataFrame.from_dict( results, orient='index' )
    return dist


  def activitiesStatistics( self ):
    df = self.data.copy()
    activities = df.groupby([ 'Activity' ])[ 'duration' ]
    stats = activities.describe()
    stats.insert(loc = 3, column = 'var', value = activities.var() )
    stats.insert(loc = 4, column = 'skew', value = activities.skew() )
    stats.insert(loc = 5, column = 'kurt', value = activities.apply(pd.Series.kurt) )
    return stats
  

  def summary( self, distributions = None, verbose = False ):
    if distributions is not None: self.distributions = distributions
    if verbose:  print( "Using the following distributions:", self.distributions )
    summary = pd.concat([ self.intervalDistribution().join( self.intervalStatistics() ), self.activitiesDistribution().join( self.activitiesStatistics() ) ] )
    summary['count'] = summary['count'].astype('int')
    self.distributions = default_distributions
    return  summary
  

  def activities( self, activity = 'Activity', verbose = False ):
    if activity in self.data.columns: return self.data[ activity ].value_counts().to_frame()
    else: print("No column named", activity, ". Make sure you have a column with that name, or as Activity.")


  def boxplot( self, dimension = 'Activity', figsize = (20,5), fontsize = 10, rot = 45, verbose = False ):
    return self.data.boxplot( by = dimension, column = [ 'duration' ], figsize = figsize, fontsize = fontsize, rot = rot )
  

  def hist( self, dimension = 'numeric', exclude = [], bins = 20, figsize = (20,5), fontsize = 10, verbose = False ):
    if dimension == 'numeric': return self.data.hist( bins = bins, figsize = figsize )
    elif dimension == 'categoric':
        # Prepare figure. Create individual axes where each bar plot will be placed
        categorical_vars =  list( set( self.data.columns ) - set( self.data._get_numeric_data().columns ).union( set( exclude ) ).union( set( [ start_time, end_time ] ) ) )
        fig, axes = plt.subplots(1, len( categorical_vars ), figsize = figsize )
        # Iterate across axes objects and associate each bar plot
        for ax, feat in zip(axes.flatten(), categorical_vars):
            feat_sorted = self.data[feat].value_counts().sort_values(ascending = False) # Sort the values in ascending order
            sns.barplot(y=feat_sorted.index, x=feat_sorted.values, ax=ax, palette='muted')
            ax.set_title(feat, fontsize = fontsize)
            ax.set_xlabel('Frequency', fontsize = fontsize)
        title = "Absolute Frequencies"
        plt.suptitle(title)
        sns.despine()
        plt.tight_layout()
        plt.show()
    else:  print("Wrong dimension. Valid values are 'numeric' | 'categoric'")


  def roles( self, role = 'Role', verbose = False ):
    if role in self.data.columns: return self.data[ role ].value_counts().to_frame()
    else: print("No column named", role, ". Make sure you have a column with that name, or as Role.")


  def resources( self, resource = 'Resource', verbose = False ):
    if resource in self.data.columns: return self.data[ resource ].value_counts().to_frame()
    else: print("No column named", resource, ". Make sure you have a column with that name, or as Resource.")


  def workhours( self, verbose = False ):
    new_log = self.data.copy()
    new_log['start_time2'] = pd.to_datetime( new_log['start_time'] ).dt.time
    new_log['end_time2'] = pd.to_datetime( new_log['end_time'] ).dt.time
    summary = new_log.groupby([ 'Role' ])['start_time2'].min().to_frame('Min. Hours')
    summary['Max. Hours'] = new_log.groupby([ 'Role' ])['end_time2'].max().to_frame()
    return summary
  

  def teams( self, dimension = 'Role', verbose = False ):
    summary = self.data.drop_duplicates([ dimension,'Resource'])[[ dimension ,'Resource']]
    summary= summary.groupby( [ dimension ], group_keys=True, as_index=True)['Resource'].apply(lambda x: x).to_frame()
    return summary