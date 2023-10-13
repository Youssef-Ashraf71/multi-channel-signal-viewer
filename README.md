# Multi-Port, Multi-Channel Signal Viewer

## Table of Contents

- [Introduction](#introduction)
- [Project Description](#project-description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

---

## Introduction

Welcome to the Multi-Port, Multi-Channel Signal Viewer project! This desktop application, developed using Python and Qt, is designed to help you visualize and analyze multiple medical signal types simultaneously. The application allows you to view various signals, such as ECG, EMG, EEG, and more, both in normal and abnormal conditions.

## Live Demo


https://github.com/Youssef-Ashraf71/DSP-task1/assets/83988379/b47c3518-ccf8-4633-b10d-4d4af63f082e



## Project Description

Monitoring vital signals in an ICU room is crucial. This application provides a user-friendly interface for viewing, analyzing, and manipulating medical signals. It supports various features to enhance the user experience and assist in understanding the signals.

## Features

- **Signal Selection**: You can browse your PC to open signal files.

- **Dual Graphs**: The application contains two main identical graphs, and each graph has its own set of controls. You can open different signals in each graph and run them independently or link both graphs to display the same time frames, signal speed, and viewport.

- **Cine Mode**: Signals are displayed in cine mode, similar to ICU monitors. You can rewind a signal if it ends.

- **Signal Manipulation**: The user can manipulate running signals through UI elements, including changing color, adding labels, showing/hiding, customizing cine speed, zooming in/out, pausing/playing/rewinding, and scrolling/panning the signal in any direction.

- **Signal Transfer**: You can move signals from one graph to the other.

- **Boundary Conditions**: The application enforces boundary conditions to prevent unrealistic manipulations, ensuring a user-friendly experience.

- **Exporting & Reporting**: You can generate a report with snapshots of the graphs and data statistics on the displayed signals, exported to a PDF file. The report includes mean, standard deviation, duration, minimum, and maximum values for each signal.

## Prerequisites

Before using this application, ensure that you have the following prerequisites installed:

- Python (version 3.11.4)
- Qt (version 5.15.4)

## Installation

1. Clone this repository to your local machine:

```shell
git clone https://github.com/Youssef-Ashraf71/multi-signal-viewer.git
```

2. Install the required Python packages:

```shell
pip install -r requirements.txt
```

## Usage

1. Run the app

```shell
python main.py
```

1. Open signal files by browsing your PC.

2. Explore and manipulate the signals using the provided controls.

3. Generate reports as needed.
