import pickle

from collections import Counter
# Normalize
from sklearn.preprocessing import MinMaxScaler

# Model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier

from Mindscope_Server import models
import shap
import pandas as pd


class StressModel:
    # variable for setting label

    stress_lv0_max = 0
    stress_lv1_max = 0
    stress_lv2_min = 0

    # variable for label
    CONST_STRESS_LOW = 0
    CONST_STRESS_LITTLE_HIGH = 1
    CONST_STRESS_HIGH = 2

    feature_df_with_state = pd.read_csv('assets/feature_with_state.csv')

    def __init__(self, uid, dayNo, emaNo):

        self.uid = uid
        self.dayNo = dayNo
        self.emaNo = emaNo

    #############################################################################################

    ## CASE 1 : Right after the end of step1
    def makeLabel(self, all_df):
        """
            Step1 끝난 시점에 한번만 계산 --> 스트레스 레벨을 세 구간으로 나눔
                - just call once after step1 (for calculating stress section)
        """

        pss_mean = all_df['Stress lvl'].mean()
        pss_std = all_df['Stress lvl'].std()

        StressModel.stress_lv0_max = pss_mean
        StressModel.stress_lv1_max = pss_mean + 1.5 * pss_std
        StressModel.stress_lv2_min = pss_mean + 2 * pss_std

        print("\n makeLabel")
        print("lv0 max : ", StressModel.stress_lv0_max)
        print("lvl max : ", StressModel.stress_lv1_max)

    # -----LV0 (LOW) ----- [lv0 max] ------ LV1 (LITTLE HIGH) -----[lv1 max ]-----LV2 (HIGH)

    #############################################################################################

    def mapLabel(self, score):
        if score <= StressModel.stress_lv0_max:
            return StressModel.CONST_STRESS_LOW

        elif (score > StressModel.stress_lv0_max) and (score < StressModel.stress_lv1_max):
            return StressModel.CONST_STRESS_LITTLE_HIGH

        elif (score >= StressModel.stress_lv1_max):
            return StressModel.CONST_STRESS_HIGH

    def preprocessing(self, df):
        """
         - 1. del NAN or replace to zero
         - 2. mapping label (Stress lvl 0, 1, 2)

        """
        print(".....preprocessing")

        delNan_col = ['Audio min.', 'Audio max.', 'Audio mean', 'Sleep dur.']

        for col in df.columns:
            if (col != 'Stress lvl') & (col != 'User id') & (col != 'Day'):
                if col in delNan_col:
                    df = df[df[col] != '-']
                else:
                    df[col] = df[col].replace('-', 0)

                df[col] = pd.to_numeric(df[col])
            df = df.fillna(0)

        df['Stress_label'] = df['Stress lvl'].apply(lambda score: StressModel.mapLabel(score))

        return df

    def normalizing(self, norm_type, preprocessed_df, new_row_preprocessed):
        print(".......normalizing")

        # user info columns
        userinfo = ['User id', 'Day', 'EMA order', 'Stress lvl', 'Stress_label']

        feature_scaled = pd.DataFrame()
        scaler = MinMaxScaler()

        feature_df = preprocessed_df[StressModel.feature_df_with_state['features'].values]

        if norm_type == "default":
            # feature list
            feature_scaled = pd.DataFrame(scaler.fit_transform(feature_df), columns=feature_df.columns)

        elif norm_type == "new":

            feature_df = pd.concat([feature_df.reset_index(drop=True), new_row_preprocessed[
                StressModel.feature_df_with_state['features'].values].reset_index(drop=True)])

            feature_scaled = pd.DataFrame(scaler.fit_transform(feature_df), columns=feature_df.columns)

        feature_scaled = pd.concat(
            [preprocessed_df[userinfo].reset_index(drop=True), feature_scaled.reset_index(drop=True)], axis=1)

        return feature_scaled

    def initModel(self, norm_df):
        """
        initModel
        """
        print(".........initModel")

        print("===================Class Count :", Counter(norm_df['Stress_label']))
        # *** 만약 훈련 데이터에 0,1,2 라벨 중 하나가 없다면? 하나의 라벨만 존재한다면?

        X = norm_df[StressModel.feature_df_with_state['features'].values]
        Y = norm_df['Stress_label'].values

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

        model = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=100)

        kfold = KFold(n_splits=10)
        scoring = {'accuracy': 'accuracy',
                   'f1_micro': 'f1_micro',
                   'f1_macro': 'f1_macro'}

        cv_results = cross_validate(model, X_train, Y_train, cv=kfold, scoring=scoring)
        model_result = {'accuracy': cv_results['test_accuracy'].mean(),
                        'f1_micro': cv_results['test_f1_micro'].mean(),
                        'f1_macro': cv_results['test_f1_macro'].mean()}

        print("===================Model Result : ", model_result)

        model.fit(X_train, Y_train)
        ## Model SAVE Path--> where?
        with open('model_result/' + str(self.uid) + "_model.p", 'wb') as file:
            pickle.dump(model, file)

    def getSHAP(self, user_all_label, pred, new_row_norm, initModel):

        model_results = []

        shap.initjs()
        explainer = shap.TreeExplainer(initModel)
        explainer.feature_perturbation = "tree_path_dependent"

        features = StressModel.feature_df_with_state['features'].values
        feature_state_df = StressModel.feature_df_with_state

        shap_values = explainer.shap_values(new_row_norm[features])
        expected_value = explainer.expected_value

        for label in user_all_label:  # 유저한테 있는 Stress label 에 따라

            feature_list = []

            index = user_all_label.index(label)
            shap_accuracy = expected_value[index]
            shap_list = shap_values[index]

            for s_value, feature_name in zip(shap_list[0], features):
                if s_value > 0:
                    feature_id = feature_state_df[feature_state_df['feature'] == feature_name]['feature_id'].values[0]
                    feature_value = new_row_norm[feature_name].values[0]
                    if feature_value >= 0.5:
                        feature_list.append(str(feature_id) + '-high')
                    else:
                        feature_list.append(str(feature_id) + '-low')
            print(feature_list)
            if label == pred:
                model_result = models.ModelResult.objects.create(uid=self.uid, day_num=self.dayNo, ema_order=self.emaNo,
                                                                 prediction_result=label, accuracy=shap_accuracy,
                                                                 feature_ids=feature_list, model_tag=True)
            else:
                model_result = models.ModelResult.objects.create(uid=self.uid, day_num=self.dayNo, ema_order=self.emaNo,
                                                                 prediction_result=label, accuracy=shap_accuracy,
                                                                 feature_ids=feature_list)

            model_results.append(model_result)

        return model_results

    def update(self, user_response):
        # update Dataframe
        with open('data_result/' + str(self.uid) + "_features.p", 'rb') as file:
            preprocessed = pickle.load(file)
            preprocessed[(preprocessed['Day'] == self.dayNo) & (preprocessed['EMA order'] == self.emaNo)][
                'Stress_label'] = user_response

            with open('data_result/' + str(self.uid) + "_features.p", 'wb') as file:
                pickle.dump(preprocessed, file)

        # retrain the model
        norm_df = StressModel.normalizing(self, "default", preprocessed, None)
        StressModel.initModel(self, norm_df)

        # update ModelResult Table
        model_result = models.ModelResult.objects.get(uid=self.uid, day_num=self.dayNo, ema_order=self.emaNo,
                                                      prediction_result=user_response)
        model_result.user_tag = True
        model_result.save()
