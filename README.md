# Project: Eworkgroup scrapper

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Prerequisites

Before you can run this project, ensure you have the following installed:

1. **Python (version 3.8 or higher)**:
    - Download Python from [python.org](https://www.python.org/downloads/).
    - Run the installer and follow the instructions. Make sure to check the option to add Python to your system PATH
      during installation.

2. **pip (Python package manager)**:
    - pip is included with Python 3.4 and later, so if you installed Python, you should already have pip.

## Installation

Follow these steps to set up the project without using Git:

1. **Download the project as a ZIP archive:**

    - Go to https://gitlab.com/mihailodaniliuk/tenders_scrapper.
    - Click on the "Code" button and choose "zip".
    - Extract the downloaded ZIP archive to your desired location.

2. **Open Terminal (or Command Prompt):**

    - **On Windows**: Press `Win + R`, type `cmd`, and press Enter.
    - **On macOS**: Press `Cmd + Space`, type `Terminal`, and press Enter.
    - **On Linux**: Open the terminal through the appropriate shortcut or menu.

3. **Navigate to the project directory:**

    - In the terminal, change directory to the project folder using your preferred file manager.

4. **Create a virtual environment:**

    - In the terminal, create a virtual environment for Python:

      ```bash
      python -m venv venv
      ```

5. **Activate the virtual environment:**

    - **On Windows:**

      ```bash
      venv\Scripts\activate
      ```

    - **On macOS and Linux:**

      ```bash
      source venv/bin/activate
      ```

6. **Install the required packages:**

    - In the terminal, install all necessary packages:

      ```bash
      pip install -r requirements.txt
      ```

## Usage

After successfully setting up the environment and installing all necessary packages, you can run `main.py`:

1. **Ensure the virtual environment is activated:**

    - If it's not activated, activate it using the steps mentioned above.


2. **Run the script:**

    - Type the following command in the terminal and press Enter:

      ```bash
      python main.py
      ```
    - Enter the dates for which you want to get data
  

