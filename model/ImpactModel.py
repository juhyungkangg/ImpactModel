from model.InputGenerator import *
import numpy as np
from scipy.optimize import least_squares
from taq.MyDirectories import *
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white
from scipy.stats import norm

class ImpactModel(object):
    def __init__(self,
                 avg_daily_volatility,
                 avg_daily_value,
                 avg_daily_imbalance,
                 arrival_prices,
                 partial_vwaps,
                 full_vwaps,
                 terminal_prices,
                 total_daily_volume
                 ):
        self.avg_daily_volatility = avg_daily_volatility
        self.avg_daily_value = avg_daily_value
        self.avg_daily_imbalance = avg_daily_imbalance
        self.arrival_prices = arrival_prices
        self.partial_vwaps = partial_vwaps
        self.full_vwaps = full_vwaps
        self.terminal_prices = terminal_prices
        self.total_daily_volume = total_daily_volume

        self.h = (self.partial_vwaps - self.arrival_prices) - (self.terminal_prices - self.arrival_prices) / 2
        # Divide h with arrival prices according to the paper (p.10)
        self.h = self.h / self.arrival_prices

        self.eta = None
        self.beta = None
        self.result = None
        self.residuals = None

        self.filtered_indices = None

        self.x_filtered = None
        self.v_filtered = None
        self.sigma_filtered = None
        self.h_filtered = None

    def set_X(self, X):
        self.avg_daily_imbalance = X

    def set_h(self, h):
        self.h = h

    def set_V(self, V):
        self.avg_daily_value = V

    def set_sigma(self, sigma):
        self.avg_daily_volatility = sigma

    def fit(self, init_params, threshold=0.00025, exclude_outliers=False):
        # Define an objective function
        def objective_func(params, x, v, sigma, h):
            model = params[0] * sigma * np.sign(x) * (np.abs(x/((6/6.5)*v))**params[1])
            residuals = model - h

            return residuals

        # Get the observed data
        x = self.avg_daily_imbalance.flatten('F')
        v = self.avg_daily_value.flatten('F')
        sigma = self.avg_daily_volatility.flatten('F')
        h = self.h.flatten('F')

        # Filter small orders (imbalance) according to the paper
        filtered_x_indices = np.where(np.abs(x/((6/6.5)*v)) > threshold)[0]
        self.filtered_indices = filtered_x_indices

        # Fiter the observed data
        x = x[filtered_x_indices]
        v = v[filtered_x_indices]
        sigma = sigma[filtered_x_indices]
        h = h[filtered_x_indices]

        # Exclude outliers based on h
        if exclude_outliers:
            # Calculate the percentile values
            lower_value = np.percentile(h, 2.5)
            upper_value = np.percentile(h, 97.5)

            # Filter indices within the percentile range
            filtered_h_indices = np.where((h >= lower_value) & (h <= upper_value))[0]

            # Fiter the observed data
            x = x[filtered_h_indices]
            v = v[filtered_h_indices]
            sigma = sigma[filtered_h_indices]
            h = h[filtered_h_indices]

            # Save filtered indexes
            self.filtered_indices = np.array([self.filtered_indices[i] for i in filtered_h_indices.tolist()])

        # Save filtered data
        self.x_filtered = x
        self.v_filtered = v
        self.sigma_filtered = sigma
        self.h_filtered = h

        # Call least squares optimization
        # Set the bound of beta as (0,1) based on the Almgren paper
        result = least_squares(objective_func, init_params, method='trf',
                               bounds=([-np.inf, 0.0001], [np.inf, 0.999]), args=(x, v, sigma, h))

        # Extract the optimized parameters
        eta, beta = result.x
        self.eta = eta
        self.beta = beta
        self.result = result

        # Calculate residuals
        self.residuals = objective_func((eta,beta), x, v, sigma, h)

    def plot_residuals(self, comment=""):
        plt.scatter(self.sigma_filtered, self.residuals)
        plt.xlabel('sigma')
        plt.ylabel('residuals')
        plt.title(f'Residual vs sigma Plot{comment}')
        plt.savefig(getDataDir() + f'/plots/Residual vs sigma Plot{comment}.png')
        plt.show()

        plt.scatter(self.x_filtered/((6/6.5)*self.v_filtered), self.residuals)
        plt.xlabel('x/((6/6.5)*v)')
        plt.ylabel('residuals')
        plt.title(f'Residual vs x/v Plot{comment}')
        plt.savefig(getDataDir() + f'/plots/Residual vs xv Plot{comment}.png')
        plt.show()

        sm.qqplot(self.residuals, line='s')
        plt.title('Q-Q Plot')
        plt.savefig(getDataDir() + f'/plots/QQ Plot{comment}.png')
        plt.show()

    def plot_actual_vs_predict(self, comment=""):
        plt.scatter(self.eta*self.sigma_filtered * np.sign(self.x_filtered) * np.abs(self.x_filtered/((6/6.5)*self.v_filtered))**self.beta, self.h_filtered)
        plt.plot(self.h, self.h, color='red', linestyle='--', label='Perfect Prediction')
        plt.xlabel('h hat')
        plt.ylabel('h')
        plt.title(f'Actual vs Predicted Plot{comment}')
        plt.savefig(getDataDir() + f'/plots/Actual vs Predicted{comment}.png')
        plt.show()

    def r_squared(self):
        # R^2 = 1- (sum of (y_i - hat(y_i)**2)/(sum of (y_i - y_bar)**2)
        y = self.h_filtered
        y_bar = np.mean(y)

        SST = np.sum((y - y_bar) ** 2)
        SSR = np.sum(np.array(self.residuals)**2)

        self.r_squared_val = 1 - SSR / SST

        return self.r_squared_val

    def white_test(self):
        errors = self.residuals
        cols = (self.x_filtered / self.v_filtered, self.sigma_filtered)

        exog = np.column_stack(cols)
        exog = sm.add_constant(exog)

        res = het_white(errors, exog)
        p_vals = res[1]

        self.white_test_result = p_vals

        return self.white_test_result

    def p_values(self):
        p_vals_li = []

        residual_var = np.sum(np.array(self.residuals)**2) / (len(self.residuals) - 2)
        jacobian = self.result.jac

        # Covariance estimate for parameters
        cov = np.linalg.inv(jacobian.T @ jacobian) * residual_var
        std_err = np.sqrt(np.diag(cov))

        # Wald's test
        wald_statistic = (np.array(self.eta, self.beta) / std_err) ** 2

        # Calculate p values
        p_vals = 2 * (1 - norm.cdf(np.abs(wald_statistic)))

        self.p_vals = p_vals

        return self.p_vals

    def summary(self):
        print('eta', self.eta, 'eta pval', self.p_vals[0])
        print('beta', self.beta, 'beta pval', self.p_vals[1])
        print('r_squared', self.r_squared_val)
        print('white_p', self.white_test_result)


if __name__ == "__main__":
    lookback = 0
    percentile = 95

    ig = InputGenerator(lookback=lookback)
    ig.vol_filter(percentile=percentile)

    x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()
    impact_model = ImpactModel(x1, x2, x3, x4, x5, x6, x7, x8)

    impact_model.fit((0.2, 0.5), threshold=0.0025, exclude_outliers=False)

    impact_model.r_squared()
    impact_model.white_test()
    impact_model.p_values()

    impact_model.plot_residuals()
    impact_model.plot_actual_vs_predict()

    impact_model.summary()