from app.models import RawAggregateData, TeamFormData
from app.scraping.sites import sofascore
# nesine/bilyoner/livescore modüllerini de burada import edebilirsin


def aggregate_team_form(team_name: str) -> TeamFormData:
    """
    Şimdilik ana kaynak Sofascore.
    İleride Nesine/diğerlerinden de destek form bilgisi toplayabiliriz.
    """
    ss = sofascore.get_team_form(team_name)
    if ss:
        return ss

    # fallback:
    return TeamFormData(team_name=team_name, form_string="", matches=[])


def aggregate_odds(home: str, away: str):
    """
    Nesine/Bilyoner odds toplanacağı yer.
    Şimdilik boş dönüyoruz.
    """
    return {
        "odds_1": None,
        "odds_x": None,
        "odds_2": None,
    }


def build_raw_aggregate(home: str, away: str) -> RawAggregateData:
    home_form = aggregate_team_form(home)
    away_form = aggregate_team_form(away)

    odds = aggregate_odds(home, away)

    return RawAggregateData(
        home=home_form,
        away=away_form,
        odds_1=odds["odds_1"],
        odds_x=odds["odds_x"],
        odds_2=odds["odds_2"],
    )
