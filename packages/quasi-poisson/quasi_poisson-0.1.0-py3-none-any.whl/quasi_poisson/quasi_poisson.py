import statsmodels.api as sm
import numpy as np
import pandas as pd
from scipy.stats import t
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

def reg(Y, X, offset = None):
  """
  It estimates a Quasi-Poisson regression.
  Parameters:
    Y : A non-negative numeric vector.
    X : A matrix with numeric values.
  Returns:
    A list of regression outputs, including regression co-efficients with 
    p-values and the dispersion parameter. 
  """

  _x = sm.add_constant(X, prepend = True)

  mle = sm.GLM(Y, _x, offset = offset, 
               family = sm.families.Poisson()).fit()

  _dp = np.round(mle.pearson_chi2 / mle.df_resid, 8)
  _se = np.round(np.diag(mle.cov_params()) ** 0.5 * (_dp ** 0.5), 8)

  est = pd.DataFrame({"estimate": mle.params,
                      "std err" : _se,
                      "t_value" : np.round(mle.params / _se, 8),
                      "p_value" : 2 * (1 - t.cdf(np.abs(mle.params / _se), mle.df_resid)),
                      "vif"     : [vif(_x, i) for i in range(_x.shape[1])]})

  return({"co-efficients": est, "dispersion": _dp, "mle": mle})

