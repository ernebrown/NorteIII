import time

import pytest

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.hrsg.hrsg_input import HrsgInput
from cctwin.helper.asset_model_executor import ModelExecutor


def test_hrsg8_constructor(hrsg8):
    assert isinstance(hrsg8.model_executor, ModelExecutor)


# List of tuples ('ctg_mw', 'ctg_exh_temp', 'db_fuel', 'expected_db_fuel', 'tol_db_fuel')
test_data_list = [
    (177.9, 1107.1, 538.0, 538.0, 10),
    (193.5, 1081.0, 541.7, 541.7, 10),
    (151.8, 1142.6, 560.9, 560.9, 10),
    (180.5, 1099.8, 574.2, 574.2, 10),
    (159.0, 1135.2, 582.5, 582.5, 10),
    (180.1, 1109.1, 590.5, 590.5, 10),
    (179.9, 1103.6, 612.0, 612.0, 10),
    (167.2, 1123.7, 612.9, 612.9, 10),
    (178.3, 1105.4, 689.6, 689.6, 45),
    # TODO... Following test case needs to be validated
    # (177.6, 1105.6, 709.4, 709.4, 45)
]


def id_function(data):
    ctg_mw, ctg_exh_temp, db_fuel, expected_db_fuel, tol_db_fuel = data
    return f'ctg_mw:{ctg_mw:0.1f}, ctg_exh_temp:{ctg_exh_temp:0.0f}, ' \
           f'db_fuel:{db_fuel:0.0f}, tolerance_db_fuel: {tol_db_fuel}'


@pytest.fixture(params=test_data_list, ids=id_function)
def hrsg8_test_data(request):
    return request.param


def test_hrsg8_performance_at_given_conditions(hrsg8, hrsg8_test_data):
    ctg_mw, ctg_exh_temp, db_fuel, expected_db_fuel, tol_db_fuel = hrsg8_test_data

    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)

    performance = hrsg8.get_performance(hrsg_input)
    db_fuel = performance.duct_burner_fuel[0]
    hp_press = performance.hp_press[0]
    hp_sh_temp = performance.hp_sh_temp[0]
    assert hp_press <= HrsgConstants.HP_PRESS_LIMIT
    assert hp_sh_temp <= HrsgConstants.HP_SH_TEMP_LIMIT
    assert db_fuel == pytest.approx(expected_db_fuel, abs=tol_db_fuel)


def test_hrsg8_performance_single_case(hrsg8):
    ctg_mw = 151.8
    ctg_exh_temp = 1142.6
    db_fuel = 695

    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)

    performance = hrsg8.get_performance(hrsg_input)
    db_fuel = performance.duct_burner_fuel[0]
    hp_press = performance.hp_press[0]
    hp_sh_temp = performance.hp_sh_temp[0]
    print(f'\n\n'
          f'Actual DB FUEL:{db_fuel:0.0f}\n'
          f'MAX DB FUEL:{HrsgConstants.MAX_FUEL}\n\n')
    assert hp_press <= HrsgConstants.HP_PRESS_LIMIT
    assert hp_sh_temp <= HrsgConstants.HP_SH_TEMP_LIMIT + 1
    assert db_fuel <= HrsgConstants.MAX_FUEL


