from aggregate_data import aggregateData
from run_rf import run_rf
import pandas as pd 


df = pd.read_csv("../../dataset_mood_smartphone_clean.csv")

i = 1
errorData =[]
while i < 15:
	print(i)
	model_data = aggregateData(df,i)
	model_error = run_rf(model_data, i)
	errorData.append(model_error)
	i+=1


errorDF = pd.concat(errorData)

errorDF.to_csv("../../errorDF.csv",index=False)
