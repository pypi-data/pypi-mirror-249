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

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def SpotPrice(self, stream: 'grpclib.server.Stream[osmosis.gamm.v2.query_pb2.QuerySpotPriceRequest, osmosis.gamm.v2.query_pb2.QuerySpotPriceResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.gamm.v2.Query/SpotPrice': grpclib.const.Handler(self.SpotPrice, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v2.query_pb2.QuerySpotPriceRequest, osmosis.gamm.v2.query_pb2.QuerySpotPriceResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.SpotPrice = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v2.Query/SpotPrice', osmosis.gamm.v2.query_pb2.QuerySpotPriceRequest, osmosis.gamm.v2.query_pb2.QuerySpotPriceResponse)