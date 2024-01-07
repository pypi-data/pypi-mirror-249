import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import cosmwasm
from .... import google
from .... import cosmos
from .... import amino

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def ContractInfo(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryContractInfoRequest, cosmwasm.wasm.v1.query_pb2.QueryContractInfoResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ContractHistory(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryContractHistoryRequest, cosmwasm.wasm.v1.query_pb2.QueryContractHistoryResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ContractsByCode(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryContractsByCodeRequest, cosmwasm.wasm.v1.query_pb2.QueryContractsByCodeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AllContractState(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryAllContractStateRequest, cosmwasm.wasm.v1.query_pb2.QueryAllContractStateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RawContractState(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryRawContractStateRequest, cosmwasm.wasm.v1.query_pb2.QueryRawContractStateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SmartContractState(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QuerySmartContractStateRequest, cosmwasm.wasm.v1.query_pb2.QuerySmartContractStateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Code(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryCodeRequest, cosmwasm.wasm.v1.query_pb2.QueryCodeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Codes(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryCodesRequest, cosmwasm.wasm.v1.query_pb2.QueryCodesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def PinnedCodes(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryPinnedCodesRequest, cosmwasm.wasm.v1.query_pb2.QueryPinnedCodesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryParamsRequest, cosmwasm.wasm.v1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ContractsByCreator(self, stream: 'grpclib.server.Stream[cosmwasm.wasm.v1.query_pb2.QueryContractsByCreatorRequest, cosmwasm.wasm.v1.query_pb2.QueryContractsByCreatorResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/cosmwasm.wasm.v1.Query/ContractInfo': grpclib.const.Handler(self.ContractInfo, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryContractInfoRequest, cosmwasm.wasm.v1.query_pb2.QueryContractInfoResponse), '/cosmwasm.wasm.v1.Query/ContractHistory': grpclib.const.Handler(self.ContractHistory, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryContractHistoryRequest, cosmwasm.wasm.v1.query_pb2.QueryContractHistoryResponse), '/cosmwasm.wasm.v1.Query/ContractsByCode': grpclib.const.Handler(self.ContractsByCode, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryContractsByCodeRequest, cosmwasm.wasm.v1.query_pb2.QueryContractsByCodeResponse), '/cosmwasm.wasm.v1.Query/AllContractState': grpclib.const.Handler(self.AllContractState, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryAllContractStateRequest, cosmwasm.wasm.v1.query_pb2.QueryAllContractStateResponse), '/cosmwasm.wasm.v1.Query/RawContractState': grpclib.const.Handler(self.RawContractState, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryRawContractStateRequest, cosmwasm.wasm.v1.query_pb2.QueryRawContractStateResponse), '/cosmwasm.wasm.v1.Query/SmartContractState': grpclib.const.Handler(self.SmartContractState, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QuerySmartContractStateRequest, cosmwasm.wasm.v1.query_pb2.QuerySmartContractStateResponse), '/cosmwasm.wasm.v1.Query/Code': grpclib.const.Handler(self.Code, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryCodeRequest, cosmwasm.wasm.v1.query_pb2.QueryCodeResponse), '/cosmwasm.wasm.v1.Query/Codes': grpclib.const.Handler(self.Codes, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryCodesRequest, cosmwasm.wasm.v1.query_pb2.QueryCodesResponse), '/cosmwasm.wasm.v1.Query/PinnedCodes': grpclib.const.Handler(self.PinnedCodes, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryPinnedCodesRequest, cosmwasm.wasm.v1.query_pb2.QueryPinnedCodesResponse), '/cosmwasm.wasm.v1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryParamsRequest, cosmwasm.wasm.v1.query_pb2.QueryParamsResponse), '/cosmwasm.wasm.v1.Query/ContractsByCreator': grpclib.const.Handler(self.ContractsByCreator, grpclib.const.Cardinality.UNARY_UNARY, cosmwasm.wasm.v1.query_pb2.QueryContractsByCreatorRequest, cosmwasm.wasm.v1.query_pb2.QueryContractsByCreatorResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.ContractInfo = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/ContractInfo', cosmwasm.wasm.v1.query_pb2.QueryContractInfoRequest, cosmwasm.wasm.v1.query_pb2.QueryContractInfoResponse)
        self.ContractHistory = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/ContractHistory', cosmwasm.wasm.v1.query_pb2.QueryContractHistoryRequest, cosmwasm.wasm.v1.query_pb2.QueryContractHistoryResponse)
        self.ContractsByCode = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/ContractsByCode', cosmwasm.wasm.v1.query_pb2.QueryContractsByCodeRequest, cosmwasm.wasm.v1.query_pb2.QueryContractsByCodeResponse)
        self.AllContractState = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/AllContractState', cosmwasm.wasm.v1.query_pb2.QueryAllContractStateRequest, cosmwasm.wasm.v1.query_pb2.QueryAllContractStateResponse)
        self.RawContractState = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/RawContractState', cosmwasm.wasm.v1.query_pb2.QueryRawContractStateRequest, cosmwasm.wasm.v1.query_pb2.QueryRawContractStateResponse)
        self.SmartContractState = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/SmartContractState', cosmwasm.wasm.v1.query_pb2.QuerySmartContractStateRequest, cosmwasm.wasm.v1.query_pb2.QuerySmartContractStateResponse)
        self.Code = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/Code', cosmwasm.wasm.v1.query_pb2.QueryCodeRequest, cosmwasm.wasm.v1.query_pb2.QueryCodeResponse)
        self.Codes = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/Codes', cosmwasm.wasm.v1.query_pb2.QueryCodesRequest, cosmwasm.wasm.v1.query_pb2.QueryCodesResponse)
        self.PinnedCodes = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/PinnedCodes', cosmwasm.wasm.v1.query_pb2.QueryPinnedCodesRequest, cosmwasm.wasm.v1.query_pb2.QueryPinnedCodesResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/Params', cosmwasm.wasm.v1.query_pb2.QueryParamsRequest, cosmwasm.wasm.v1.query_pb2.QueryParamsResponse)
        self.ContractsByCreator = grpclib.client.UnaryUnaryMethod(channel, '/cosmwasm.wasm.v1.Query/ContractsByCreator', cosmwasm.wasm.v1.query_pb2.QueryContractsByCreatorRequest, cosmwasm.wasm.v1.query_pb2.QueryContractsByCreatorResponse)