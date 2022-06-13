import re


def is_valid_site_config(site_config: str) -> bool:
    pattern = re.compile('(?P<ctgs>\d)[xX](?P<stgs>\d)')
    match = re.match(pattern, site_config)
    return match is not None


def is_valid_model_key(model_key: str) -> bool:
    pattern = re.compile('(?P<desc>.+)<(?P<outputs>.+)><(?P<inputs>.+)>')
    match = re.match(pattern, model_key)
    return match is not None


def get_sklearn_predictor(model_info_string, model):
    pattern = re.compile('(?P<desc>.+)<(?P<outputs>.+)><(?P<inputs>.+)>')
    match = re.match(pattern, model_info_string)
    if not match:
        raise ValueError('Given model info string does not match expected format of desc<outputs><inputs>\n'
                         'each output and input should be separated by a pipe "|"')

    outputs = match.group('outputs').split('|')
    inputs = match.group('inputs').split('|')

    return inputs, model, outputs
