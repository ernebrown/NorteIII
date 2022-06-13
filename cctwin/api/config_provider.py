from flask import jsonify

from cctwin.api import bp
from cctwin.assets.block.block import BlockBiddingConfigSchema, BlockSimulationConfigSchema
from cctwin.twin import block_twin


@bp.route('/simulation/config', methods=['GET'])
def simulation_config():
    schema = BlockSimulationConfigSchema()
    json_dict = schema.dump(block_twin)

    response = jsonify(json_dict)
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@bp.route('/bidding/config', methods=['GET'])
def bidding_config():
    schema = BlockBiddingConfigSchema()
    json_dict = schema.dump(block_twin)

    response = jsonify(json_dict)
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
