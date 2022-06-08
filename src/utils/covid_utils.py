from src.api.worldometers_covid import WorldometersClient
from src.entities import CovidStats, Country


def get_country_stats(country: dict):
    client = WorldometersClient()
    response = client.get_stats_by_country(country["name"])

    json_response = response.as_dict
    new_cases = json_response["data"]["New Cases"]
    new_deaths = json_response["data"]["New Deaths"]
    new_recovered = json_response["data"]["New Recovered"]

    return CovidStats(
        country=Country(country["name"], country["emoji"]),
        new_cases=new_cases if new_cases else "No Data Available :(",
        new_deaths=new_deaths if new_deaths else "No Data Available :(",
        new_recovered=new_recovered if new_recovered else "No Data Available :(",
        total_population=json_response["data"]["Population"]
    )