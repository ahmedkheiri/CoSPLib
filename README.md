# CSPLib User Guides

## Version 0.1

## Overview

The Conference Scheduler is an advanced tool designed to optimise the process of scheduling conferences in an autonomous, effortless, and fully automated manner. This tool uses Excel, which follows a specific template, to store input data and Python for the implementation of optimisation algorithms, ensuring that conference schedules are created efficiently and effectively. The primary goal is to provide a complete solution for scheduling conferences with minimal manual intervention.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
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

## Usage

To use the Conference Scheduler, follow these steps:

1. Prepare your input data in the provided Excel template.
2. Run the scheduler script:
    ```sh
    python scheduler.py
    ```
3. The generated conference schedule will be outputted to a specified location.

## Features

- **Automated Scheduling**: Automatically generates conference schedules based on input data.
- **Excel Integration**: Utilizes an Excel template for easy data input.
- **Optimization Algorithms**: Implements sophisticated algorithms to optimize scheduling.

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
