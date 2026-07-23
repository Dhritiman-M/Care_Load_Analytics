# System Capacity & Care Load Analytics for Unaccompanied Children

## Project Overview

The Unaccompanied Alien Children (UAC) Program is a federally mandated initiative that supports children transferred from U.S. Customs and Border Protection (CBP) custody into Department of Health and Human Services (HHS) care facilities.

This project provides a comprehensive analytics and forecasting framework for monitoring system capacity, care load, backlog accumulation, and operational stress across the UAC care pipeline.

The solution combines healthcare analytics, time-series forecasting, and interactive visualization through a Streamlit dashboard.

---

## Problem Statement

The UAC program continuously receives children into care while simultaneously discharging children to approved sponsors.

Without structured analytics, decision makers face challenges in:

* Monitoring total system load
* Identifying capacity strain periods
* Tracking inflow vs outflow balance
* Planning shelter and staffing resources
* Forecasting future care demand

This project addresses these challenges through data-driven monitoring and forecasting.

---

## Objectives

### Primary Objectives

* Quantify daily and cumulative care load
* Identify periods of system stress and relief
* Measure balance between intake, transfers, and discharges

### Secondary Objectives

* Support healthcare staffing decisions
* Improve shelter capacity planning
* Provide operational awareness
* Enable evidence-based policy evaluation

---

## Dataset Description

The dataset contains daily operational records from the UAC care system.

| Column                                         | Description                   |
| ---------------------------------------------- | ----------------------------- |
| Date                                           | Reporting date                |
| Children apprehended and placed in CBP custody | Daily intake volume           |
| Children in CBP custody                        | Active CBP care load          |
| Children transferred out of CBP custody        | Flow into HHS system          |
| Children in HHS Care                           | Active HHS care load          |
| Children discharged from HHS Care              | Successful sponsor placements |

---

## Project Architecture

```
UAC_Care_Load_Analytics/
├── dashboard/
│   ├── __init__.py
│   └── streamlit_app.py
├── data/
│   └── HHS_Unaccompanied_Alien_Children_Program.csv
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── feature_engineering.py
│   ├── forecasting.py
│   ├── preprocessing.py
│   ├── trend_analysis.py
│   └── validation.py
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```


---
## Key Metrics

| Metric                  | Description                                         |
|------------------------:|:----------------------------------------------------|
| Total System Load       | CBP Custody + HHS Care                              |
| Net Daily Intake        | Transfers into HHS − Discharges from HHS            |
| Care Load Growth Rate   | Daily percentage change in total system load        |
| Backlog Indicator       | Cumulative net intake over time                     | 
| Discharge Offset Ratio  | Discharges ÷ Transfers                              |
| Volatility Index        | 7-day rolling standard deviation of system load     |

---

## Dashboard Modules

### 1. System Load Overview

* Total care load trends
* Daily, weekly, monthly analysis

### 2. CBP vs HHS Comparison

* Comparative care burden
* Resource allocation insights

### 3. Net Intake & Backlog Analysis

* Inflow vs outflow balance
* Backlog accumulation monitoring

### 4. Stress Monitoring

* 7-Day rolling average
* 14-Day rolling average
* Stress and relief period detection

### 5. Temporal Analysis

* Monthly trends
* Weekly trends
* Early vs late timeline comparison

### 6. Forecasting

* Prophet forecasting model
* 30-Day future projection
* Confidence intervals

---

## Forecasting Methodology

The forecasting module uses Facebook Prophet.

Features:

* Yearly seasonality
* Weekly seasonality
* Trend decomposition
* Confidence interval estimation

Forecast targets:

* Total System Load
* HHS Care Load
* CBP Care Load

---

## Data Validation

The system automatically validates:

To ensure data quality and integrity, the pipeline performs automated validation checks before analysis and forecasting. Validation results are reported with clear error messages and summary statistics.

Key validation rules

- Constraint 1 — Transfers must not exceed CBP custody counts
	- Condition: Transfers ≤ Children in CBP custody
	- Action on violation: flag record and report daily totals that break the rule

- Constraint 2 — Discharges must not exceed HHS care counts
	- Condition: Discharges ≤ Children in HHS Care
	- Action on violation: flag record and exclude from aggregate metrics until resolved

Additional integrity checks

- Missing dates: detect gaps in the daily time series and optionally impute or flag
- Duplicate dates: identify duplicate rows for the same date and resolve by aggregation or manual review
- Reporting anomalies: large sudden increases/decreases beyond expected volatility are flagged for inspection

Validation output

- A summary report listing constraint violations and anomalies
- Daily and cumulative counts of flagged records
- Optionally a cleaned dataset produced after automated or manual remediation

---

## Installation

### Clone Repository

```bash
git clone <repository_url>
cd UAC_Care_Load_Analytics
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

---

## Expected Outcomes

The dashboard enables stakeholders to:

* Monitor capacity utilization
* Detect operational stress
* Assess backlog growth
* Forecast future demand
* Support staffing decisions
* Improve resource allocation

---

## Future Enhancements

* Advanced forecasting models
* Automated alerting system
* Real-time data integration
* Scenario simulation
* Resource optimization models

---

## Author

Healthcare Analytics Project

System Capacity & Care Load Analytics for Unaccompanied Children
