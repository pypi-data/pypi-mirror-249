"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ....osmosis.poolmanager.v1beta1 import query_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2

class QueryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Params = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/Params', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ParamsRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ParamsResponse.FromString)
        self.EstimateSwapExactAmountIn = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountIn', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.FromString)
        self.EstimateSwapExactAmountInWithPrimitiveTypes = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountInWithPrimitiveTypes', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInWithPrimitiveTypesRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.FromString)
        self.EstimateSinglePoolSwapExactAmountIn = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountIn', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSinglePoolSwapExactAmountInRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.FromString)
        self.EstimateSwapExactAmountOut = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountOut', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.FromString)
        self.EstimateSwapExactAmountOutWithPrimitiveTypes = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountOutWithPrimitiveTypes', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutWithPrimitiveTypesRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.FromString)
        self.EstimateSinglePoolSwapExactAmountOut = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountOut', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSinglePoolSwapExactAmountOutRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.FromString)
        self.NumPools = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/NumPools', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.NumPoolsRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.NumPoolsResponse.FromString)
        self.Pool = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/Pool', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.PoolRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.PoolResponse.FromString)
        self.AllPools = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/AllPools', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.AllPoolsRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.AllPoolsResponse.FromString)
        self.ListPoolsByDenom = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/ListPoolsByDenom', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ListPoolsByDenomRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ListPoolsByDenomResponse.FromString)
        self.SpotPrice = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/SpotPrice', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.SpotPriceRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.SpotPriceResponse.FromString)
        self.TotalPoolLiquidity = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/TotalPoolLiquidity', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalPoolLiquidityRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalPoolLiquidityResponse.FromString)
        self.TotalLiquidity = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/TotalLiquidity', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalLiquidityRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalLiquidityResponse.FromString)
        self.TotalVolumeForPool = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/TotalVolumeForPool', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalVolumeForPoolRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalVolumeForPoolResponse.FromString)
        self.TradingPairTakerFee = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/TradingPairTakerFee', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TradingPairTakerFeeRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TradingPairTakerFeeResponse.FromString)
        self.EstimateTradeBasedOnPriceImpact = channel.unary_unary('/osmosis.poolmanager.v1beta1.Query/EstimateTradeBasedOnPriceImpact', request_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateTradeBasedOnPriceImpactRequest.SerializeToString, response_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateTradeBasedOnPriceImpactResponse.FromString)

class QueryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Params(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateSwapExactAmountIn(self, request, context):
        """Estimates swap amount out given in.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateSwapExactAmountInWithPrimitiveTypes(self, request, context):
        """EstimateSwapExactAmountInWithPrimitiveTypes is an alternative query for
        EstimateSwapExactAmountIn. Supports query via GRPC-Gateway by using
        primitive types instead of repeated structs. Each index in the
        routes_pool_id field corresponds to the respective routes_token_out_denom
        value, thus they are required to have the same length and are grouped
        together as pairs.
        example usage:
        http://0.0.0.0:1317/osmosis/poolmanager/v1beta1/1/estimate/
        swap_exact_amount_in_with_primitive_types?token_in=100000stake&routes_token_out_denom=uatom
        &routes_token_out_denom=uion&routes_pool_id=1&routes_pool_id=2
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateSinglePoolSwapExactAmountIn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateSwapExactAmountOut(self, request, context):
        """Estimates swap amount in given out.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateSwapExactAmountOutWithPrimitiveTypes(self, request, context):
        """Estimates swap amount in given out.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateSinglePoolSwapExactAmountOut(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NumPools(self, request, context):
        """Returns the total number of pools existing in Osmosis.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Pool(self, request, context):
        """Pool returns the Pool specified by the pool id
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AllPools(self, request, context):
        """AllPools returns all pools on the Osmosis chain sorted by IDs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListPoolsByDenom(self, request, context):
        """ListPoolsByDenom return all pools by denom
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpotPrice(self, request, context):
        """SpotPrice defines a gRPC query handler that returns the spot price given
        a base denomination and a quote denomination.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TotalPoolLiquidity(self, request, context):
        """TotalPoolLiquidity returns the total liquidity of the specified pool.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TotalLiquidity(self, request, context):
        """TotalLiquidity returns the total liquidity across all pools.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TotalVolumeForPool(self, request, context):
        """TotalVolumeForPool returns the total volume of the specified pool.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TradingPairTakerFee(self, request, context):
        """TradingPairTakerFee returns the taker fee for a given set of denoms
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EstimateTradeBasedOnPriceImpact(self, request, context):
        """EstimateTradeBasedOnPriceImpact returns an estimated trade based on price
        impact, if a trade cannot be estimated a 0 input and 0 output would be
        returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'Params': grpc.unary_unary_rpc_method_handler(servicer.Params, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ParamsRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ParamsResponse.SerializeToString), 'EstimateSwapExactAmountIn': grpc.unary_unary_rpc_method_handler(servicer.EstimateSwapExactAmountIn, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.SerializeToString), 'EstimateSwapExactAmountInWithPrimitiveTypes': grpc.unary_unary_rpc_method_handler(servicer.EstimateSwapExactAmountInWithPrimitiveTypes, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInWithPrimitiveTypesRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.SerializeToString), 'EstimateSinglePoolSwapExactAmountIn': grpc.unary_unary_rpc_method_handler(servicer.EstimateSinglePoolSwapExactAmountIn, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSinglePoolSwapExactAmountInRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.SerializeToString), 'EstimateSwapExactAmountOut': grpc.unary_unary_rpc_method_handler(servicer.EstimateSwapExactAmountOut, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.SerializeToString), 'EstimateSwapExactAmountOutWithPrimitiveTypes': grpc.unary_unary_rpc_method_handler(servicer.EstimateSwapExactAmountOutWithPrimitiveTypes, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutWithPrimitiveTypesRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.SerializeToString), 'EstimateSinglePoolSwapExactAmountOut': grpc.unary_unary_rpc_method_handler(servicer.EstimateSinglePoolSwapExactAmountOut, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSinglePoolSwapExactAmountOutRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.SerializeToString), 'NumPools': grpc.unary_unary_rpc_method_handler(servicer.NumPools, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.NumPoolsRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.NumPoolsResponse.SerializeToString), 'Pool': grpc.unary_unary_rpc_method_handler(servicer.Pool, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.PoolRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.PoolResponse.SerializeToString), 'AllPools': grpc.unary_unary_rpc_method_handler(servicer.AllPools, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.AllPoolsRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.AllPoolsResponse.SerializeToString), 'ListPoolsByDenom': grpc.unary_unary_rpc_method_handler(servicer.ListPoolsByDenom, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ListPoolsByDenomRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ListPoolsByDenomResponse.SerializeToString), 'SpotPrice': grpc.unary_unary_rpc_method_handler(servicer.SpotPrice, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.SpotPriceRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.SpotPriceResponse.SerializeToString), 'TotalPoolLiquidity': grpc.unary_unary_rpc_method_handler(servicer.TotalPoolLiquidity, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalPoolLiquidityRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalPoolLiquidityResponse.SerializeToString), 'TotalLiquidity': grpc.unary_unary_rpc_method_handler(servicer.TotalLiquidity, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalLiquidityRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalLiquidityResponse.SerializeToString), 'TotalVolumeForPool': grpc.unary_unary_rpc_method_handler(servicer.TotalVolumeForPool, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalVolumeForPoolRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalVolumeForPoolResponse.SerializeToString), 'TradingPairTakerFee': grpc.unary_unary_rpc_method_handler(servicer.TradingPairTakerFee, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TradingPairTakerFeeRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TradingPairTakerFeeResponse.SerializeToString), 'EstimateTradeBasedOnPriceImpact': grpc.unary_unary_rpc_method_handler(servicer.EstimateTradeBasedOnPriceImpact, request_deserializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateTradeBasedOnPriceImpactRequest.FromString, response_serializer=osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateTradeBasedOnPriceImpactResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('osmosis.poolmanager.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Params(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/Params', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ParamsRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateSwapExactAmountIn(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountIn', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateSwapExactAmountInWithPrimitiveTypes(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountInWithPrimitiveTypes', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInWithPrimitiveTypesRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateSinglePoolSwapExactAmountIn(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountIn', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSinglePoolSwapExactAmountInRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountInResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateSwapExactAmountOut(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountOut', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateSwapExactAmountOutWithPrimitiveTypes(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountOutWithPrimitiveTypes', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutWithPrimitiveTypesRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateSinglePoolSwapExactAmountOut(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountOut', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSinglePoolSwapExactAmountOutRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateSwapExactAmountOutResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NumPools(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/NumPools', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.NumPoolsRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.NumPoolsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Pool(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/Pool', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.PoolRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.PoolResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AllPools(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/AllPools', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.AllPoolsRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.AllPoolsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListPoolsByDenom(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/ListPoolsByDenom', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ListPoolsByDenomRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.ListPoolsByDenomResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SpotPrice(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/SpotPrice', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.SpotPriceRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.SpotPriceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TotalPoolLiquidity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/TotalPoolLiquidity', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalPoolLiquidityRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalPoolLiquidityResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TotalLiquidity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/TotalLiquidity', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalLiquidityRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalLiquidityResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TotalVolumeForPool(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/TotalVolumeForPool', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalVolumeForPoolRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TotalVolumeForPoolResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TradingPairTakerFee(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/TradingPairTakerFee', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TradingPairTakerFeeRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.TradingPairTakerFeeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EstimateTradeBasedOnPriceImpact(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.poolmanager.v1beta1.Query/EstimateTradeBasedOnPriceImpact', osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateTradeBasedOnPriceImpactRequest.SerializeToString, osmosis_dot_poolmanager_dot_v1beta1_dot_query__pb2.EstimateTradeBasedOnPriceImpactResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)