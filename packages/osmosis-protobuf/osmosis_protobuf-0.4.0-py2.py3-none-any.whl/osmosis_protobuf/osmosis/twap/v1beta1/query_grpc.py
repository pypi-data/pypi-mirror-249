import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import osmosis
from .... import cosmos
from .... import google
import google.protobuf.any_pb2
from .... import cosmos_proto
import google.protobuf.timestamp_pb2

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.twap.v1beta1.query_pb2.ParamsRequest, osmosis.twap.v1beta1.query_pb2.ParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ArithmeticTwap(self, stream: 'grpclib.server.Stream[osmosis.twap.v1beta1.query_pb2.ArithmeticTwapRequest, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ArithmeticTwapToNow(self, stream: 'grpclib.server.Stream[osmosis.twap.v1beta1.query_pb2.ArithmeticTwapToNowRequest, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapToNowResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GeometricTwap(self, stream: 'grpclib.server.Stream[osmosis.twap.v1beta1.query_pb2.GeometricTwapRequest, osmosis.twap.v1beta1.query_pb2.GeometricTwapResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GeometricTwapToNow(self, stream: 'grpclib.server.Stream[osmosis.twap.v1beta1.query_pb2.GeometricTwapToNowRequest, osmosis.twap.v1beta1.query_pb2.GeometricTwapToNowResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.twap.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.twap.v1beta1.query_pb2.ParamsRequest, osmosis.twap.v1beta1.query_pb2.ParamsResponse), '/osmosis.twap.v1beta1.Query/ArithmeticTwap': grpclib.const.Handler(self.ArithmeticTwap, grpclib.const.Cardinality.UNARY_UNARY, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapRequest, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapResponse), '/osmosis.twap.v1beta1.Query/ArithmeticTwapToNow': grpclib.const.Handler(self.ArithmeticTwapToNow, grpclib.const.Cardinality.UNARY_UNARY, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapToNowRequest, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapToNowResponse), '/osmosis.twap.v1beta1.Query/GeometricTwap': grpclib.const.Handler(self.GeometricTwap, grpclib.const.Cardinality.UNARY_UNARY, osmosis.twap.v1beta1.query_pb2.GeometricTwapRequest, osmosis.twap.v1beta1.query_pb2.GeometricTwapResponse), '/osmosis.twap.v1beta1.Query/GeometricTwapToNow': grpclib.const.Handler(self.GeometricTwapToNow, grpclib.const.Cardinality.UNARY_UNARY, osmosis.twap.v1beta1.query_pb2.GeometricTwapToNowRequest, osmosis.twap.v1beta1.query_pb2.GeometricTwapToNowResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.twap.v1beta1.Query/Params', osmosis.twap.v1beta1.query_pb2.ParamsRequest, osmosis.twap.v1beta1.query_pb2.ParamsResponse)
        self.ArithmeticTwap = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.twap.v1beta1.Query/ArithmeticTwap', osmosis.twap.v1beta1.query_pb2.ArithmeticTwapRequest, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapResponse)
        self.ArithmeticTwapToNow = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.twap.v1beta1.Query/ArithmeticTwapToNow', osmosis.twap.v1beta1.query_pb2.ArithmeticTwapToNowRequest, osmosis.twap.v1beta1.query_pb2.ArithmeticTwapToNowResponse)
        self.GeometricTwap = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.twap.v1beta1.Query/GeometricTwap', osmosis.twap.v1beta1.query_pb2.GeometricTwapRequest, osmosis.twap.v1beta1.query_pb2.GeometricTwapResponse)
        self.GeometricTwapToNow = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.twap.v1beta1.Query/GeometricTwapToNow', osmosis.twap.v1beta1.query_pb2.GeometricTwapToNowRequest, osmosis.twap.v1beta1.query_pb2.GeometricTwapToNowResponse)