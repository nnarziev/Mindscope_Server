import json
import pickle

from main_service.grpc_handler import GrpcHandler
from main_service.models import ModelResult
from main_service.feature_extraction import Features

import threading
import schedule
import time
import pandas as pd
import datetime

from main_service.stress_model import StressModel, makeLabel

# region Notes:
#################################################################################################
# This is the Mindscope Server application
# It runs a prediction_task() function at every prediction time (prediction_times)
# Inside prediction task we have following steps for each user in the study:
# Step1. Check if the users day num is 14 and job is for initial model training
# Step2. Check if users day num is more than 14 days, only then extract features and make prediction
# Step3. Retrieve the last 4 hours data from the gRPC server
# Step4. Extract features from retrieved data
# Step5. Pre-process and normalize the extracted features
# Step6. Get trained stress prediction model
# Step7. Make prediction using current extracted features
# Step8. Insert a new pre-processed feature entry together with it's predicted label in DB for further model re-train
# Step9. Save prediction and important features in DB
# Step10. Construct a result message and send it to gRPC server with "STRESS_PREDICTION" data source id
# Step11. Lastly, check if user self reported his stress, then update the DB of pre-processed features with reported stress label
#################################################################################################
# endregion


# region Constants
FLAG_EMA_ORDER_1 = 0
FLAG_EMA_ORDER_2 = 1
FLAG_EMA_ORDER_3 = 2
FLAG_EMA_ORDER_4 = 3
FLAG_INITIAL_MODEL_TRAIN = -1

PREDICTION_HOURS = [11, 15, 19, 23]
SURVEY_DURATION = 3  # in days

SERVER_IP_PORT = '165.246.21.202:50051'
CAMPAIGN_ID = 13

MANAGER_ID = 21
MANAGER_EMAIL = 'mindscope.nsl@gmail.com'
# endregion


# region Variables
run_service = None
thread = None
grpc_handler = None


# endregion

def start():
    global run_service, thread
    run_service = True
    thread = threading.Thread(target=service_routine())
    thread.start()


def stop():
    global run_service
    run_service = False


def service_routine():
    prediction_task(FLAG_EMA_ORDER_4)
    # job_regular_at_11 = schedule.every().day.at("10:45").do(prediction_task, FLAG_EMA_ORDER_1)
    # job_regular_at_15 = schedule.every().day.at("14:45").do(prediction_task, FLAG_EMA_ORDER_2)
    # job_regular_at_19 = schedule.every().day.at("18:45").do(prediction_task, FLAG_EMA_ORDER_3)
    # job_regular_at_23 = schedule.every().day.at("22:45").do(prediction_task, FLAG_EMA_ORDER_4)
    #
    # job_initial_train = schedule.every().day.at("23:50").do(prediction_task, FLAG_INITIAL_MODEL_TRAIN)
    #
    # while run_service:
    #     try:
    #         schedule.run_pending()
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         stop()
    #
    # schedule.cancel_job(job=job_regular_at_11)
    # schedule.cancel_job(job=job_regular_at_15)
    # schedule.cancel_job(job=job_regular_at_19)
    # schedule.cancel_job(job=job_regular_at_23)
    # schedule.cancel_job(job=job_initial_train)

    exit(0)


