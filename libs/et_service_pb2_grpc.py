# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import et_service_pb2 as et__service__pb2


class ETServiceStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.loginWithGoogleId = channel.unary_unary(
            '/ETService/loginWithGoogleId',
            request_serializer=et__service__pb2.LoginWithGoogleIdTokenRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.LoginResponseMessage.FromString,
        )
        self.bindUserToCampaign = channel.unary_unary(
            '/ETService/bindUserToCampaign',
            request_serializer=et__service__pb2.BindUserToCampaignRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.BindUserToCampaignResponseMessage.FromString,
        )
        self.dashboardLoginWithEmail = channel.unary_unary(
            '/ETService/dashboardLoginWithEmail',
            request_serializer=et__service__pb2.DashboardLoginWithEmailRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.LoginResponseMessage.FromString,
        )
        self.registerCampaign = channel.unary_unary(
            '/ETService/registerCampaign',
            request_serializer=et__service__pb2.RegisterCampaignRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RegisterCampaignResponseMessage.FromString,
        )
        self.deleteCampaign = channel.unary_unary(
            '/ETService/deleteCampaign',
            request_serializer=et__service__pb2.DeleteCampaignRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.DefaultResponseMessage.FromString,
        )
        self.retrieveCampaigns = channel.unary_unary(
            '/ETService/retrieveCampaigns',
            request_serializer=et__service__pb2.RetrieveCampaignsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveCampaignsResponseMessage.FromString,
        )
        self.retrieveCampaign = channel.unary_unary(
            '/ETService/retrieveCampaign',
            request_serializer=et__service__pb2.RetrieveCampaignRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveCampaignResponseMessage.FromString,
        )
        self.submitDataRecord = channel.unary_unary(
            '/ETService/submitDataRecord',
            request_serializer=et__service__pb2.SubmitDataRecordRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.DefaultResponseMessage.FromString,
        )
        self.submitDataRecords = channel.unary_unary(
            '/ETService/submitDataRecords',
            request_serializer=et__service__pb2.SubmitDataRecordsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.DefaultResponseMessage.FromString,
        )
        self.submitHeartbeat = channel.unary_unary(
            '/ETService/submitHeartbeat',
            request_serializer=et__service__pb2.SubmitHeartbeatRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.DefaultResponseMessage.FromString,
        )
        self.submitDirectMessage = channel.unary_unary(
            '/ETService/submitDirectMessage',
            request_serializer=et__service__pb2.SubmitDirectMessageRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.DefaultResponseMessage.FromString,
        )
        self.retrieveParticipants = channel.unary_unary(
            '/ETService/retrieveParticipants',
            request_serializer=et__service__pb2.RetrieveParticipantsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveParticipantsResponseMessage.FromString,
        )
        self.retrieveParticipantStatistics = channel.unary_unary(
            '/ETService/retrieveParticipantStatistics',
            request_serializer=et__service__pb2.RetrieveParticipantStatisticsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveParticipantStatisticsResponseMessage.FromString,
        )
        self.retrieve100DataRecords = channel.unary_unary(
            '/ETService/retrieve100DataRecords',
            request_serializer=et__service__pb2.Retrieve100DataRecordsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.Retrieve100DataRecordsResponseMessage.FromString,
        )
        self.retrieveFilteredDataRecords = channel.unary_unary(
            '/ETService/retrieveFilteredDataRecords',
            request_serializer=et__service__pb2.RetrieveFilteredDataRecordsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveFilteredDataRecordsResponseMessage.FromString,
        )
        self.retrieveUnreadDirectMessages = channel.unary_unary(
            '/ETService/retrieveUnreadDirectMessages',
            request_serializer=et__service__pb2.RetrieveUnreadDirectMessagesRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveUnreadDirectMessagesResponseMessage.FromString,
        )
        self.retrieveUnreadNotifications = channel.unary_unary(
            '/ETService/retrieveUnreadNotifications',
            request_serializer=et__service__pb2.RetrieveUnreadNotificationsRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveUnreadNotificationsResponseMessage.FromString,
        )
        self.bindDataSource = channel.unary_unary(
            '/ETService/bindDataSource',
            request_serializer=et__service__pb2.BindDataSourceRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.BindDataSourceResponseMessage.FromString,
        )
        self.retrieveAllDataSources = channel.unary_unary(
            '/ETService/retrieveAllDataSources',
            request_serializer=et__service__pb2.RetrieveAllDataSourcesRequestMessage.SerializeToString,
            response_deserializer=et__service__pb2.RetrieveAllDataSourcesResponseMessage.FromString,
        )


class ETServiceServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def loginWithGoogleId(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def bindUserToCampaign(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def dashboardLoginWithEmail(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerCampaign(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteCampaign(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveCampaigns(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveCampaign(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def submitDataRecord(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def submitDataRecords(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def submitHeartbeat(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def submitDirectMessage(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveParticipants(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveParticipantStatistics(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieve100DataRecords(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveFilteredDataRecords(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveUnreadDirectMessages(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveUnreadNotifications(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def bindDataSource(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieveAllDataSources(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ETServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'loginWithGoogleId': grpc.unary_unary_rpc_method_handler(
            servicer.loginWithGoogleId,
            request_deserializer=et__service__pb2.LoginWithGoogleIdTokenRequestMessage.FromString,
            response_serializer=et__service__pb2.LoginResponseMessage.SerializeToString,
        ),
        'bindUserToCampaign': grpc.unary_unary_rpc_method_handler(
            servicer.bindUserToCampaign,
            request_deserializer=et__service__pb2.BindUserToCampaignRequestMessage.FromString,
            response_serializer=et__service__pb2.BindUserToCampaignResponseMessage.SerializeToString,
        ),
        'dashboardLoginWithEmail': grpc.unary_unary_rpc_method_handler(
            servicer.dashboardLoginWithEmail,
            request_deserializer=et__service__pb2.DashboardLoginWithEmailRequestMessage.FromString,
            response_serializer=et__service__pb2.LoginResponseMessage.SerializeToString,
        ),
        'registerCampaign': grpc.unary_unary_rpc_method_handler(
            servicer.registerCampaign,
            request_deserializer=et__service__pb2.RegisterCampaignRequestMessage.FromString,
            response_serializer=et__service__pb2.RegisterCampaignResponseMessage.SerializeToString,
        ),
        'deleteCampaign': grpc.unary_unary_rpc_method_handler(
            servicer.deleteCampaign,
            request_deserializer=et__service__pb2.DeleteCampaignRequestMessage.FromString,
            response_serializer=et__service__pb2.DefaultResponseMessage.SerializeToString,
        ),
        'retrieveCampaigns': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveCampaigns,
            request_deserializer=et__service__pb2.RetrieveCampaignsRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveCampaignsResponseMessage.SerializeToString,
        ),
        'retrieveCampaign': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveCampaign,
            request_deserializer=et__service__pb2.RetrieveCampaignRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveCampaignResponseMessage.SerializeToString,
        ),
        'submitDataRecord': grpc.unary_unary_rpc_method_handler(
            servicer.submitDataRecord,
            request_deserializer=et__service__pb2.SubmitDataRecordRequestMessage.FromString,
            response_serializer=et__service__pb2.DefaultResponseMessage.SerializeToString,
        ),
        'submitDataRecords': grpc.unary_unary_rpc_method_handler(
            servicer.submitDataRecords,
            request_deserializer=et__service__pb2.SubmitDataRecordsRequestMessage.FromString,
            response_serializer=et__service__pb2.DefaultResponseMessage.SerializeToString,
        ),
        'submitHeartbeat': grpc.unary_unary_rpc_method_handler(
            servicer.submitHeartbeat,
            request_deserializer=et__service__pb2.SubmitHeartbeatRequestMessage.FromString,
            response_serializer=et__service__pb2.DefaultResponseMessage.SerializeToString,
        ),
        'submitDirectMessage': grpc.unary_unary_rpc_method_handler(
            servicer.submitDirectMessage,
            request_deserializer=et__service__pb2.SubmitDirectMessageRequestMessage.FromString,
            response_serializer=et__service__pb2.DefaultResponseMessage.SerializeToString,
        ),
        'retrieveParticipants': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveParticipants,
            request_deserializer=et__service__pb2.RetrieveParticipantsRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveParticipantsResponseMessage.SerializeToString,
        ),
        'retrieveParticipantStatistics': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveParticipantStatistics,
            request_deserializer=et__service__pb2.RetrieveParticipantStatisticsRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveParticipantStatisticsResponseMessage.SerializeToString,
        ),
        'retrieve100DataRecords': grpc.unary_unary_rpc_method_handler(
            servicer.retrieve100DataRecords,
            request_deserializer=et__service__pb2.Retrieve100DataRecordsRequestMessage.FromString,
            response_serializer=et__service__pb2.Retrieve100DataRecordsResponseMessage.SerializeToString,
        ),
        'retrieveFilteredDataRecords': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveFilteredDataRecords,
            request_deserializer=et__service__pb2.RetrieveFilteredDataRecordsRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveFilteredDataRecordsResponseMessage.SerializeToString,
        ),
        'retrieveUnreadDirectMessages': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveUnreadDirectMessages,
            request_deserializer=et__service__pb2.RetrieveUnreadDirectMessagesRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveUnreadDirectMessagesResponseMessage.SerializeToString,
        ),
        'retrieveUnreadNotifications': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveUnreadNotifications,
            request_deserializer=et__service__pb2.RetrieveUnreadNotificationsRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveUnreadNotificationsResponseMessage.SerializeToString,
        ),
        'bindDataSource': grpc.unary_unary_rpc_method_handler(
            servicer.bindDataSource,
            request_deserializer=et__service__pb2.BindDataSourceRequestMessage.FromString,
            response_serializer=et__service__pb2.BindDataSourceResponseMessage.SerializeToString,
        ),
        'retrieveAllDataSources': grpc.unary_unary_rpc_method_handler(
            servicer.retrieveAllDataSources,
            request_deserializer=et__service__pb2.RetrieveAllDataSourcesRequestMessage.FromString,
            response_serializer=et__service__pb2.RetrieveAllDataSourcesResponseMessage.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'ETService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
