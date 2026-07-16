# Banking BI Data Model & Reporting IS
***Ayebazibwe Clare Mujuni | Banking Data Analyst Portfolio**

---

## Business Problem

Banks generate millions of transactions daily across branches, products
and customer segments. The core banking system records these accurately
but is poorly suited for analytical queries — asking "which branch grew
fastest in Q3?" requires scanning millions of rows across multiple tables.

This project builds a complete BI Information System: a star schema
data model populated via an ETL pipeline, with five advanced analytical
SQL queries and an interactive Streamlit dashboard on top.

---

## Architecture
dim_date
                   │
                   dim_branch ──── fact_transactions ──── dim_product
│
dim_account ──── dim_customer

**Fact table:** `fact_transactions` — 20,000 transactions across 3 years  
**Dimensions:** date, branch, product, customer, account

**Why a star schema?**  
Analytical queries become fast and readable — filtering by branch, product,
or time period is a simple JOIN rather than a complex subquery across a
normalised transactional schema. This is the standard design pattern used
in banking BI teams worldwide (Kimball dimensional modelling).

---

## Stack

| Layer | Technology |
|---|---|
| Analytical database | DuckDB (embedded OLAP engine) |
| ETL pipeline | Python + Pandas |
| SQL | DuckDB SQL (CTEs, window functions, RANK, LAG) |
| Dashboard | Streamlit + Plotly |

---

## Five Analytical SQL Queries

| Query | Technique | Business Purpose |
|---|---|---|
| Monthly Commercial KPIs | GROUP BY, CASE WHEN | Monthly scorecard: volume, transactions, loan vs deposit split |
| Branch Performance Ranking | CTE + RANK() + LAG() | Annual branch ranking with YoY change |
| Product Penetration by Segment | Multi-level CTE | Cross-sell depth and segment value |
| Month-on-Month Growth | LAG() window function | Trend analysis and growth rate calculation |
| Top Customers by Branch | RANK() with PARTITION BY | Relationship manager priority list per branch |

---

## Key Findings

**UGX 40B** total transaction volume across 3 years and 6 branches

**Mbarara** topped branch rankings in 2024 — the Western Uganda region
outperforming Central branches despite lower population density

**"Lost" customers hold the highest total segment value (UGX 9.1B)** —
they were not low-value customers, they were poorly retained.
Strong case for a targeted win-back campaign before full attrition.

**Kampala Main's top 3 customers are all "At Risk"** with volumes
between UGX 124M–163M — an immediate commercial alert requiring
urgent relationship manager intervention.

**December consistently shows the strongest MoM growth** — driven by
year-end salary payments, business settlements and seasonal spending.
A predictable pattern useful for branch staffing and liquidity planning.

---

## Dashboard

Interactive Streamlit dashboard with:
- KPI summary cards (total volume, transactions, top branch)
- Monthly volume trend line chart
- Month-on-month growth bar chart (green/red)
- Branch ranking by year (filterable)
- Product penetration by customer segment
- Loan vs deposit volume split
- Top customers by branch (filterable)

---

## How to Run

```bash
pip install -r requirements.txt
python 01_star_schema.ipynb   # or run notebook cells in order
streamlit run dashboard.py
```

---

## Author

**Ayebazibwe Clare Mujuni**  
20 years banking experience across Branch Management, Credit Risk, and Internal Audit  
[GitHub](https://github.com/Claraoptions) | mujuniclare@gmail.com