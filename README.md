# BI-Mini-Project
# BI Mini Project — Flight Data Dashboard

##  Overview
This project analyzes flight performance data using a combination of KPIs and business questions.  
The dashboard provides insights into delays, cancellations, airport performance, airline behavior, and traffic patterns.

The goal is to present a clear, interactive, and defendable BI dashboard using SQL and Metabase.

---

##  Key Performance Indicators (KPIs)

### 1. Ratio Between Cancelled Flights and Airlines  
Percentage of flights cancelled per airline. This was visualised with a line chart comapring cancelation ratio across airline codes. 

### 2. Ratio Between Delayed Flights and Airlines  
Percentage of delayed flights per airline. Displayed as abar chart for easy comparison. 

### 3. Ratio Between Delayed Flights and Destination Airports  
Percentage of delayed flights per destination airport. Visualised as a bar chart (Top 10 airports)

### 4. Ratio Between Delayed Flights and Departure Airports  
Percentage of delayed flights per departure airport. Displayed as a line chart (Top 10 airports)

### 5. Custom KPI — Net Passenger Flow Leader  
Airport with the highest net inflow of flights (arrivals minus departures). PHX is the airport with highest net inflow

---

##  Tasks / Business Questions

### 1. Five Most Popular Flight Connections  
Top origin–destination pairs by total flights. Arow chart was used to show this display
SFO - LAX
LAX - SFO
LAX - LAS
LAS - LAX
LAX - PHX

### 2. Ten Most Often Cancelled Flights  
Routes with the highest cancellation counts. Visualised with a waterfall chart

### 3. Busiest Days in the Year  
Daily flight volume visualised over time represented on a line chart

### 4. Busiest Weeks in the Year  
Weekly flight volume visualised over time visulaised on a bar chart

### 5. Custom Task  
Which airline operated the most flights in a given year say 2007, visualised on a flannel

---

##  Dashboard Layout

###  KPI Row  
A row of single-number KPIs summarising overall performance with charts below respective kpi

###  Task Section  
Charts answering each business question.


---

## Tools Used
- SQL  
- Metabase  
- Docker Desktop
- GitHub  

---

## Visuals 
<img width="1126" height="1465" alt="image" src="https://github.com/user-attachments/assets/c52c45df-bb1d-40e5-86f0-1cc7ef2f9e33" />



---

## Repository Structure
/sql
   kpi_queries.sql
   task_queries.sql
README.md

# Author
Keith Emanzi
BI Mini Project - 2026

