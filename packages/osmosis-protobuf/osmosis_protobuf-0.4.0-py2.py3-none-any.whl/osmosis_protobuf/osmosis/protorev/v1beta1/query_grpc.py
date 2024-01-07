import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import cosmos
from .... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryParamsRequest, osmosis.protorev.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevNumberOfTrades(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevNumberOfTradesRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevNumberOfTradesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevProfitsByDenom(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevProfitsByDenomRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevProfitsByDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevAllProfits(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllProfitsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllProfitsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevStatisticsByRoute(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevStatisticsByRouteRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevStatisticsByRouteResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevAllRouteStatistics(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllRouteStatisticsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllRouteStatisticsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevTokenPairArbRoutes(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevTokenPairArbRoutesRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevTokenPairArbRoutesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevAdminAccount(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAdminAccountRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAdminAccountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevDeveloperAccount(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevDeveloperAccountRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevDeveloperAccountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevInfoByPoolType(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevInfoByPoolTypeRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevInfoByPoolTypeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevMaxPoolPointsPerTx(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerTxRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerTxResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevMaxPoolPointsPerBlock(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerBlockRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerBlockResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevBaseDenoms(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevBaseDenomsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevBaseDenomsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevEnabled(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevEnabledRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevEnabledResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetProtoRevPool(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevPoolRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevPoolResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetAllProtocolRevenue(self, stream: 'grpclib.server.Stream[osmosis.protorev.v1beta1.query_pb2.QueryGetAllProtocolRevenueRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetAllProtocolRevenueResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.protorev.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryParamsRequest, osmosis.protorev.v1beta1.query_pb2.QueryParamsResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevNumberOfTrades': grpclib.const.Handler(self.GetProtoRevNumberOfTrades, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevNumberOfTradesRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevNumberOfTradesResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevProfitsByDenom': grpclib.const.Handler(self.GetProtoRevProfitsByDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevProfitsByDenomRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevProfitsByDenomResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevAllProfits': grpclib.const.Handler(self.GetProtoRevAllProfits, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllProfitsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllProfitsResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevStatisticsByRoute': grpclib.const.Handler(self.GetProtoRevStatisticsByRoute, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevStatisticsByRouteRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevStatisticsByRouteResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevAllRouteStatistics': grpclib.const.Handler(self.GetProtoRevAllRouteStatistics, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllRouteStatisticsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllRouteStatisticsResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevTokenPairArbRoutes': grpclib.const.Handler(self.GetProtoRevTokenPairArbRoutes, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevTokenPairArbRoutesRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevTokenPairArbRoutesResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevAdminAccount': grpclib.const.Handler(self.GetProtoRevAdminAccount, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAdminAccountRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAdminAccountResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevDeveloperAccount': grpclib.const.Handler(self.GetProtoRevDeveloperAccount, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevDeveloperAccountRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevDeveloperAccountResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevInfoByPoolType': grpclib.const.Handler(self.GetProtoRevInfoByPoolType, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevInfoByPoolTypeRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevInfoByPoolTypeResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevMaxPoolPointsPerTx': grpclib.const.Handler(self.GetProtoRevMaxPoolPointsPerTx, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerTxRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerTxResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevMaxPoolPointsPerBlock': grpclib.const.Handler(self.GetProtoRevMaxPoolPointsPerBlock, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerBlockRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerBlockResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevBaseDenoms': grpclib.const.Handler(self.GetProtoRevBaseDenoms, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevBaseDenomsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevBaseDenomsResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevEnabled': grpclib.const.Handler(self.GetProtoRevEnabled, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevEnabledRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevEnabledResponse), '/osmosis.protorev.v1beta1.Query/GetProtoRevPool': grpclib.const.Handler(self.GetProtoRevPool, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevPoolRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevPoolResponse), '/osmosis.protorev.v1beta1.Query/GetAllProtocolRevenue': grpclib.const.Handler(self.GetAllProtocolRevenue, grpclib.const.Cardinality.UNARY_UNARY, osmosis.protorev.v1beta1.query_pb2.QueryGetAllProtocolRevenueRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetAllProtocolRevenueResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/Params', osmosis.protorev.v1beta1.query_pb2.QueryParamsRequest, osmosis.protorev.v1beta1.query_pb2.QueryParamsResponse)
        self.GetProtoRevNumberOfTrades = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevNumberOfTrades', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevNumberOfTradesRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevNumberOfTradesResponse)
        self.GetProtoRevProfitsByDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevProfitsByDenom', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevProfitsByDenomRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevProfitsByDenomResponse)
        self.GetProtoRevAllProfits = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevAllProfits', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllProfitsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllProfitsResponse)
        self.GetProtoRevStatisticsByRoute = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevStatisticsByRoute', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevStatisticsByRouteRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevStatisticsByRouteResponse)
        self.GetProtoRevAllRouteStatistics = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevAllRouteStatistics', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllRouteStatisticsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAllRouteStatisticsResponse)
        self.GetProtoRevTokenPairArbRoutes = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevTokenPairArbRoutes', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevTokenPairArbRoutesRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevTokenPairArbRoutesResponse)
        self.GetProtoRevAdminAccount = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevAdminAccount', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAdminAccountRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevAdminAccountResponse)
        self.GetProtoRevDeveloperAccount = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevDeveloperAccount', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevDeveloperAccountRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevDeveloperAccountResponse)
        self.GetProtoRevInfoByPoolType = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevInfoByPoolType', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevInfoByPoolTypeRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevInfoByPoolTypeResponse)
        self.GetProtoRevMaxPoolPointsPerTx = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevMaxPoolPointsPerTx', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerTxRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerTxResponse)
        self.GetProtoRevMaxPoolPointsPerBlock = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevMaxPoolPointsPerBlock', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerBlockRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevMaxPoolPointsPerBlockResponse)
        self.GetProtoRevBaseDenoms = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevBaseDenoms', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevBaseDenomsRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevBaseDenomsResponse)
        self.GetProtoRevEnabled = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevEnabled', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevEnabledRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevEnabledResponse)
        self.GetProtoRevPool = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetProtoRevPool', osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevPoolRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetProtoRevPoolResponse)
        self.GetAllProtocolRevenue = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.protorev.v1beta1.Query/GetAllProtocolRevenue', osmosis.protorev.v1beta1.query_pb2.QueryGetAllProtocolRevenueRequest, osmosis.protorev.v1beta1.query_pb2.QueryGetAllProtocolRevenueResponse)