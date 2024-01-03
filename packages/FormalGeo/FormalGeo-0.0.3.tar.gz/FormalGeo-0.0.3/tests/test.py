import copy

from formalgeo.solver import Interactor, ForwardSearcher, BackwardSearcher
from formalgeo.tools import load_json, save_json
from formalgeo.tools import show_solution, draw_solution_hypertree
from formalgeo.parse import parse_theorem_seqs, inverse_parse_one_theorem, parse_one_theorem
from formalgeo.tools import get_solution_hypertree, get_theorem_dag, draw_theorem_dag, get_meta_hypertree
from formalgeo.data import DatasetLoader, download_dataset
from formalgeo.core import EquationKiller as EqKiller
from formalgeo.problem import Problem
import time
import random
from formalgeo.tools import debug_print
import warnings
import re

predicate_words = [
    'Shape', 'Collinear', 'Cocircular', 'Point', 'Line', 'Arc', 'Angle', 'Polygon', 'Circle',
    'RightTriangle', 'IsoscelesTriangle', 'IsoscelesRightTriangle', 'EquilateralTriangle', 'Kite',
    'Parallelogram', 'Rhombus', 'Rectangle', 'Square', 'Trapezoid', 'IsoscelesTrapezoid',
    'RightTrapezoid', 'IsMidpointOfLine', 'IsMidpointOfArc', 'ParallelBetweenLine',
    'PerpendicularBetweenLine', 'IsPerpendicularBisectorOfLine', 'IsBisectorOfAngle',
    'IsMedianOfTriangle', 'IsAltitudeOfTriangle', 'IsMidsegmentOfTriangle', 'IsCircumcenterOfTriangle',
    'IsIncenterOfTriangle', 'IsCentroidOfTriangle', 'IsOrthocenterOfTriangle',
    'CongruentBetweenTriangle', 'MirrorCongruentBetweenTriangle', 'SimilarBetweenTriangle',
    'MirrorSimilarBetweenTriangle', 'IsAltitudeOfQuadrilateral', 'IsMidsegmentOfQuadrilateral',
    'IsCircumcenterOfQuadrilateral', 'IsIncenterOfQuadrilateral', 'CongruentBetweenQuadrilateral',
    'MirrorCongruentBetweenQuadrilateral', 'SimilarBetweenQuadrilateral',
    'MirrorSimilarBetweenQuadrilateral', 'CongruentBetweenArc', 'SimilarBetweenArc',
    'IsDiameterOfCircle', 'IsTangentOfCircle', 'IsCentreOfCircle'
]

