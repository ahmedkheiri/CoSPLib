# CSPLib User Guides (Version 0.1)

## Overview

The Conference Scheduler is an advanced tool designed to optimise the process of scheduling conferences in an autonomous, effortless, and fully automated manner. This tool uses Excel, which follows a specific template, to store input data and Python for the implementation of optimisation algorithms, ensuring that conference schedules are created efficiently and effectively. The primary goal is to provide a complete solution for scheduling conferences with minimal manual intervention.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Benefits](#benefits)
- [Using the Conference Scheduler](#using-the-conference-scheduler)
4. [Configuration](#configuration)
5. [Support](#support)
6. [Contributing](#contributing)
7. [License](#license)

## Installation

To install CSPLib and its dependencies, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/ahmedkheiri/CSPLib.git
    ```

2. Navigate to the project directory:
    ```sh
    cd CSPLib
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Requirements

- NumPy >= 1.24.2
- pandas >= 2.2.2
- PuLP >= 2.8.0
- Python >= 3.8.16
- pytz >= 2022.2

## Features

1. **User-Friendly Data Input:**
   Users can easily input and manage their data using Excel. An Excel template along with data examples are provided to standardise the data entry process, minimise errors and offer flexibility.

2. **Automated Scheduling:**
   Automatically assigns tracks to sessions and rooms, and submissions to sessions, time slots and rooms based on the input data and optimisation criteria. It also detects and resolves potential conflicts, ensuring a smooth and conflict-free conference schedule.

3. **Constraints Management:**
   Contains a pool of constraints to select from and allows weight assignment for each constraint based on user's preferences.

4. **Advanced Optimisation Techniques:**
   Advanced optimisation algorithms are included in the scheduler to ensure quick schedule generation, even for large-scale conferences with thousands of submissions.

5. **Hybrid & Online Conferences:**
   Suitable for hybrid and online conferences where submissions need to be scheduled in appropriate sessions considering timezone information.

6. **Output and Reporting:**
   Generates comprehensive optimised schedules in Excel format that can be easily reviewed and shared with stakeholders. The user can view a detailed report of violations for each constraint and can manually edit the solution to observe the impact of changes on solution quality.

## Benefits

- **Time-Saving:**
  Automates the arduous and time-consuming manual process of conference scheduling, saving significant time and effort for conference organisers.

- **Optimisation:**
  Uses advanced optimisation techniques to deliver high-quality conference schedules considering numerous preferences and constraints.

- **Flexibility:**
  Adaptable to different types of conferences and can handle a wide range of scheduling requirements.

- **Accuracy:**
  Reduces the likelihood of human error through automated checks and optimisations.

- **Scalability:**
  Suitable for managing both small and large conferences.

## Using the Conference Scheduler

To effectively use the Conference Scheduler, follow these steps:

1. **Excel file configuration:**
   Users enter their data into the provided Excel template, set scheduling requirements, and specify preferences.

2. **Optimisation Process:**
   The Excel data is imported into the system, and users select their preferred algorithm for scheduling optimisation.

3. **Review and Adjustments:**
   The system generates the optimised schedule, which is then exported back into Excel. Users can easily review the generated schedule, make any necessary adjustments, observe the impact on the schedule quality, and finalise the conference plan.















## Configuration

To configure the Conference Scheduler, modify the `config.json` file with your preferred settings. Here are the key configuration options:

- **input_file**: Path to the Excel file containing the input data.
- **output_file**: Path where the generated schedule will be saved.
- **algorithm**: The optimization algorithm to use (e.g., `genetic`, `greedy`).

## Support

For support, please open an issue on the [GitHub repository](https://github.com/yourusername/conference-scheduler/issues).

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
