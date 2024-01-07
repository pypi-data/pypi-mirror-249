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
    async def Pools(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryPoolsRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def NumPools(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryNumPoolsRequest, osmosis.gamm.v1beta1.query_pb2.QueryNumPoolsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalLiquidity(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryTotalLiquidityRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalLiquidityResponse]') -> None:
        pass

    @abc.abstractmethod
    async def PoolsWithFilter(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryPoolsWithFilterRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolsWithFilterResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Pool(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryPoolRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolResponse]') -> None:
        pass

    @abc.abstractmethod
    async def PoolType(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryPoolTypeRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolTypeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def CalcJoinPoolNoSwapShares(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolNoSwapSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolNoSwapSharesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def CalcJoinPoolShares(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolSharesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def CalcExitPoolCoinsFromShares(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryCalcExitPoolCoinsFromSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcExitPoolCoinsFromSharesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def PoolParams(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryPoolParamsRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalPoolLiquidity(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryTotalPoolLiquidityRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalPoolLiquidityResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalShares(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryTotalSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalSharesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SpotPrice(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QuerySpotPriceRequest, osmosis.gamm.v1beta1.query_pb2.QuerySpotPriceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSwapExactAmountIn(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountInRequest, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountInResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSwapExactAmountOut(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountOutRequest, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountOutResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ConcentratedPoolIdLinkFromCFMM(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryConcentratedPoolIdLinkFromCFMMRequest, osmosis.gamm.v1beta1.query_pb2.QueryConcentratedPoolIdLinkFromCFMMResponse]') -> None:
        pass

    @abc.abstractmethod
    async def CFMMConcentratedPoolLinks(self, stream: 'grpclib.server.Stream[osmosis.gamm.v1beta1.query_pb2.QueryCFMMConcentratedPoolLinksRequest, osmosis.gamm.v1beta1.query_pb2.QueryCFMMConcentratedPoolLinksResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.gamm.v1beta1.Query/Pools': grpclib.const.Handler(self.Pools, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryPoolsRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolsResponse), '/osmosis.gamm.v1beta1.Query/NumPools': grpclib.const.Handler(self.NumPools, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryNumPoolsRequest, osmosis.gamm.v1beta1.query_pb2.QueryNumPoolsResponse), '/osmosis.gamm.v1beta1.Query/TotalLiquidity': grpclib.const.Handler(self.TotalLiquidity, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryTotalLiquidityRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalLiquidityResponse), '/osmosis.gamm.v1beta1.Query/PoolsWithFilter': grpclib.const.Handler(self.PoolsWithFilter, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryPoolsWithFilterRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolsWithFilterResponse), '/osmosis.gamm.v1beta1.Query/Pool': grpclib.const.Handler(self.Pool, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryPoolRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolResponse), '/osmosis.gamm.v1beta1.Query/PoolType': grpclib.const.Handler(self.PoolType, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryPoolTypeRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolTypeResponse), '/osmosis.gamm.v1beta1.Query/CalcJoinPoolNoSwapShares': grpclib.const.Handler(self.CalcJoinPoolNoSwapShares, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolNoSwapSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolNoSwapSharesResponse), '/osmosis.gamm.v1beta1.Query/CalcJoinPoolShares': grpclib.const.Handler(self.CalcJoinPoolShares, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolSharesResponse), '/osmosis.gamm.v1beta1.Query/CalcExitPoolCoinsFromShares': grpclib.const.Handler(self.CalcExitPoolCoinsFromShares, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryCalcExitPoolCoinsFromSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcExitPoolCoinsFromSharesResponse), '/osmosis.gamm.v1beta1.Query/PoolParams': grpclib.const.Handler(self.PoolParams, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryPoolParamsRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolParamsResponse), '/osmosis.gamm.v1beta1.Query/TotalPoolLiquidity': grpclib.const.Handler(self.TotalPoolLiquidity, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryTotalPoolLiquidityRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalPoolLiquidityResponse), '/osmosis.gamm.v1beta1.Query/TotalShares': grpclib.const.Handler(self.TotalShares, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryTotalSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalSharesResponse), '/osmosis.gamm.v1beta1.Query/SpotPrice': grpclib.const.Handler(self.SpotPrice, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QuerySpotPriceRequest, osmosis.gamm.v1beta1.query_pb2.QuerySpotPriceResponse), '/osmosis.gamm.v1beta1.Query/EstimateSwapExactAmountIn': grpclib.const.Handler(self.EstimateSwapExactAmountIn, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountInRequest, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountInResponse), '/osmosis.gamm.v1beta1.Query/EstimateSwapExactAmountOut': grpclib.const.Handler(self.EstimateSwapExactAmountOut, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountOutRequest, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountOutResponse), '/osmosis.gamm.v1beta1.Query/ConcentratedPoolIdLinkFromCFMM': grpclib.const.Handler(self.ConcentratedPoolIdLinkFromCFMM, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryConcentratedPoolIdLinkFromCFMMRequest, osmosis.gamm.v1beta1.query_pb2.QueryConcentratedPoolIdLinkFromCFMMResponse), '/osmosis.gamm.v1beta1.Query/CFMMConcentratedPoolLinks': grpclib.const.Handler(self.CFMMConcentratedPoolLinks, grpclib.const.Cardinality.UNARY_UNARY, osmosis.gamm.v1beta1.query_pb2.QueryCFMMConcentratedPoolLinksRequest, osmosis.gamm.v1beta1.query_pb2.QueryCFMMConcentratedPoolLinksResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Pools = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/Pools', osmosis.gamm.v1beta1.query_pb2.QueryPoolsRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolsResponse)
        self.NumPools = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/NumPools', osmosis.gamm.v1beta1.query_pb2.QueryNumPoolsRequest, osmosis.gamm.v1beta1.query_pb2.QueryNumPoolsResponse)
        self.TotalLiquidity = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/TotalLiquidity', osmosis.gamm.v1beta1.query_pb2.QueryTotalLiquidityRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalLiquidityResponse)
        self.PoolsWithFilter = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/PoolsWithFilter', osmosis.gamm.v1beta1.query_pb2.QueryPoolsWithFilterRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolsWithFilterResponse)
        self.Pool = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/Pool', osmosis.gamm.v1beta1.query_pb2.QueryPoolRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolResponse)
        self.PoolType = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/PoolType', osmosis.gamm.v1beta1.query_pb2.QueryPoolTypeRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolTypeResponse)
        self.CalcJoinPoolNoSwapShares = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/CalcJoinPoolNoSwapShares', osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolNoSwapSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolNoSwapSharesResponse)
        self.CalcJoinPoolShares = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/CalcJoinPoolShares', osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcJoinPoolSharesResponse)
        self.CalcExitPoolCoinsFromShares = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/CalcExitPoolCoinsFromShares', osmosis.gamm.v1beta1.query_pb2.QueryCalcExitPoolCoinsFromSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryCalcExitPoolCoinsFromSharesResponse)
        self.PoolParams = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/PoolParams', osmosis.gamm.v1beta1.query_pb2.QueryPoolParamsRequest, osmosis.gamm.v1beta1.query_pb2.QueryPoolParamsResponse)
        self.TotalPoolLiquidity = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/TotalPoolLiquidity', osmosis.gamm.v1beta1.query_pb2.QueryTotalPoolLiquidityRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalPoolLiquidityResponse)
        self.TotalShares = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/TotalShares', osmosis.gamm.v1beta1.query_pb2.QueryTotalSharesRequest, osmosis.gamm.v1beta1.query_pb2.QueryTotalSharesResponse)
        self.SpotPrice = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/SpotPrice', osmosis.gamm.v1beta1.query_pb2.QuerySpotPriceRequest, osmosis.gamm.v1beta1.query_pb2.QuerySpotPriceResponse)
        self.EstimateSwapExactAmountIn = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/EstimateSwapExactAmountIn', osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountInRequest, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountInResponse)
        self.EstimateSwapExactAmountOut = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/EstimateSwapExactAmountOut', osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountOutRequest, osmosis.gamm.v1beta1.query_pb2.QuerySwapExactAmountOutResponse)
        self.ConcentratedPoolIdLinkFromCFMM = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/ConcentratedPoolIdLinkFromCFMM', osmosis.gamm.v1beta1.query_pb2.QueryConcentratedPoolIdLinkFromCFMMRequest, osmosis.gamm.v1beta1.query_pb2.QueryConcentratedPoolIdLinkFromCFMMResponse)
        self.CFMMConcentratedPoolLinks = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.gamm.v1beta1.Query/CFMMConcentratedPoolLinks', osmosis.gamm.v1beta1.query_pb2.QueryCFMMConcentratedPoolLinksRequest, osmosis.gamm.v1beta1.query_pb2.QueryCFMMConcentratedPoolLinksResponse)