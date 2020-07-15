import pickle

from main_service.grpc_handler import GrpcHandler
from main_service.models import ModelResult
from main_service.feature_extraction import Features

import threading
import schedule
import time
import pandas as pd
import datetime

from main_service.stress_model import StressModel

# Notes:
#################################################################################################
# This is the Mindscope Server application
# It runs a prediction_task() function at every prediction time (prediction_times)
# Inside prediction task we have following steps for each user in the study:
# Step1. Check if users day num is more than 14 days, only then extract features and make prediction
# Step2. Check if the first ema order at 15th day of participation, then make initial model training
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


prediction_times = [11, 15, 19, 23]
survey_duration = 1  # in days

run_service = None
thread = None
grpc_handler = None
manager_email = 'mindscope.nsl@gmail.com'
manager_id = 21
campaign_id = 1


def start():
    global run_service, thread
    run_service = True
    thread = threading.Thread(target=service_routine())
    thread.start()


def stop():
    global run_service
    run_service = False


def service_routine():
    job10 = schedule.every().day.at("11:00").do(prediction_task, 0)
    job14 = schedule.every().day.at("15:00").do(prediction_task, 1)
    job18 = schedule.every().day.at("17:16").do(prediction_task, 2)
    job22 = schedule.every().day.at("23:00").do(prediction_task, 3)

    while run_service:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            stop()

    schedule.cancel_job(job=job10)
    schedule.cancel_job(job=job14)
    schedule.cancel_job(job=job18)
    schedule.cancel_job(job=job22)
    exit(0)


def prediction_task(i):
    global grpc_handler
    print("Prediction task for {} is running... ".format(prediction_times[i]))
    grpc_handler = GrpcHandler('165.246.21.202:50051', manager_id, manager_email, campaign_id)
    print(grpc_handler)

    now_time = int(datetime.datetime.now().timestamp()) * 1000
    from_time = now_time - (4 * 3600 * 1000)  # from 4 hours before now time

    users_info = grpc_handler.grpc_load_user_emails()
    print("User info: {}".format(users_info))
    ema_order = i + 1

    data_sources = grpc_handler.grpc_get_data_sources_info()
    print("Data sources: {}".format(data_sources))

    for user_email, id_day in users_info.items():
        user_id = id_day['uid']
        day_num = id_day['dayNum']
        sm = StressModel(uid=user_email, dayNo=day_num, emaNo=ema_order)

        # 1. Check if users day num is more than 14 days, only then extract features and make prediction
        if day_num > survey_duration:

            # 2. Check if the first ema order at 15th day of participation, then make initial model training
            if day_num == survey_duration + 1 and ema_order == 1:
                initialModelTraining(user_email, data_sources, sm)

            # 3. Retrieve the last 4 hours data from the gRPC server
            data = grpc_handler.grpc_load_user_data(from_ts=from_time, uid=user_email, data_sources=data_sources, data_src_for_sleep_detection=Features.SCREEN_ON_OFF)

            # 4. Extract features from retrieved data
            with open('data_result/' + str(user_email) + "_features.p", 'rb') as file:
                step1_preprocessed = pickle.load(file)
            features = Features(uid=user_email, dataset=data)
            df = pd.DataFrame(features.extract_regular(start_ts=from_time, end_ts=now_time, ema_order=ema_order))

            # 5. Pre-process and normalize the extracted features
            new_row_preprocessed = sm.preprocessing(df)
            norm_df = sm.normalizing("new", step1_preprocessed, new_row_preprocessed)
            new_row_for_test = norm_df[(norm_df['Day'] == day_num) & (norm_df['EMA order'] == ema_order)]  # get test data

            # 6. Get trained stress prediction model
            with open('model_result/' + str(user_email) + "_model.p", 'rb') as file:
                initModel = pickle.load(file)

            # 7. Make prediction using current extracted features
            features = StressModel.feature_df_with_state['features'].values
            y_pred = initModel.predict(new_row_for_test[features])
            new_row_preprocessed['Sterss_label'] = y_pred

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
                result_data[model_result.prediction_result] = {
                    "day_num": model_result.day_num,
                    "ema_order": model_result.ema_order,
                    "accuracy": model_result.accuracy,
                    "feature_ids": model_result.feature_ids,
                    "model_tag": model_result.model_tag
                }
            grpc_handler.grpc_send_user_data(user_id, user_email, data_sources['STRESS_PREDICTION'], now_time, str(result_data))

            # 11. Lastly, check if user self reported his stress, then update the DB of pre-processed features with reported stress label
            check_and_handle_self_report(user_email, data, sm)

    grpc_handler.grpc_close()


def initialModelTraining(user_email, data_sources, stress_model):
    # first model init based on 14 days data
    from_time = 0  # from the very beginning of data collection
    data = grpc_handler.grpc_load_user_data(from_ts=from_time, uid=user_email, data_sources=data_sources,
                                            data_src_for_sleep_detection=Features.SCREEN_ON_OFF)

    features = Features(uid=user_email, dataset=data)
    df = pd.DataFrame(features.extract_for_after_survey())

    # preprocessing and saving the result
    df_preprocessed = stress_model.preprocessing(df)
    with open('data_result/' + str(user_email) + "_features.p", 'wb') as file:
        pickle.dump(df_preprocessed, file)

    # normalizing
    norm_df = stress_model.normalizing("default", df_preprocessed, None)

    # init model
    stress_model.initModel(norm_df)


def check_and_handle_self_report(user_email, data, stress_model):
    # 'SELF_STRESS_REPORT' data source in gRPC server holds self reported stress from users
    sr_day_num = 0
    sr_ema_order = 0
    sr_value = -1  # self report value
    if data['SELF_STRESS_REPORT'][-1][1]:  # data['SELF_STRESS_REPORT'][-1][1] takes the value of the latest SELF_STRESS_REPORT data source
        sr_day_num, sr_ema_order, sr_value = [int(i) for i in data['SELF_STRESS_REPORT'][-1][1].split(" ")]

    model_result_to_update = ModelResult.objects.get(uid=user_email, day_num=sr_day_num, ema_order=sr_ema_order, prediction_result=sr_value)
    # check if this result was not already updated by the user, if it wasn't then update the user tag and re-train the model
    if model_result_to_update.user_tag == False:
        stress_model.update(sr_value)
