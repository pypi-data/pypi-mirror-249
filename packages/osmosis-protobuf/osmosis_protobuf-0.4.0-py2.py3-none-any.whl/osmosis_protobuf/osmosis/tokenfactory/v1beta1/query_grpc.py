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
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.tokenfactory.v1beta1.query_pb2.QueryParamsRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DenomAuthorityMetadata(self, stream: 'grpclib.server.Stream[osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomAuthorityMetadataRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomAuthorityMetadataResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DenomsFromCreator(self, stream: 'grpclib.server.Stream[osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomsFromCreatorRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomsFromCreatorResponse]') -> None:
        pass

    @abc.abstractmethod
    async def BeforeSendHookAddress(self, stream: 'grpclib.server.Stream[osmosis.tokenfactory.v1beta1.query_pb2.QueryBeforeSendHookAddressRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryBeforeSendHookAddressResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.tokenfactory.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.tokenfactory.v1beta1.query_pb2.QueryParamsRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryParamsResponse), '/osmosis.tokenfactory.v1beta1.Query/DenomAuthorityMetadata': grpclib.const.Handler(self.DenomAuthorityMetadata, grpclib.const.Cardinality.UNARY_UNARY, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomAuthorityMetadataRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomAuthorityMetadataResponse), '/osmosis.tokenfactory.v1beta1.Query/DenomsFromCreator': grpclib.const.Handler(self.DenomsFromCreator, grpclib.const.Cardinality.UNARY_UNARY, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomsFromCreatorRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomsFromCreatorResponse), '/osmosis.tokenfactory.v1beta1.Query/BeforeSendHookAddress': grpclib.const.Handler(self.BeforeSendHookAddress, grpclib.const.Cardinality.UNARY_UNARY, osmosis.tokenfactory.v1beta1.query_pb2.QueryBeforeSendHookAddressRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryBeforeSendHookAddressResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.tokenfactory.v1beta1.Query/Params', osmosis.tokenfactory.v1beta1.query_pb2.QueryParamsRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryParamsResponse)
        self.DenomAuthorityMetadata = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.tokenfactory.v1beta1.Query/DenomAuthorityMetadata', osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomAuthorityMetadataRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomAuthorityMetadataResponse)
        self.DenomsFromCreator = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.tokenfactory.v1beta1.Query/DenomsFromCreator', osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomsFromCreatorRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryDenomsFromCreatorResponse)
        self.BeforeSendHookAddress = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.tokenfactory.v1beta1.Query/BeforeSendHookAddress', osmosis.tokenfactory.v1beta1.query_pb2.QueryBeforeSendHookAddressRequest, osmosis.tokenfactory.v1beta1.query_pb2.QueryBeforeSendHookAddressResponse)