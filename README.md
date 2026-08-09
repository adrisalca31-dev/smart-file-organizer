# Smart File Organizer

A Python-based file organization tool that automatically scans a selected folder, categorizes files by type, detects duplicates, and moves files into organized category folders.

The project was developed as a software engineering portfolio project, with an emphasis on modular architecture, automated testing, clean code, and practical file-system automation.


## Features

- Automatic file categorization
- Image, document, PDF, video, audio, and other file categories
- Duplicate file detection using SHA-256 hashing
- Dedicated `Duplicates` folder for duplicate files
- Hidden file detection and exclusion
- Internal log file exclusion
- Automatic creation of category folders
- Execution summary with file statistics
- Execution time measurement
- Operation logging
- CLI support
- Preview / dry-run mode
- Input folder validation
- Automated tests with Pytest


## Project Structure

01-smart-file-organizer/
│
├── assets/
│
├── docs/
│
├── src/
│   ├── cli.py
│   ├── main.py
│   ├── scanner.py
│   ├── categorizer.py
│   ├── organizer.py
│   ├── duplicate_checker.py
│   └── logger.py
│
├── testing/
│   └── sample_files/
│
├── tests/
│   ├── test_categorizer.py
│   ├── test_duplicate_checker.py
│   ├── test_organizer.py
│   └── test_scanner.py
│
├── .gitignore
├── PROJECT.md
├── README.md
└── requirements.txt


## How It Works

The application follows a simple processing pipeline:

User selects a folder
        ↓
Scanner finds valid files
        ↓
Duplicate checker analyzes file hashes
        ↓
File categorizer determines the file type
        ↓
Organizer creates the destination folder
        ↓
File is moved to its category
        ↓
Logger records the operation
        ↓
Execution summary is displayed


Duplicate files follow a separate path:

File
 ↓
SHA-256 hash
 ↓
Hash already processed?
 ├── Yes → Duplicates/
 └── No  → Continue classification


## Supported Categories

The application currently organizes files into:

| Category   | Examples                          |
| ---------- | --------------------------------- |
| Images     | `.jpg`, `.png`, `.jpeg`, etc.     |
| Documents  | `.docx`, `.txt`, `.xlsx`, etc.    |
| PDF        | `.pdf`                            |
| Videos     | `.mp4`, `.mov`, etc.              |
| Audio      | `.mp3`, `.wav`, etc.              |
| Others     | Unsupported or unknown extensions |
| Duplicates | Files with identical content      |


## Duplicate Detection

Duplicate files are detected using SHA-256 hashing.

Instead of relying only on filenames, the application calculates a cryptographic hash based on the file contents.

This allows files with different names to still be recognized as duplicates when their contents are identical.

Example:

photo.jpg
photo_copy.jpg

If both files contain exactly the same data, the application identifies the second file as a duplicate and moves it to:

Duplicates/



## Logging

The application generates an `organization_log.txt` file containing information about the organization process.

The log includes:

* Files processed
* File categories
* Duplicate detections
* Summary statistics
* Execution time

The application also prevents its own log file from being processed during subsequent executions.


## Preview / Dry-Run Mode

The project includes a preview mode that allows users to inspect the operations that would be performed without actually moving files.

This provides a safer way to verify the expected organization before modifying the file system.


## Installation

### 1. Clone the repository

bash
git clone https://github.com/adrisalca31-dev/smart-file-organizer.git


### 2. Enter the project directory

bash
cd smart-file-organizer


### 3. Create a virtual environment

bash
python3 -m venv .venv


### 4. Activate the virtual environment

On macOS/Linux:

bash
source .venv/bin/activate


### 5. Install dependencies

bash
python -m pip install -r requirements.txt



## Running the Application

Run the application with:

bash
python src/main.py


The application will request the path of the folder to organize.

Example:

Welcome to Smart File Organizer!

Enter folder path: /Users/example/Documents/test_files


## Running Tests

The project uses Pytest for automated testing.

Run all tests with:

bash
python -m pytest


The test suite covers core functionality including:

* File scanning
* Hidden file exclusion
* File categorization
* Folder creation
* File movement
* Duplicate detection
* SHA-256 hashing

Current test suite:

18 tests

## Technologies

* Python 3
* pathlib
* hashlib
* Pytest
* Git
* GitHub

The project primarily uses Python's standard library, keeping external dependencies to a minimum.


## Engineering Practices

This project follows several software engineering practices:

* Modular architecture
* Separation of responsibilities
* Type hints
* Docstrings
* Automated testing
* Virtual environments
* Git version control
* Incremental development
* Error handling
* Clear project documentation


## Future Improvements

Potential future improvements include:

* More advanced CLI options
* Recursive directory scanning
* Configurable categories
* Configurable file extensions
* Improved error handling
* Integration tests
* Code quality and linting tools
* Packaging the application as an installable CLI tool
* Performance improvements for large directories


## Project Documentation

Additional technical information about the architecture, requirements, design decisions, testing strategy, and development process can be found in:

[`PROJECT.md`](PROJECT.md)

## Author

Developed as part of a professional software engineering portfolio.
