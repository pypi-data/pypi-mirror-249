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
    async def ModuleBalance(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.ModuleBalanceRequest, osmosis.lockup.query_pb2.ModuleBalanceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ModuleLockedAmount(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.ModuleLockedAmountRequest, osmosis.lockup.query_pb2.ModuleLockedAmountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountUnlockableCoins(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountUnlockableCoinsRequest, osmosis.lockup.query_pb2.AccountUnlockableCoinsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountUnlockingCoins(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountUnlockingCoinsRequest, osmosis.lockup.query_pb2.AccountUnlockingCoinsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedCoins(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedCoinsRequest, osmosis.lockup.query_pb2.AccountLockedCoinsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedPastTime(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedPastTimeRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedPastTimeNotUnlockingOnly(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedPastTimeNotUnlockingOnlyRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeNotUnlockingOnlyResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountUnlockedBeforeTime(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountUnlockedBeforeTimeRequest, osmosis.lockup.query_pb2.AccountUnlockedBeforeTimeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedPastTimeDenom(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedPastTimeDenomRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LockedDenom(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.LockedDenomRequest, osmosis.lockup.query_pb2.LockedDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LockedByID(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.LockedRequest, osmosis.lockup.query_pb2.LockedResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LockRewardReceiver(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.LockRewardReceiverRequest, osmosis.lockup.query_pb2.LockRewardReceiverResponse]') -> None:
        pass

    @abc.abstractmethod
    async def NextLockID(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.NextLockIDRequest, osmosis.lockup.query_pb2.NextLockIDResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SyntheticLockupsByLockupID(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.SyntheticLockupsByLockupIDRequest, osmosis.lockup.query_pb2.SyntheticLockupsByLockupIDResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SyntheticLockupByLockupID(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.SyntheticLockupByLockupIDRequest, osmosis.lockup.query_pb2.SyntheticLockupByLockupIDResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedLongerDuration(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedLongerDurationRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedDuration(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedDurationRequest, osmosis.lockup.query_pb2.AccountLockedDurationResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedLongerDurationNotUnlockingOnly(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedLongerDurationNotUnlockingOnlyRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationNotUnlockingOnlyResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AccountLockedLongerDurationDenom(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.AccountLockedLongerDurationDenomRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.lockup.query_pb2.QueryParamsRequest, osmosis.lockup.query_pb2.QueryParamsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.lockup.Query/ModuleBalance': grpclib.const.Handler(self.ModuleBalance, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.ModuleBalanceRequest, osmosis.lockup.query_pb2.ModuleBalanceResponse), '/osmosis.lockup.Query/ModuleLockedAmount': grpclib.const.Handler(self.ModuleLockedAmount, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.ModuleLockedAmountRequest, osmosis.lockup.query_pb2.ModuleLockedAmountResponse), '/osmosis.lockup.Query/AccountUnlockableCoins': grpclib.const.Handler(self.AccountUnlockableCoins, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountUnlockableCoinsRequest, osmosis.lockup.query_pb2.AccountUnlockableCoinsResponse), '/osmosis.lockup.Query/AccountUnlockingCoins': grpclib.const.Handler(self.AccountUnlockingCoins, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountUnlockingCoinsRequest, osmosis.lockup.query_pb2.AccountUnlockingCoinsResponse), '/osmosis.lockup.Query/AccountLockedCoins': grpclib.const.Handler(self.AccountLockedCoins, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedCoinsRequest, osmosis.lockup.query_pb2.AccountLockedCoinsResponse), '/osmosis.lockup.Query/AccountLockedPastTime': grpclib.const.Handler(self.AccountLockedPastTime, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedPastTimeRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeResponse), '/osmosis.lockup.Query/AccountLockedPastTimeNotUnlockingOnly': grpclib.const.Handler(self.AccountLockedPastTimeNotUnlockingOnly, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedPastTimeNotUnlockingOnlyRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeNotUnlockingOnlyResponse), '/osmosis.lockup.Query/AccountUnlockedBeforeTime': grpclib.const.Handler(self.AccountUnlockedBeforeTime, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountUnlockedBeforeTimeRequest, osmosis.lockup.query_pb2.AccountUnlockedBeforeTimeResponse), '/osmosis.lockup.Query/AccountLockedPastTimeDenom': grpclib.const.Handler(self.AccountLockedPastTimeDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedPastTimeDenomRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeDenomResponse), '/osmosis.lockup.Query/LockedDenom': grpclib.const.Handler(self.LockedDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.LockedDenomRequest, osmosis.lockup.query_pb2.LockedDenomResponse), '/osmosis.lockup.Query/LockedByID': grpclib.const.Handler(self.LockedByID, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.LockedRequest, osmosis.lockup.query_pb2.LockedResponse), '/osmosis.lockup.Query/LockRewardReceiver': grpclib.const.Handler(self.LockRewardReceiver, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.LockRewardReceiverRequest, osmosis.lockup.query_pb2.LockRewardReceiverResponse), '/osmosis.lockup.Query/NextLockID': grpclib.const.Handler(self.NextLockID, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.NextLockIDRequest, osmosis.lockup.query_pb2.NextLockIDResponse), '/osmosis.lockup.Query/SyntheticLockupsByLockupID': grpclib.const.Handler(self.SyntheticLockupsByLockupID, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.SyntheticLockupsByLockupIDRequest, osmosis.lockup.query_pb2.SyntheticLockupsByLockupIDResponse), '/osmosis.lockup.Query/SyntheticLockupByLockupID': grpclib.const.Handler(self.SyntheticLockupByLockupID, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.SyntheticLockupByLockupIDRequest, osmosis.lockup.query_pb2.SyntheticLockupByLockupIDResponse), '/osmosis.lockup.Query/AccountLockedLongerDuration': grpclib.const.Handler(self.AccountLockedLongerDuration, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedLongerDurationRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationResponse), '/osmosis.lockup.Query/AccountLockedDuration': grpclib.const.Handler(self.AccountLockedDuration, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedDurationRequest, osmosis.lockup.query_pb2.AccountLockedDurationResponse), '/osmosis.lockup.Query/AccountLockedLongerDurationNotUnlockingOnly': grpclib.const.Handler(self.AccountLockedLongerDurationNotUnlockingOnly, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedLongerDurationNotUnlockingOnlyRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationNotUnlockingOnlyResponse), '/osmosis.lockup.Query/AccountLockedLongerDurationDenom': grpclib.const.Handler(self.AccountLockedLongerDurationDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.AccountLockedLongerDurationDenomRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationDenomResponse), '/osmosis.lockup.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.lockup.query_pb2.QueryParamsRequest, osmosis.lockup.query_pb2.QueryParamsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.ModuleBalance = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/ModuleBalance', osmosis.lockup.query_pb2.ModuleBalanceRequest, osmosis.lockup.query_pb2.ModuleBalanceResponse)
        self.ModuleLockedAmount = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/ModuleLockedAmount', osmosis.lockup.query_pb2.ModuleLockedAmountRequest, osmosis.lockup.query_pb2.ModuleLockedAmountResponse)
        self.AccountUnlockableCoins = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountUnlockableCoins', osmosis.lockup.query_pb2.AccountUnlockableCoinsRequest, osmosis.lockup.query_pb2.AccountUnlockableCoinsResponse)
        self.AccountUnlockingCoins = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountUnlockingCoins', osmosis.lockup.query_pb2.AccountUnlockingCoinsRequest, osmosis.lockup.query_pb2.AccountUnlockingCoinsResponse)
        self.AccountLockedCoins = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedCoins', osmosis.lockup.query_pb2.AccountLockedCoinsRequest, osmosis.lockup.query_pb2.AccountLockedCoinsResponse)
        self.AccountLockedPastTime = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedPastTime', osmosis.lockup.query_pb2.AccountLockedPastTimeRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeResponse)
        self.AccountLockedPastTimeNotUnlockingOnly = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedPastTimeNotUnlockingOnly', osmosis.lockup.query_pb2.AccountLockedPastTimeNotUnlockingOnlyRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeNotUnlockingOnlyResponse)
        self.AccountUnlockedBeforeTime = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountUnlockedBeforeTime', osmosis.lockup.query_pb2.AccountUnlockedBeforeTimeRequest, osmosis.lockup.query_pb2.AccountUnlockedBeforeTimeResponse)
        self.AccountLockedPastTimeDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedPastTimeDenom', osmosis.lockup.query_pb2.AccountLockedPastTimeDenomRequest, osmosis.lockup.query_pb2.AccountLockedPastTimeDenomResponse)
        self.LockedDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/LockedDenom', osmosis.lockup.query_pb2.LockedDenomRequest, osmosis.lockup.query_pb2.LockedDenomResponse)
        self.LockedByID = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/LockedByID', osmosis.lockup.query_pb2.LockedRequest, osmosis.lockup.query_pb2.LockedResponse)
        self.LockRewardReceiver = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/LockRewardReceiver', osmosis.lockup.query_pb2.LockRewardReceiverRequest, osmosis.lockup.query_pb2.LockRewardReceiverResponse)
        self.NextLockID = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/NextLockID', osmosis.lockup.query_pb2.NextLockIDRequest, osmosis.lockup.query_pb2.NextLockIDResponse)
        self.SyntheticLockupsByLockupID = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/SyntheticLockupsByLockupID', osmosis.lockup.query_pb2.SyntheticLockupsByLockupIDRequest, osmosis.lockup.query_pb2.SyntheticLockupsByLockupIDResponse)
        self.SyntheticLockupByLockupID = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/SyntheticLockupByLockupID', osmosis.lockup.query_pb2.SyntheticLockupByLockupIDRequest, osmosis.lockup.query_pb2.SyntheticLockupByLockupIDResponse)
        self.AccountLockedLongerDuration = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedLongerDuration', osmosis.lockup.query_pb2.AccountLockedLongerDurationRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationResponse)
        self.AccountLockedDuration = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedDuration', osmosis.lockup.query_pb2.AccountLockedDurationRequest, osmosis.lockup.query_pb2.AccountLockedDurationResponse)
        self.AccountLockedLongerDurationNotUnlockingOnly = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedLongerDurationNotUnlockingOnly', osmosis.lockup.query_pb2.AccountLockedLongerDurationNotUnlockingOnlyRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationNotUnlockingOnlyResponse)
        self.AccountLockedLongerDurationDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/AccountLockedLongerDurationDenom', osmosis.lockup.query_pb2.AccountLockedLongerDurationDenomRequest, osmosis.lockup.query_pb2.AccountLockedLongerDurationDenomResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.lockup.Query/Params', osmosis.lockup.query_pb2.QueryParamsRequest, osmosis.lockup.query_pb2.QueryParamsResponse)