theorem_words = [
    "self", "none",
    'line_addition_1', 'midpoint_of_line_judgment_1', 'parallel_judgment_corresponding_angle_1',
    'parallel_judgment_corresponding_angle_2', 'parallel_judgment_alternate_interior_angle_1',
    'parallel_judgment_alternate_interior_angle_2', 'parallel_judgment_ipsilateral_internal_angle_1',
    'parallel_judgment_par_par_1', 'parallel_judgment_per_per_1', 'parallel_judgment_per_per_2',
    'parallel_property_collinear_extend_1', 'parallel_property_collinear_extend_2',
    'parallel_property_collinear_extend_3', 'parallel_property_corresponding_angle_1',
    'parallel_property_corresponding_angle_2', 'parallel_property_alternate_interior_angle_1',
    'parallel_property_alternate_interior_angle_2', 'parallel_property_ipsilateral_internal_angle_1',
    'parallel_property_par_per_1', 'parallel_property_par_per_2', 'perpendicular_judgment_angle_1',
    'perpendicular_bisector_judgment_per_and_mid_1', 'perpendicular_bisector_judgment_distance_equal_1',
    'perpendicular_bisector_property_distance_equal_1', 'perpendicular_bisector_property_bisector_1',
    'angle_addition_1', 'flat_angle_1', 'adjacent_complementary_angle_1', 'round_angle_1', 'vertical_angle_1',
    'bisector_of_angle_judgment_angle_equal_1', 'bisector_of_angle_property_distance_equal_1',
    'bisector_of_angle_property_line_ratio_1', 'bisector_of_angle_property_length_formula_1',
    'triangle_property_angle_sum_1', 'sine_theorem_1', 'cosine_theorem_1', 'triangle_perimeter_formula_1',
    'triangle_area_formula_common_1', 'triangle_area_formula_sine_1', 'median_of_triangle_judgment_1',
    'altitude_of_triangle_judgment_1', 'altitude_of_triangle_judgment_2', 'altitude_of_triangle_judgment_3',
    'midsegment_of_triangle_judgment_midpoint_1', 'midsegment_of_triangle_judgment_parallel_1',
    'midsegment_of_triangle_judgment_parallel_2', 'midsegment_of_triangle_judgment_parallel_3',
    'midsegment_of_triangle_property_parallel_1', 'midsegment_of_triangle_property_length_1',
    'circumcenter_of_triangle_judgment_intersection_1', 'circumcenter_of_triangle_property_intersection_1',
    'circumcenter_of_triangle_property_intersection_2', 'incenter_of_triangle_judgment_intersection_1',
    'centroid_of_triangle_judgment_intersection_1', 'centroid_of_triangle_property_intersection_1',
    'centroid_of_triangle_property_line_ratio_1', 'orthocenter_of_triangle_judgment_intersection_1',
    'orthocenter_of_triangle_property_intersection_1', 'orthocenter_of_triangle_property_angle_1',
    'congruent_triangle_judgment_sss_1', 'congruent_triangle_judgment_sas_1', 'congruent_triangle_judgment_aas_1',
    'congruent_triangle_judgment_aas_2', 'congruent_triangle_judgment_aas_3', 'congruent_triangle_judgment_hl_1',
    'congruent_triangle_judgment_hl_2', 'congruent_triangle_property_line_equal_1',
    'congruent_triangle_property_angle_equal_1', 'congruent_triangle_property_perimeter_equal_1',
    'congruent_triangle_property_area_equal_1', 'congruent_triangle_property_exchange_1',
    'mirror_congruent_triangle_judgment_sss_1', 'mirror_congruent_triangle_judgment_sas_1',
    'mirror_congruent_triangle_judgment_aas_1', 'mirror_congruent_triangle_judgment_aas_2',
    'mirror_congruent_triangle_judgment_aas_3', 'mirror_congruent_triangle_judgment_hl_1',
    'mirror_congruent_triangle_judgment_hl_2', 'mirror_congruent_triangle_property_line_equal_1',
    'mirror_congruent_triangle_property_angle_equal_1', 'mirror_congruent_triangle_property_perimeter_equal_1',
    'mirror_congruent_triangle_property_area_equal_1', 'mirror_congruent_triangle_property_exchange_1',
    'similar_triangle_judgment_sss_1', 'similar_triangle_judgment_sas_1', 'similar_triangle_judgment_aa_1',
    'similar_triangle_judgment_hl_1', 'similar_triangle_judgment_hl_2', 'similar_triangle_property_ratio_1',
    'similar_triangle_property_line_ratio_1', 'similar_triangle_property_angle_equal_1',
    'similar_triangle_property_perimeter_ratio_1', 'similar_triangle_property_area_square_ratio_1',
    'mirror_similar_triangle_judgment_sss_1', 'mirror_similar_triangle_judgment_sas_1',
    'mirror_similar_triangle_judgment_aa_1', 'mirror_similar_triangle_judgment_hl_1',
    'mirror_similar_triangle_judgment_hl_2', 'mirror_similar_triangle_property_ratio_1',
    'mirror_similar_triangle_property_line_ratio_1', 'mirror_similar_triangle_property_angle_equal_1',
    'mirror_similar_triangle_property_perimeter_ratio_1', 'mirror_similar_triangle_property_area_square_ratio_1',
    'right_triangle_judgment_angle_1', 'right_triangle_judgment_pythagorean_inverse_1',
    'right_triangle_property_pythagorean_1', 'right_triangle_property_length_of_median_1',
    'isosceles_triangle_judgment_line_equal_1', 'isosceles_triangle_judgment_angle_equal_1',
    'isosceles_triangle_property_angle_equal_1', 'isosceles_triangle_property_line_coincidence_1',
    'isosceles_triangle_property_line_coincidence_2', 'isosceles_triangle_property_line_coincidence_3',
    'isosceles_right_triangle_judgment_isosceles_and_right_1', 'isosceles_right_triangle_property_angle_1',
    'equilateral_triangle_judgment_isosceles_and_isosceles_1', 'equilateral_triangle_property_angle_1',
    'quadrilateral_property_angle_sum_1', 'quadrilateral_perimeter_formula_1', 'altitude_of_quadrilateral_judgment_1',
    'altitude_of_quadrilateral_judgment_2', 'altitude_of_quadrilateral_judgment_3',
    'altitude_of_quadrilateral_judgment_4', 'altitude_of_quadrilateral_judgment_5',
    'altitude_of_quadrilateral_judgment_6', 'altitude_of_quadrilateral_judgment_left_vertex_1',
    'altitude_of_quadrilateral_judgment_left_vertex_2', 'altitude_of_quadrilateral_judgment_left_vertex_3',
    'altitude_of_quadrilateral_judgment_left_vertex_4', 'altitude_of_quadrilateral_judgment_left_vertex_5',
    'altitude_of_quadrilateral_judgment_left_vertex_6', 'altitude_of_quadrilateral_judgment_right_vertex_1',
    'altitude_of_quadrilateral_judgment_right_vertex_2', 'altitude_of_quadrilateral_judgment_right_vertex_3',
    'altitude_of_quadrilateral_judgment_right_vertex_4', 'altitude_of_quadrilateral_judgment_right_vertex_5',
    'altitude_of_quadrilateral_judgment_right_vertex_6', 'altitude_of_quadrilateral_judgment_diagonal_1',
    'altitude_of_quadrilateral_judgment_diagonal_2', 'altitude_of_quadrilateral_judgment_diagonal_3',
    'altitude_of_quadrilateral_judgment_diagonal_4', 'midsegment_of_quadrilateral_judgment_midpoint_1',
    'midsegment_of_quadrilateral_judgment_parallel_1', 'midsegment_of_quadrilateral_judgment_parallel_2',
    'midsegment_of_quadrilateral_judgment_parallel_3', 'midsegment_of_quadrilateral_judgment_parallel_4',
    'midsegment_of_quadrilateral_judgment_parallel_5', 'midsegment_of_quadrilateral_judgment_parallel_6',
    'midsegment_of_quadrilateral_property_length_1', 'midsegment_of_quadrilateral_property_parallel_1',
    'midsegment_of_quadrilateral_property_parallel_2', 'circumcenter_of_quadrilateral_property_intersection_1',
    'circumcenter_of_quadrilateral_property_intersection_2', 'congruent_quadrilateral_property_line_equal_1',
    'congruent_quadrilateral_property_angle_equal_1', 'congruent_quadrilateral_property_perimeter_equal_1',
    'congruent_quadrilateral_property_area_equal_1', 'congruent_quadrilateral_property_exchange_1',
    'mirror_congruent_quadrilateral_property_line_equal_1', 'mirror_congruent_quadrilateral_property_angle_equal_1',
    'mirror_congruent_quadrilateral_property_perimeter_equal_1',
    'mirror_congruent_quadrilateral_property_area_equal_1', 'mirror_congruent_quadrilateral_property_exchange_1',
    'similar_quadrilateral_property_ratio_1', 'similar_quadrilateral_property_line_ratio_1',
    'similar_quadrilateral_property_angle_equal_1', 'similar_quadrilateral_property_perimeter_ratio_1',
    'similar_quadrilateral_property_area_square_ratio_1', 'mirror_similar_quadrilateral_property_ratio_1',
    'mirror_similar_quadrilateral_property_line_ratio_1', 'mirror_similar_quadrilateral_property_angle_equal_1',
    'mirror_similar_quadrilateral_property_perimeter_ratio_1',
    'mirror_similar_quadrilateral_property_area_square_ratio_1', 'parallelogram_judgment_parallel_and_parallel_1',
    'parallelogram_judgment_parallel_and_equal_1', 'parallelogram_judgment_equal_and_equal_1',
    'parallelogram_judgment_angle_and_angle_1', 'parallelogram_judgment_diagonal_bisection_1',
    'parallelogram_property_opposite_line_equal_1', 'parallelogram_property_opposite_angle_equal_1',
    'parallelogram_property_diagonal_bisection_1', 'parallelogram_area_formula_common_1',
    'parallelogram_area_formula_sine_1', 'kite_judgment_equal_and_equal_1',
    'kite_property_diagonal_perpendicular_bisection_1', 'kite_property_opposite_angle_equal_1',
    'kite_area_formula_diagonal_1', 'kite_area_formula_sine_1', 'rectangle_judgment_right_angle_1',
    'rectangle_judgment_diagonal_equal_1', 'rectangle_property_diagonal_equal_1',
    'rhombus_judgment_parallelogram_and_kite_1', 'square_judgment_rhombus_and_rectangle_1',
    'trapezoid_judgment_parallel_1', 'trapezoid_area_formula_1', 'right_trapezoid_judgment_right_angle_1',
    'right_trapezoid_area_formular_1', 'isosceles_trapezoid_judgment_line_equal_1',
    'isosceles_trapezoid_judgment_angle_equal_1', 'isosceles_trapezoid_judgment_diagonal_equal_1',
    'isosceles_trapezoid_property_angle_equal_1', 'isosceles_trapezoid_property_diagonal_equal_1', 'round_arc_1',
    'arc_addition_length_1', 'arc_addition_measure_1', 'arc_property_center_angle_1',
    'arc_property_circumference_angle_external_1', 'arc_property_circumference_angle_internal_1',
    'arc_length_formula_1', 'congruent_arc_judgment_length_equal_1', 'congruent_arc_judgment_measure_equal_1',
    'congruent_arc_judgment_chord_equal_1', 'congruent_arc_property_length_equal_1',
    'congruent_arc_property_measure_equal_1', 'congruent_arc_property_chord_equal_1',
    'similar_arc_judgment_cocircular_1', 'similar_arc_property_ratio_1', 'similar_arc_property_length_ratio_1',
    'similar_arc_property_measure_ratio_1', 'similar_arc_property_chord_ratio_1',
    'circle_property_length_of_radius_and_diameter_1', 'circle_property_circular_power_chord_and_chord_1',
    'circle_property_circular_power_tangent_and_segment_line_1',
    'circle_property_circular_power_segment_and_segment_line_1',
    'circle_property_circular_power_tangent_and_segment_angle_1',
    'circle_property_circular_power_tangent_and_segment_angle_2',
    'circle_property_circular_power_segment_and_segment_angle_1',
    'circle_property_circular_power_segment_and_segment_angle_2', 'circle_property_chord_perpendicular_bisect_chord_1',
    'circle_property_chord_perpendicular_bisect_chord_2', 'circle_property_chord_perpendicular_bisect_arc_1',
    'circle_property_chord_perpendicular_bisect_arc_2', 'circle_property_angle_of_osculation_1',
    'circle_property_angle_of_osculation_2', 'circle_perimeter_formula_1', 'circle_area_formula_1',
    'radius_of_circle_property_length_equal_1', 'diameter_of_circle_judgment_pass_centre_1',
    'diameter_of_circle_judgment_length_equal_1', 'diameter_of_circle_judgment_right_angle_1',
    'diameter_of_circle_property_length_equal_1', 'diameter_of_circle_property_right_angle_1',
    'tangent_of_circle_judgment_perpendicular_1', 'tangent_of_circle_judgment_perpendicular_2',
    'tangent_of_circle_property_perpendicular_1', 'tangent_of_circle_property_perpendicular_2',
    'tangent_of_circle_property_length_equal_1', 'sector_perimeter_formula_1', 'sector_area_formula_1',
    'perpendicular_bisector_judgment_per_and_bisect_1'
]

