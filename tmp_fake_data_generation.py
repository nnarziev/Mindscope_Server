import grpc

from libs import et_service_pb2_grpc, et_service_pb2

channel = grpc.insecure_channel('165.246.21.202:50051')
stub = et_service_pb2_grpc.ETServiceStub(channel)
manager_email = 'hrgoh@nsl.inha.ac.kr'
manager_id = 23
campaign_id = 13

# values = []
# times = [1593568800000, 1593583200000, 1593597600000, 1593612000000, 1593655200000, 1593669600000, 1593684000000, 1593698400000, 1593741600000, 1593756000000, 1593770400000, 1593784800000]
#
# values.append({"1": {'model_tag': True, 'feature_ids': '1-low 2-high 3-low 5-high 8-low 2-high 12-high 21-low 22-low', 'ema_order': 1, 'day_num': 1, 'accuracy': 50},
#                "2": {'model_tag': False, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'ema_order': 1, 'day_num': 1, 'accuracy': 30},
#                "3": {'model_tag': False, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'ema_order': 1, 'day_num': 1, 'accuracy': 20}})
# values.append({"1": {'model_tag': False, 'day_num': 1, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'ema_order': 2, 'accuracy': 30},
#                "2": {'model_tag': True, 'day_num': 1, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'ema_order': 2, 'accuracy': 50},
#                "3": {'model_tag': False, 'day_num': 1, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'ema_order': 2, 'accuracy': 20}})
# values.append({"1": {'ema_order': 3, 'model_tag': False, 'day_num': 1, 'accuracy': 30, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low'},
#                "2": {'ema_order': 3, 'model_tag': True, 'day_num': 1, 'accuracy': 50, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low'},
#                "3": {'ema_order': 3, 'model_tag': False, 'day_num': 1, 'accuracy': 20, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low'}})
# values.append({"1": {'model_tag': False, 'day_num': 1, 'accuracy': 30, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'ema_order': 4},
#                "2": {'model_tag': True, 'day_num': 1, 'accuracy': 50, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'ema_order': 4},
#                "3": {'model_tag': False, 'day_num': 1, 'accuracy': 20, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'ema_order': 4}})
# values.append({"1": {'ema_order': 1, 'day_num': 2, 'accuracy': 30, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'model_tag': False},
#                "2": {'ema_order': 1, 'day_num': 2, 'accuracy': 50, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'model_tag': True},
#                "3": {'ema_order': 1, 'day_num': 2, 'accuracy': 20, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'model_tag': False}})
# values.append({"1": {'accuracy': 30, 'model_tag': False, 'ema_order': 2, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'day_num': 2},
#                "2": {'accuracy': 50, 'model_tag': True, 'ema_order': 2, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'day_num': 2},
#                "3": {'accuracy': 20, 'model_tag': False, 'ema_order': 2, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'day_num': 2}})
# values.append({"1": {'model_tag': False, 'ema_order': 3, 'accuracy': 30, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'day_num': 2},
#                "2": {'model_tag': True, 'ema_order': 3, 'accuracy': 50, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'day_num': 2},
#                "3": {'model_tag': False, 'ema_order': 3, 'accuracy': 20, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'day_num': 2}})
# values.append({"1": {'accuracy': 30, 'model_tag': False, 'ema_order': 4, 'day_num': 2, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low'},
#                "2": {'accuracy': 50, 'model_tag': True, 'ema_order': 4, 'day_num': 2, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low'},
#                "3": {'accuracy': 20, 'model_tag': False, 'ema_order': 4, 'day_num': 2, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low'}})
# values.append({"1": {'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'day_num': 3, 'ema_order': 1, 'accuracy': 30, 'model_tag': False},
#                "2": {'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'day_num': 3, 'ema_order': 1, 'accuracy': 50, 'model_tag': True},
#                "3": {'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'day_num': 3, 'ema_order': 1, 'accuracy': 20, 'model_tag': False}})
# values.append({"1": {'model_tag': False, 'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'accuracy': 30, 'day_num': 3, 'ema_order': 2},
#                "2": {'model_tag': True, 'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'accuracy': 50, 'day_num': 3, 'ema_order': 2},
#                "3": {'model_tag': False, 'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'accuracy': 20, 'day_num': 3, 'ema_order': 2}})
# values.append({"1": {'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'ema_order': 3, 'accuracy': 30, 'model_tag': False, 'day_num': 3},
#                "2": {'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'ema_order': 3, 'accuracy': 50, 'model_tag': True, 'day_num': 3},
#                "3": {'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'ema_order': 3, 'accuracy': 20, 'model_tag': False, 'day_num': 3}})
# values.append({"1": {'feature_ids': '1-low 2-low 3-high 5-high 8-low 2-high 12-high 21-low 22-low', 'model_tag': False, 'accuracy': 30, 'day_num': 3, 'ema_order': 4},
#                "2": {'feature_ids': '1-low 2-high 3-low 4-high 8-low 7-high 10-high 21-low', 'model_tag': True, 'accuracy': 50, 'day_num': 3, 'ema_order': 4},
#                "3": {'feature_ids': '1-low 2-high 3-low 5-high 6-low 7-high 11-high 21-low', 'model_tag': False, 'accuracy': 20, 'day_num': 3, 'ema_order': 4}})

times = [
    1594692000000,
    1594706400000,
    1594720800000,
    1594735200000,
    1594778400000,
    1594792800000,
    1594807200000,
    1594821600000,
    1594864800000,
    1594879200000,
    1594893600000,
    1594908000000,
    1594994400000
]

values = [
    "1594692000000 1 3 3 4 4 3",
    "1594706400000 2 2 3 4 2 3",
    "1594720800000 3 0 0 0 0 2",
    "1594735200000 4 5 5 5 5 2",
    "1594778400000 1 1 1 3 1 1",
    "1594792800000 2 5 2 2 2 1",
    "1594807200000 3 4 4 2 4 1",
    "1594821600000 4 3 3 2 1 1",
    "1594864800000 1 4 4 4 2 2",
    "1594879200000 2 5 3 4 4 1",
    "1594893600000 3 5 5 5 2 1",
    "1594908000000 4 2 2 3 4 1",
    "1594994400000 4 1 1 4 4 3"
]

for index, value in enumerate(values):
    req = et_service_pb2.SubmitDataRecordsRequestMessage(
        userId=manager_id,
        email=manager_email
    )
    req.dataSource.extend([13])
    req.timestamp.extend([times[index]])
    req.accuracy.extend([1])
    req.values.extend([str(values[index])])
    res = stub.submitDataRecords(req)

    print(res)
    if res.doneSuccessfully:
        print('S')
    else:
        print('failed to submit')
