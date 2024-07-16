# CSPLib User Guides (Version 0.1)

## Overview

The Conference Scheduler is an advanced tool designed to optimise the process of scheduling conferences in an autonomous, effortless, and fully automated manner. This tool uses Excel, which follows a specific template, to store input data and Python for the implementation of optimisation algorithms, ensuring that conference schedules are created efficiently and effectively. The primary goal is to provide a complete solution for scheduling conferences with minimal manual intervention.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Benefits](#benefits)
- [Using the Conference Scheduler](#using-the-conference-scheduler)
- [Terminology](#terminology)
- [Constraints Available](#constraints-available)
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

## Terminology

- **Submission:** A formal event that requires scheduling at a conference (e.g., paper, presentation, tutorial, workshop, etc.).
- **Track:** A group of submissions with similar subject (e.g., stream, subject area, topic, etc.).
- **Time slot:** A fixed predefined amount of time available for presentation (e.g., 15 minutes, 20 minutes, etc.).
- **Session:** A certain time period of the conference that consists of a number of time slots (e.g., the duration of a session consisting of 4 time slots is 1 hour, assuming each time slot is 15 minutes).

## Constraints Available

Users are able to select the constraints to include during the schedule optimisation by assigning a weight value to each constraint. The following constraints are available to select from:

- **Presenters' conflicts:** In many conferences, authors are allowed to present more than one submission. This is resolved by either scheduling such submissions within the same room of a session or within different sessions (or time slots). Users can select between session or time slot level conflict resolution.

- **Presenters' preferences:** These are requests received from presenters in which they either express a preferred session to present their submission or declare their unavailability to present at specific sessions.

- **Presenters' time zones:** On the occasion of an online or hybrid conference, presenters may request the consideration of time zone differences upon scheduling.

- **Rooms preferences:** Sometimes presenters may request to present their submission at a specific room for various reasons. Some examples are that a room may provide specific facilities which others do not provide, and some rooms may be easier to access in comparison to others.

- **Attendees' conflicts:** Some conferences collect preferences from attendees regarding which submissions they would prefer to attend. In such cases, an attendee conflict occurs when two preferred submissions of an attendee are scheduled in parallel. This is resolved in the same way as presenters' conflicts, and users can select between session or time slot level conflict resolution.

- **Rooms capacities:** Users can express preferences regarding the scheduling of tracks into rooms by setting appropriate penalty values.

- **Similar tracks:** Sometimes, conferences have a number of tracks which are similar with the potential of attracting the interest of the same audience. Users can define which tracks are similar to avoid having them scheduled in parallel by setting appropriate penalty values.

- **Parallel tracks:** This constraint avoids scheduling the same track in parallel.

- **Session hopping:** Having a track scheduled in multiple rooms is inconvenient for the participants as they would have to switch rooms frequently. This constraint minimises the number of rooms that each track utilises.

- **Track chairs' conflicts:** Tracks are usually chaired by a person who might be also a presenter and/or an attendee at a conference. A track chair conflict occurs when either a track chair is responsible for two tracks which are scheduled in parallel or a track chair is also a presenter or an attendee of a submission belonging to another track which is scheduled in parallel.

- **Tracks' scheduling preferences:** Users can express preferences regarding the scheduling of tracks into sessions by setting appropriate penalty values.

- **Rooms unavailability:** Sometimes, certain rooms might be unavailable for utilisation during certain sessions. Users can define which rooms are unavailable during certain sessions by setting appropriate penalty values.

- **Consecutive tracks:** This constraint aims to schedule tracks in a consecutive manner.

- **Submission's Order:** Users can define the scheduling order of submissions within their tracks.













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
