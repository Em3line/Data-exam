
import os
import joblib

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

from trainer.encoders import OrdinalEncoder, TimeFeaturesExtractor, \
    CyclicalEncoder


class Trainer():
    def __init__(self):
        self.X, self.y = self.get_data()
        self.feat_num = self.X.select_dtypes(include="number") \
            .columns.to_list()

        self.feat_time = ["datetime_start", "datetime_end"]

    def get_data(self):
        df = pd.read_csv("https://wagon-public-datasets.s3.amazonaws.com/certification_france_2021_q3/gen_df_binary.csv")

        df.drop_duplicates(inplace=True)

        for c in df:
            if df[c].isna().sum() / len(df) > .3:
                df.drop(c, axis=1, inplace=True)

        df.dropna(inplace=True)

        data = df

        y = data.target

        X = data.drop(["id", "scientist", "target"], axis=1)

        return X, y

    def make_pipeline(self):

        preprocessing_time = Pipeline([
            ("extractor_time", TimeFeaturesExtractor(
                "datetime_start", "datetime_end")),
            ("preprocessing_time", ColumnTransformer([
                ("scaler_minmax_", MinMaxScaler(), ["duration"]),
                ("encoder_cyclical_", CyclicalEncoder("month"), ["month"])
            ]))
        ])

        preprocessing_advanced = Pipeline([
            ("preprocessing",
                ColumnTransformer([
                    ("scaler_minmax", MinMaxScaler(), self.feat_num),
                    ("encoder_onehot", OneHotEncoder(), ["main_element"]),
                    ("encoderordinal", OrdinalEncoder(
                        "soil_condition"), ["soil_condition"]),
                    ("preprocessing_time", preprocessing_time, self.feat_time)
                ]))
        ])

        preprocessing_advanced.steps.append(
            ("pca_reductor", PCA(n_components=12)))

        grid_search = Pipeline([
            ("preprocessing_advanced", preprocessing_advanced),
            ("model_ensemble",
             AdaBoostClassifier(DecisionTreeClassifier(min_samples_leaf=2),
                                n_estimators=80,
                                learning_rate=1e-1))
        ])

        return grid_search

    def train(self):
        pipeline = self.make_pipeline().fit(self.X, self.y)
        return pipeline

    def save_model(self, model):
        root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))

        path = os.path.join(root, "assets", "model.joblib")

        joblib.dump(model, path)


if __name__ == "__main__":
    trainer = Trainer()
    model = trainer.train()
    trainer.save_model(model)