def prediction_task(i):
    global grpc_handler

    if i == -1:
        print("Initial model training task is running...")
    else:
        print("Regular task for hour {} is running...".format(PREDICTION_HOURS[i]))

    grpc_handler = GrpcHandler(SERVER_IP_PORT, MANAGER_ID, MANAGER_EMAIL, CAMPAIGN_ID)

    now_time = int(datetime.datetime.now().timestamp()) * 1000
    from_time = now_time - (4 * 3600 * 1000)  # from 4 hours before now time

    users_info = grpc_handler.grpc_load_user_emails()
    ema_order = i + 1

    data_sources = {}
    campaign_start_time = 0
    campaign_info = grpc_handler.grpc_get_campaign_info()

    if campaign_info:
        for data_source in json.loads(campaign_info.configJson):
            data_sources[data_source['name']] = data_source['data_source_id']

        campaign_start_time = int(campaign_info.startTimestamp)
    else:
        print("No Campaign Info")
        exit(1)

    # check if the study duration day is more one day to the SURVEY_DURATION day then do following
    # get SURVEY_EMA data of all participants and pass it to StreesModel.makeLabel() function
    # to initialize some stress thresholds
    if fromNowToGivenTimeToDayNum(campaign_start_time) == SURVEY_DURATION - 1 and ema_order == 4:
        initStressThresholds(users_info, data_sources)

    users_total_cnt = users_info.__len__()
    user_current_cnt = 0

    for user_email, id_jointime in users_info.items():
        # TODO: temporarily check for one user
        # if user_email == 'nnarziev@gmail.com':
        user_current_cnt += 1
        print("User {}/{} : {}".format(user_current_cnt, users_total_cnt, user_email))
        user_id = id_jointime['uid']
        day_num = fromNowToGivenTimeToDayNum(id_jointime['joinedTime'])
        threshold_data = grpc_handler.grpc_load_user_data(from_ts=0, uid=user_email, data_sources={Features.STRESS_LVL_THRESHOLDS: data_sources[Features.STRESS_LVL_THRESHOLDS]}, data_src_for_sleep_detection=None)
        stress_lv0_max = 0
        stress_lv1_max = 0
        stress_lv2_min = 0

        if list(threshold_data[Features.STRESS_LVL_THRESHOLDS]).__len__() > 0:
            for item in reversed(threshold_data[Features.STRESS_LVL_THRESHOLDS]):
                stress_lv0_max, stress_lv1_max, stress_lv2_min = item[1].split(" ")
                break

        sm = StressModel(user_email, day_num, ema_order, float(stress_lv0_max), float(stress_lv1_max), float(stress_lv2_min))

        # 1. Check if the users day num is 14 and job is for initial model training
        if day_num == SURVEY_DURATION and i == FLAG_INITIAL_MODEL_TRAIN:
            print("1. Initial model training...")
            from_time = 0  # from the very beginning of data collection
            data = grpc_handler.grpc_load_user_data(from_ts=from_time, uid=user_email, data_sources=data_sources,
                                                    data_src_for_sleep_detection=Features.SCREEN_ON_OFF)
            initialModelTraining(data, user_email, id_jointime['joinedTime'], sm)
            # 2. Check if users day num is more than 14 days, only then extract features and make prediction
        elif day_num > SURVEY_DURATION:
            print("2. Regular prediction...")
            # 3. Retrieve the last 4 hours data from the gRPC server
            data = grpc_handler.grpc_load_user_data(from_ts=from_time, uid=user_email, data_sources=data_sources, data_src_for_sleep_detection=Features.SCREEN_ON_OFF)

            # 4. Extract features from retrieved data
            with open('data_result/' + str(user_email) + "_features.p", 'rb') as file:
                step1_preprocessed = pickle.load(file)

            features = Features(uid=user_email, dataset=data, joinTimestamp=id_jointime['joinedTime'])
            df = pd.DataFrame(features.extract_regular(start_ts=from_time, end_ts=now_time, ema_order=ema_order))

            # 5. Pre-process and normalize the extracted features
            new_row_preprocessed = sm.preprocessing(df=df, prep_type=None)
            norm_df = sm.normalizing("new", step1_preprocessed, new_row_preprocessed, user_email, day_num, ema_order)
            new_row_for_test = norm_df[(norm_df['Day'] == day_num) & (norm_df['EMA order'] == ema_order)]  # get test data

            # 6. Get trained stress prediction model
            with open('model_result/' + str(user_email) + "_model.p", 'rb') as file:
                initModel = pickle.load(file)

            # 7. Make prediction using current extracted features
            features = StressModel.feature_df_with_state['features'].values
            y_pred = initModel.predict(new_row_for_test[features])
            new_row_preprocessed['Stress_label'] = y_pred

            # 8. Insert a new pre-processed feature entry together with it's predicted label in DB for further model re-train
            update_df = pd.concat([step1_preprocessed.reset_index(drop=True), new_row_preprocessed.reset_index(drop=True)])
            with open('data_result/' + str(user_email) + "_features.p", 'wb') as file:
                pickle.dump(update_df, file)

            # 9. Save prediction and important features in DB
            user_all_labels = list(set(step1_preprocessed['Stress_label']))
            model_results = list(sm.saveAndGetSHAP(user_all_labels, y_pred, new_row_for_test, initModel))  # saves results on ModelResult table in DB

            # 10. Construct a result message and send it to gRPC server with "STRESS_PREDICTION" data source id
            result_data = {}
            for model_result in model_results:
                result_data[str(model_result.prediction_result)] = {
                    "day_num": model_result.day_num,
                    "ema_order": model_result.ema_order,
                    "accuracy": model_result.accuracy,
                    "feature_ids": model_result.feature_ids,
                    "model_tag": model_result.model_tag
                }
            grpc_handler.grpc_send_user_data(user_id, user_email, data_sources[Features.STRESS_PREDICTION], now_time, str(result_data))

            # 11. Lastly, check if user self reported his stress, then update the DB of pre-processed features with reported stress label
            check_and_handle_self_report(user_email, data, sm)
        else:
            print("3. Waiting until survey completion day ({} days)...".format(SURVEY_DURATION))

    grpc_handler.grpc_close()


