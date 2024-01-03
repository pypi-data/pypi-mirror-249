import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error

from player_performance_ratings.scorer.score import SklearnScorer
from player_performance_ratings.tuner.rating_generator_tuner import OpponentAdjustedRatingGeneratorTuner

from player_performance_ratings import ColumnNames, PredictColumnNames
from player_performance_ratings.predictor.estimators import SklearnPredictor
from player_performance_ratings.ratings import RatingColumnNames, OpponentAdjustedRatingGenerator, ColumnWeight
from player_performance_ratings.tuner import MatchPredictorTuner
from player_performance_ratings.tuner.match_predictor_factory import MatchPredictorFactory
from player_performance_ratings.tuner.utils import get_default_team_rating_search_range

df = pd.read_pickle(r"data/game_player_subsample.pickle")

df = (
    df.assign(team_count=df.groupby("game_id")["team_id"].transform('nunique'))
    .loc[lambda x: x.team_count == 2]
)

df = df.sort_values(["start_date", "game_id", "team_id", "player_id"])
df[PredictColumnNames.TARGET] = df['points']

column_names = ColumnNames(
    match_id="game_id",
    team_id="team_id",
    player_id="player_id",
    start_date="start_date",
    performance="points"
)

match_predictor_factory = MatchPredictorFactory(
    rating_generators=[OpponentAdjustedRatingGenerator(column_names=column_names,
                                                       features_out=[RatingColumnNames.RATING_DIFFERENCE_PROJECTED,
                                                                     RatingColumnNames.PLAYER_RATING_DIFFERENCE_PROJECTED])],
    predictor=SklearnPredictor(model=LGBMRegressor(), features=[RatingColumnNames.RATING_DIFFERENCE_PROJECTED,
                                                                RatingColumnNames.PLAYER_RATING_DIFFERENCE_PROJECTED],
                               pred_column='pred'),
    use_auto_create_performance_calculator=True,
    column_weights=[ColumnWeight(name='points', weight=1)],
)

rating_generator_tuner = OpponentAdjustedRatingGeneratorTuner(
    team_rating_n_trials=30,
    team_rating_search_ranges=get_default_team_rating_search_range(),
)

match_predictor_tuner = MatchPredictorTuner(
    match_predictor_factory=match_predictor_factory,
    rating_generator_tuners=rating_generator_tuner,
    scorer=SklearnScorer(pred_column=match_predictor_factory.predictor.pred_column,
                         scorer_function=mean_absolute_error),
)

match_predictor_tuner.tune(df)
