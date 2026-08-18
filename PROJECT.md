# Smart File Organizer — Project Documentation

## 1. Project Overview

Smart File Organizer is a Python application designed to automate the organization of files inside a selected directory.

The application scans a folder, identifies valid files, determines their categories based on file extensions, detects duplicate files using SHA-256 hashing, creates the required destination folders, moves the files, and generates an execution log.

The project was developed as part of a professional software engineering portfolio, with an emphasis on modularity, maintainability, automated testing, and practical file-system automation.

---

## 2. Project Goals

The main goals of the project are:

- Automate repetitive file organization tasks.
- Reduce manual organization of files.
- Detect duplicate files based on file content rather than filenames.
- Provide a clear and predictable folder structure.
- Record file organization operations.
- Provide useful execution statistics.
- Implement automated tests for core functionality.
- Follow software engineering practices suitable for a portfolio project.

---

## 3. Functional Requirements

The application should be able to:

1. Accept a folder selected by the user.
2. Validate that the selected path exists.
3. Validate that the selected path is a directory.
4. Scan the selected directory for valid files.
5. Ignore hidden files.
6. Ignore the application's own log file.
7. Determine the category of each file.
8. Create category folders when necessary.
9. Detect duplicate files using SHA-256.
10. Move files into their corresponding folders.
11. Move duplicate files into a dedicated `Duplicates` folder.
12. Prevent filename conflicts when moving files.
13. Generate unique filenames when a destination file already exists.
14. Generate an execution log.
15. Display an execution summary.
16. Measure execution time.
17. Support preview/dry-run functionality.
18. Handle file movement errors without terminating the complete process.
19. Provide automated tests for core components.
20. Provide CLI argument support through `--help` and `--dry-run`.


## 4. Non-Functional Requirements

The project should also satisfy the following requirements:

### Maintainability

The code should be divided into modules with clear responsibilities.

### Reliability

Core functionality should be covered by automated tests.

### Usability

The application should provide clear messages during execution and understandable error messages.

### Portability

The project should rely primarily on Python's standard library and avoid unnecessary external dependencies.

### Safety

Preview functionality should allow users to inspect expected operations before modifying files.

### Performance

File hashing and scanning should be implemented efficiently enough for normal personal and small-to-medium directory workloads.


## 5. Architecture

The application follows a modular architecture in which each module has a specific responsibility.

```text
                         ┌──────────────┐
                         │    main.py   │
                         │ Application  │
                         │ Coordinator  │
                         └──────┬───────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
    ┌───────────┐       ┌──────────────┐       ┌───────────┐
    │  scanner  │       │     cli      │       │ duplicate │
    │           │       │              │       │  checker  │
    └─────┬─────┘       └──────────────┘       └─────┬─────┘
          │                                          │
          │                                          │
          ▼                                          ▼
    ┌──────────────┐                         SHA-256 hashes
    │ categorizer  │
    └──────┬───────┘
           │
           ▼
    ┌─────────────────────────────┐
    │         organizer.py        │
    │ Folder creation + movement  │
    │ Conflict handling           │
    └──────────────┬──────────────┘
                   │
                   ▼
            ┌──────────────┐
            │   logger.py  │
            └──────────────┘
```

The main application coordinates the workflow while the individual modules handle scanning, classification, duplicate detection, file-system operations, command-line arguments, and logging independently.

Duplicate processing follows a separate decision path:

```text
File
  │
  ▼
SHA-256 hash
  │
  ▼
Hash already processed?
  │
  ├── Yes → Duplicates/
  │
  └── No → Continue classification
```
## 6. Module Responsibilities

### `main.py`

Acts as the main application coordinator.

Responsibilities:

* Create category directories.
* Move files into destination directories.
* Detect filename conflicts.
* Generate a unique filename when the destination already contains a file with the same name.

The module coordinates the application rather than implementing every operation itself.

---

### `cli.py`

Handles command-line arguments and application options.

The CLI is intended to provide a clean interface for controlling application behavior.

The project includes support for preview/dry-run functionality.

---

### `scanner.py`

Responsible for discovering valid files inside the selected directory.

Responsibilities:

* Validate the selected folder.
* Find files contained directly in the folder.
* Ignore hidden files.
* Ignore `organization_log.txt`.
* Ignore directories.

The scanner does not categorize or move files.

---

### `categorizer.py`

Determines the category of a file based on its extension.

Current categories:

* Images
* Documents
* PDF
* Videos
* Audio
* Others

The module is intentionally separated from the scanner so that file discovery and file classification remain independent responsibilities.

---

### `organizer.py`

