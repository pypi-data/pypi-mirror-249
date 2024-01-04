import pandas as pd

__all__ = ['Rates']
       
class Rates:
    """Class to perform operations on financial rates."""

    def __init__(self, rates):
        """
        Initialize the Rates class.

        Parameters:
        rates (pandas.DataFrame): DataFrame containing financial rates data.
        """
        self._rates = pd.DataFrame(rates)
        self._rates['time'] = pd.to_datetime(self._rates['time'], unit='s')
        self._rates['date'] = self._rates['time'].dt.date
        self._rates['hlcc'] = (self._rates['close'] * 2 + self._rates['low'] + self._rates['high']) / 4
        self._rates = self._rates[['date', 'time', 'open', 'high', 'low', 'close', 'hlcc', 'spread', 'tick_volume', 'real_volume']]

    def get_rates(self):
        """
        Get the rates DataFrame.

        Returns:
        pandas.DataFrame: DataFrame containing financial rates data.
        """
        return self._rates

    def moving_stat(self, col, how='backward', window=3, stat='mean', stat_param=None, inplace=False, new_col=None):
        """
        Calculate moving statistics for a column in the rates DataFrame.

        Parameters:
        col (str): Column name for which to calculate the statistic.
        how (str, optional): Direction for the moving statistic ('backward' or 'forward'). Default is 'backward'.
        window (int, optional): Window size for the moving statistic. Default is 3.
        stat (str, optional): Type of statistic to calculate ('mean', 'median', 'sum', 'min', 'max', 'std').
                             Default is 'mean'.
        stat_param (Any, optional): Parameter for the statistic calculation. Default is None.
        inplace (bool, optional): Whether to modify the DataFrame in-place. Default is False.
        new_col (str, optional): Name of the new column to store the calculated statistic. Default is None.

        Returns:
        pandas.Series or None: Series with calculated moving statistic if inplace=False, otherwise None.
        """
        window = int(window)
        moving = None

        if how in ['backward', 'forward']:
            if stat in ['mean', 'median', 'sum', 'min', 'max', 'std'] and stat_param is None:
                moving = getattr(self._rates[col].rolling(window), stat)()
            elif stat_param is not None:
                if stat == 'mean':
                    prod_aux = self._rates[col] * self._rates[stat_param]
                    prod_sum_aux = prod_aux.rolling(window).sum()
                    sum_aux = self._rates[stat_param].rolling(window).sum()
                    moving = prod_sum_aux / sum_aux
                elif stat == 'quantile':
                    moving = self._rates[col].rolling(window).quantile(stat_param)

        if how == 'forward' and moving is not None:
            moving = moving.shift(-window)

        if inplace:
            if not new_col:
                if stat == 'quantile':
                    new_col = f"{col}_{how[0]}wd_pctl{int(100*stat_param)}_{window}w"
                elif stat == 'mean' and stat_param:
                    new_col = f"{col}_{how[0]}wd_w{stat}_{window}w"
                else:
                    new_col = f"{col}_{how[0]}wd_{stat}_{window}w"
            self._rates[new_col] = moving
        else:
            return moving