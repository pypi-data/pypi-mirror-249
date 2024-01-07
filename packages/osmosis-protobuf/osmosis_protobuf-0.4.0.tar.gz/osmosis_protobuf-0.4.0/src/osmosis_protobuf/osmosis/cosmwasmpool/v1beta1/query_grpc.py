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
    async def Pools(self, stream: 'grpclib.server.Stream[osmosis.cosmwasmpool.v1beta1.query_pb2.PoolsRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.PoolsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.cosmwasmpool.v1beta1.query_pb2.ParamsRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.ParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ContractInfoByPoolId(self, stream: 'grpclib.server.Stream[osmosis.cosmwasmpool.v1beta1.query_pb2.ContractInfoByPoolIdRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.ContractInfoByPoolIdResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.cosmwasmpool.v1beta1.Query/Pools': grpclib.const.Handler(self.Pools, grpclib.const.Cardinality.UNARY_UNARY, osmosis.cosmwasmpool.v1beta1.query_pb2.PoolsRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.PoolsResponse), '/osmosis.cosmwasmpool.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.cosmwasmpool.v1beta1.query_pb2.ParamsRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.ParamsResponse), '/osmosis.cosmwasmpool.v1beta1.Query/ContractInfoByPoolId': grpclib.const.Handler(self.ContractInfoByPoolId, grpclib.const.Cardinality.UNARY_UNARY, osmosis.cosmwasmpool.v1beta1.query_pb2.ContractInfoByPoolIdRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.ContractInfoByPoolIdResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Pools = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.cosmwasmpool.v1beta1.Query/Pools', osmosis.cosmwasmpool.v1beta1.query_pb2.PoolsRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.PoolsResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.cosmwasmpool.v1beta1.Query/Params', osmosis.cosmwasmpool.v1beta1.query_pb2.ParamsRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.ParamsResponse)
        self.ContractInfoByPoolId = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.cosmwasmpool.v1beta1.Query/ContractInfoByPoolId', osmosis.cosmwasmpool.v1beta1.query_pb2.ContractInfoByPoolIdRequest, osmosis.cosmwasmpool.v1beta1.query_pb2.ContractInfoByPoolIdResponse)