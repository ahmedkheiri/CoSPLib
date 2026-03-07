# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.run_mode import (
    solve_with_exact_milp,
    solve_with_extended_milp,
    solve_with_hyper_heuristic,
    solve_with_matheuristic,
)
from domain.problem import Problem
from pathlib import Path
import config
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    problem = Problem(file_path=Path(config.INPUT_PATH))
    problem.build()

    if config.HYPER_HEURISTIC:
        final_solution = solve_with_hyper_heuristic(problem)
    if config.MATHEURISTIC:
        final_solution = solve_with_matheuristic(problem)
    if config.EXACT_MILP:
        final_solution = solve_with_exact_milp(problem)
    if config.EXTENDED_MILP:
        final_solution = solve_with_extended_milp(problem)

    logging.info(
        f"Is solution feasible? {final_solution.evaluate_all_submissions_scheduled()}"
    )
    logging.info(f"Objective value: {final_solution.evaluate_solution()}")
    final_solution.print_violations()
    if config.SAVE_SOLUTION:
        final_solution.to_excel(file_path=Path(config.OUTPUT_PATH))
