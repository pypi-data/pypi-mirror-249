import pytest
from src.utagmsengine.solver import Solver, Inconsistency
from src.utagmsengine.dataclasses import Comparison, Criterion, Position, Intensity


@pytest.fixture()
def performance_table_dict_dummy():
    return {
        'A': {'g1': 26.0, 'g2': 40.0, 'g3': 44.0},
        'B': {'g1': 2.0, 'g2': 2.0, 'g3': 68.0},
        'C': {'g1': 18.0, 'g2': 17.0, 'g3': 14.0},
        'D': {'g1': 35.0, 'g2': 62.0, 'g3': 25.0},
        'E': {'g1': -7.0, 'g2': 55.0, 'g3': 12.0},
        'F': {'g1': 25.0, 'g2': 30.0, 'g3': 12.0},
        'G': {'g1': 9.0, 'g2': 62.0, 'g3': 88.0},
        'H': {'g1': 0.0, 'g2': 24.0, 'g3': 73.0},
        'I': {'g1': 6.0, 'g2': 15.0, 'g3': 100.0},
        'J': {'g1': 16.0, 'g2': -9.0, 'g3': 0.0},
        'K': {'g1': 26.0, 'g2': 17.0, 'g3': 17.0},
        'L': {'g1': 62.0, 'g2': 43.0, 'g3': 0.0}
    }


@pytest.fixture()
def comparison_dummy():
    return [
        Comparison(alternative_1='G', alternative_2='F', sign='>'),
        Comparison(alternative_1='F', alternative_2='E', sign='>'),
        Comparison(alternative_1='D', alternative_2='G', sign='='),
    ]


@pytest.fixture()
def criterions_dummy():
    return [Criterion(criterion_id='g1', gain=True, number_of_linear_segments=0), Criterion(criterion_id='g2', gain=True, number_of_linear_segments=0), Criterion(criterion_id='g3', gain=True, number_of_linear_segments=0)]


@pytest.fixture()
def predefined_criterions_dummy():
    return [Criterion(criterion_id='g1', gain=True, number_of_linear_segments=4), Criterion(criterion_id='g2', gain=True, number_of_linear_segments=4), Criterion(criterion_id='g3', gain=True, number_of_linear_segments=4)]


@pytest.fixture()
def positions_dummy():
    return [Position(alternative_id='A', worst_position=12, best_position=2)]


@pytest.fixture()
def intensities_dummy():
    return [Intensity(alternative_id_1='H', alternative_id_2='G', alternative_id_3='B', alternative_id_4='D', criteria=['g1', 'g2'])]


@pytest.fixture()
def resolved_inconsistencies_dummy():
    return [[[], [], [Position(alternative_id='A', worst_position=12, best_position=9, criteria=[])], []], [[Comparison(alternative_1='G', alternative_2='F', criteria=[], sign='>')], [], [], []], [[], [Comparison(alternative_1='D', alternative_2='G', criteria=[], sign='=')], [], []]]


@pytest.fixture()
def hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


@pytest.fixture()
def representative_value_function_dict_dummy():
    return {'J': 0.0738, 'E': 0.1955, 'L': 0.2244, 'C': 0.3235, 'F': 0.382, 'B': 0.4467, 'H': 0.4523, 'K': 0.4741, 'A': 0.6248, 'D': 0.6248, 'G': 0.6248, 'I': 0.7754}


@pytest.fixture()
def criterion_functions_dummy():
    return {'g1': [(-7.0, 0.0), (0.0, 0.0), (2.0, 0.0), (6.0, 0.0), (9.0, 0.0), (10.25, 0.0), (16.0, 0.0737571), (18.0, 0.0994118), (25.0, 0.189203), (26.0, 0.20203), (27.5, 0.221271), (35.0, 0.221271), (44.75, 0.221271), (62.0, 0.221271)], 'g2': [(-9.0, 0.0), (2.0, 0.0), (8.75, 0.0), (15.0, 0.0), (17.0, 0.0), (24.0, 0.0), (26.5, 0.0), (30.0, 0.000661446), (40.0, 0.00255129), (43.0, 0.00311825), (44.25, 0.00335448), (55.0, 0.00335448), (62.0, 0.00335448)], 'g3': [(0.0, 0.0), (12.0, 0.192056), (14.0, 0.224065), (17.0, 0.272079), (25.0, 0.400116), (44.0, 0.42016), (50.0, 0.42649), (68.0, 0.446706), (73.0, 0.452322), (75.0, 0.454568), (88.0, 0.621387), (100.0, 0.775374)]}


@pytest.fixture()
def predefined_hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


@pytest.fixture()
def extreme_ranking_dummy():
    return {'A': ((11, 2), (7, 2)), 'B': ((12, 4), (12, 1)), 'C': ((12, 5), (11, 3)), 'D': ((7, 2), (4, 1)), 'E': ((12, 5), (12, 5)), 'F': ((11, 4), (10, 3)), 'G': ((7, 2), (4, 1)), 'H': ((12, 3), (12, 1)), 'I': ((11, 1), (10, 1)), 'J': ((12, 8), (12, 4)), 'K': ((12, 4), (10, 3)), 'L': ((12, 1), (11, 1))}


def test_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy,
        hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy
    )

    assert hasse_diagram_list == hasse_diagram_dict_dummy


def test_get_representative_value_function_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        predefined_criterions_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy,
        representative_value_function_dict_dummy,
        criterion_functions_dummy,
        resolved_inconsistencies_dummy,
        extreme_ranking_dummy
):
    solver = Solver(show_logs=True)

    try:
        representative_value_function_dict, criterion_functions, position_percentage, pairwise_percentage, number_of_rejected, extreme_ranking, necessary, possible, sampler_error = (
            solver.get_representative_value_function_dict(
                performance_table_dict_dummy,
                comparison_dummy,
                predefined_criterions_dummy,
                positions_dummy,
                intensities_dummy,
                'files/polyrun-1.1.0-jar-with-dependencies.jar',
                '10'
            )
        )

        assert representative_value_function_dict == representative_value_function_dict_dummy
        assert criterion_functions == criterion_functions_dummy
        assert extreme_ranking == extreme_ranking_dummy

    except Inconsistency as e:
        resolved_inconsistencies = e.data

        assert resolved_inconsistencies == resolved_inconsistencies_dummy


def test_predefined_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        predefined_criterions_dummy,
        positions_dummy,
        predefined_hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        predefined_criterions_dummy,
        positions_dummy
    )

    assert hasse_diagram_list == predefined_hasse_diagram_dict_dummy
