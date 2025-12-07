from pydantic import BaseModel
from typing import List, Optional, Dict


class AnalyzeRequest(BaseModel):
    home: str
    away: str


class MatchResult(BaseModel):
    home: str
    away: str
    score: Optional[str] = None
    date: Optional[str] = None
    home_is_home: Optional[bool] = True


class TeamFormData(BaseModel):
    team_name: str
    form_string: str  # "G B M G G"
    matches: List[MatchResult] = []
    # Ruh hali / baskı proxy alanları
    league_position: Optional[int] = None
    total_teams: Optional[int] = None


class RawAggregateData(BaseModel):
    home: TeamFormData
    away: TeamFormData
    odds_1: Optional[float] = None
    odds_x: Optional[float] = None
    odds_2: Optional[float] = None


class PredictionOutput(BaseModel):
    home_prob: float
    draw_prob: float
    away_prob: float
    reasoning: str


class AnalyzeResponse(BaseModel):
    home: str
    away: str
    form_home: str
    form_away: str
    prediction: PredictionOutput
    raw: RawAggregateData
