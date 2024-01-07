import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.mint.v1beta1.query_pb2.QueryParamsRequest, osmosis.mint.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EpochProvisions(self, stream: 'grpclib.server.Stream[osmosis.mint.v1beta1.query_pb2.QueryEpochProvisionsRequest, osmosis.mint.v1beta1.query_pb2.QueryEpochProvisionsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.mint.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.mint.v1beta1.query_pb2.QueryParamsRequest, osmosis.mint.v1beta1.query_pb2.QueryParamsResponse), '/osmosis.mint.v1beta1.Query/EpochProvisions': grpclib.const.Handler(self.EpochProvisions, grpclib.const.Cardinality.UNARY_UNARY, osmosis.mint.v1beta1.query_pb2.QueryEpochProvisionsRequest, osmosis.mint.v1beta1.query_pb2.QueryEpochProvisionsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.mint.v1beta1.Query/Params', osmosis.mint.v1beta1.query_pb2.QueryParamsRequest, osmosis.mint.v1beta1.query_pb2.QueryParamsResponse)
        self.EpochProvisions = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.mint.v1beta1.Query/EpochProvisions', osmosis.mint.v1beta1.query_pb2.QueryEpochProvisionsRequest, osmosis.mint.v1beta1.query_pb2.QueryEpochProvisionsResponse)