symbol_words = [
    ",", "+", "-", "**", "*", "/", "sin", "asin", "cos", "acos", "tan", "atan", "sqrt", "(", ")",
    "nums", 'll_', 'ma_', 'pt_', 'at_', 'ht_', 'rst_', 'rmt_', 'pq_', 'aq_', 'hq_', 'rsq_', 'rmq_', 'la_',
    'mar_', 'rsa_', 'rc_', 'dc_', 'pc_', 'ac_', 'ps_', 'as_'
]

letter_words = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
    "t", "u", "v", "w", "x", "y", "z"
]

special_words = [
    "<padding>", "<start>", "<end>", "<and>", "<to>"
]


def test():
    test_datasets_path = "F:/FormalGeoTest/datasets"
    dataset = "formalgeo-imo_v1"
    pid = 1

    dl = DatasetLoader(dataset, test_datasets_path)
    solver = Interactor(dl.predicate_GDL, dl.theorem_GDL)
    problem_CDL = dl.get_problem(pid)
    solver.load_problem(problem_CDL)
    for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):  # apply theorem_seqs
        solver.apply_theorem(t_name, t_branch, t_para)
    solver.problem.check_goal()
    show_solution(solver.problem)
    save_json(get_solution_hypertree(solver.problem), "{}_imo_hyper.json".format(pid))
    draw_solution_hypertree(solver.problem, "./")
    save_json(get_theorem_dag(solver.problem), "{}_imo_dag.json".format(pid))
    draw_theorem_dag(solver.problem, "./")
    draw_solution_hypertree(solver.problem, './')


