# Mary Kay Tax Helper

A Python-based data processing project that helps organize and summarize business expense data for tax preparation and reporting.

## Project Overview

The Mary Kay Tax Helper reads expense data from a CSV file, validates and cleans the records, and generates summarized reports by expense category and month.

The goal of the project was to practice real-world Python data processing, validation, modular programming, and report generation using business expense data.

## Features

* Reads business expense data from CSV files
* Validates required fields
* Validates date formats and numeric expense amounts
* Identifies missing vendor information
* Checks expense categories and generates category warnings
* Separates Mary Kay business expenses from other business expenses
* Calculates expense totals by category
* Calculates expense totals by month
* Exports summarized reports as CSV files
* Uses a modular Python project structure

## Technologies Used

* Python
* CSV file processing
* Python modules and packages
* Data validation
* Exception handling
* Command-line arguments
* Git and GitHub

## Project Structure

```text
mk_tax_helper/
│
├── data/
│   └── sample_expenses.csv
│
├── src/
│   └── mk_tax/
│       ├── io_csv.py
│       ├── models.py
│       ├── validate.py
│       ├── reports.py
│       └── main.py
│
├── out/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Data Privacy

The repository does not contain actual personal or business financial data. Sample data is used for demonstration purposes only.

## Example Output

The application can generate reports such as:

* Expenses summarized by category
* Expenses summarized by month
* Mary Kay-specific business expense totals
* Overall business expense totals

Example output files:

```text
2025_mary_kay_by_category.csv
2025_mary_kay_by_month.csv
```

## What I Practiced

This project provided hands-on experience with:

* Building a Python data-processing workflow
* Organizing code into reusable modules
* Validating and cleaning incoming data
* Applying business rules to real-world data
* Transforming raw transaction data into summarized reporting outputs
* Working with file input and output
* Using Git and GitHub for version control

## Future Improvements

Potential enhancements include:

* Add automated unit testing with pytest
* Add PostgreSQL database integration
* Improve error logging and exception handling
* Create additional reporting and visualization options
* Develop an API or simple user interface
