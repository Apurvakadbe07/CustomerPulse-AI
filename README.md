# CustomerPulse AI

## Customer Churn Analysis & Retention Intelligence Platform

CustomerPulse AI is a customer analytics project built using the Olist Brazilian E-Commerce Dataset. It examines customer purchasing behaviour, customer value, churn risk, and revenue exposure, and uses these findings to support retention analysis.

The project covers the complete analytical process from data preparation and Customer 360 development to SQL analysis, customer segmentation, churn prediction, revenue risk assessment, and business reporting.

---

## Business Problem

Customer information in an e-commerce business is distributed across multiple sources such as customers, orders, payments, products, sellers, reviews, and delivery records.

Analysing these sources independently makes it difficult to answer important business questions:

- Which customers are at higher risk of churn?
- What is the value of these customers?
- How much revenue is associated with customers at risk?
- Which customers should receive greater retention attention?
- How can customer data be used to support retention decisions?

CustomerPulse AI addresses these questions by bringing customer behaviour, value, churn risk, and revenue exposure together at the customer level.

---

## Project Goal

The goal of the project is to develop a customer-level analytical framework that can be used to understand customer behaviour, identify churn risk, evaluate business exposure, and support retention prioritisation.

The project focuses on:

- Building a reliable Customer 360 dataset
- Understanding customer purchasing behaviour
- Analysing customer value
- Segmenting customers based on behaviour
- Predicting churn risk
- Measuring revenue exposure
- Prioritising customers for retention analysis
- Presenting the findings through interactive business dashboards

---

## Key Results

The project produces verified analytical outputs covering:

- Customer-level churn prediction
- Churn probability
- Risk segmentation
- Customer value tiers
- Revenue-at-risk analysis
- Retention recommendations
- Customer priorities
- Customer action planning

> Project metrics are based on the final validated datasets and model outputs included in the repository.

---

## Dataset

### Source

**Olist Brazilian E-Commerce Dataset**

The dataset contains information related to:

- Customers
- Orders
- Order items
- Payments
- Products
- Sellers
- Reviews

The original Olist datasets used for this project are included in the repository under:

1 data/01_raw_data/

Processed and project-generated datasets are available under:

1 data/02_processed data/
1 data/03_analysis/.

### Key Customer-Level Features

The Customer 360 dataset contains information related to:

- Customer profile
- Purchasing behaviour
- Spending
- Purchase frequency
- Customer tenure
- Reviews
- Delivery experience
- Payment behaviour
- Customer value
- Churn-related features
- Risk information
- Retention outputs

---

## Analytical Approach

### 1. Data Understanding

The Olist datasets were examined individually to understand their structure, relationships, data types, and data quality.

### 2. Data Cleaning & Validation

The datasets were cleaned and validated before being used for analysis.

This included:

- Missing-value analysis
- Duplicate checks
- Data type validation
- Data cleaning
- Dataset integration
- Final validation

### 3. Customer 360

Relevant customer and transaction information was consolidated into a customer-level dataset.

This created a single analytical view combining purchasing behaviour, spending, frequency, tenure, reviews, delivery experience, payments, and customer value.

### 4. Exploratory Data Analysis

EDA was performed to understand customer behaviour and identify patterns related to:

- Spending
- Purchase frequency
- Customer value
- Customer tenure
- Reviews
- Delivery experience
- Churn-related features

### 5. SQL Business Analysis

PostgreSQL was used to analyse the Customer 360 dataset through 20 business-focused SQL queries.

The analysis covers:

- Overall business health and customer performance
- Customer value tier performance and risk
- State-wise revenue and customer risk
- Monthly revenue and customer acquisition
- Pareto revenue analysis
- High-spending customers with low purchase frequency
- Customer Lifetime Value by value tier
- Early identification of at-risk customers
- Inactive repeat customers
- High Average Order Value and low-frequency customers
- Repeat purchase rate by customer value tier
- Impact of delivery delay on customer risk
- Review score, repeat purchase behaviour, and customer risk
- State-wise cancellation rate and customer satisfaction
- Overall customer risk distribution
- Factors associated with at-risk customers
- Revenue associated with at-risk customers
- High-risk VIP and high-spending customers
- SQL-based customer risk scoring
- Retention priority analysis

The SQL analysis connects customer behaviour, customer value, customer experience, risk, and revenue exposure to support business-focused retention analysis.

### 6. RFM Segmentation

RFM analysis was performed using:

**Recency | Frequency | Monetary Value**

This provided a behavioural and monetary view of customers based on their purchasing activity.

### 7. Churn Prediction

Four classification models were developed and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

The selected model generates customer-level churn predictions, probability scores, and risk segments.

### 8. Revenue Risk & Retention Analysis

Churn results were combined with customer value and revenue information to assess business exposure.

The retention analysis follows:

**Churn Risk → Customer Value → Revenue Risk → Retention Recommendation → Priority**

This connects the prediction output with business context instead of treating churn prediction as a standalone model.

---
## Power BI Dashboard

A Power BI dashboard was developed to present the analysis in a business-focused format.

The dashboard covers:

- Executive customer and revenue overview
- Customer churn intelligence
- Churn risk and risk segmentation
- Customer value and revenue analysis
- Revenue at risk
- Retention recommendations
- Model performance and business impact

The dashboard is designed to help review customer risk, business exposure, and retention priorities from a single interface.

## Key Insights

- **71.13%** of customers were classified under the churn flag, highlighting significant churn exposure.
- **68,352 customers** were identified as at-risk, with **11.26M** in revenue at risk.
- **High-value customers contributed 10.88M in revenue**, making customer value an important factor in retention analysis.
- The churn prediction model achieved **77.10% Accuracy, 77.46% Precision, 95.62% Recall, 85.59% F1 Score, and 78.15% ROC-AUC**.
- Risk segmentation was used to identify customer groups requiring different levels of retention attention.
---

## Visualizations & Screenshots

### Power BI Dashboard

The Power BI dashboard presents the major findings through multiple analytical pages.

#### Customer Analytics Overview

![Customer Analytics Dashboard](assets/page%201%20dashboard.png)

#### Customer Churn Intelligence

![Customer Churn Dashboard](assets/page%202%20%20dashboard.png)

#### AI-Powered Retention Intelligence
![Retension Dashboard](assets/page%203%20dashboard.png)

The dashboard covers customer and revenue analysis, churn intelligence, risk segmentation, customer value, revenue risk, retention analysis, and model performance.

---

## Streamlit Application

A multi-page Streamlit application was developed to provide an interactive interface for the project.

The application includes:

- Project Overview
- Dataset & Data Preparation
- Data Understanding
- Data Cleaning & Preprocessing
- Customer 360 Intelligence
- Exploratory Data Analysis
- SQL Business Analysis
- Customer Segmentation & RFM Analysis
- Customer Churn Intelligence & Revenue Risk
- Retention Recommendation
- Final Project Report
- Project Conclusion & Future Scope

---

Olist E-Commerce Dataset
          ↓
Data Understanding
          ↓
Data Cleaning & Validation
          ↓
Customer 360
          ↓
Exploratory Data Analysis
          ↓
SQL Business Analysis
          ↓
RFM Segmentation
          ↓
Churn Prediction
          ↓
Customer Risk & Revenue Analysis
          ↓
Retention Analysis
          ↓
Power BI & Streamlit