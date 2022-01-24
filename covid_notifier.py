from src.coronavirus_manager import CovidManager

if __name__ == "__main__":
    team_fixtures_manager = CovidManager()
    team_fixtures_manager.notify_daily_stats()
