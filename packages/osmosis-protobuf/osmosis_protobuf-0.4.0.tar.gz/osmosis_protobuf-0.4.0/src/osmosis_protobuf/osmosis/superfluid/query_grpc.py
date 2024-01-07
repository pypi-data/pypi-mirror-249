import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from ... import gogoproto
from ... import cosmos
from ... import google
import google.protobuf.timestamp_pb2
import google.protobuf.duration_pb2
from ... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.QueryParamsRequest, osmosis.superfluid.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AssetType(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.AssetTypeRequest, osmosis.superfluid.query_pb2.AssetTypeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AllAssets(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.AllAssetsRequest, osmosis.superfluid.query_pb2.AllAssetsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AssetMultiplier(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.AssetMultiplierRequest, osmosis.superfluid.query_pb2.AssetMultiplierResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AllIntermediaryAccounts(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.AllIntermediaryAccountsRequest, osmosis.superfluid.query_pb2.AllIntermediaryAccountsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ConnectedIntermediaryAccount(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.ConnectedIntermediaryAccountRequest, osmosis.superfluid.query_pb2.ConnectedIntermediaryAccountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalDelegationByValidatorForDenom(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.QueryTotalDelegationByValidatorForDenomRequest, osmosis.superfluid.query_pb2.QueryTotalDelegationByValidatorForDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalSuperfluidDelegations(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.TotalSuperfluidDelegationsRequest, osmosis.superfluid.query_pb2.TotalSuperfluidDelegationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SuperfluidDelegationAmount(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.SuperfluidDelegationAmountRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationAmountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SuperfluidDelegationsByDelegator(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.SuperfluidDelegationsByDelegatorRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationsByDelegatorResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SuperfluidUndelegationsByDelegator(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.SuperfluidUndelegationsByDelegatorRequest, osmosis.superfluid.query_pb2.SuperfluidUndelegationsByDelegatorResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SuperfluidDelegationsByValidatorDenom(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.SuperfluidDelegationsByValidatorDenomRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationsByValidatorDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSuperfluidDelegatedAmountByValidatorDenom(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.EstimateSuperfluidDelegatedAmountByValidatorDenomRequest, osmosis.superfluid.query_pb2.EstimateSuperfluidDelegatedAmountByValidatorDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalDelegationByDelegator(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.QueryTotalDelegationByDelegatorRequest, osmosis.superfluid.query_pb2.QueryTotalDelegationByDelegatorResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UnpoolWhitelist(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.QueryUnpoolWhitelistRequest, osmosis.superfluid.query_pb2.QueryUnpoolWhitelistResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserConcentratedSuperfluidPositionsDelegated(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsDelegatedRequest, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsDelegatedResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserConcentratedSuperfluidPositionsUndelegating(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsUndelegatingRequest, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsUndelegatingResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RestSupply(self, stream: 'grpclib.server.Stream[osmosis.superfluid.query_pb2.QueryRestSupplyRequest, osmosis.superfluid.query_pb2.QueryRestSupplyResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.superfluid.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.QueryParamsRequest, osmosis.superfluid.query_pb2.QueryParamsResponse), '/osmosis.superfluid.Query/AssetType': grpclib.const.Handler(self.AssetType, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.AssetTypeRequest, osmosis.superfluid.query_pb2.AssetTypeResponse), '/osmosis.superfluid.Query/AllAssets': grpclib.const.Handler(self.AllAssets, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.AllAssetsRequest, osmosis.superfluid.query_pb2.AllAssetsResponse), '/osmosis.superfluid.Query/AssetMultiplier': grpclib.const.Handler(self.AssetMultiplier, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.AssetMultiplierRequest, osmosis.superfluid.query_pb2.AssetMultiplierResponse), '/osmosis.superfluid.Query/AllIntermediaryAccounts': grpclib.const.Handler(self.AllIntermediaryAccounts, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.AllIntermediaryAccountsRequest, osmosis.superfluid.query_pb2.AllIntermediaryAccountsResponse), '/osmosis.superfluid.Query/ConnectedIntermediaryAccount': grpclib.const.Handler(self.ConnectedIntermediaryAccount, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.ConnectedIntermediaryAccountRequest, osmosis.superfluid.query_pb2.ConnectedIntermediaryAccountResponse), '/osmosis.superfluid.Query/TotalDelegationByValidatorForDenom': grpclib.const.Handler(self.TotalDelegationByValidatorForDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.QueryTotalDelegationByValidatorForDenomRequest, osmosis.superfluid.query_pb2.QueryTotalDelegationByValidatorForDenomResponse), '/osmosis.superfluid.Query/TotalSuperfluidDelegations': grpclib.const.Handler(self.TotalSuperfluidDelegations, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.TotalSuperfluidDelegationsRequest, osmosis.superfluid.query_pb2.TotalSuperfluidDelegationsResponse), '/osmosis.superfluid.Query/SuperfluidDelegationAmount': grpclib.const.Handler(self.SuperfluidDelegationAmount, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.SuperfluidDelegationAmountRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationAmountResponse), '/osmosis.superfluid.Query/SuperfluidDelegationsByDelegator': grpclib.const.Handler(self.SuperfluidDelegationsByDelegator, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.SuperfluidDelegationsByDelegatorRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationsByDelegatorResponse), '/osmosis.superfluid.Query/SuperfluidUndelegationsByDelegator': grpclib.const.Handler(self.SuperfluidUndelegationsByDelegator, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.SuperfluidUndelegationsByDelegatorRequest, osmosis.superfluid.query_pb2.SuperfluidUndelegationsByDelegatorResponse), '/osmosis.superfluid.Query/SuperfluidDelegationsByValidatorDenom': grpclib.const.Handler(self.SuperfluidDelegationsByValidatorDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.SuperfluidDelegationsByValidatorDenomRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationsByValidatorDenomResponse), '/osmosis.superfluid.Query/EstimateSuperfluidDelegatedAmountByValidatorDenom': grpclib.const.Handler(self.EstimateSuperfluidDelegatedAmountByValidatorDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.EstimateSuperfluidDelegatedAmountByValidatorDenomRequest, osmosis.superfluid.query_pb2.EstimateSuperfluidDelegatedAmountByValidatorDenomResponse), '/osmosis.superfluid.Query/TotalDelegationByDelegator': grpclib.const.Handler(self.TotalDelegationByDelegator, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.QueryTotalDelegationByDelegatorRequest, osmosis.superfluid.query_pb2.QueryTotalDelegationByDelegatorResponse), '/osmosis.superfluid.Query/UnpoolWhitelist': grpclib.const.Handler(self.UnpoolWhitelist, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.QueryUnpoolWhitelistRequest, osmosis.superfluid.query_pb2.QueryUnpoolWhitelistResponse), '/osmosis.superfluid.Query/UserConcentratedSuperfluidPositionsDelegated': grpclib.const.Handler(self.UserConcentratedSuperfluidPositionsDelegated, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsDelegatedRequest, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsDelegatedResponse), '/osmosis.superfluid.Query/UserConcentratedSuperfluidPositionsUndelegating': grpclib.const.Handler(self.UserConcentratedSuperfluidPositionsUndelegating, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsUndelegatingRequest, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsUndelegatingResponse), '/osmosis.superfluid.Query/RestSupply': grpclib.const.Handler(self.RestSupply, grpclib.const.Cardinality.UNARY_UNARY, osmosis.superfluid.query_pb2.QueryRestSupplyRequest, osmosis.superfluid.query_pb2.QueryRestSupplyResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/Params', osmosis.superfluid.query_pb2.QueryParamsRequest, osmosis.superfluid.query_pb2.QueryParamsResponse)
        self.AssetType = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/AssetType', osmosis.superfluid.query_pb2.AssetTypeRequest, osmosis.superfluid.query_pb2.AssetTypeResponse)
        self.AllAssets = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/AllAssets', osmosis.superfluid.query_pb2.AllAssetsRequest, osmosis.superfluid.query_pb2.AllAssetsResponse)
        self.AssetMultiplier = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/AssetMultiplier', osmosis.superfluid.query_pb2.AssetMultiplierRequest, osmosis.superfluid.query_pb2.AssetMultiplierResponse)
        self.AllIntermediaryAccounts = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/AllIntermediaryAccounts', osmosis.superfluid.query_pb2.AllIntermediaryAccountsRequest, osmosis.superfluid.query_pb2.AllIntermediaryAccountsResponse)
        self.ConnectedIntermediaryAccount = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/ConnectedIntermediaryAccount', osmosis.superfluid.query_pb2.ConnectedIntermediaryAccountRequest, osmosis.superfluid.query_pb2.ConnectedIntermediaryAccountResponse)
        self.TotalDelegationByValidatorForDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/TotalDelegationByValidatorForDenom', osmosis.superfluid.query_pb2.QueryTotalDelegationByValidatorForDenomRequest, osmosis.superfluid.query_pb2.QueryTotalDelegationByValidatorForDenomResponse)
        self.TotalSuperfluidDelegations = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/TotalSuperfluidDelegations', osmosis.superfluid.query_pb2.TotalSuperfluidDelegationsRequest, osmosis.superfluid.query_pb2.TotalSuperfluidDelegationsResponse)
        self.SuperfluidDelegationAmount = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/SuperfluidDelegationAmount', osmosis.superfluid.query_pb2.SuperfluidDelegationAmountRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationAmountResponse)
        self.SuperfluidDelegationsByDelegator = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/SuperfluidDelegationsByDelegator', osmosis.superfluid.query_pb2.SuperfluidDelegationsByDelegatorRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationsByDelegatorResponse)
        self.SuperfluidUndelegationsByDelegator = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/SuperfluidUndelegationsByDelegator', osmosis.superfluid.query_pb2.SuperfluidUndelegationsByDelegatorRequest, osmosis.superfluid.query_pb2.SuperfluidUndelegationsByDelegatorResponse)
        self.SuperfluidDelegationsByValidatorDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/SuperfluidDelegationsByValidatorDenom', osmosis.superfluid.query_pb2.SuperfluidDelegationsByValidatorDenomRequest, osmosis.superfluid.query_pb2.SuperfluidDelegationsByValidatorDenomResponse)
        self.EstimateSuperfluidDelegatedAmountByValidatorDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/EstimateSuperfluidDelegatedAmountByValidatorDenom', osmosis.superfluid.query_pb2.EstimateSuperfluidDelegatedAmountByValidatorDenomRequest, osmosis.superfluid.query_pb2.EstimateSuperfluidDelegatedAmountByValidatorDenomResponse)
        self.TotalDelegationByDelegator = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/TotalDelegationByDelegator', osmosis.superfluid.query_pb2.QueryTotalDelegationByDelegatorRequest, osmosis.superfluid.query_pb2.QueryTotalDelegationByDelegatorResponse)
        self.UnpoolWhitelist = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/UnpoolWhitelist', osmosis.superfluid.query_pb2.QueryUnpoolWhitelistRequest, osmosis.superfluid.query_pb2.QueryUnpoolWhitelistResponse)
        self.UserConcentratedSuperfluidPositionsDelegated = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/UserConcentratedSuperfluidPositionsDelegated', osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsDelegatedRequest, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsDelegatedResponse)
        self.UserConcentratedSuperfluidPositionsUndelegating = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/UserConcentratedSuperfluidPositionsUndelegating', osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsUndelegatingRequest, osmosis.superfluid.query_pb2.UserConcentratedSuperfluidPositionsUndelegatingResponse)
        self.RestSupply = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.superfluid.Query/RestSupply', osmosis.superfluid.query_pb2.QueryRestSupplyRequest, osmosis.superfluid.query_pb2.QueryRestSupplyResponse)