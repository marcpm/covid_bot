import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

def _delta(current, reference):
    return current - reference

def _delta_percent(current, reference):
    return (current / reference - 1) * 100


class DataSystem:
    def __init__(self, countries=[]):
        self.countries= countries
        self.data = None

    
    def update(self):
        URL = "https://pomber.github.io/covid19/timeseries.json"
        _dat = requests.get(URL).json()
        self.data = {country: CountryData(country, _dat) for country in self.countries}


    def daily_stats(self, country, ref_country, metric="deaths", rolling_days=3, y_0=10, plots=True, show=False):
        """ gets daily metrics on rolling days, y_0 refers to metric at the day used as starting date. e.g. default: deaths metrics starting from 10 deaths.
        """
        register_matplotlib_converters()
        country = self.data[country]
        ref_country = self.data[ref_country]
        df = country.get_df()
        df_ref = ref_country.get_df()

        new_metric = "{}day_{}".format(rolling_days, metric)
        df[new_metric] = df.loc[df[metric] > y_0][metric] - df.loc[df[metric] > y_0][metric].shift(rolling_days, fill_value=0)

        df2 = df.loc[df[metric] > y_0] - df.loc[df[metric] > y_0].shift(rolling_days, fill_value=0)

        df_ref[new_metric] = df_ref.loc[df_ref[metric] > y_0][metric] - df_ref.loc[df_ref[metric] > y_0][metric].shift(rolling_days, fill_value=0)

        df_ref2  = df_ref.loc[df_ref[metric] > y_0] - df_ref.loc[df_ref[metric] > y_0].shift(rolling_days, fill_value=0)

        n_days = df_ref2.shape[0]
        idx = pd.date_range(df2.index[0] , df2.index[0] + pd.Timedelta("{} days".format(n_days)))
        df2 = df2.reindex(idx, fill_value=0)
        dateformat = mdates.DateFormatter('%d %b')

        if plots:
            fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 5), gridspec_kw={"height_ratios": [3,2]})
            axes[0].bar(df2.index, df2[metric], color="darkblue")
            axes[0].set_title("{} {}-day {}".format(country.name, rolling_days, metric.title()))
            axes[0].set_ylabel(str(metric).title())
            axes[0].xaxis.set_major_formatter(dateformat)

            axes[1].bar(df_ref2.index, df_ref2[metric], color="mediumseagreen")
            axes[1].set_title("{}  {}-day {}".format(ref_country.name, rolling_days, metric.title()))
            axes[1].set_ylabel(str(metric).title())
            axes[1].xaxis.set_major_formatter(dateformat)

            fig.tight_layout()
            if show: 
                plt.show()
            file_path = "{}.png".format(new_metric)
            fig.savefig(file_path)

        new_data = df[new_metric][-1]
        new_data_delta = _delta_percent(df[new_metric][-1], df[new_metric][-2])
        daily_deaths = df["daily_deaths"][-1]
        daily_deaths_delta = _delta_percent(df["daily_deaths"][-1], df["daily_deaths"][-2])
        return {"fig_path": file_path , "new_data": new_data, "new_data_delta": new_data_delta, 
                "daily_deaths": daily_deaths, "daily_deaths_delta": daily_deaths_delta, "date": df.index[-1].strftime("%d %B" )}


class CountryData:
    def __init__(self, name, data_json):
        self.name = name
        self.data = data_json[name]
        self.df = self.setup_data()

    def setup_data(self):
        country_df = pd.DataFrame(self.data)
        country_df["date"] = country_df["date"].apply(pd.to_datetime)
        country_df.index = country_df["date"]
        country_df["daily_deaths"] = country_df["deaths"] - country_df["deaths"].shift(1)
        return country_df

    def get_df(self):
        return self.df