def test_speed_of_calculations(hrsg8):
    ctg_mw = [209.2339735, 208.9884055, 208.402487, 207.931428, 207.7680566, 206.5798119, 206.3556056, 205.9108798,
              205.1507476, 204.0099726, 203.9119653, 203.1264553, 202.6375891, 202.341321, 201.7144164, 200.8467964,
              200.6352543, 199.3208687, 198.9548423, 198.540244, 197.5271831, 197.0617885, 196.9587513, 196.9256533,
              195.7807355, 195.4406137, 193.9664529, 193.7489926, 193.6978042, 193.6730229, 193.2299715, 192.3836407,
              192.0300125, 192.1408643, 192.0719965, 190.2037871, 190.0141736, 188.0696209, 187.3946451, 187.2847401,
              186.2802772, 185.1842554, 185.2384228, 184.1483196, 183.6188485, 183.316546, 181.8300475, 181.5217336,
              180.9441601, 181.1742306, 181.163309, 181.1284124, 180.0612301, 178.406284, 178.0548568, 177.7677498,
              176.1496342, 175.9460832, 176.2349821, 174.7656933, 173.8902325, 174.3122191, 174.0209496, 173.7289948,
              173.7289948, 171.8201081, 170.4493503, 171.1529173, 169.0732225, 169.3988246, 168.4775727, 167.2993282,
              167.8555737, 167.8537407, 166.3184246, 166.0766277, 166.0651172, 164.8808414, 164.7584402, 163.8412514,
              163.1971842, 163.0736769, 162.5872427, 160.3832183, 158.5134232, 158.5370373, 158.2175736, 158.0175263,
              157.1189463, 157.0414496, 157.0478902, 157.0895136, 156.9981723, 156.1473344, 155.2031632, 154.8810034,
              154.8774552, 152.8379719, 152.4969196, 151.8482006, 150.6169442, 150.3291953, 150.2851765, 149.9722271,
              147.6516821, 147.5099338, 147.3224508, 147.3140301, 147.1023602, 146.5476758]
    ctg_exh_temp = [1057.998989, 1058.083175, 1059.166613, 1059.608727, 1060.524325, 1061.468221, 1062.482266,
                    1062.871417, 1063.556241, 1066.05116, 1066.201793, 1066.930549, 1067.932049, 1068.509844,
                    1069.365664, 1070.46111, 1071.041287, 1072.960279, 1074.006022, 1074.130462, 1074.790131,
                    1076.175118, 1076.203019, 1076.146399, 1078.47599, 1078.217031, 1080.898741, 1081.244093,
                    1081.18828, 1081.351546, 1081.75445, 1084.080737, 1083.548616, 1083.895277, 1083.91049, 1087.864687,
                    1088.820241, 1092.212379, 1092.637322, 1093.082395, 1092.802907, 1092.961694, 1093.249708,
                    1095.667562, 1096.369551, 1096.235725, 1097.009775, 1099.550796, 1100.192819, 1100.957927,
                    1101.539625, 1101.508947, 1107.525777, 1108.522809, 1106.356825, 1107.497881, 1108.751807,
                    1111.510092, 1112.337117, 1112.945818, 1113.556421, 1112.785971, 1112.245231, 1114.524247,
                    1115.548869, 1119.600286, 1119.403164, 1119.422752, 1120.009419, 1122.726092, 1123.463843,
                    1123.794096, 1124.033226, 1124.186711, 1124.12371, 1124.689186, 1123.781991, 1124.445818,
                    1125.459231, 1128.58571, 1128.792813, 1131.859912, 1131.87982, 1132.574482, 1136.27505, 1136.105962,
                    1137.072966, 1138.331504, 1137.875991, 1137.648277, 1137.399067, 1136.773393, 1136.80061,
                    1137.614223, 1138.2807, 1139.419634, 1139.442089, 1142.024609, 1142.712828, 1145.266499,
                    1145.935905, 1146.747602, 1146.966354, 1147.051522, 1150.319102, 1150.653204, 1150.95769, 1151.0219,
                    1152.57895, 1152.726923]
    db_fuel= [HrsgConstants.MAX_FUEL] * len(ctg_mw)

    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)

    start_time = time.time()

    performance = hrsg8.get_performance(hrsg_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time

    print(
        f'\n\nTime taken: {duration_in_seconds:0.2f} secs '
        f'to run {len(ctg_mw)} cases for {hrsg8.name}')

    assert len(performance.hp_sh_temp) == len(ctg_mw)
    assert duration_in_seconds <= 0.5

    print('fuel, hp_sh_temp')
    for fuel, hp_sh_temp in zip(performance.duct_burner_fuel, performance.hp_sh_temp):
        print(f'{fuel}, {hp_sh_temp}')