def initialModelTraining(dataset, user_email, joined_timestamp, stress_model):
    # first model init based on 14 days data
    global grpc_handler

    features = Features(uid=user_email, dataset=dataset, joinTimestamp=joined_timestamp)
    df = pd.DataFrame(features.extract_for_after_survey())

    # preprocessing and saving the result
    df_preprocessed = stress_model.preprocessing(df=df, prep_type="default")
    with open('data_result/' + str(user_email) + "_features.p", 'wb') as file:
        pickle.dump(df_preprocessed, file)

    # normalizing
    norm_df = stress_model.normalizing("default", df_preprocessed, None, None, None, None)

    # init model
    stress_model.initModel(norm_df)


def check_and_handle_self_report(user_email, data, stress_model):
    # 'SELF_STRESS_REPORT' data source in gRPC server holds self reported stress from users
    sr_day_num = 0
    sr_ema_order = 0
    sr_value = -1  # self report value
    if data['SELF_STRESS_REPORT'][-1][1]:  # data['SELF_STRESS_REPORT'][-1][1] takes the value of the latest SELF_STRESS_REPORT data source
        sr_day_num, sr_ema_order, yes_no, sr_value = [int(i) for i in data['SELF_STRESS_REPORT'][-1][1].split(" ")]

    model_result_to_update = ModelResult.objects.get(uid=user_email, day_num=sr_day_num, ema_order=sr_ema_order, prediction_result=sr_value)
    # check if this result was not already updated by the user, if it wasn't then update the user tag and re-train the model
    if model_result_to_update.user_tag == False:
        stress_model.update(sr_value)


def fromNowToGivenTimeToDayNum(givenTimestamp):
    nowTime = int(datetime.datetime.now().timestamp()) * 1000
    return int((nowTime - givenTimestamp) / 1000 / 3600 / 24)


def initStressThresholds(users_info, data_sources):
    global grpc_handler
    all_stress_level_values = []
    for user_email, id_jointime in users_info.items():
        data = grpc_handler.grpc_load_user_data(from_ts=0, uid=user_email, data_sources={Features.SURVEY_EMA: data_sources[Features.SURVEY_EMA]}, data_src_for_sleep_detection=None)
        ema_responses = list(data[Features.SURVEY_EMA])
        if ema_responses.__len__() > 0:
            for index, ema_res in enumerate(ema_responses):
                values = ema_res[1].split(" ")
                responded_time = values[0]
                ema_order = values[1]
                ans1 = values[2]
                ans2 = values[3]
                ans3 = values[4]
                ans4 = values[5]
                all_stress_level_values.append(int(ans1) + int(ans2) + int(ans3) + int(ans4))

    threshold_results = makeLabel(all_stress_level_values)

    final_stress_threshold_results = "{} {} {}".format(threshold_results[0], threshold_results[1], threshold_results[2])

    now_time = int(datetime.datetime.now().timestamp() * 1000)
    for user_email, id_jointime in users_info.items():
        try:
            grpc_handler.grpc_send_user_data(id_jointime['uid'], user_email, data_sources[Features.STRESS_LVL_THRESHOLDS], now_time, final_stress_threshold_results)
        except Exception as e:
            print(e)
