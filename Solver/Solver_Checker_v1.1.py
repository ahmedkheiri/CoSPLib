# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
from solution import Solution
from pathlib import Path
import config
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    problem = Problem(file_path=Path(config.INPUT_PATH))
    problem.build()
    final_solution = Solution(problem)
    final_solution.load_solution(file_path=config.SOLUTION_INPUT_PATH)
    logging.info(
        f"Is solution feasible? {final_solution.evaluate_all_submissions_scheduled()}"
    )
    logging.info(f"Is solution valid? {final_solution.validate_solution()}")
    logging.info(f"Objective value: {final_solution.evaluate_solution()}")
    final_solution.print_violations()
    if config.SAVE_SOLUTION:
        final_solution.to_excel(file_path=Path(config.SOLUTION_OUTPUT_PATH))
