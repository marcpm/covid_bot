from cov_stats import DataSystem
from bot_comms import _compose_message, push


def main():
    system = DataSystem(countries=["Spain", "China"])
    system.update()
    query = system.daily_stats("Spain", "China", metric="deaths", rolling_days=3, y_0=5, plots=True)
    message = _compose_message(query)
    push(message, query["fig_path"], target="telegram")
    
if __name__ == "__main__":
    main()