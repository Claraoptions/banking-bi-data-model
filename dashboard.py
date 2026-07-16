import os
from pathlib import Path
os.chdir(Path(__file__).parent)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Banking BI Dashboard",
    page_icon="🏦",
    layout="wide"
)

# ── Load query outputs ────────────────────────────────────
q1 = pd.read_csv("query1_monthly_kpis.csv")
q2 = pd.read_csv("query2_branch_ranking.csv")
q3 = pd.read_csv("query3_product_penetration.csv")
q4 = pd.read_csv("query4_mom_growth.csv")
q5 = pd.read_csv("query5_top_customers_by_branch.csv")

# ── Header ────────────────────────────────────────────────
st.title("🏦 Banking BI Information System")
st.markdown("**Commercial Performance Dashboard | Clara Mujuni**")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────
total_volume = q1['total_volume_ugx_m'].sum()
total_txns   = int(q1['total_transactions'].sum())
avg_monthly  = q1['total_volume_ugx_m'].mean()
best_branch  = q2[q2['year'] == 2024].sort_values('total_volume_ugx_m', ascending=False).iloc[0]['branch_name']

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Volume (3 Years)",   f"UGX {total_volume:,.0f}M")
col2.metric("Total Transactions",        f"{total_txns:,}")
col3.metric("Avg Monthly Volume",        f"UGX {avg_monthly:,.0f}M")
col4.metric("Top Branch (2024)",         best_branch)

st.divider()

# ── Row 1: Monthly volume trend + MoM growth ──────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Monthly Transaction Volume (UGX M)")
    q1['period'] = q1['year'].astype(str) + "-" + q1['month'].astype(str).str.zfill(2)
    fig1 = px.line(
        q1, x='period', y='total_volume_ugx_m',
        markers=True,
        labels={'period': 'Month', 'total_volume_ugx_m': 'Volume (UGX M)'}
    )
    fig1.update_traces(line_color='#1F4E79', line_width=2)
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Month-on-Month Growth (%)")
    q4_clean = q4.dropna(subset=['mom_growth_pct']).copy()
    q4_clean['period'] = q4_clean['year'].astype(str) + "-" + q4_clean['month'].astype(str).str.zfill(2)
    q4_clean['colour'] = q4_clean['mom_growth_pct'].apply(lambda x: 'positive' if x >= 0 else 'negative')
    fig2 = px.bar(
        q4_clean, x='period', y='mom_growth_pct',
        color='colour',
        color_discrete_map={'positive': '#2ecc71', 'negative': '#e74c3c'},
        labels={'period': 'Month', 'mom_growth_pct': 'MoM Growth (%)'}
    )
    fig2.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Row 2: Branch ranking + Product penetration ───────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Branch Volume Ranking by Year")
    year_filter = st.selectbox("Select Year", sorted(q2['year'].unique(), reverse=True))
    q2_filtered = q2[q2['year'] == year_filter].sort_values('total_volume_ugx_m', ascending=True)
    fig3 = px.bar(
        q2_filtered,
        x='total_volume_ugx_m', y='branch_name',
        orientation='h',
        color='region',
        text='volume_rank',
        labels={'total_volume_ugx_m': 'Volume (UGX M)', 'branch_name': 'Branch'}
    )
    fig3.update_traces(textposition='inside')
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("Product Penetration by Customer Segment")
    fig4 = px.bar(
        q3.sort_values('total_segment_value_ugx_m', ascending=False),
        x='segment', y='total_segment_value_ugx_m',
        color='avg_products_held',
        color_continuous_scale='Blues',
        text='customers',
        labels={
            'segment': 'Segment',
            'total_segment_value_ugx_m': 'Total Value (UGX M)',
            'avg_products_held': 'Avg Products Held'
        }
    )
    fig4.update_traces(textposition='outside')
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Row 3: Loan vs Deposit split + Top customers ──────────
col_left3, col_right3 = st.columns(2)

with col_left3:
    st.subheader("Loan vs Deposit Volume by Month")
    q1['period'] = q1['year'].astype(str) + "-" + q1['month'].astype(str).str.zfill(2)
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=q1['period'], y=q1['loan_volume_ugx_m'],
        name='Loan Volume', fill='tonexty',
        line=dict(color='#e74c3c')
    ))
    fig5.add_trace(go.Scatter(
        x=q1['period'], y=q1['deposit_volume_ugx_m'],
        name='Deposit Volume', fill='tozeroy',
        line=dict(color='#2ecc71')
    ))
    fig5.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig5, use_container_width=True)

with col_right3:
    st.subheader("Top Customers by Branch")
    branch_filter = st.selectbox("Select Branch", sorted(q5['branch_name'].unique()))
    q5_filtered = q5[q5['branch_name'] == branch_filter][
        ['branch_rank', 'customer_id', 'segment', 'total_volume_ugx_m', 'txn_count']
    ].rename(columns={
        'branch_rank': 'Rank',
        'customer_id': 'Customer',
        'segment': 'Segment',
        'total_volume_ugx_m': 'Volume (UGX M)',
        'txn_count': 'Transactions'
    })
    st.dataframe(q5_filtered, hide_index=True, use_container_width=True)

st.divider()
st.caption("Data: Synthetic banking data | Stack: DuckDB · Python · Streamlit · Plotly")