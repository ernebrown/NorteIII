from flask import jsonify, request

from cctwin.api import bp
from cctwin.assets.block.ambient_conditions import AmbientConditions
from cctwin.assets.block.block_output import BlockSimulationOutputSchema, BlockBiddingOutputSchema
from cctwin.assets.block.block_request import BlockBiddingRequest, BlockBiddingRequestSchema, BlockSimulationRequest, \
    BlockSimulationRequestSchema
from cctwin.helper.helper import get_db_temp_list
from cctwin.twin import block_twin


@bp.route('/simulation/simulate', methods=['POST'])
def simulate():
    data = request.get_json() or {}

    schema = BlockSimulationRequestSchema()
    block_simulation_request: BlockSimulationRequest = schema.load(data)

    db = block_simulation_request.ambient_conditions.db[0]
    rh = block_simulation_request.ambient_conditions.rh[0]
    baro = block_simulation_request.ambient_conditions.baro[0]

    db_list = get_db_temp_list(db)
    rh_list = [rh for _ in db_list]
    baro_list = [baro for _ in db_list]

    db_list.insert(0, db)
    rh_list.insert(0, rh)
    baro_list.insert(0, baro)

    block_simulation_request.ambient_conditions = AmbientConditions(db_list, rh_list, baro_list)

    block_output = block_twin.get_performance(block_simulation_request)

    schema = BlockSimulationOutputSchema()

    json_dict = schema.dump(block_output)

    response = jsonify(json_dict)
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


@bp.route('/bidding/simulate', methods=['POST'])
def prepare_bids():
    data = request.get_json() or {}

    schema = BlockBiddingRequestSchema()
    block_bidding_request: BlockBiddingRequest = schema.load(data)

    block_bidding_outputs = block_twin.get_data_for_bids(block_twin.create_block_configs(), block_bidding_request)

    schema = BlockBiddingOutputSchema()
    json_dict = schema.dump(block_bidding_outputs, many=True)

    response = jsonify(json_dict)
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response