Responsible for file-system organization.

Responsibilities:

* Create category directories.
* Move files into destination directories.

The module does not determine why a file belongs to a category.

---

### `duplicate_checker.py`

Responsible for duplicate detection.

The module calculates a SHA-256 hash for each file.

The application stores previously processed hashes in a set:

python
seen_hashes: set[str]


When a file is processed:

text
Calculate hash
      ↓
Is hash already in set?
      │
      ├── Yes → Duplicate
      │
      └── No → Add hash and continue


This allows files with different names to be recognized as duplicates when their contents are identical.

---

### `logger.py`

Responsible for generating the organization log.

The log records information about:

* Processed files.
* Categories.
* Duplicate detections.
* File movement errors.
* Summary information.
* Execution time.
---

## 7. File Categorization

File categorization is based on file extensions.

Example:

text
photo.jpg      → Images
report.docx    → Documents
manual.pdf     → PDF
movie.mp4      → Videos
song.mp3       → Audio
unknown.xyz    → Others


File extensions are normalized to lowercase before classification.

This means:

text
PHOTO.JPG
photo.jpg
Photo.JpG


are treated as the same extension category.

---

## 8. Duplicate Detection Strategy

The application uses SHA-256 to identify duplicate files.

The algorithm is content-based rather than filename-based.

For each file:

1. Open the file in binary mode.
2. Read the file in chunks.
3. Update the SHA-256 hash.
4. Generate the final hexadecimal digest.
5. Compare the hash with previously processed hashes.

Conceptually:

text
File A
  ↓
SHA-256
  ↓
Hash A

File B
  ↓
SHA-256
  ↓
Hash B

Hash A == Hash B
      ↓
Duplicate


The files do not need to have the same filename.

---

## 9. File Organization Workflow

The normal processing workflow is:

```text
Start
  ↓
Select folder
  ↓
Validate folder
  ↓
Scan files
  ↓
For each file
  ↓
Calculate duplicate hash
  ↓
Duplicate?
 ├── Yes → Move to Duplicates
 │           ↓
 │      Handle filename conflict
 │
 └── No
      ↓
   Determine category
      ↓
   Create category folder
      ↓
   Check filename conflict
      ↓
   Move file
      ↓
   Record operation
  ↓
Display summary
  ↓
Generate log
  ↓
Finish
```


## 10. Error Handling

The application validates the selected path before processing.

If the path does not exist, the application reports that the folder could not be found.

If the path exists but is not a directory, the application reports that the selected path is not a folder.

The scanner also raises appropriate Python exceptions when invalid paths are passed directly to its functions.

During file movement, `OSError` exceptions are handled so that a failure affecting one file does not terminate the complete organization process.

Failed files are counted separately and included in the execution summary.

Movement errors are also recorded in the organization log when logging is enabled.

This allows both the application and automated tests to handle invalid input and file-system failures predictably.


## 11. Testing Strategy

The project uses Pytest for automated testing.

Tests are located in:

```text
tests/
```

Current test modules:

```text
test_categorizer.py
test_cli.py
test_duplicate_checker.py
test_integration.py
test_logger.py
test_organizer.py
test_scanner.py
```

The test suite currently contains **26 tests**.

### Current coverage areas

#### Categorization

Tests verify:

* Image classification.
* PDF classification.
* Video classification.
* Audio classification.
* Document classification.
* Unknown extension handling.

#### Duplicate Detection

Tests verify:

* Consistent SHA-256 hashes.
* Detection of identical file contents.
* Correct handling of different file contents.
* Duplicate detection during the complete organization workflow.

#### Organization

Tests verify:

* Category folder creation.
* Existing folder handling.
* File movement.
* Filename conflict handling.
* Automatic filename generation when conflicts exist.
* Missing source file error handling.

#### Scanning

Tests verify:

* Visible file detection.
* Hidden file exclusion.
* Log file exclusion.
* Directory exclusion.
* Missing folder errors.
* Invalid directory errors.

#### CLI

Tests verify:

* Command-line argument parsing.
* Preview / dry-run option handling.

#### Logging

Tests verify:

* Organization log creation.
* Logged operation information.

#### Integration Testing

The project includes integration tests that simulate a complete organization workflow using temporary directories.

The integration tests verify:

* File scanning.
* Duplicate detection.
* File categorization.
* Category folder creation.
* File movement.
* Duplicate file organization.
* Final file locations.
* Filename conflict handling.

## 12. Testing Environment

The project uses a Python virtual environment:

```text
.venv/
```

The virtual environment isolates project dependencies from the system Python installation.

