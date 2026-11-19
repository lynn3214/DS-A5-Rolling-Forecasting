import numpy as np

def summarize(y,p):
    m=np.isfinite(y)&np.isfinite(p); err=p[m]-y[m]
    return {'count':int(m.sum()),'mae':float(np.mean(np.abs(err))) if len(err) else None,'rmse':float(np.sqrt(np.mean(err**2))) if len(err) else None}
