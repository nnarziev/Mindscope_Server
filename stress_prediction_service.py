import pickle

from feature_extraction import Features
from Mindscope_Server import models
import threading
import schedule
import time
import pandas as pd
import datetime

from stress_model import StressModel
from grpc_handler import GrpcHandler

# Notes:
#################################################################################################
# This is the Mindscope Server application
# It runs a prediction_task() function at every prediction time (prediction_times)
# Inside prediction task we have following steps for each user in the study:
# Step0. check users day num if it's more than 14 days, only then extract features for 14 days and init the model
# Step1: retrieve the users' data from the gRPC server (John) - Done
# Step2: extract features from retrieved data (John) - Done
# Step3: pre-process and normalize the extracted features (Soyoung) - Need to integrate
# Step4: init StressModel by taking pre-processed data from DB and normalizing (Soyoung) - Need to integrate
# Step5: make prediction using current features with that model (Soyoung) - Need to integrate
# Step6: save current features prediction as label to DB (John)
# Step7: return prediction to gRPC server (John)
# Step8: check user self report and update the DB of pre-processed features with reported stress label if there is self report from user
#################################################################################################


prediction_times = [11, 15, 19, 23]
survey_duration = 1  # in days

run_service = None
thread = None
grpc_handler = None
manager_email = 'nnarziev@nsl.inha.ac.kr'
manager_id = 2
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
    job18 = schedule.every().day.at("19:00").do(prediction_task, 2)
    job22 = schedule.every().day.at("23:00").do(prediction_task, 3)

    while run_service:
        schedule.run_pending()
        time.sleep(1)

    schedule.cancel_job(job=job10)
    schedule.cancel_job(job=job14)
    schedule.cancel_job(job=job18)
    schedule.cancel_job(job=job22)


def prediction_task(i):
    global grpc_handler
    print("Prediction task for {} is running... ".format(prediction_times[i]))
    grpc_handler = GrpcHandler('165.246.21.202:50051', manager_id, manager_email, campaign_id)

    now_time = int(datetime.datetime.now().timestamp()) * 1000
    from_time = now_time - (4 * 3600 * 1000)  # from 4 hours before now time

    users_info = grpc_handler.grpc_load_user_emails()
    ema_order = i + 1

    data_sources = grpc_handler.grpc_get_data_sources_info()

    for user_email, id_day in users_info.items():
        user_id = id_day['uid']
        day_num = id_day['dayNum']
        sm = StressModel(uid=user_email, dayNo=day_num, emaNo=ema_order)

        # 0. check users day num if it's more than 14 days, only then extract features for 14 days and init the model
        if day_num > survey_duration:
            # if the first day and the first ema order after 14days
            if day_num == survey_duration + 1 and ema_order == 1:
                initialModelTraining(user_email, data_sources, sm)
            else:
                # 1. retrieve the data from the gRPC server
                # get all user data from gRPC server between start_ts and end_ts
                data = grpc_handler.grpc_load_user_data(from_ts=from_time, uid=user_email, data_sources=data_sources, data_src_for_sleep_detection=Features.SCREEN_ON_OFF)

                # 2. extract features from retrieved data
                with open('data_result/' + str(user_email) + "_features.p", 'rb') as file:
                    step1_preprocessed = pickle.load(file)

                features = Features(uid=user_email, dataset=data)
                df = pd.DataFrame(features.extract_regular(start_ts=from_time, end_ts=now_time, ema_order=ema_order))

                # 3. pre-process and normalize the extracted features
                new_row_preprocessed = sm.preprocessing(df)
                norm_df = sm.normalizing("new", step1_preprocessed, new_row_preprocessed)

                # 4. init StressModel here
                # get test data
                new_row_for_test = norm_df[(norm_df['Day'] == day_num) & (norm_df['EMA order'] == ema_order)]

                ## get trained model
                with open('model_result/' + str(user_email) + "_model.p", 'rb') as file:
                    initModel = pickle.load(file)

                # 5. make prediction using current features with that model
                features = StressModel.feature_df_with_state['features'].values

                y_pred = initModel.predict(new_row_for_test[features])

                new_row_preprocessed['Sterss_label'] = y_pred

                # 6. save current features prediction as label to DB
                # insert a new pre-processed feature entry in DB with predicted label
                # DATA- , Model UPDATE
                update_df = pd.concat([step1_preprocessed.reset_index(drop=True), new_row_preprocessed.reset_index(drop=True)])

                with open('data_result/' + str(user_email) + "_features.p", 'wb') as file:
                    pickle.dump(update_df, file)

                # 7. save prediction in DB and return it to gRPC server
                # Send the prediction with "STRESS_PREDICTION" data source and "day_num ema_order prediction_value" value
                user_all_labels = list(set(step1_preprocessed['Stress_label']))
                model_results = list(sm.getSHAP(user_all_labels, y_pred, new_row_for_test, initModel))  # saves results on ModelResult table in DB

                # construct a message from model results and return it to gRPC server
                result_data = {}
                for model_result in model_results:
                    result_data[model_result.prediction_result] = {
                        "day_num": model_result.day_num,
                        "ema_order": model_result.ema_order,
                        "accuracy": model_result.accuracy,
                        "feature_ids": model_result.feature_ids
                    }
                #return prediction message to gRPC for user to see
                grpc_handler.grpc_send_user_data(user_id, user_email, data_sources['STRESS_PREDICTION'], now_time, result_data)

                # 8. check user self report and update the DB of pre-processed features with reported stress label if if there is self report from user
                # check 'SELF_STRESS_REPORT' data source for user and run retrain if needed and retrain
                # region Retrain the models with prev self reports
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
    # TODO: return prediction message to gRPC for user to see


def check_and_handle_self_report(user_email, data, stress_model):
    sr_day_num = 0
    sr_ema_order = 0
    sr_value = -1  # self report value
    if data['SELF_STRESS_REPORT'][-1][1]:  # data['SELF_STRESS_REPORT'][-1][1] takes the value of the latest SELF_STRESS_REPORT data source
        sr_day_num, sr_ema_order, sr_value = [int(i) for i in data['SELF_STRESS_REPORT'][-1][1].split(" ")]

    model_result_to_update = models.ModelResult.objects.get(uid=user_email, day_num=sr_day_num, ema_order=sr_ema_order, prediction_result=sr_value)
    # check if this result was not already updated by the user, if it wasn't then update the user tag and re-train the model
    if model_result_to_update.user_tag == False:
        stress_model.update(sr_value)