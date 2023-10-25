# API-CryptoCurrency

[![Author](https://img.shields.io/badge/Author-Matheus%20Monteiro-red)](https://www.linkedin.com/in/matheus-monteiro)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

The **API-CryptoCurrency** project is designed to facilitate access to the API of Mercado Bitcoin, a prominent Brazilian cryptocurrency broker. This project empowers you to retrieve trade data and daily summaries for various cryptocurrencies. It is implemented in Python using Object-Oriented Programming (OOP) principles for a clean and structured codebase.

In addition to the core functionality, the project has plans for future enhancements, including integration with Amazon Web Services (AWS). This will involve uploading data files to AWS S3 using Lambda scripts and populating Athena, making data analysis more efficient and accessible.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Classes](#classes)
- [Contributing](#contributing)
- [Contact](#contributing)
- [License](#license)

# Installation

To get started with this project, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/mmont9594/API-CryptoCurrency.git

2. Navigate to the project directory:

   ```bash
   cd API-CryptoCurrency

3. Install the required libraries by running:

   ```bash
   pip install -r requirements.txt

# Usage

Mercado Bitcoin API Configuration

Before you use this project, you can look in the API Docs for more information about the structure. 
Please access these steps: 

[Click here to visit the Mercado Bitcoin API Docs](https://www.mercadobitcoin.com.br/termo-de-uso-apis)

# Classes

## Using the Project

The project is organized into several classes, each serving a specific purpose. Here is a brief description of the classes:

#### 1. ingestor.py
Description: The ingestor.py file is responsible for ingesting data from Mercado Bitcoin's API. It contains classes and functions for fetching, processing and transforming data.

#### 2. apis.py
Description: The apis.py file includes classes interacting with Mercado Bitcoin's API. These classes are used to make API requests and receive cryptocurrency trade and daily summary data.

#### 3. main.py
Description: The main.py file serves as the entry point for the project. It orchestrates the entire data capture and processing process, invoking methods from the other files to collect and handle data.

#### 4. writers.py
Description: The writers.py file is responsible for writing or storing data. It contains classes and functions for saving data, such as trade data and daily summaries, to various storage solutions, like databases or files.

## Example:

Here's an example of how to use the project to retrieve day summary data for the BTC, ETH, LTC cryptocurrency information:

  ```python
  # Import the Libraries
  import datetime
  from ingestor import DaySummaryIngestor
  from writers import DataWriter

  # Initialize the Day Summary Class from Mercado Bitcoin API with the parameters and create an Object
  if __name__ == "__main__":
      day_summary_ingestor = DaySummaryIngestor(
          writer=DataWriter,  
          coins=["BTC", "ETH", "LTC"],  
          default_start_date=datetime.date(2023, 1, 1)
          )

  # Create function to run the job
  def job():
      day_summary_ingestor.ingest()

  # Get recent day summary information
  job()
```
# Contributing

If you would like to contribute to this project, please open an issue, fork the repository, and submit a pull request with your changes.

# Contact

### Feel free to contact me:

**Matheus Monteiro**
- LinkedIn: [Matheus Monteiro](https://www.linkedin.com/in/matheus-monteiro/)
