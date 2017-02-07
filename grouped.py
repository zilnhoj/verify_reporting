grouped = (df.groupby('RP name', 'Response type').apply(lambda g: g.set_index('Timestamp').resample('W-MON', how='count')).unstack(level=0).fillna(0)
    

    weekly_resultdf = weekly_resultdf.groupby(['RP name','Response type']).resample('W-MON')['Response type'].count()
    weekly_resultdf = weekly_resultdf.unstack(level=0)
