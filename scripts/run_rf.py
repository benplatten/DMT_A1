import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def run_rf(df,num_days):

    target = df['target']

    features= df[['call','circumplex.valence','circumplex.arousal','mood','screen','appCat.entertainment','sms']] #df.drop(['target','id'], axis = 1)
    feature_list = list(features.columns)
    features = np.array(features)

    train_features, test_features, train_target, test_target = train_test_split(features, target, test_size = 0.25, random_state = 42)

    rf = RandomForestRegressor(n_estimators = 1000)

    rf.fit(train_features, train_target);

    # Use the forest's predict method on the test data
    predictions = rf.predict(test_features)
    # Calculate the absolute errors
    errors = abs(predictions - test_target)
    # Print out the mean absolute error (mae)
    mae = round(np.mean(errors), 2)
    mse = mean_squared_error(test_target,predictions)
    rmse = np.sqrt(mse)

    output_data = {
    'num_days':[num_days],
    'mse' :[mse],
    'mae':[mae],
    'rmse':[rmse]
    }

    output_df = pd.DataFrame (output_data, columns = ['num_days','mse','mae','rmse'])

    return output_df





