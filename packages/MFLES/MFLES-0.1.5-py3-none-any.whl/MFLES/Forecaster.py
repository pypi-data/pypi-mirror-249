# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from MFLES.Conformal import get_interval
from MFLES.Model import median, ses_ensemble, ols, fast_ols, lasso_nb, siegel_repeated_medians
from MFLES.FeatureEngineering import (get_basis,get_future_basis,get_fourier_series)
from MFLES.utils import (calc_cov,calc_seas_strength,calc_trend_strength,
                       cap_outliers,calc_rsq,calc_mse, cross_validation,
                       set_fourier)


class MFLES:
    def __init__(self, robust=None):
        self.penalty = None
        self.trend = None
        self.seasonality = None
        self.robust = robust
        self.const = None
        self.aic = None
        self.upper = None
        self.lower= None

    def fit(self,
            y,
            seasonal_period=None,
            fourier_order=None,
            ma=None,
            alpha=.1,
            decay=-1,
            n_changepoints=.25,
            seasonal_lr=.9,
            ets_lr=1,
            linear_lr=.9,
            cov_threshold=.7,
            moving_medians=False,
            max_rounds=10,
            min_alpha=.05,
            max_alpha=1.0,
            trend_penalty=True,
            multiplicative=None,
            changepoints=True,
            smoother=False,
            calc_aic=False):
        """
        

        Parameters
        ----------
        y : TYPE
            DESCRIPTION.
        seasonal_period : TYPE, optional
            DESCRIPTION. The default is None.
        fourier_order : TYPE, optional
            DESCRIPTION. The default is None.
        ma : TYPE, optional
            DESCRIPTION. The default is None.
        alpha : TYPE, optional
            DESCRIPTION. The default is .1.
        decay : TYPE, optional
            DESCRIPTION. The default is -1.
        n_changepoints : TYPE, optional
            DESCRIPTION. The default is .25.
        seasonal_lr : TYPE, optional
            DESCRIPTION. The default is .9.
        ets_lr : TYPE, optional
            DESCRIPTION. The default is 1.
        linear_lr : TYPE, optional
            DESCRIPTION. The default is .9.
        cov_threshold : TYPE, optional
            DESCRIPTION. The default is .7.
        moving_medians : TYPE, optional
            DESCRIPTION. The default is False.
        max_rounds : TYPE, optional
            DESCRIPTION. The default is 10.
        min_alpha : TYPE, optional
            DESCRIPTION. The default is .05.
        max_alpha : TYPE, optional
            DESCRIPTION. The default is 1.0.
        trend_penalty : TYPE, optional
            DESCRIPTION. The default is True.
        multiplicative : TYPE, optional
            DESCRIPTION. The default is None.
        changepoints : TYPE, optional
            DESCRIPTION. The default is True.
        smoother : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        if len(y) < 4 or np.all(y == np.mean(y)):
            print('series too short or input is constant, defaulting to mean')
            self.trend = np.append(y[-1], y[-1])
            self.seasonality = np.zeros(len(y))
            self.trend_penalty = False
            self.mean = 0
            self.std = 0
            return np.tile(y[-1], len(y))
        og_y = y
        self.og_y = og_y
        y = y.copy()
        n = len(y)
        k = 0
        if n_changepoints is None:
            changepoints = False
        if isinstance(n_changepoints, float) and n_changepoints < 1:
            n_changepoints = int(n_changepoints * n)
        self.linear_component = np.zeros(n)
        self.seasonal_component = np.zeros(n)
        self.ses_component = np.zeros(n)
        self.median_component = np.zeros(n)
        if multiplicative is None:
            if seasonal_period is None:
                multiplicative = False
            else:
                multiplicative = True
            if min(y) <= 0:
                multiplicative = False
        if multiplicative:
            self.const = y.min()
            y = np.log(y)
        else:
            self.const = None
            self.std = np.std(y)
            self.mean = np.mean(y)
            y = (y - self.mean) / self.std
        if seasonal_period is not None:
            if not isinstance(seasonal_period, list):
                seasonal_period = [seasonal_period]
        self.trend_penalty = trend_penalty
        if moving_medians and seasonal_period is not None:
            fitted = median(y, max(seasonal_period))
            k += int(n / max(seasonal_period))
        else:
            k += 1
            fitted = median(y, None)
        self.median_component += fitted
        self.trend = np.append(fitted.copy()[-1:], fitted.copy()[-1:])
        mse = None
        equal = 0
        if ma is None:
            ma_cycle = cycle([1])
        else:
            if not isinstance(ma, list):
                ma = [ma]
            ma_cycle = cycle(ma)
        if seasonal_period is not None:
            seasons_cycle = cycle(list(range(len(seasonal_period))))
            self.seasonality = np.zeros(max(seasonal_period))
            fourier_series = []
            for period in seasonal_period:
                if fourier_order is None:
                    fourier = set_fourier(period)
                else:
                    fourier = fourier_order
                fourier_series.append(get_fourier_series(n,
                                                    period,
                                                    fourier))
            k += int(np.shape(fourier_series[0])[1] / 2)
        else:
            self.seasonality = None
        for i in range(max_rounds):
            resids = y - fitted
            if mse is None:
                mse = calc_mse(y, fitted)
            else:
                if mse <= calc_mse(y, fitted):
                    if equal == 6:
                        break
                    equal += 1
                else:
                    mse = calc_mse(y, fitted)
            if seasonal_period is not None:
                seasonal_period_cycle = next(seasons_cycle)
                seas = ols(fourier_series[seasonal_period_cycle],
                           resids)
                seas = seas * seasonal_lr
                component_mse = calc_mse(y, fitted + seas)
                if mse > component_mse:
                    mse = component_mse
                    fitted += seas
                    resids = y - fitted
                    self.seasonality += np.resize(seas[-seasonal_period[seasonal_period_cycle]:],
                                                  len(self.seasonality))
                    self.seasonal_component += seas
            if i % 2:
                if self.robust:
                    tren = siegel_repeated_medians(x=np.arange(n),
                                    y=resids)
                    k += 1
                else:
                    if i==1 or not changepoints:
                        tren = fast_ols(x=np.arange(n),
                                        y=resids)
                        k += 1
                    else:
                        lbf = get_basis(y=resids,
                                        n_changepoints=min(n_changepoints, int(.1*n)),
                                        decay=decay)
                        k += np.shape(lbf)[1]
                        tren = np.dot(lbf, lasso_nb(lbf, resids, alpha=alpha))
                        tren = tren * linear_lr
                component_mse = calc_mse(y, fitted + tren)
                if mse > component_mse:
                    mse = component_mse
                    fitted += tren
                    self.linear_component += tren
                    self.trend += tren[-2:]
                    if i == 1:
                        self.penalty = calc_rsq(resids, tren)
            elif i > 4 and not i % 2:
                if smoother is None:
                    if seasonal_period is not None:
                        len_check = int(max(seasonal_period))
                    else:
                        len_check = 12
                    if resids[-1] > np.mean(resids[-len_check:-1]) + 3 * np.std(resids[-len_check:-1]):
                        smoother = 0
                    if resids[-1] < np.mean(resids[-len_check:-1]) - 3 * np.std(resids[-len_check:-1]):
                        smoother = 0
                    if resids[-2] > np.mean(resids[-len_check:-2]) + 3 * np.std(resids[-len_check:-2]):
                        smoother = 0
                    if resids[-2] < np.mean(resids[-len_check:-2]) - 3 * np.std(resids[-len_check:-2]):
                        smoother = 0
                    if smoother is None:
                        smoother = 1
                    else:
                        resids[-2:] = cap_outliers(resids, 3)[-2:]
                k += len(y)
                tren = ses_ensemble(resids,
                                    min_alpha=min_alpha,
                                    max_alpha=max_alpha,
                                    smooth=smoother*1,
                                    order=next(ma_cycle)
                                    )
                tren = tren * ets_lr
                component_mse = calc_mse(y, fitted + tren)
                if mse > component_mse + .01 * mse:
                    mse = component_mse
                    fitted += tren
                    self.ses_component += tren
                    self.trend += tren[-1]
            if i == 0:
                if self.robust is None:
                    try:
                        if calc_cov(resids, multiplicative) > cov_threshold:
                            self.robust = True
                        else:
                            self.robust = False
                    except:
                        self.robust = True

            if i == 1:
                resids = cap_outliers(resids, 5)
        if multiplicative:
            fitted = np.exp(fitted)
        else:
            fitted = self.mean + (fitted * self.std)
        if calc_aic:
            self.aic = 2 * k + n * np.log(np.sum((og_y - fitted)**2) / n)
        self.multiplicative = multiplicative
        self.fitted = fitted
        return fitted

    def predict(self, forecast_horizon):
        last_point = self.trend[1]
        slope = last_point - self.trend[0]
        if self.trend_penalty and self.penalty is not None:
            slope = slope * max(0, self.penalty)
        line = slope * np.arange(1, forecast_horizon + 1) + last_point
        if self.seasonality is not None:
            predicted = line + np.resize(self.seasonality, forecast_horizon)
        else:
            predicted = line
        if self.const is not None:
            predicted = np.exp(predicted)
        else:
            predicted = self.mean + (predicted * self.std)
        self.predicted = predicted
        return predicted

    def conformal(self, y, forecast_horizon, n_windows, coverage, **kwargs):
        intervals = get_interval(y,
                                 forecast_horizon,
                                 n_windows, coverage,
                                 self,
                                 **kwargs)
        self.fitted = self.fit(y, **kwargs)
        self.predicted = self.predict(forecast_horizon)
        if isinstance(coverage, list):
            upper = []
            lower = []
            for i in range(len(coverage)):
                upper.append(np.append(self.fitted + intervals[0][i],
                                       self.predicted + intervals[1][i]))
                lower.append(np.append(self.fitted - intervals[0][i],
                                       self.predicted - intervals[1][i]))
        else:
            upper = np.append(self.fitted + intervals[0],
                              self.predicted + intervals[1])
            lower = np.append(self.fitted - intervals[0],
                              self.predicted - intervals[1])
        self.upper = upper
        self.lower = lower
        return np.append(self.fitted, self.predicted), upper, lower

    def seasonal_decompose(self, y, seasonal_period, **kwargs):
        fitted = self.fit(y, seasonal_period, **kwargs)
        trend = self.linear_component
        level = self.median_component + self.ses_component
        seasonality = self.seasonal_component
        if self.multiplicative:
            trend = np.exp(trend)
            level = np.exp(level)
            if seasonal_period is not None:
                seasonality = np.exp(seasonality)
            trend = trend * level
        else:
            trend = self.mean + (trend * self.std)
            level = self.mean + (level * self.std)
            if seasonal_period is not None:
                seasonality = self.mean + (seasonality * self.std)
            trend = trend + level - self.mean
        residuals = y - fitted
        self.decomposition = {'y': y,
                              'trend': trend,
                              'seasonality': seasonality,
                              'residuals': residuals
            }
        return self.decomposition

    def plot(self):
        plt.style.use("ggplot")
        plt.plot(np.append(self.fitted, self.predicted), color='red', linestyle='dashed')
        plt.plot(self.og_y, color='black')
        colors = ['royalblue', 'lightblue', 'lightsteelblue', 'lightgrey']
        if self.upper is not None:
            if not isinstance(self.upper, list):
                self.upper = [self.upper]
                self.lower = [self.lower]
            for i in range(len(self.upper)):
                colors = colors[:len(self.upper)]
                plt.fill_between(range(len(self.upper[0])),
                                         self.upper[i],
                                         self.lower[i],
                                         color=colors[i],
                                         alpha=.7)
        plt.show()

    def plot_decomposition(self):
        plt.style.use("ggplot")
        fig, ax = plt.subplots(3)
        ax[0].plot(self.decomposition['trend'])
        ax[0].plot(self.decomposition['y'],
                   alpha=.5,
                   linestyle='dashed')
        ax[1].plot(self.decomposition['seasonality'])
        if self.multiplicative:
            detrended = self.decomposition['y'] / self.decomposition['trend']
        else:
            detrended = self.decomposition['y'] - self.decomposition['trend']
        ax[1].plot(detrended,
                   alpha=.5,
                   linestyle='dashed')
        cmap = plt.cm.Reds
        ax[2].scatter(range(len(detrended)), y=self.decomposition['residuals'],
                   color=cmap(np.abs(self.decomposition['residuals']) / np.mean(np.abs(self.decomposition['residuals']))))
        ax[0].set_title('Trend')
        ax[1].set_title('Seasonality')
        ax[2].set_title('Residuals')
        plt.tight_layout()
        plt.show()