def tokenize(cdl):
    """
    Build hypertree and return.
    :param cdl: CDL, such as 'CongruentBetweenTriangle(RST,XYZ)' or 'Equation(ll_tr-x-21)'.
    :return tokenized: tokenized CDL, such as ['CongruentBetweenTriangle', 'R', 'S', 'T', ',', 'X', 'Y', 'Z'].
    """
    cdl = cdl[0:len(cdl) - 1].split("(", maxsplit=1)
    tokenized = [cdl[0]]
    if cdl[0] != "Equation":
        tokenized += list(cdl[1])
    else:
        for matched in re.findall(r"sin\(pi\*ma_\w+/180\)", cdl[1]):  # adjust trigonometric
            cdl[1] = cdl[1].replace(matched, "sin({})".format(matched[7:13]))
        for matched in re.findall(r"cos\(pi\*ma_\w+/180\)", cdl[1]):
            cdl[1] = cdl[1].replace(matched, "cos({})".format(matched[7:13]))
        for matched in re.findall(r"tan\(pi\*ma_\w+/180\)", cdl[1]):
            cdl[1] = cdl[1].replace(matched, "tan({})".format(matched[7:13]))

        for matched in re.findall(r"\d+\.*\d*", cdl[1]):  # replace real number with 'nums'
            cdl[1] = cdl[1].replace(matched, "nums", 1)

        while len(cdl[1]) > 0:  # tokenize
            length = len(cdl[1])
            for c in symbol_words:
                if cdl[1].startswith(c):
                    tokenized.append(cdl[1][0:len(c)])
                    cdl[1] = cdl[1][len(c):len(cdl[1])]
            if length == len(cdl[1]):
                tokenized.append(cdl[1][0])
                cdl[1] = cdl[1][1:len(cdl[1])]

    return tokenized


