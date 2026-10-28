import numpy as np
from sklearn.metrics import mean_absolute_error,mean_squared_error
def metrics(y_true,y_pred):
    y=np.asarray(y_true,dtype=float);p=np.maximum(0,np.asarray(y_pred,dtype=float))
    return {"mae_kg":round(float(mean_absolute_error(y,p)),3),"rmse_kg":round(float(np.sqrt(mean_squared_error(y,p))),3),"wape_pct":round(float(100*np.abs(y-p).sum()/max(1e-8,y.sum())),2),"n":len(y)}
