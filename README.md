# Stock Market Analysis

[![Python Version](https://img.shields.io/badge/python-3.7.12-brightgreen.svg)](https://python.org)

## Table of Contents

* [Project Goal](#project-goal)
* [Running the Project Locally](#running-the-project-locally)
* [Key Features](#key-features)
* [Todo](#todo)
* [License](#license)

## Project Goal

Make life easier by automating stock market analysis.

## Running the Project Locally

1. First, clone the repository to your local machine and cd into the project directory:

```bash
git clone https://github.com/Akshat-Jain/stock-market-analysis.git
cd stock-market-analysis
```

2. Build Docker image from Dockerfile:

```bash
docker build . -t stock-market-analysis
```

Run the above command whenever you make some change in the source code files for it to reflect in the Docker container.

3. Create and run container from the image:

```bash
docker run stock-market-analysis
```

## Key Features

1. Strategy 1: Detect stocks with MACD bullish crossover on last trading day with good RSI value and report them to us.
2. Basic mailing service to send the output to specified list of emails in tabular format.

## Todo:

1. Take holidays into account. Currently the program doesn't work if the last trading day was a holiday.
2. Strategy 2: Detect stocks with MACD bullish crossover on last to last trading day, and check if it showed strength last day. Report such stocks along with corresponding RSI value.
3. Strategy 3: For huge / custom list of companies like RELIANCE, TCS, INFOSYS, etc, report their today's change. Maybe think about some better strategy for these later.
4. Integrate mailing service to mail us the outputs of the program.
    - For all the stocks in output, plot and save graphs (with MACD and RSI and volume) and attach them in the mail.
5. Minor enhancements:
    - Add respective volume in the output as well.
    - Code needs a serious refactoring.
6. Deploy and enjoy.
7. Maybe:
    - Push Docker image to Docker Hub.

## License

The source code is released under the [MIT License](https://github.com/Akshat-Jain/stock-market-analysis/blob/main/LICENSE).