def get_hypertree(problem):
    """
    Build hypertree and return.
    :param problem: instance of <formalgeo.problem.Problem>.
    :return nodes: n*1, List of hyper nodes.
    :return path: n*1, Path from hyper node i to other nodes.
    """
    nodes, edges, free_nodes, tree = get_meta_hypertree(problem)

    for edge_id in edges:
        if "(" in edges[edge_id]:
            t_name, para = edges[edge_id].split("(")
            edges[edge_id] = "{}_{}".format(t_name, para[0])
    all_nodes = list(nodes.keys())
    path = [[["none"] for _ in all_nodes] for _ in all_nodes]
    for node_id in all_nodes:
        path[all_nodes.index(node_id)][all_nodes.index(node_id)] = ["self"]

    for premise, theorem in tree:  # init path
        conclusion = tree[(premise, theorem)]
        for head_node_id in premise:
            for tail_node_id in conclusion:
                path[all_nodes.index(head_node_id)][all_nodes.index(tail_node_id)] = [edges[theorem]]

    update = True
    while update:  # gen path
        update = False
        for i in range(len(path)):
            for j in range(len(path)):
                if path[i][j] == ["self"] or path[i][j] == ["none"]:
                    continue
                for k in range(len(path)):
                    if path[i][k] == ["none"] and path[j][k] != ["self"] and path[j][k] != ["none"]:
                        path[i][k] = path[i][j] + path[j][k]
                        update = True
    joined_path = []
    for i in range(len(path)):
        node_i_paths = [path[i][0][0]]
        for k in range(1, len(path[i][0])):
            node_i_paths.append("<to>")
            node_i_paths.append(path[i][0][k])

        for j in range(1, len(path[i])):
            node_i_paths.append("<and>")
            node_i_paths.append(path[i][j][0])
            for k in range(1, len(path[i][j])):
                node_i_paths.append("<to>")
                node_i_paths.append(path[i][j][k])

        joined_path.append(node_i_paths)

    tokenized_nodes = []
    for node in nodes.values():
        tokenized_nodes.append(tokenize(node))

    return tokenized_nodes, joined_path


