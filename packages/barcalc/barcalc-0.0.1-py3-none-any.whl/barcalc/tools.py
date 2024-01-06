""" barcalc tools module """

import numpy as np

from scipy import stats

from sklearn.linear_model import LinearRegression

from bardata.utils import get_sampling
from bardata.prices import combine_prices


# MAYBE create function that accept prices matrix
# MAYBE move module to another package (xlquery maybe) ?
# MAYBE can we remove/archive simple_regression? does not seem to be used anywhere ... ?
# MAYBE create notebook for ab_regression (stats.lineregress)

def ab_regression(x, y, sampling=1.0, dropna=True):
    """ alpha and beta analysis (uses stats.linregress) """

    x = np.asarray(x)
    y = np.asarray(y)

    if dropna:
        mask = np.isfinite(x * y)
        x, y = x[mask], y[mask]

    res = stats.linregress(x, y)
    alpha = res.intercept * sampling
    beta = res.slope
    rvalue = res.rvalue

    result = dict(alpha=alpha, beta=beta, rvalue=rvalue)

    return result


def simple_regression(ticker, benchmark, period=None, resample=None):
    """ fetches prices and calculates alpha/beta (uses ab_regression) """

    tickers = (ticker, benchmark)
    returns = combine_prices(tickers, period=period, resample=resample, pct_change=True)

    x = returns.iloc[:, 1].values
    y = returns.iloc[:, 0].values

    sampling = get_sampling(returns)

    result = ab_regression(x, y, sampling=sampling)

    return result


def multiple_regression(ticker, basket, *,
                        period=None, resample=None,
                        positive=True, verbose=False):
    """ fetches multiple prices and calculates alpha/beta (uses LinearRegression) """

    if isinstance(basket, str):
        basket = basket.split(",")

    tickers = [ticker, *basket]
    returns = combine_prices(tickers, period=period, resample=resample, pct_change=True)

    sampling = get_sampling(returns)

    y = returns.get(ticker).values
    X = returns.drop(columns=ticker).values

    model = LinearRegression(positive=positive)

    model.fit(X, y)

    rsquare = model.score(X, y)
    rvalue = rsquare ** 0.5 if rsquare > 0 else np.nan

    if verbose:
        print(vars(model))

    alpha = model.intercept_ * sampling
    beta = np.sum(model.coef_)

    result = dict(alpha=alpha, beta=beta, rvalue=rvalue)

    return result


def closest_regression(ticker, benchmarks, period=None, resample=None):
    """ fetches prices for ticker and benchmark and return info about closest benchmark """

    if isinstance(benchmarks, str):
        benchmarks = benchmarks.split(",")

    tickers = [ticker, *benchmarks]
    returns = combine_prices(tickers, period=period, resample=resample, pct_change=True)

    sampling = get_sampling(returns)
    x = returns.get(ticker)

    closest = None

    for benchmark in benchmarks:
        y = returns.get(benchmark)
        result = ab_regression(x, y, sampling=sampling)
        if closest is None or result.get('rvalue') > closest.get('rvalue'):
            closest = dict(result, benchmark=benchmark)

    return closest


def capture_ratios(ticker, market, period=None, resample=None):
    """ fetches prices and calculates capture ratios """

    tickers = (ticker, market)
    returns = combine_prices(tickers, period=period, resample=resample, pct_change=True)

    y = returns.iloc[:, 0]
    x = returns.iloc[:, 1]

    mask = x > 0
    upside = y[mask].mean() / x[mask].mean()

    mask = x < 0
    downside = y[mask].mean() / x[mask].mean()

    result = dict(upside=upside, downside=downside)

    return result
