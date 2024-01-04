from tempfile import TemporaryFile
from typing import Tuple, List, Dict

from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize, lpSum, GLPK
from collections import defaultdict
import re
import subprocess


class SolverUtils:

    @staticmethod
    def calculate_solved_problem(
            performance_table_list: List[List[float]],
            comparisons: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            alternative_id_1: int = -1,
            alternative_id_2: int = -1,
            alternative_id_extreme: int = -1,
            type_of_rank: int = -1,
            type_of_relation: int = 0,
            show_logs: bool = False,
    ) -> LpProblem:
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems

        :param type_of_relation:
        :param type_of_rank:
        :param alternative_id_extreme:
        :param comprehensive_intensities:
        :param performance_table_list:
        :param comparisons:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param alternative_id_1: used only in calculation for hasse graphs
        :param alternative_id_2: used only in calculation for hasse graphs
        :param show_logs: default None

        :return problem:
        """
        type_of_model: int = LpMaximize
        if alternative_id_extreme != -1:
            type_of_model: int = LpMinimize

        problem: LpProblem = LpProblem("UTA-GMS", type_of_model)

        epsilon: LpVariable = LpVariable("epsilon")
        if alternative_id_extreme != -1:
            problem += epsilon == 0.0001

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list, key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(var.name.split("_")[-1])) for lp_var_list in u_list]

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        # Monotonicity constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i])):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += u_list_of_characteristic_points[i][j - 1] >= u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i]) - 1):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][-1] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][0]
                else:
                    problem += u_list_of_characteristic_points[i][0] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][-1]

        # Comparison constraint
        for comparison in comparisons:
            left_alternative: List[float] = performance_table_list[comparison[0]]
            right_alternative: List[float] = performance_table_list[comparison[1]]

            indices_to_keep: List[int] = comparison[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            if comparison[3] == '>':
                problem += lpSum(left_side) >= lpSum(right_side) + epsilon
            if comparison[3] == '=':
                problem += lpSum(left_side) == lpSum(right_side)
            if comparison[3] == '>=':
                problem += lpSum(left_side) >= lpSum(right_side)

        if alternative_id_1 >= 0 and alternative_id_2 >= 0:
            left_alternative: List[float] = performance_table_list[alternative_id_2]
            right_alternative: List[float] = performance_table_list[alternative_id_1]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            if type_of_relation == 0:
                problem += lpSum(left_side) >= lpSum(right_side) + epsilon
            else:
                problem += lpSum(left_side) >= lpSum(right_side)

        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, List[Dict[int, LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_{i[0]}_higher_than_{j}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])

                    variable_2_name: str = f"v_{i[0]}_{j}_higher_than_{i[0]}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])

                    pom_dict[j] = pom[:]

            if i[0] not in alternatives_binary_variables:
                alternatives_binary_variables[i[0]] = []

            alternatives_binary_variables[i[0]].append(pom_dict)

        big_M: int = 1e20
        x: int = 0
        for worst_best in worst_best_position:
            if len(alternatives_binary_variables[worst_best[0]]) == 1:
                x: int = 0
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:
                    position_constraints: List[LpVariable] = alternatives_variables[worst_best[0]]
                    compared_constraints: List[LpVariable] = alternatives_variables[i]

                    indices_to_keep: List[int] = worst_best[3]
                    if indices_to_keep:
                        position_constraints: List[LpVariable] = [position_constraints[i] for i in indices_to_keep]
                        compared_constraints: List[LpVariable] = [compared_constraints[i] for i in indices_to_keep]

                    problem += lpSum(position_constraints) - lpSum(compared_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][0] >= 0

                    problem += lpSum(compared_constraints) - lpSum(position_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][1] >= epsilon

                    problem += alternatives_binary_variables[worst_best[0]][x][i][0] + alternatives_binary_variables[worst_best[0]][x][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]][x]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][x][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][x][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2]

            # If there are more Positions than one, relevant to one alternative
            if len(alternatives_binary_variables[worst_best[0]]) > 1:
                x += 1

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1

                    if len(u_list_dict[i][j].name.split("_")) == 4:
                        val = -float(u_list_dict[i][j].name.split("_")[-1])
                    else:
                        val = float(u_list_dict[i][j].name.split("_")[-1])
                    while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before],
                                                             u_list_dict[i][
                                                                 float(characteristic_points[i][point_before])],
                                                             characteristic_points[i][point_after], u_list_dict[i][
                                                                 float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]

            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[-1] == '>':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                    right_side_2) + epsilon
            elif intensity[-1] == '>=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(right_side_2)
            else:
                problem += lpSum(left_side_1) - lpSum(left_side_2) == lpSum(right_side_1) - lpSum(right_side_2)

        # extreme ranking
        binary_variables_rank_dict = {}
        binary_variables_rank = []
        if alternative_id_extreme >= 0:
            for i in range(len(performance_table_list)):
                if i != alternative_id_extreme:
                    left_alternative: List[float] = performance_table_list[alternative_id_extreme]
                    right_alternative: List[float] = performance_table_list[i]
                    left_side: List[LpVariable] = []
                    right_side: List[LpVariable] = []
                    for j in range(len(left_alternative)):
                        left_side.append(u_list_dict[j][left_alternative[j]])
                        right_side.append(u_list_dict[j][right_alternative[j]])

                    variable: str = f"vrank_{i}"
                    if variable not in binary_variables_rank_dict:
                        variable_1: LpVariable = LpVariable(variable, cat='Binary')
                        binary_variables_rank_dict[variable] = variable_1
                        binary_variables_rank.append(variable_1)
                    if type_of_rank == 0:
                        problem += lpSum(left_side) - lpSum(right_side) + big_M * variable_1 >= 0
                    elif type_of_rank == 1:
                        problem += lpSum(left_side) - lpSum(right_side) + big_M * variable_1 >= epsilon
                    elif type_of_rank == 2:
                        problem += lpSum(right_side) - lpSum(left_side) + big_M * variable_1 >= epsilon
                    elif type_of_rank == 3:
                        problem += lpSum(right_side) - lpSum(left_side) + big_M * variable_1 >= 0

            problem += lpSum(binary_variables_rank)
        else:
            problem += epsilon

        problem.solve(solver=GLPK(msg=show_logs))

        return problem

    @staticmethod
    def calculate_the_most_representative_function(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            comparisons: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            show_logs: bool = False,
            sampler_path: str = 'files/polyrun-1.1.0-jar-with-dependencies.jar',
            number_of_samples: str = '100',
            sampler_on: bool = True
    ) -> Tuple[LpProblem, Dict[str, List[float]], Dict[str, Dict[str, float]], int, str]:
        """
        Main method used in getting the most representative value function.

        :param comprehensive_intensities:
        :param performance_table_list:
        :param alternatives_id_list:
        :param comparisons:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None
        :param sampler_path:
        :param number_of_samples:
        :param sampler_on:

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        delta: LpVariable = LpVariable("delta")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list, key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(var.name.split("_")[-1])) for lp_var_list in u_list]

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        # Monotonicity constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i])):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += u_list_of_characteristic_points[i][j - 1] >= u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i]) - 1):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][-1] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][0]
                else:
                    problem += u_list_of_characteristic_points[i][0] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][-1]

        # Comparison constraint, but not indifference
        for comparison in comparisons:
            left_alternative: List[float] = performance_table_list[comparison[0]]
            right_alternative: List[float] = performance_table_list[comparison[1]]

            indices_to_keep: List[int] = comparison[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            if comparison[3] == '>':
                problem += lpSum(left_side) >= lpSum(right_side) + epsilon
            if comparison[3] == '>=':
                problem += lpSum(left_side) >= lpSum(right_side)

        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]

            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[-1] == '>':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                    right_side_2) + epsilon
            elif intensity[-1] == '>=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(right_side_2)

        if sampler_on:
            position_percentage, pairwise_percentage, number_of_samples_used, sampler_error = SolverUtils.get_sampler_metrics(
                problem=problem,
                performance_table_list=performance_table_list,
                alternatives_id_list=alternatives_id_list,
                sampler_path=sampler_path,
                number_of_samples=number_of_samples,
                u_list_of_characteristic_points=u_list_of_characteristic_points,
                u_list_dict=u_list_dict,
                characteristic_points=characteristic_points,
                positions=worst_best_position,
            )
        else:
            position_percentage = None
            pairwise_percentage = None
            number_of_samples_used = None
            sampler_error = None

        # Comparison constraint, only indifference
        for comparison in comparisons:
            left_alternative: List[float] = performance_table_list[comparison[0]]
            right_alternative: List[float] = performance_table_list[comparison[1]]

            indices_to_keep: List[int] = comparison[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            if comparison[3] == '=':
                problem += lpSum(left_side) == lpSum(right_side)

        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]

            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[-1] == '=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) == lpSum(right_side_1) - lpSum(right_side_2)

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1

                    if len(u_list_dict[i][j].name.split("_")) == 4:
                        val = -float(u_list_dict[i][j].name.split("_")[-1])
                    else:
                        val = float(u_list_dict[i][j].name.split("_")[-1])
                    while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before], u_list_dict[i][float(characteristic_points[i][point_before])], characteristic_points[i][point_after], u_list_dict[i][float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        necessary_preference: Dict[str, List[str]] = SolverUtils.get_necessary_relations(
            performance_table_list=performance_table_list,
            alternatives_id_list=alternatives_id_list,
            comparisons=comparisons,
            criteria=criteria,
            worst_best_position=worst_best_position,
            number_of_points=number_of_points,
            comprehensive_intensities=comprehensive_intensities
        )

        # Representative value
        for i in range(len(alternatives_id_list) - 1):
            for j in range(i + 1, len(alternatives_id_list)):
                name_i = alternatives_id_list[i]
                name_j = alternatives_id_list[j]
                pom1 = []
                pom2 = []
                for k in range(len(performance_table_list[i])):
                    pom1.append(u_list_dict[k][float(performance_table_list[i][k])])
                    pom2.append(u_list_dict[k][float(performance_table_list[j][k])])
                sum_i = lpSum(pom1[:])
                sum_j = lpSum(pom2[:])

                if (name_i not in necessary_preference and name_j in necessary_preference and name_i in
                    necessary_preference[name_j]) or \
                        (name_i in necessary_preference and name_j in necessary_preference and name_i in
                         necessary_preference[name_j] and name_j not in necessary_preference[name_i]):
                    problem += sum_j >= sum_i + epsilon
                elif (name_j not in necessary_preference and name_i in necessary_preference and name_j in
                      necessary_preference[name_i]) or \
                        (name_i in necessary_preference and name_j in necessary_preference and name_j in
                         necessary_preference[name_i] and name_i not in necessary_preference[name_j]):
                    problem += sum_i >= sum_j + epsilon
                elif (name_i not in necessary_preference and name_j not in necessary_preference) or \
                        (name_i not in necessary_preference and name_j in necessary_preference and name_i not in
                         necessary_preference[name_j]) or \
                        (name_j not in necessary_preference and name_i in necessary_preference and name_j not in
                         necessary_preference[name_i]) or \
                        (name_i in necessary_preference and name_j not in necessary_preference[
                            name_i] and name_j in necessary_preference and name_i not in necessary_preference[name_j]):
                    problem += sum_i <= delta + sum_j
                    problem += sum_j <= delta + sum_i

        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, List[Dict[int, LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_{i[0]}_higher_than_{j}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])

                    variable_2_name: str = f"v_{i[0]}_{j}_higher_than_{i[0]}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])

                    pom_dict[j] = pom[:]

            if i[0] not in alternatives_binary_variables:
                alternatives_binary_variables[i[0]] = []

            alternatives_binary_variables[i[0]].append(pom_dict)

        big_M: int = 1e20
        x: int = 0
        for worst_best in worst_best_position:
            if len(alternatives_binary_variables[worst_best[0]]) == 1:
                x: int = 0
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:
                    position_constraints: List[LpVariable] = alternatives_variables[worst_best[0]]
                    compared_constraints: List[LpVariable] = alternatives_variables[i]

                    indices_to_keep: List[int] = worst_best[3]
                    if indices_to_keep:
                        position_constraints: List[LpVariable] = [position_constraints[i] for i in indices_to_keep]
                        compared_constraints: List[LpVariable] = [compared_constraints[i] for i in indices_to_keep]

                    problem += lpSum(position_constraints) - lpSum(compared_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][0] >= 0

                    problem += lpSum(compared_constraints) - lpSum(position_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][1] >= epsilon

                    problem += alternatives_binary_variables[worst_best[0]][x][i][0] + alternatives_binary_variables[worst_best[0]][x][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]][x]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][x][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][x][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2]

            # If there are more Positions than one, relevant to one alternative
            if len(alternatives_binary_variables[worst_best[0]]) > 1:
                x += 1

        if 'delta' in problem.variablesDict():
            problem += big_M * epsilon - delta
        else:
            problem += big_M * epsilon

        problem.solve(solver=GLPK(msg=show_logs))

        return problem, position_percentage, pairwise_percentage, number_of_samples_used, sampler_error

    @staticmethod
    def get_necessary_relations(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            comparisons: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            show_logs: bool = False
    ) -> Dict[str, List[str]]:
        """
        Method used for getting necessary relations.

        :param comprehensive_intensities:
        :param performance_table_list:
        :param alternatives_id_list:
        :param comparisons:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None

        :return necessary:
        """
        necessary: Dict[str, List[str]] = {}
        for i in range(len(performance_table_list)):
            for j in range(len(performance_table_list)):
                if i == j:
                    continue

                problem: LpProblem = SolverUtils.calculate_solved_problem(
                    performance_table_list=performance_table_list,
                    comparisons=comparisons,
                    criteria=criteria,
                    worst_best_position=worst_best_position,
                    number_of_points=number_of_points,
                    comprehensive_intensities=comprehensive_intensities,
                    alternative_id_1=i,
                    alternative_id_2=j,
                    show_logs=show_logs
                )

                if problem.variables()[0].varValue <= 0:
                    if alternatives_id_list[i] not in necessary:
                        necessary[alternatives_id_list[i]] = []
                    necessary[alternatives_id_list[i]].append(alternatives_id_list[j])

        return necessary

    @staticmethod
    def create_variables_list_and_dict(performance_table: List[list]) -> Tuple[List[list], List[dict]]:
        """
        Method responsible for creating a technical list of variables and a technical dict of variables that are used
        for adding constraints to the problem.

        :param performance_table:

        :return u_list, u_list_dict: ex. Tuple([[u_0_0.0, u_0_2.0], [u_1_2.0, u_1_9.0]], [{26.0: u_0_26.0, 2.0: u_0_2.0}, {40.0: u_1_40.0, 2.0: u_1_2.0}])
        """
        u_list: List[List[LpVariable]] = []
        u_list_dict: List[Dict[float, LpVariable]] = []

        for i in range(len(performance_table[0])):
            row: List[LpVariable] = []
            row_dict: Dict[float, LpVariable] = {}

            for j in range(len(performance_table)):
                variable_name: str = f"u_{i}_{float(performance_table[j][i])}"
                variable: LpVariable = LpVariable(variable_name)

                if performance_table[j][i] not in row_dict:
                    row_dict[float(performance_table[j][i])] = variable

                flag: int = 1
                for var in row:
                    if str(var) == variable_name:
                        flag: int = 0
                if flag:
                    row.append(variable)

            u_list_dict.append(row_dict)

            row = sorted(row, key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(var.name.split("_")[-1]))
            u_list.append(row)

        return u_list, u_list_dict

    @staticmethod
    def calculate_direct_relations(necessary: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Method for getting only direct relations in Hasse Diagram
        :param necessary:
        :return direct_relations:
        """
        direct_relations: Dict[str, List[str]] = {}
        # first create the relation list for each node
        for node1, relations in necessary.items():
            direct_relations[node1] = sorted(relations)
        # then prune the indirect relations
        for node1, related_nodes in list(direct_relations.items()):  # make a copy of items
            related_nodes_copy: List[str] = related_nodes.copy()
            for node2 in related_nodes:
                # Check if node2 is also related to any other node that is related to node1
                for other_node in related_nodes:
                    if other_node != node2 and other_node in direct_relations and node2 in direct_relations[other_node]:
                        # If such a relationship exists, remove the relation between node1 and node2
                        related_nodes_copy.remove(node2)
                        break
            direct_relations[node1] = sorted(related_nodes_copy)  # sort the list

        return direct_relations

    @staticmethod
    def get_alternatives_and_utilities_dict(
            variables_and_values_dict,
            performance_table_list,
            alternatives_id_list,
    ) -> Dict[str, float]:
        """
        Method for getting alternatives_and_utilities_dict

        :param variables_and_values_dict:
        :param performance_table_list:
        :param alternatives_id_list:

        :return sorted_dict:
        """

        utilities: List[float] = []
        for i in range(len(performance_table_list)):
            utility: float = 0.0
            for j in range(len(performance_table_list[i])):
                variable_name: str = f"u_{j}_{performance_table_list[i][j]}"
                if '-' in variable_name:
                    variable_name: str = variable_name.replace('-', '_')
                utility += round(variables_and_values_dict[variable_name], 4)

            utilities.append(round(utility, 4))

        utilities_dict: Dict[str, float] = {}
        # TODO: Sorting possibly unnecessary, but for now it's nicer for human eye :)
        for i in range(len(utilities)):
            utilities_dict[alternatives_id_list[i]] = utilities[i]
        sorted_dict: Dict[str, float] = dict(sorted(utilities_dict.items(), key=lambda item: item[1]))

        return sorted_dict

    @staticmethod
    def calculate_characteristic_points(
            number_of_points,
            performance_table_list,
            u_list_dict,
            u_list
    ) -> List[List[float]]:
        """
        Method for calculating characteristic points

        :param number_of_points:
        :param performance_table_list:
        :param u_list_dict:
        :param u_list:

        :return characteristic_points:
        """
        columns: List[Tuple[float]] = list(zip(*performance_table_list))
        worst_values: List[float] = [min(col) for col in columns]
        best_values: List[float] = [max(col) for col in columns]
        characteristic_points: List[List[float]] = []

        for i in range(len(worst_values)):
            pom = []
            if number_of_points[i] != 0:
                for j in range(number_of_points[i]):
                    x = round(worst_values[i] + (j / (number_of_points[i] - 1)) * (best_values[i] - worst_values[i]), 4)
                    if x not in u_list_dict[i]:
                        new: str = f"u_{i}_{x}"
                        variable: LpVariable = LpVariable(new)
                        new: Dict[float, LpVariable] = {x: variable}
                        u_list_dict[i].update(new)
                        u_list[i].append(variable)
                    pom.append(x)
                characteristic_points.append(pom[:])
            else:
                for j in range(len(performance_table_list)):
                    if float(performance_table_list[j][i]) not in pom:
                        pom.append(float(performance_table_list[j][i]))
                pom.sort()
                characteristic_points.append(pom[:])
        return characteristic_points

    @staticmethod
    def linear_interpolation(x, x1, y1, x2, y2) -> float:
        """Perform linear interpolation to estimate a value at a specific point on a straight line"""
        result = y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return result

    @staticmethod
    def get_criterion_functions(
            variables_and_values_dict,
            criteria
    ) -> Dict[str, List[Tuple[float, float]]]:
        """
        Method responsible for getting criterion functions

        :param variables_and_values_dict:
        :param criteria:
        :return:
        """
        criterion_functions: Dict[str, List[Tuple[float, float]]] = defaultdict(list)

        criterion_ids: List[str] = []
        for crit in criteria:
            criterion_ids.append(crit.criterion_id)

        for key, value in variables_and_values_dict.items():
            if key.startswith('u'):
                first_part, x_value = key.rsplit('_', 1)
                if first_part.endswith('_'):
                    _, i, __ = first_part.rsplit('_', 2)
                    x_value = -float(key.rsplit('_', 1)[1])
                else:
                    _, i = first_part.rsplit('_', 1)

                criterion_functions[criterion_ids[int(i)]].append((float(x_value), value))

        for key, values in criterion_functions.items():
            criterion_functions[key] = sorted(values, key=lambda x: x[0])

        return dict(criterion_functions)

    @staticmethod
    def get_sampler_metrics(
            problem,
            performance_table_list,
            alternatives_id_list,
            sampler_path,
            number_of_samples,
            u_list_of_characteristic_points,
            u_list_dict,
            characteristic_points,
            positions
    ) -> Tuple[Dict[str, List[float]], Dict[str, Dict[str, float]], int, str]:
        refined_number_of_samples: str = SolverUtils.calculate_rejected_ratio(
            problem=problem,
            performance_table_list=performance_table_list,
            alternatives_id_list=alternatives_id_list,
            sampler_path=sampler_path,
            number_of_samples=number_of_samples,
            u_list_of_characteristic_points=u_list_of_characteristic_points,
            u_list_dict=u_list_dict,
            characteristic_points=characteristic_points,
            positions=positions
        )

        if refined_number_of_samples == 'Rejection ratio to high':
            return None, None, None, refined_number_of_samples

        precision = 5
        worst_variants = []
        characteristic_points_in_one_list = {}
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(len(u_list_of_characteristic_points[i])):
                if j == 0:
                    worst_variants.append(u_list_of_characteristic_points[i][j].name)
                characteristic_points_in_one_list[u_list_of_characteristic_points[i][j].name] = 1

        # Write input file for Sampler
        with TemporaryFile("w+") as input_file, TemporaryFile("w+") as output_file, TemporaryFile("w+") as error_file:
            positions_of_the_worst = []
            # Write header, useful only for testing
            variable_names = [var.name for var in problem.variables()]

            for constraint in problem.constraints.values():
                pom = []
                constraint_values = []
                for var in problem.variables():
                    if var in constraint:

                        if var.name in characteristic_points_in_one_list or var.name == 'epsilon':
                            constraint_values.append(str(round(constraint[var], precision)))

                        else:
                            point_before = 0
                            point_after = 1
                            if len(var.name.split("_")) == 4:
                                val = -float(var.name.split("_")[-1])
                            else:
                                val = float(var.name.split("_")[-1])

                            while characteristic_points[int(var.name.split("_")[1])][point_before] > val or val > \
                                    characteristic_points[int(var.name.split("_")[1])][point_after]:
                                point_before += 1
                                point_after += 1

                            value = SolverUtils.linear_interpolation(val, characteristic_points[int(var.name.split("_")[1])][point_before], u_list_dict[int(var.name.split("_")[1])][float(characteristic_points[int(var.name.split("_")[1])][point_before])], characteristic_points[int(var.name.split("_")[1])][point_after], u_list_dict[int(var.name.split("_")[1])][float(characteristic_points[int(var.name.split("_")[1])][point_after])])
                            for variable in value:
                                i = 0
                                for var1 in problem.variables():

                                    if var1.name != variable.name:
                                        if var1.name in characteristic_points_in_one_list or var1.name == 'epsilon':
                                            i += 1
                                            if var.name in worst_variants and i not in positions_of_the_worst:
                                                positions_of_the_worst.append(iteration)
                                    else:
                                        break
                                if round(constraint[var], 4) >= 0:
                                    pom.append([i, str(round(value[variable], precision))])
                                else:
                                    pom.append([i, str(round(-value[variable], precision))])

                    else:
                        if var.name in characteristic_points_in_one_list or var.name == 'epsilon':
                            constraint_values.append("0")

                iteration = 0
                for var1 in problem.variables():
                    if var1.name in characteristic_points_in_one_list or var1.name == 'epsilon':
                        if var1.name in worst_variants and iteration not in positions_of_the_worst:
                            positions_of_the_worst.append(iteration)
                        iteration += 1

                constraint_values.append(re.search(r'([<>=]=?)', str(constraint)).group(1))
                if str(constraint.constant) == '0.0':
                    constraint_values.append(str(0))
                else:
                    constraint_values.append(str(-constraint.constant))

                for k in range(len(pom)):
                    if pom[k][0] in positions_of_the_worst:
                        continue
                    else:
                        if constraint_values[pom[k][0]] != '0':
                            constraint_values[pom[k][0]] = str(round(float(pom[k][1]) + float(constraint_values[pom[k][0]]), precision))
                        else:
                            constraint_values[pom[k][0]] = str(round(float(pom[k][1]), precision))

                input_file.write(" ".join(constraint_values) + "\n")

            epsilon_constraint = ["1"]
            if 'epsilon' in variable_names:
                epsilon_constraint.extend(["0"] * (len(constraint_values) - 3))
                epsilon_constraint.append(">=")
                epsilon_constraint.append("0.0000001")

                input_file.write(" ".join(epsilon_constraint) + "\n")

            input_file.seek(0)
            error_file.seek(0)
            # Write Sampler output file
            number_of_rejected = 0
            subprocess.call(
                ['java', '-jar', sampler_path, '-n', refined_number_of_samples],
                stdin=input_file,
                stdout=output_file,
                stderr=error_file
            )
            error_file.seek(0)
            error: str = error_file.read()

            points_in_constrtaints_file = []
            for i in range(len(u_list_of_characteristic_points)):
                for j in range(len(u_list_of_characteristic_points[i])):
                    points_in_constrtaints_file.append(u_list_of_characteristic_points[i][j].name)
            points_in_constrtaints_file.sort()

            output: Dict[str, List[float]] = {}
            for alternative in alternatives_id_list:
                output[alternative] = [0] * len(alternatives_id_list)

            output2: Dict[str, Dict[str, float]] = {}
            for alternative in alternatives_id_list:
                output2[alternative] = {}
            for alternative1 in alternatives_id_list:
                for alternative2 in alternatives_id_list:
                    if alternative1 != alternative2:
                        output2[alternative1][alternative2] = 0

            output_file.seek(0)
            for line in output_file:
                variables_and_values_dict: Dict[str, float] = {}

                if 'epsilon' in variable_names:
                    var_names = variable_names[1:]
                    values = line.strip().split('\t')[1:]
                else:
                    var_names = variable_names
                    values = line.strip().split('\t')

                number_of_value = 0
                for var_name in var_names:
                    if var_name in points_in_constrtaints_file:
                        variables_and_values_dict[var_name] = float(values[number_of_value])
                        number_of_value += 1
                    else:
                        variables_and_values_dict[var_name] = float(10000)

                for i in range(len(performance_table_list)):
                    for j in range(len(performance_table_list[i])):
                        variable_name: str = f"u_{j}_{performance_table_list[i][j]}"
                        if '-' in variable_name:
                            variable_name: str = variable_name.replace('-', '_')
                        if variable_name not in variables_and_values_dict:
                            variables_and_values_dict[variable_name] = float(10000)

                for var_name in variables_and_values_dict:
                    if variables_and_values_dict[var_name] == 10000.0:
                        point_before = 0
                        point_after = 1

                        if len(var_name.split("_")) == 4:
                            val = -float(var_name.split("_")[-1])
                        else:
                            val = float(var_name.split("_")[-1])

                        while characteristic_points[int(var_name.split("_")[1])][point_before] > val or val > \
                                characteristic_points[int(var_name.split("_")[1])][point_after]:
                            point_before += 1
                            point_after += 1

                        value = SolverUtils.linear_interpolation(val, characteristic_points[int(var_name.split("_")[1])][point_before], variables_and_values_dict[str(u_list_dict[int(var_name.split("_")[1])][float(characteristic_points[int(var_name.split("_")[1])][point_before])])], characteristic_points[int(var_name.split("_")[1])][point_after], variables_and_values_dict[str(u_list_dict[int(var_name.split("_")[1])][float(characteristic_points[int(var_name.split("_")[1])][point_after])])])

                        variables_and_values_dict[var_name] = float(value)

                alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
                    variables_and_values_dict=variables_and_values_dict,
                    performance_table_list=performance_table_list,
                    alternatives_id_list=alternatives_id_list,
                )

                to_continue: bool = False
                for position in positions:
                    alternative = alternatives_id_list[position[0]]
                    ranking = list(alternatives_and_utilities_dict.keys())
                    position_in_ranking = len(performance_table_list) - ranking.index(alternative)

                    if position_in_ranking > position[1] or position_in_ranking < position[2]:
                        number_of_rejected += 1
                        to_continue: bool = True
                        break

                if to_continue:
                    continue

                letter_value_pairs = [(letter, value) for letter, value in alternatives_and_utilities_dict.items()]

                letter_value_pairs.sort(key=lambda x: x[1], reverse=True)

                # Calculate the pairwise percentage
                for i in range(len(letter_value_pairs)):
                    for j in range(len(letter_value_pairs)):
                        if i != j:
                            letter1, value1 = letter_value_pairs[i]
                            letter2, value2 = letter_value_pairs[j]

                            if value1 > value2:
                                output2[letter1][letter2] += 1

                # Calculate the percentage on each position
                single_ranking = {}
                place = 1
                for i in range(len(letter_value_pairs)):
                    letter, value = letter_value_pairs[i]

                    # Check if the current value is the same as the previous value
                    if i > 0 and value == letter_value_pairs[i - 1][1]:
                        single_ranking[letter] = single_ranking[letter_value_pairs[i - 1][0]]
                    else:
                        single_ranking[letter] = place

                    place += 1

                for key, value in single_ranking.items():
                    output[key][value - 1] = output[key][value - 1] + 1

            for alternative1, alternative_dict in output2.items():
                for alternative2, value in alternative_dict.items():
                    try:
                        output2[alternative1][alternative2] = output2[alternative1][alternative2] * 100 / sum(output[alternative1])
                    except:
                        output2[alternative1][alternative2] = -1

            for key, value in output.items():
                try:
                    output[key] = [round(val / sum(output[key]) * 100, 10) for val in value]
                except:
                    output[key] = []

            number_of_samples_used: int = int(refined_number_of_samples) - number_of_rejected

            return output, output2, number_of_samples_used, error

    @staticmethod
    def resolve_incosistency(
            performance_table_list: List[List[float]],
            comparisons: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            subsets_to_remove: List[List[List[List[int]]]],
            show_logs: bool = False,
    ):
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems

        :param subsets_to_remove:
        :param performance_table_list:
        :param comparisons:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param comprehensive_intensities:
        :param show_logs: default None

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMinimize)

        epsilon: LpVariable = LpVariable("epsilon")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list,
                         key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(
                             var.name.split("_")[-1])) for lp_var_list in u_list]

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        problem += epsilon == 0.0001

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []

        for i in range(len(u_list)):

            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        # Monotonicity constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i])):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += u_list_of_characteristic_points[i][j - 1] >= u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i]) - 1):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][-1] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][0]
                else:
                    problem += u_list_of_characteristic_points[i][0] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][-1]

        binary_variables_inconsistency_dict = {}
        binary_variables_inconsistency_list_worst_best = []
        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, List[Dict[int, LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_{i[0]}_higher_than_{j}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])

                    variable_2_name: str = f"v_{i[0]}_{j}_higher_than_{i[0]}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])

                    pom_dict[j] = pom[:]

            if i[0] not in alternatives_binary_variables:
                alternatives_binary_variables[i[0]] = []

            alternatives_binary_variables[i[0]].append(pom_dict)

        big_M: float = 1e20
        x: int = 0
        for worst_best in worst_best_position:
            if len(alternatives_binary_variables[worst_best[0]]) == 1:
                x: int = 0
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:

                    position_constraints: List[LpVariable] = alternatives_variables[worst_best[0]]
                    compared_constraints: List[LpVariable] = alternatives_variables[i]

                    indices_to_keep: List[int] = worst_best[3]
                    if indices_to_keep:
                        position_constraints: List[LpVariable] = [position_constraints[i] for i in indices_to_keep]
                        compared_constraints: List[LpVariable] = [compared_constraints[i] for i in indices_to_keep]

                    variable: str = f"vwb_{worst_best[0]}_{worst_best[1]}_{worst_best[2]}_criteria_{'_'.join(map(str, worst_best[3]))}"
                    if variable not in binary_variables_inconsistency_dict:
                        variable_1: LpVariable = LpVariable(variable, cat='Binary')
                        binary_variables_inconsistency_dict[variable] = variable_1
                        binary_variables_inconsistency_list_worst_best.append(variable_1)

                    problem += lpSum(position_constraints) - lpSum(compared_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][0] >= 0

                    problem += lpSum(compared_constraints) - lpSum(position_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][1] >= epsilon

                    problem += alternatives_binary_variables[worst_best[0]][x][i][0] + alternatives_binary_variables[worst_best[0]][x][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]][x]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][x][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][x][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1 + big_M * variable_1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2] + big_M * variable_1

            # If there are more Positions than one, relevant to one alternative
            if len(alternatives_binary_variables[worst_best[0]]) > 1:
                x += 1

        binary_variables_inconsistency_list_comparisons = []
        # Comparison constraint
        for comparison in comparisons:
            left_alternative: List[float] = performance_table_list[comparison[0]]
            right_alternative: List[float] = performance_table_list[comparison[1]]

            indices_to_keep: List[int] = comparison[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            if comparison[3] == '>':
                variable: str = f"vp_{comparison[0]}_{comparison[1]}_criteria_{'_'.join(map(str, comparison[2]))}"
                if variable not in binary_variables_inconsistency_dict:
                    variable_1: LpVariable = LpVariable(variable, cat='Binary')
                    binary_variables_inconsistency_dict[variable] = variable_1
                    binary_variables_inconsistency_list_comparisons.append(variable_1)

                if comparison[0] == comparison[1]:
                    problem += lpSum(left_side) >= lpSum(right_side) + epsilon - big_M * variable_1
                    problem += variable_1 == 1
                else:
                    problem += lpSum(left_side) >= lpSum(right_side) + epsilon - big_M * variable_1

            if comparison[3] == '=':
                variable: str = f"vi_{comparison[0]}_{comparison[1]}_criteria_{'_'.join(map(str, comparison[2]))}"
                if variable not in binary_variables_inconsistency_dict:
                    variable_1: LpVariable = LpVariable(variable, cat='Binary')
                    binary_variables_inconsistency_dict[variable] = variable_1
                    binary_variables_inconsistency_list_comparisons.append(variable_1)

                problem += lpSum(left_side) + big_M * variable_1 >= lpSum(right_side)
                problem += lpSum(right_side) + big_M * variable_1 >= lpSum(left_side)

            if comparison[3] == '>=':
                variable: str = f"vx_{comparison[0]}_{comparison[1]}_criteria_{'_'.join(map(str, comparison[2]))}"
                if variable not in binary_variables_inconsistency_dict:
                    variable_1: LpVariable = LpVariable(variable, cat='Binary')
                    binary_variables_inconsistency_dict[variable] = variable_1
                    binary_variables_inconsistency_list_comparisons.append(variable_1)

                if comparison[0] == comparison[1]:
                    problem += lpSum(left_side) >= lpSum(right_side) - big_M * variable_1
                    problem += variable_1 == 1
                else:
                    problem += lpSum(left_side) >= lpSum(right_side) - big_M * variable_1

        binary_variables_inconsistency_list_comprehensive_intensities = []
        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]

            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[8] == '=':
                relation = 'e'
            elif intensity[8] == '>':
                relation = 'g'
            elif intensity[8] == '>=':
                relation = 'ge'

            variable: str = f"vci_{intensity[0]}_{intensity[2]}_{intensity[4]}_{intensity[6]}_{relation}_c_{'_'.join(map(str, intensity[1]))}_c_{'_'.join(map(str, intensity[3]))}_c_{'_'.join(map(str, intensity[5]))}_c_{'_'.join(map(str, intensity[7]))}"
            if variable not in binary_variables_inconsistency_dict:
                variable_1: LpVariable = LpVariable(variable, cat='Binary')
                binary_variables_inconsistency_dict[variable] = variable_1
                binary_variables_inconsistency_list_comprehensive_intensities.append(variable_1)

            if intensity[-1] == '>':
                if (intensity[0] == intensity[2] and intensity[1] == intensity[3] and intensity[4] == intensity[6] and
                    intensity[5] == intensity[7]) or (
                        intensity[0] == intensity[4] and intensity[1] == intensity[5] and intensity[2] == intensity[
                    6] and intensity[3] == intensity[7]):
                    problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                        right_side_2) + epsilon - big_M * variable_1
                    problem += variable_1 == 1
                else:
                    problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                        right_side_2) + epsilon - big_M * variable_1
            elif intensity[-1] == '>=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) + big_M * variable_1 >= lpSum(right_side_1) - lpSum(
                    right_side_2)
            else:
                problem += lpSum(left_side_1) - lpSum(left_side_2) + big_M * variable_1 >= lpSum(right_side_1) - lpSum(
                    right_side_2)
                problem += lpSum(left_side_1) - lpSum(left_side_2) <= lpSum(right_side_1) - lpSum(
                    right_side_2) + big_M * variable_1

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1

                    if len(u_list_dict[i][j].name.split("_")) == 4:
                        val = -float(u_list_dict[i][j].name.split("_")[-1])
                    else:
                        val = float(u_list_dict[i][j].name.split("_")[-1])
                    while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before],
                                                             u_list_dict[i][
                                                                 float(characteristic_points[i][point_before])],
                                                             characteristic_points[i][point_after], u_list_dict[i][
                                                                 float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        if subsets_to_remove != []:
            for i in range(len(subsets_to_remove)):
                pom = []
                for j in range(len(subsets_to_remove[i])):
                    for k in range(len(subsets_to_remove[i][j])):
                        if j == 0:
                            if subsets_to_remove[i][j][k][-1] == '>':
                                variable: str = f"vp_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][2]))}"
                                pom.append(binary_variables_inconsistency_dict[variable])
                            if subsets_to_remove[i][j][k][-1] == '=':
                                variable: str = f"vi_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][2]))}"
                                pom.append(binary_variables_inconsistency_dict[variable])
                            if subsets_to_remove[i][j][k][-1] == '>=':
                                variable: str = f"vx_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][2]))}"
                                pom.append(binary_variables_inconsistency_dict[variable])
                        elif j == 1:
                            variable: str = f"vwb_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_{subsets_to_remove[i][j][k][2]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][3]))}"
                            pom.append(binary_variables_inconsistency_dict[variable])
                        elif j == 2:

                            if subsets_to_remove[i][j][k][8] == '=':
                                relation = 'e'
                            elif subsets_to_remove[i][j][k][8] == '>':
                                relation = 'g'
                            elif subsets_to_remove[i][j][k][8] == '>=':
                                relation = 'ge'

                            variable: str = f"vci_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][2]}_{subsets_to_remove[i][j][k][4]}_{subsets_to_remove[i][j][k][6]}_{relation}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][1]))}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][3]))}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][5]))}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][7]))}"
                            pom.append(binary_variables_inconsistency_dict[variable])

                problem += lpSum(pom[:]) <= len(subsets_to_remove[i][0]) + len(subsets_to_remove[i][1]) + len(
                    subsets_to_remove[i][2]) - 1

        v = lpSum(binary_variables_inconsistency_list_comparisons) + lpSum(
            binary_variables_inconsistency_list_worst_best) + lpSum(
            binary_variables_inconsistency_list_comprehensive_intensities)
        problem += v

        problem.solve(solver=GLPK(msg=show_logs))

        result = []
        resultc = []
        resultwb = []
        resultci = []
        for i in problem.variables():
            pom = []
            name = i.name
            numbers_in_string = name.split("_")
            if i.name[0] == "v" and i.name[1] == "i" and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 3:
                        continue
                    elif j > 2:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                pom.append('=')
                resultc.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "p" and i.name[2] != 'i' and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 3:
                        continue
                    elif j > 2:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                pom.append('>')
                resultc.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "x" and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 3:
                        continue
                    elif j > 2:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                pom.append('>=')
                resultc.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "w" and i.name[2] == "b" and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 4:
                        continue
                    elif j > 4:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                resultwb.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "c" and i.name[2] == "i" and i.varValue == 1:
                criterion = []
                for x in range(1, 5):
                    pom.append(int(numbers_in_string[x]))
                if numbers_in_string[5] == 'e':
                    relation = '='
                elif numbers_in_string[5] == 'g':
                    relation = '>'
                elif numbers_in_string[5] == 'ge':
                    relation = '>='
                pom.append(relation)
                x = 7
                pom_criteria = []
                for y in range(4):
                    while numbers_in_string[x] != "c" and numbers_in_string[x] != "":
                        pom_criteria.append(int(numbers_in_string[x]))
                        x = x + 1

                        if x >= len(numbers_in_string):
                            break
                    criterion.append(pom_criteria[:])
                    x = x + 1

                    pom_criteria = []

                pom_final = []
                for x in range(5):
                    if x == 4:
                        pom_final.append(pom[x])
                    else:
                        pom_final.append(pom[x])
                        pom_final.append(criterion[x])
                resultci.append(pom_final[:])

        result.append(resultc)
        result.append(resultwb)
        result.append(resultci)
        subsets_to_remove.append(result)

        if subsets_to_remove[-1][0] == [] and subsets_to_remove[-1][1] == [] and subsets_to_remove[-1][2] == []:
            return subsets_to_remove
        else:
            return SolverUtils.resolve_incosistency(
                performance_table_list,
                comparisons,
                criteria,
                worst_best_position,
                number_of_points,
                comprehensive_intensities,
                subsets_to_remove
            )

    @staticmethod
    def calculate_extreme_ranking_analysis(
            performance_table_list: List[List[float]],
            comparisons: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            show_logs: bool = False,
    ):

        results = []

        for j in range(len(performance_table_list)):
            problem_max_position_optimistic = SolverUtils.calculate_solved_problem(performance_table_list, comparisons, criteria, worst_best_position, number_of_points, comprehensive_intensities, alternative_id_extreme=j, type_of_rank=0)
            problem_max_position_pessimistic = SolverUtils.calculate_solved_problem(performance_table_list, comparisons, criteria, worst_best_position, number_of_points, comprehensive_intensities, alternative_id_extreme=j, type_of_rank=1)
            problem_min_position_optimistic = SolverUtils.calculate_solved_problem(performance_table_list, comparisons, criteria, worst_best_position, number_of_points, comprehensive_intensities, alternative_id_extreme=j, type_of_rank=2)
            problem_min_position_pessimistic = SolverUtils.calculate_solved_problem(performance_table_list, comparisons, criteria, worst_best_position, number_of_points, comprehensive_intensities, alternative_id_extreme=j, type_of_rank=3)

            count_from_max_optimistic = 0
            for i in problem_max_position_optimistic.variables():
                name = i.name
                name = name.split("_")
                if name[0] == 'vrank' and i.varValue == 1:
                    count_from_max_optimistic = count_from_max_optimistic + 1

            count_from_max_pessimistic = 0
            for i in problem_max_position_pessimistic.variables():
                name = i.name
                name = name.split("_")
                if name[0] == 'vrank' and i.varValue == 1:
                    count_from_max_pessimistic = count_from_max_pessimistic + 1

            count_from_min_optimistic = 0
            for i in problem_min_position_optimistic.variables():
                name = i.name
                name = name.split("_")
                if name[0] == 'vrank' and i.varValue == 1:
                    count_from_min_optimistic = count_from_min_optimistic + 1

            count_from_min_pessimistic = 0
            for i in problem_min_position_pessimistic.variables():
                name = i.name
                name = name.split("_")
                if name[0] == 'vrank' and i.varValue == 1:
                    count_from_min_pessimistic = count_from_min_pessimistic + 1

            pom = [j, len(performance_table_list) - count_from_min_pessimistic, len(performance_table_list) - count_from_min_optimistic, count_from_max_pessimistic + 1, count_from_max_optimistic + 1]

            results.append(pom)

        return results

    @staticmethod
    def calculate_necessary_and_possible_relation_matrix(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            comparisons: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            show_logs: bool = False
    ):
        """
        Method used for getting relation_matrix.

        :param comprehensive_intensities:
        :param performance_table_list:
        :param alternatives_id_list:
        :param comparisons:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None

        :return necessary, possible:
        """
        necessary: Dict[str, List[str]] = {}
        possible: Dict[str, List[str]] = {}
        for i in range(len(performance_table_list)):
            for j in range(len(performance_table_list)):
                if i == j:
                    continue

                problem_necessary: LpProblem = SolverUtils.calculate_solved_problem(
                    performance_table_list=performance_table_list,
                    comparisons=comparisons,
                    criteria=criteria,
                    worst_best_position=worst_best_position,
                    number_of_points=number_of_points,
                    comprehensive_intensities=comprehensive_intensities,
                    alternative_id_1=i,
                    alternative_id_2=j,
                    type_of_relation=0,
                    show_logs=show_logs
                )

                problem_possible: LpProblem = SolverUtils.calculate_solved_problem(
                    performance_table_list=performance_table_list,
                    comparisons=comparisons,
                    criteria=criteria,
                    worst_best_position=worst_best_position,
                    number_of_points=number_of_points,
                    comprehensive_intensities=comprehensive_intensities,
                    alternative_id_1=j,
                    alternative_id_2=i,
                    type_of_relation=1,
                    show_logs=show_logs
                )

                if problem_necessary.variables()[0].varValue <= 0:
                    if alternatives_id_list[i] not in necessary:
                        necessary[alternatives_id_list[i]] = []
                    necessary[alternatives_id_list[i]].append(alternatives_id_list[j])

                if problem_possible.variables()[0].varValue > 0:
                    if alternatives_id_list[i] not in possible:
                        possible[alternatives_id_list[i]] = []
                    possible[alternatives_id_list[i]].append(alternatives_id_list[j])

        return necessary, possible

    @staticmethod
    def calculate_rejected_ratio(
            problem,
            performance_table_list,
            alternatives_id_list,
            sampler_path,
            number_of_samples,
            u_list_of_characteristic_points,
            u_list_dict,
            characteristic_points,
            positions
    ) -> str:
        precision: int = 5
        worst_variants = []
        characteristic_points_in_one_list = {}
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(len(u_list_of_characteristic_points[i])):
                if j == 0:
                    worst_variants.append(u_list_of_characteristic_points[i][j].name)
                characteristic_points_in_one_list[u_list_of_characteristic_points[i][j].name] = 1

        # Write input file for Sampler
        with TemporaryFile("w+") as input_file2, TemporaryFile("w+") as output_file2:
            positions_of_the_worst = []
            # Write header, useful only for testing
            variable_names = [var.name for var in problem.variables()]

            for constraint in problem.constraints.values():
                pom = []
                constraint_values = []
                for var in problem.variables():
                    if var in constraint:

                        if var.name in characteristic_points_in_one_list or var.name == 'epsilon':
                            constraint_values.append(str(round(constraint[var], precision)))

                        else:
                            point_before = 0
                            point_after = 1
                            if len(var.name.split("_")) == 4:
                                val = -float(var.name.split("_")[-1])
                            else:
                                val = float(var.name.split("_")[-1])

                            while characteristic_points[int(var.name.split("_")[1])][point_before] > val or val > characteristic_points[int(var.name.split("_")[1])][point_after]:
                                point_before += 1
                                point_after += 1

                            value = SolverUtils.linear_interpolation(val,
                                                                     characteristic_points[int(var.name.split("_")[1])][
                                                                         point_before],
                                                                     u_list_dict[int(var.name.split("_")[1])][float(
                                                                         characteristic_points[
                                                                             int(var.name.split("_")[1])][
                                                                             point_before])],
                                                                     characteristic_points[int(var.name.split("_")[1])][
                                                                         point_after],
                                                                     u_list_dict[int(var.name.split("_")[1])][float(
                                                                         characteristic_points[
                                                                             int(var.name.split("_")[1])][
                                                                             point_after])])
                            for variable in value:
                                i = 0
                                for var1 in problem.variables():

                                    if var1.name != variable.name:
                                        if var1.name in characteristic_points_in_one_list or var1.name == 'epsilon':
                                            i += 1
                                            if var.name in worst_variants and i not in positions_of_the_worst:
                                                positions_of_the_worst.append(iteration)
                                    else:
                                        break
                                if round(constraint[var], 4) >= 0:
                                    pom.append([i, str(round(value[variable], precision))])
                                else:
                                    pom.append([i, str(round(-value[variable], precision))])

                    else:
                        if var.name in characteristic_points_in_one_list or var.name == 'epsilon':
                            constraint_values.append("0")

                iteration = 0
                for var1 in problem.variables():
                    if var1.name in characteristic_points_in_one_list or var1.name == 'epsilon':
                        if var1.name in worst_variants and iteration not in positions_of_the_worst:
                            positions_of_the_worst.append(iteration)
                        iteration += 1

                constraint_values.append(re.search(r'([<>=]=?)', str(constraint)).group(1))
                if str(constraint.constant) == '0.0':
                    constraint_values.append(str(0))
                else:
                    constraint_values.append(str(-constraint.constant))

                for k in range(len(pom)):
                    if pom[k][0] in positions_of_the_worst:
                        continue
                    else:
                        if constraint_values[pom[k][0]] != '0':
                            constraint_values[pom[k][0]] = str(
                                round(float(pom[k][1]) + float(constraint_values[pom[k][0]]), precision))
                        else:
                            constraint_values[pom[k][0]] = str(round(float(pom[k][1]), precision))

                input_file2.write(" ".join(constraint_values) + "\n")

            epsilon_constraint = ["1"]
            if 'epsilon' in variable_names:
                epsilon_constraint.extend(["0"] * (len(constraint_values) - 3))
                epsilon_constraint.append(">=")
                epsilon_constraint.append("0.0000001")

                input_file2.write(" ".join(epsilon_constraint) + "\n")

            input_file2.seek(0)
            # Write Sampler output file
            number_of_rejected = 0

            subprocess.call(
                ['java', '-jar', sampler_path, '-n', '1000'],
                stdin=input_file2,
                stdout=output_file2
            )

            points_in_constrtaints_file = []
            for i in range(len(u_list_of_characteristic_points)):
                for j in range(len(u_list_of_characteristic_points[i])):
                    points_in_constrtaints_file.append(u_list_of_characteristic_points[i][j].name)
            points_in_constrtaints_file.sort()

            output: Dict[str, List[float]] = {}
            for alternative in alternatives_id_list:
                output[alternative] = [0] * len(alternatives_id_list)

            output2: Dict[str, Dict[str, float]] = {}
            for alternative in alternatives_id_list:
                output2[alternative] = {}
            for alternative1 in alternatives_id_list:
                for alternative2 in alternatives_id_list:
                    if alternative1 != alternative2:
                        output2[alternative1][alternative2] = 0

            output_file2.seek(0)
            for line in output_file2:
                variables_and_values_dict: Dict[str, float] = {}

                if 'epsilon' in variable_names:
                    var_names = variable_names[1:]
                    values = line.strip().split('\t')[1:]
                else:
                    var_names = variable_names
                    values = line.strip().split('\t')

                number_of_value = 0
                for var_name in var_names:
                    if var_name in points_in_constrtaints_file:
                        variables_and_values_dict[var_name] = float(values[number_of_value])
                        number_of_value += 1
                    else:
                        variables_and_values_dict[var_name] = float(10000)

                for i in range(len(performance_table_list)):
                    for j in range(len(performance_table_list[i])):
                        variable_name: str = f"u_{j}_{performance_table_list[i][j]}"
                        if '-' in variable_name:
                            variable_name: str = variable_name.replace('-', '_')
                        if variable_name not in variables_and_values_dict:
                            variables_and_values_dict[variable_name] = float(10000)

                for var_name in variables_and_values_dict:
                    if variables_and_values_dict[var_name] == 10000.0:
                        point_before = 0
                        point_after = 1

                        if len(var_name.split("_")) == 4:
                            val = -float(var_name.split("_")[-1])
                        else:
                            val = float(var_name.split("_")[-1])

                        while characteristic_points[int(var_name.split("_")[1])][point_before] > val or val > \
                                characteristic_points[int(var_name.split("_")[1])][point_after]:
                            point_before += 1
                            point_after += 1

                        value = SolverUtils.linear_interpolation(val,
                                                                 characteristic_points[int(var_name.split("_")[1])][
                                                                     point_before], variables_and_values_dict[str(
                                u_list_dict[int(var_name.split("_")[1])][
                                    float(characteristic_points[int(var_name.split("_")[1])][point_before])])],
                                                                 characteristic_points[int(var_name.split("_")[1])][
                                                                     point_after], variables_and_values_dict[str(
                                u_list_dict[int(var_name.split("_")[1])][
                                    float(characteristic_points[int(var_name.split("_")[1])][point_after])])])

                        variables_and_values_dict[var_name] = float(value)

                alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
                    variables_and_values_dict=variables_and_values_dict,
                    performance_table_list=performance_table_list,
                    alternatives_id_list=alternatives_id_list,
                )

                for position in positions:
                    alternative = alternatives_id_list[position[0]]
                    ranking = list(alternatives_and_utilities_dict.keys())
                    position_in_ranking = len(performance_table_list) - ranking.index(alternative)

                    if position_in_ranking > position[1] or position_in_ranking < position[2]:
                        number_of_rejected += 1

            ratio = 1 - (number_of_rejected/1000)

            if ratio <= 0.1:
                return 'Rejection ratio to high'

            refined_number_of_samples = str(round(int(number_of_samples) / ratio))

            return refined_number_of_samples