def traverse_theorem_dag(dag):
    """Traverse theorem dag and return all theorem seqs. A simple DAG can generate many sequences."""
    choice = copy.copy(dag["START"])
    traversed = []
    stack = [(choice, traversed)]
    theorem_seqs = []

    while len(stack) > 0:
        choice, traversed = stack.pop()
        for i in range(len(choice)):
            new_choice = copy.copy(choice)
            new_traversed = copy.copy(traversed)
            theorem = new_choice.pop(i)
            new_traversed.append(theorem)
            if theorem in dag:
                new_choice += dag[theorem]

            if len(new_choice) == 0:
                theorem_seqs.append(new_traversed)
            else:
                stack.append((new_choice, new_traversed))

    return theorem_seqs


def main():
    test_datasets_path = "F:/FormalGeoTest/datasets"
    dataset = "formalgeo7k_v1"
    dl = DatasetLoader(dataset, test_datasets_path)
    solver = Interactor(dl.predicate_GDL, dl.theorem_GDL)

    while True:
        pid = int(input("pid:"))
        problem_CDL = dl.get_problem(pid)

        # theorem_seqs = traverse_theorem_dag(problem_CDL["theorem_seqs_dag"])
        # for i in range(len(theorem_seqs)):
        #     print(theorem_seqs[i])

        solver.load_problem(problem_CDL)
        for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):  # apply theorem_seqs
            solver.apply_theorem(t_name, t_branch, t_para)
        solver.problem.check_goal()
        nodes, path = get_hypertree(solver.problem)
        for i in range(len(nodes)):
            print(nodes[i])
        print()
        for i in range(len(path)):
            print(path[i])
        print()


if __name__ == '__main__':
    import json

    # 示例JSON数据
    data = {
        "name": "John Doe",
        "age": 30,
        "married": True,
        "children": ["Alice", "Bob"],
        "pets": None,
        "cars": [{"model": "Toyota", "year": 2018}, {"model": "Ford", "year": 2020}]
    }
