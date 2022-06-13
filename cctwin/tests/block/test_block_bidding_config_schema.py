from marshmallow import pprint

from cctwin.assets.block.block import BlockBiddingConfigSchema


def test_to_json(block):
    schema = BlockBiddingConfigSchema()
    json_dict = schema.dump(block)

    assert isinstance(json_dict, dict)
    print('\n\n')
    pprint(json_dict, indent=4)
