"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....osmosis.poolmanager.v1beta1 import genesis_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_genesis__pb2
from ....osmosis.txfees.v1beta1 import genesis_pb2 as osmosis_dot_txfees_dot_v1beta1_dot_genesis__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'osmosis/protorev/v1beta1/protorev.proto\x12\x18osmosis.protorev.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a)osmosis/poolmanager/v1beta1/genesis.proto\x1a$osmosis/txfees/v1beta1/genesis.proto"\xba\x01\n\x12TokenPairArbRoutes\x12N\n\narb_routes\x18\x01 \x03(\x0b2\x1f.osmosis.protorev.v1beta1.RouteB\x19\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"arb_routes"\x12%\n\x08token_in\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x12\'\n\ttoken_out\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"token_out":\x04\xe8\xa0\x1f\x01"\x9b\x01\n\x05Route\x12F\n\x06trades\x18\x01 \x03(\x0b2\x1f.osmosis.protorev.v1beta1.TradeB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"trades"\x12D\n\tstep_size\x18\x02 \x01(\tB1\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x10yaml:"step_size":\x04\xe8\xa0\x1f\x01"|\n\x05Trade\x12\x1d\n\x04pool\x18\x01 \x01(\x04B\x0f\xf2\xde\x1f\x0byaml:"pool"\x12%\n\x08token_in\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x12\'\n\ttoken_out\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"token_out":\x04\xe8\xa0\x1f\x01"\xca\x01\n\x0fRouteStatistics\x12B\n\x07profits\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x16\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"\x12R\n\x10number_of_trades\x18\x02 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"number_of_trades"\x12\x1f\n\x05route\x18\x03 \x03(\x04B\x10\xf2\xde\x1f\x0cyaml:"route""\xe5\x01\n\x0bPoolWeights\x12/\n\rstable_weight\x18\x01 \x01(\x04B\x18\xf2\xde\x1f\x14yaml:"stable_weight"\x123\n\x0fbalancer_weight\x18\x02 \x01(\x04B\x1a\xf2\xde\x1f\x16yaml:"balancer_weight"\x12;\n\x13concentrated_weight\x18\x03 \x01(\x04B\x1e\xf2\xde\x1f\x1ayaml:"concentrated_weight"\x123\n\x0fcosmwasm_weight\x18\x04 \x01(\x04B\x1a\xf2\xde\x1f\x16yaml:"cosmwasm_weight""\xf2\x02\n\x0eInfoByPoolType\x12O\n\x06stable\x18\x01 \x01(\x0b2(.osmosis.protorev.v1beta1.StablePoolInfoB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"stable"\x12U\n\x08balancer\x18\x02 \x01(\x0b2*.osmosis.protorev.v1beta1.BalancerPoolInfoB\x17\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"balancer"\x12a\n\x0cconcentrated\x18\x03 \x01(\x0b2..osmosis.protorev.v1beta1.ConcentratedPoolInfoB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"concentrated"\x12U\n\x08cosmwasm\x18\x04 \x01(\x0b2*.osmosis.protorev.v1beta1.CosmwasmPoolInfoB\x17\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"cosmwasm""3\n\x0eStablePoolInfo\x12!\n\x06weight\x18\x01 \x01(\x04B\x11\xf2\xde\x1f\ryaml:"weight""5\n\x10BalancerPoolInfo\x12!\n\x06weight\x18\x01 \x01(\x04B\x11\xf2\xde\x1f\ryaml:"weight""r\n\x14ConcentratedPoolInfo\x12!\n\x06weight\x18\x01 \x01(\x04B\x11\xf2\xde\x1f\ryaml:"weight"\x127\n\x11max_ticks_crossed\x18\x02 \x01(\x04B\x1c\xf2\xde\x1f\x18yaml:"max_ticks_crossed""h\n\x10CosmwasmPoolInfo\x12T\n\x0bweight_maps\x18\x01 \x03(\x0b2#.osmosis.protorev.v1beta1.WeightMapB\x1a\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"weight_maps""e\n\tWeightMap\x12!\n\x06weight\x18\x01 \x01(\x04B\x11\xf2\xde\x1f\ryaml:"weight"\x125\n\x10contract_address\x18\x02 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"contract_address""r\n\tBaseDenom\x12\x1f\n\x05denom\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom"\x12D\n\tstep_size\x18\x02 \x01(\tB1\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x10yaml:"step_size""\xcd\x02\n\x12AllProtocolRevenue\x12l\n\x12taker_fees_tracker\x18\x01 \x01(\x0b2-.osmosis.poolmanager.v1beta1.TakerFeesTrackerB!\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"taker_fees_tracker"\x12^\n\x0ftx_fees_tracker\x18\x02 \x01(\x0b2%.osmosis.txfees.v1beta1.TxFeesTrackerB\x1e\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"tx_fees_tracker"\x12i\n\x12cyclic_arb_tracker\x18\x03 \x01(\x0b2*.osmosis.protorev.v1beta1.CyclicArbTrackerB!\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"cyclic_arb_tracker""\xc4\x01\n\x10CyclicArbTracker\x12_\n\ncyclic_arb\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12O\n\x1dheight_accounting_starts_from\x18\x02 \x01(\x03B(\xf2\xde\x1f$yaml:"height_accounting_starts_from"B6Z4github.com/osmosis-labs/osmosis/v21/x/protorev/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.protorev.v1beta1.protorev_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z4github.com/osmosis-labs/osmosis/v21/x/protorev/types'
    _TOKENPAIRARBROUTES.fields_by_name['arb_routes']._options = None
    _TOKENPAIRARBROUTES.fields_by_name['arb_routes']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"arb_routes"'
    _TOKENPAIRARBROUTES.fields_by_name['token_in']._options = None
    _TOKENPAIRARBROUTES.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _TOKENPAIRARBROUTES.fields_by_name['token_out']._options = None
    _TOKENPAIRARBROUTES.fields_by_name['token_out']._serialized_options = b'\xf2\xde\x1f\x10yaml:"token_out"'
    _TOKENPAIRARBROUTES._options = None
    _TOKENPAIRARBROUTES._serialized_options = b'\xe8\xa0\x1f\x01'
    _ROUTE.fields_by_name['trades']._options = None
    _ROUTE.fields_by_name['trades']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"trades"'
    _ROUTE.fields_by_name['step_size']._options = None
    _ROUTE.fields_by_name['step_size']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x10yaml:"step_size"'
    _ROUTE._options = None
    _ROUTE._serialized_options = b'\xe8\xa0\x1f\x01'
    _TRADE.fields_by_name['pool']._options = None
    _TRADE.fields_by_name['pool']._serialized_options = b'\xf2\xde\x1f\x0byaml:"pool"'
    _TRADE.fields_by_name['token_in']._options = None
    _TRADE.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _TRADE.fields_by_name['token_out']._options = None
    _TRADE.fields_by_name['token_out']._serialized_options = b'\xf2\xde\x1f\x10yaml:"token_out"'
    _TRADE._options = None
    _TRADE._serialized_options = b'\xe8\xa0\x1f\x01'
    _ROUTESTATISTICS.fields_by_name['profits']._options = None
    _ROUTESTATISTICS.fields_by_name['profits']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"'
    _ROUTESTATISTICS.fields_by_name['number_of_trades']._options = None
    _ROUTESTATISTICS.fields_by_name['number_of_trades']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"number_of_trades"'
    _ROUTESTATISTICS.fields_by_name['route']._options = None
    _ROUTESTATISTICS.fields_by_name['route']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"route"'
    _POOLWEIGHTS.fields_by_name['stable_weight']._options = None
    _POOLWEIGHTS.fields_by_name['stable_weight']._serialized_options = b'\xf2\xde\x1f\x14yaml:"stable_weight"'
    _POOLWEIGHTS.fields_by_name['balancer_weight']._options = None
    _POOLWEIGHTS.fields_by_name['balancer_weight']._serialized_options = b'\xf2\xde\x1f\x16yaml:"balancer_weight"'
    _POOLWEIGHTS.fields_by_name['concentrated_weight']._options = None
    _POOLWEIGHTS.fields_by_name['concentrated_weight']._serialized_options = b'\xf2\xde\x1f\x1ayaml:"concentrated_weight"'
    _POOLWEIGHTS.fields_by_name['cosmwasm_weight']._options = None
    _POOLWEIGHTS.fields_by_name['cosmwasm_weight']._serialized_options = b'\xf2\xde\x1f\x16yaml:"cosmwasm_weight"'
    _INFOBYPOOLTYPE.fields_by_name['stable']._options = None
    _INFOBYPOOLTYPE.fields_by_name['stable']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"stable"'
    _INFOBYPOOLTYPE.fields_by_name['balancer']._options = None
    _INFOBYPOOLTYPE.fields_by_name['balancer']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"balancer"'
    _INFOBYPOOLTYPE.fields_by_name['concentrated']._options = None
    _INFOBYPOOLTYPE.fields_by_name['concentrated']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"concentrated"'
    _INFOBYPOOLTYPE.fields_by_name['cosmwasm']._options = None
    _INFOBYPOOLTYPE.fields_by_name['cosmwasm']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"cosmwasm"'
    _STABLEPOOLINFO.fields_by_name['weight']._options = None
    _STABLEPOOLINFO.fields_by_name['weight']._serialized_options = b'\xf2\xde\x1f\ryaml:"weight"'
    _BALANCERPOOLINFO.fields_by_name['weight']._options = None
    _BALANCERPOOLINFO.fields_by_name['weight']._serialized_options = b'\xf2\xde\x1f\ryaml:"weight"'
    _CONCENTRATEDPOOLINFO.fields_by_name['weight']._options = None
    _CONCENTRATEDPOOLINFO.fields_by_name['weight']._serialized_options = b'\xf2\xde\x1f\ryaml:"weight"'
    _CONCENTRATEDPOOLINFO.fields_by_name['max_ticks_crossed']._options = None
    _CONCENTRATEDPOOLINFO.fields_by_name['max_ticks_crossed']._serialized_options = b'\xf2\xde\x1f\x18yaml:"max_ticks_crossed"'
    _COSMWASMPOOLINFO.fields_by_name['weight_maps']._options = None
    _COSMWASMPOOLINFO.fields_by_name['weight_maps']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"weight_maps"'
    _WEIGHTMAP.fields_by_name['weight']._options = None
    _WEIGHTMAP.fields_by_name['weight']._serialized_options = b'\xf2\xde\x1f\ryaml:"weight"'
    _WEIGHTMAP.fields_by_name['contract_address']._options = None
    _WEIGHTMAP.fields_by_name['contract_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"contract_address"'
    _BASEDENOM.fields_by_name['denom']._options = None
    _BASEDENOM.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _BASEDENOM.fields_by_name['step_size']._options = None
    _BASEDENOM.fields_by_name['step_size']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x10yaml:"step_size"'
    _ALLPROTOCOLREVENUE.fields_by_name['taker_fees_tracker']._options = None
    _ALLPROTOCOLREVENUE.fields_by_name['taker_fees_tracker']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"taker_fees_tracker"'
    _ALLPROTOCOLREVENUE.fields_by_name['tx_fees_tracker']._options = None
    _ALLPROTOCOLREVENUE.fields_by_name['tx_fees_tracker']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"tx_fees_tracker"'
    _ALLPROTOCOLREVENUE.fields_by_name['cyclic_arb_tracker']._options = None
    _ALLPROTOCOLREVENUE.fields_by_name['cyclic_arb_tracker']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"cyclic_arb_tracker"'
    _CYCLICARBTRACKER.fields_by_name['cyclic_arb']._options = None
    _CYCLICARBTRACKER.fields_by_name['cyclic_arb']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _CYCLICARBTRACKER.fields_by_name['height_accounting_starts_from']._options = None
    _CYCLICARBTRACKER.fields_by_name['height_accounting_starts_from']._serialized_options = b'\xf2\xde\x1f$yaml:"height_accounting_starts_from"'
    _globals['_TOKENPAIRARBROUTES']._serialized_start = 232
    _globals['_TOKENPAIRARBROUTES']._serialized_end = 418
    _globals['_ROUTE']._serialized_start = 421
    _globals['_ROUTE']._serialized_end = 576
    _globals['_TRADE']._serialized_start = 578
    _globals['_TRADE']._serialized_end = 702
    _globals['_ROUTESTATISTICS']._serialized_start = 705
    _globals['_ROUTESTATISTICS']._serialized_end = 907
    _globals['_POOLWEIGHTS']._serialized_start = 910
    _globals['_POOLWEIGHTS']._serialized_end = 1139
    _globals['_INFOBYPOOLTYPE']._serialized_start = 1142
    _globals['_INFOBYPOOLTYPE']._serialized_end = 1512
    _globals['_STABLEPOOLINFO']._serialized_start = 1514
    _globals['_STABLEPOOLINFO']._serialized_end = 1565
    _globals['_BALANCERPOOLINFO']._serialized_start = 1567
    _globals['_BALANCERPOOLINFO']._serialized_end = 1620
    _globals['_CONCENTRATEDPOOLINFO']._serialized_start = 1622
    _globals['_CONCENTRATEDPOOLINFO']._serialized_end = 1736
    _globals['_COSMWASMPOOLINFO']._serialized_start = 1738
    _globals['_COSMWASMPOOLINFO']._serialized_end = 1842
    _globals['_WEIGHTMAP']._serialized_start = 1844
    _globals['_WEIGHTMAP']._serialized_end = 1945
    _globals['_BASEDENOM']._serialized_start = 1947
    _globals['_BASEDENOM']._serialized_end = 2061
    _globals['_ALLPROTOCOLREVENUE']._serialized_start = 2064
    _globals['_ALLPROTOCOLREVENUE']._serialized_end = 2397
    _globals['_CYCLICARBTRACKER']._serialized_start = 2400
    _globals['_CYCLICARBTRACKER']._serialized_end = 2596