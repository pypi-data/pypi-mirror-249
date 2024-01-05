# BU Course CLI

## Description
BU Course CLI is a command-line tool designed to interact with the Boston University course data. It allows users to list courses, get detailed information about specific courses, search for courses, compare courses, and check course prerequisites. This tool aims to provide an efficient way for students and faculty to access course-related information quickly and conveniently.

## Features
- **List All Courses**: Display a list of all available courses.
- **Get Course Information**: Retrieve detailed information about a specific course.
- **Search for Courses**: Find courses based on keywords.
- **Compare Courses**: Compare the details of two courses side-by-side.
- **Check Prerequisites**: View the prerequisites for a specific course.

## Installation
To install BU Course CLI, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/SuzzukiW/bu-course-cli.git
   ```
2. Navigate to the project directory:
   ```bash
   cd bu-course-cli
   ```
3. Install the package:
   ```bash
   pip install -e .
   ```

## Usage
After installation, you can use the following commands:

- **List All Courses**:
  ```bash
  bu-course-cli --list
  ```
- **Get Specific Course Information**:
  ```bash
  bu-course-cli --get "CDS DS 100"
  ```
- **Search for Courses**:
  ```bash
  bu-course-cli --search "data science"
  ```
- **Compare Two Courses**:
  ```bash
  bu-course-cli --compare "CDS DS 100,CDS DS 101"
  ```
- **Check Course Prerequisites**:
  ```bash
  bu-course-cli --prereqs "CDS DS 100"
  ```

## Configuration
You can configure the base URL for the course API by using the `--base-url` option with any command. By default, it uses `http://127.0.0.1:5000`.

## Contributing
Contributions to BU Course CLI are welcome. Please fork the repository and submit a pull request with your proposed changes.