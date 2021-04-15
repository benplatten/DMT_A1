import pandas as pd
from datetime import datetime, timedelta

def aggregateData(df, num_days):

    df = df.sort_values(['id','time'])
    df.reset_index(drop=True,inplace=True)

    target = df[df['variable']=='mood']
    target = target.groupby(['id','date']).mean().reset_index()
    target = target.groupby(['id']).nth(-1).reset_index()

    users = list(df.id.unique())

    AggregatedTime=[]
    for i in users:
        
        AggTime = df[df['id']==i]
        targetIndex = AggTime['variable'].where(AggTime['variable']=='mood').last_valid_index()
        end_date = AggTime.loc[targetIndex].date
        start_date = str((datetime.fromisoformat(end_date) - timedelta(days=num_days)).date())
        date_range = [str(i.date()) for i in pd.date_range(start_date, end_date)]
        del date_range[-1]
        AggTime=  AggTime[AggTime['date'].isin(date_range)]
        AggregatedTime.append(AggTime)

    aDF = pd.concat(AggregatedTime)
    aDF = aDF[['id', 'variable', 'value', 'date']]
    
    average = ['mood','circumplex.arousal','circumplex.valence','activity']
    df_av = aDF[aDF['variable'].isin(average)]
    df_sum = aDF[~aDF['variable'].isin(average)]

    df_sum =df_sum.groupby(['id','variable']).sum().unstack().reset_index().sort_values(['id']).fillna(0)
    df_av =df_av.groupby(['id','variable']).mean().unstack().reset_index().sort_values(['id']).fillna(0)
    data = df_sum.merge(df_av,how='outer', on=["id"]).fillna(0)

    data.columns=data.columns.get_level_values(1)

    cols = ['id', 'appCat.builtin', 'appCat.communication',
       'appCat.entertainment', 'appCat.finance', 'appCat.game',
       'appCat.office', 'appCat.other', 'appCat.social', 'appCat.travel',
       'appCat.unknown', 'appCat.utilities', 'appCat.weather', 'call',
       'screen', 'sms', 'activity', 'circumplex.arousal', 'circumplex.valence',
       'mood']
    data.columns=cols

    target = target[['id','value']]
    target.columns = ['id','target']

    final_data = data.merge(target,how='left', on=["id"])

    return final_data









