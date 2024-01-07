import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
import google.protobuf.duration_pb2
from .... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def FeeTokens(self, stream: 'grpclib.server.Stream[osmosis.txfees.v1beta1.query_pb2.QueryFeeTokensRequest, osmosis.txfees.v1beta1.query_pb2.QueryFeeTokensResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DenomSpotPrice(self, stream: 'grpclib.server.Stream[osmosis.txfees.v1beta1.query_pb2.QueryDenomSpotPriceRequest, osmosis.txfees.v1beta1.query_pb2.QueryDenomSpotPriceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DenomPoolId(self, stream: 'grpclib.server.Stream[osmosis.txfees.v1beta1.query_pb2.QueryDenomPoolIdRequest, osmosis.txfees.v1beta1.query_pb2.QueryDenomPoolIdResponse]') -> None:
        pass

    @abc.abstractmethod
    async def BaseDenom(self, stream: 'grpclib.server.Stream[osmosis.txfees.v1beta1.query_pb2.QueryBaseDenomRequest, osmosis.txfees.v1beta1.query_pb2.QueryBaseDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetEipBaseFee(self, stream: 'grpclib.server.Stream[osmosis.txfees.v1beta1.query_pb2.QueryEipBaseFeeRequest, osmosis.txfees.v1beta1.query_pb2.QueryEipBaseFeeResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.txfees.v1beta1.Query/FeeTokens': grpclib.const.Handler(self.FeeTokens, grpclib.const.Cardinality.UNARY_UNARY, osmosis.txfees.v1beta1.query_pb2.QueryFeeTokensRequest, osmosis.txfees.v1beta1.query_pb2.QueryFeeTokensResponse), '/osmosis.txfees.v1beta1.Query/DenomSpotPrice': grpclib.const.Handler(self.DenomSpotPrice, grpclib.const.Cardinality.UNARY_UNARY, osmosis.txfees.v1beta1.query_pb2.QueryDenomSpotPriceRequest, osmosis.txfees.v1beta1.query_pb2.QueryDenomSpotPriceResponse), '/osmosis.txfees.v1beta1.Query/DenomPoolId': grpclib.const.Handler(self.DenomPoolId, grpclib.const.Cardinality.UNARY_UNARY, osmosis.txfees.v1beta1.query_pb2.QueryDenomPoolIdRequest, osmosis.txfees.v1beta1.query_pb2.QueryDenomPoolIdResponse), '/osmosis.txfees.v1beta1.Query/BaseDenom': grpclib.const.Handler(self.BaseDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.txfees.v1beta1.query_pb2.QueryBaseDenomRequest, osmosis.txfees.v1beta1.query_pb2.QueryBaseDenomResponse), '/osmosis.txfees.v1beta1.Query/GetEipBaseFee': grpclib.const.Handler(self.GetEipBaseFee, grpclib.const.Cardinality.UNARY_UNARY, osmosis.txfees.v1beta1.query_pb2.QueryEipBaseFeeRequest, osmosis.txfees.v1beta1.query_pb2.QueryEipBaseFeeResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.FeeTokens = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.txfees.v1beta1.Query/FeeTokens', osmosis.txfees.v1beta1.query_pb2.QueryFeeTokensRequest, osmosis.txfees.v1beta1.query_pb2.QueryFeeTokensResponse)
        self.DenomSpotPrice = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.txfees.v1beta1.Query/DenomSpotPrice', osmosis.txfees.v1beta1.query_pb2.QueryDenomSpotPriceRequest, osmosis.txfees.v1beta1.query_pb2.QueryDenomSpotPriceResponse)
        self.DenomPoolId = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.txfees.v1beta1.Query/DenomPoolId', osmosis.txfees.v1beta1.query_pb2.QueryDenomPoolIdRequest, osmosis.txfees.v1beta1.query_pb2.QueryDenomPoolIdResponse)
        self.BaseDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.txfees.v1beta1.Query/BaseDenom', osmosis.txfees.v1beta1.query_pb2.QueryBaseDenomRequest, osmosis.txfees.v1beta1.query_pb2.QueryBaseDenomResponse)
        self.GetEipBaseFee = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.txfees.v1beta1.Query/GetEipBaseFee', osmosis.txfees.v1beta1.query_pb2.QueryEipBaseFeeRequest, osmosis.txfees.v1beta1.query_pb2.QueryEipBaseFeeResponse)