The environment itself is not committed to Git.

Dependencies are installed using:

```bash
python -m pip install -r requirements.txt
```

Tests are executed with:

```bash
python -m pytest
```

Code formatting is checked with:

```bash
black --check .
```

Static analysis is performed with:

```bash
ruff check .
```

## 13. Version Control Strategy

Git is used for source control.

The project follows incremental commits representing meaningful development milestones.

Examples of meaningful commit types include:

text
Add duplicate detection
Add execution logging
Add automated tests for core file logic
Update project documentation


Small formatting changes or temporary debugging changes should generally be grouped into the relevant feature commit rather than committed independently.

The main branch represents the stable version of the project.

---

## 14. Repository Hygiene

The repository should not contain generated or local-only files such as:

text
.venv/
__pycache__/
.pytest_cache/
*.pyc


These files are excluded through `.gitignore`.

The repository should contain source code, tests, documentation, configuration, and other files necessary to reproduce the project.

---

## 15. Current Project Status

### Completed

* [x] Modular project structure
* [x] File scanning
* [x] Folder validation
* [x] File categorization
* [x] Automatic folder creation
* [x] File movement
* [x] Filename conflict handling
* [x] Automatic unique filename generation
* [x] Duplicate detection using SHA-256
* [x] Dedicated duplicate folder
* [x] Hidden file exclusion
* [x] Log file exclusion
* [x] Execution summary
* [x] Execution time measurement
* [x] Operation logging
* [x] CLI argument parsing
* [x] `--help` support
* [x] Preview/dry-run functionality
* [x] File movement error handling
* [x] Python virtual environment
* [x] Automated unit tests
* [x] Integration testing
* [x] 26 passing tests
* [x] Black formatting
* [x] Ruff static analysis
* [x] README documentation

### Final Review

* [ ] Final review of README and PROJECT.md
* [ ] Final repository cleanup
* [ ] Final end-to-end application demonstration
* [ ] Optional GitHub Actions / CI setup


## 16. Future Improvements

The core project is considered functionally complete. The following improvements are optional future extensions:

### Recursive Scanning

Allow the application to process files inside nested directories.

### Configuration File

Allow users to customize categories and file extensions through a configuration file.

### Advanced CLI

Add additional command-line options such as:

```text
--verbose
--recursive
--version
```

### Continuous Integration

Add GitHub Actions to automatically execute tests and code quality checks when changes are pushed to the repository.

### Packaging

Package the application as an installable command-line application.

### Performance Improvements

Optimize processing for directories containing very large numbers of files.

## 17. Design Principles

The project follows several important software engineering principles.

### Separation of Concerns

Each module has a focused responsibility.

### Single Responsibility

Functions and modules should avoid performing unrelated tasks.

### Reusability

Core operations such as scanning, categorization, hashing, and file movement are implemented independently so they can be tested and reused.

### Testability

File-system operations are designed to work with temporary directories, allowing automated tests without modifying real user files.

### Maintainability

Type hints, docstrings, modular design, and clear naming are used to make the code easier to understand and maintain.

---

## 18. Development Roadmap

The project evolved through the following development stages:

```text
Core functionality
       ↓
Modular architecture
       ↓
Duplicate detection
       ↓
Logging
       ↓
CLI functionality
       ↓
Preview / dry-run mode
       ↓
Automated unit testing
       ↓
Integration testing
       ↓
Filename conflict handling
       ↓
Error handling
       ↓
Code quality tooling
       ↓
Documentation
       ↓
Final project review
       ↓
Portfolio-ready release
```

The remaining work is focused primarily on final documentation review, repository cleanup, and optional continuous integration.

## 19. Definition of Done

The project is considered portfolio-ready when:

* [x] Core functionality works reliably.
* [x] Automated tests pass.
* [x] Integration tests cover the main workflow.
* [x] Documentation accurately reflects the implementation.
* [x] The repository contains no unnecessary generated files.
* [x] Dependencies are reproducible.
* [x] Code quality checks pass.
* [x] CLI behavior is documented.
* [x] README provides clear installation and usage instructions.
* [x] The project can be cloned and executed by another developer.
* [x] The repository history contains meaningful development milestones.

Optional future improvements such as GitHub Actions, recursive scanning, advanced CLI features, and packaging are not required for the current portfolio release.


## 20. Conclusion

Smart File Organizer demonstrates a practical Python application built with modular design, file-system automation, duplicate detection, logging, command-line functionality, automated testing, and version control.

The project is intentionally designed to evolve beyond a simple scripting exercise into a maintainable and portfolio-ready software project.




