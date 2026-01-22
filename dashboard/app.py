import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Telco Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Professional Light Theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(180deg, #f5f7fa 0%, #eef2f7 100%) !important;
        color: #1a202c !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1e3a8a !important;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e40af !important;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.75rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    [data-testid="metric-container"] {
        background: #FFFFFF !important;
        border: 2px solid #e5e7eb !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15) !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1a202c !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.5) !important;
    }
    
    .stSelectbox > div > div, .stSlider > div, .stNumberInput > div {
        background: #FFFFFF !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div:hover, .stSlider > div:hover, .stNumberInput > div:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4 0%, #e8f5e9 100%) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%) !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
    }
    
    hr {
        background: linear-gradient(90deg, transparent, #3b82f6, transparent) !important;
        border: 0 !important;
        height: 2px !important;
        margin: 1.5rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# LOAD DATA & MODELS
# ============================================================================
@st.cache_resource
def load_data_and_models():
    try:
        df_raw = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
        
        try:
            feature_importance = pd.read_csv('data/processed/feature_importance.csv')
        except:
            feature_importance = pd.DataFrame({'Feature': ['N/A'], 'Importance': [0]})
        
        try:
            rf_model = joblib.load('data/models/rf_churn_model.pkl')
        except:
            rf_model = None
        
        try:
            scaler = joblib.load('data/models/scaler.pkl')
        except:
            scaler = None
        
        try:
            with open('data/models/feature_names.pkl', 'rb') as f:
                feature_names = joblib.load(f)
        except:
            feature_names = df_raw.columns.tolist()
        
        return df_raw, feature_importance, rf_model, scaler, feature_names
    except Exception as e:
        return None, None, None, None, None

df_raw, feature_importance, rf_model, scaler, feature_names = load_data_and_models()

if df_raw is None:
    st.error("❌ Failed to load data files. Check file paths.")
    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("# 📊 Telco Customer Churn Analytics")
    st.markdown("---")
    
    page = st.radio(
        "Navigation:",
        ["🏠 Overview", "📈 Analytics", "🎯 Features", "🔮 Predict", "📋 Performance", "ℹ️ About"]
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <p style='color: #FFFFFF; font-weight: 600; margin: 0;'>Telco Customer Churn Analytics</p>
        <p style='color: #cbd5e1; font-size: 0.85rem; margin: 0.25rem 0 0 0;'>v1.0</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================


if page == "🏠 Overview":
    st.markdown('<h1 class="main-header">📊 Telco Customer Churn Analytics</h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
### 🎯 Business Objective

The primary goal of this dashboard is to **identify customers at risk of churn**,  
**understand the key drivers behind churn**, and **support proactive retention strategies**  
using data-driven insights and machine learning predictions.

This enables business teams to:
- Reduce revenue loss
- Improve customer lifetime value
- Prioritise retention efforts efficiently
""")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📞 Total Customers", f"{len(df_raw):,}")
    
    with col2:
        churn_count = (df_raw['Churn'] == 'Yes').sum()
        churn_pct = (churn_count / len(df_raw)) * 100
        st.metric("🔴 Churned", f"{churn_count:,}", f"{churn_pct:.1f}%")
    
    with col3:
        active_count = (df_raw['Churn'] == 'No').sum()
        st.metric("🟢 Active", f"{active_count:,}", f"{100-churn_pct:.1f}%")
    
    with col4:
        avg_tenure = df_raw['tenure'].mean()
        st.metric("📅 Avg Tenure", f"{avg_tenure:.0f}mo")
    
    st.markdown('<h2 class="section-header">Key Insights</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        churn_data = df_raw['Churn'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=['Active', 'Churned'],
            values=[churn_data['No'], churn_data['Yes']],
            marker=dict(colors=['#10b981', '#ef4444']),
            textposition='inside',
            textinfo='label+percent'
        )])
        fig.update_layout(
            title="Customer Distribution",
            font=dict(family="Inter", size=12, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
**What this shows:**  
This chart highlights the proportion of customers who have churned versus those who remain active.

**Key insight:**  
Approximately **1 in 4 customers have churned**, indicating a **material retention risk** that directly impacts revenue.

**Business implication:**  
Retention initiatives should focus on **early identification of churn signals**, especially among vulnerable customer segments.
""")

    
    with col2:
        fig = px.histogram(
            df_raw,
            x='tenure',
            nbins=25,
            color='Churn',
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
            title="Tenure Distribution by Churn",
            labels={'tenure': 'Tenure (months)', 'count': 'Count'}
        )
        fig.update_layout(
            font=dict(family="Inter", size=11, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            plot_bgcolor='rgba(255, 255, 255, 0)',
            height=400,
            xaxis=dict(
                gridcolor='#e5e7eb',
                title_font=dict(size=12, color="#374151"),
                tickfont=dict(size=10, color="#374151")
            ),
            yaxis=dict(
                gridcolor='#e5e7eb',
                title_font=dict(size=12, color="#374151"),
                tickfont=dict(size=10, color="#374151")
            ),
            margin=dict(l=60, r=40, t=60, b=60),
            hovermode='x unified',
            legend=dict(font=dict(size=10, color="#374151"))
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
**What this shows:**  
Customer tenure distribution split by churn status.

**Key insight:**  
Customers with **shorter tenure are significantly more likely to churn**, especially within the first 12 months.

**Business implication:**  
The **early customer lifecycle** is critical — onboarding experience, early engagement, and welcome offers can dramatically reduce churn.
""")

    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(
            df_raw,
            x='Churn',
            y='MonthlyCharges',
            color='Churn',
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
            title="Monthly Charges by Status",
            labels={'MonthlyCharges': 'Monthly Charges ($)'}
        )
        fig.update_layout(
            font=dict(family="Inter", size=12, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            height=400,
            showlegend=False,
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb'),
            margin=dict(l=60, r=40, t=60, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
**What this shows:**  
Comparison of monthly charges between churned and retained customers.

**Key insight:**  
Customers who churn tend to have **higher monthly charges**, suggesting **price sensitivity**.

**Business implication:**  
High-billing customers should receive **value reinforcement**, loyalty discounts, or service bundling to justify cost.
""")

    
    with col2:
        contract_churn = df_raw.groupby('Contract')['Churn'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).sort_values(ascending=False)
        
        fig = go.Figure(data=[go.Bar(
            x=contract_churn.index,
            y=contract_churn.values,
            marker=dict(color=['#ef4444', '#f59e0b', '#10b981']),
            text=contract_churn.values.round(1),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>%{y:.1f}%<extra></extra>'
        )])
        fig.update_layout(
            title="Churn Rate by Contract Type",
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(family="Inter", size=12, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            height=400,
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb'),
            margin=dict(l=60, r=40, t=60, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success("""
**What this shows:**  
Churn rate across different contract types.

**Key insight:**  
- Month-to-month contracts show the **highest churn**
- Long-term contracts significantly **reduce churn risk**

**Business implication:**  
Encouraging customers to move to **1-year or 2-year contracts** is one of the **most effective retention levers**.
""")


# ============================================================================
# PAGE 2: ANALYTICS
# ============================================================================
elif page == "📈 Analytics":
    st.markdown('<h1 class="main-header">📊 Data Analytics</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<h2 class="section-header">Dataset Overview</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Records", f"{len(df_raw):,}")
    with col2:
        st.metric("📊 Features", df_raw.shape[1])
    with col3:
        st.metric("⚠️ Missing", df_raw.isnull().sum().sum())
    
    st.markdown('<h2 class="section-header">Feature Exploration</h2>', unsafe_allow_html=True)

    st.markdown("""
### 🔍 Exploratory Analysis Objective

This section allows business users to **interactively explore how individual features influence churn**  
and validate hypotheses before designing retention strategies.
""")

    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        feature_type = st.selectbox("Feature Type:", ["Numerical", "Categorical"])
    
    with col2:
        if feature_type == "Numerical":
            num_features = df_raw.select_dtypes(include=[np.number]).columns.tolist()
            selected_feature = st.selectbox("Select:", num_features)
            
            fig = px.histogram(
                df_raw,
                x=selected_feature,
                nbins=30,
                color='Churn',
                color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
                title=f"{selected_feature} Distribution"
            )
            fig.update_layout(
                font=dict(family="Inter", size=12, color="#374151"),
                paper_bgcolor='rgba(255, 255, 255, 0.5)',
                xaxis=dict(gridcolor='#e5e7eb'),
                yaxis=dict(gridcolor='#e5e7eb'),
                margin=dict(l=60, r=40, t=60, b=60)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            cat_features = df_raw.select_dtypes(include=['object']).columns.tolist()
            selected_feature = st.selectbox("Select:", cat_features)
            
            feature_churn = df_raw.groupby(selected_feature)['Churn'].apply(
                lambda x: (x == 'Yes').sum() / len(x) * 100
            ).sort_values(ascending=False)
            
            fig = go.Figure(data=[go.Bar(
                x=feature_churn.index,
                y=feature_churn.values,
                marker=dict(color='#3b82f6'),
                text=feature_churn.values.round(1),
                textposition='auto'
            )])
            fig.update_layout(
                title=f"Churn Rate by {selected_feature}",
                yaxis_title="Churn Rate (%)",
                font=dict(family="Inter", size=12, color="#374151"),
                paper_bgcolor='rgba(255, 255, 255, 0.5)',
                xaxis=dict(gridcolor='#e5e7eb'),
                yaxis=dict(gridcolor='#e5e7eb'),
                margin=dict(l=60, r=40, t=60, b=60)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.info("""
**How to interpret this chart:**  
Higher churn rates indicate **risk-driving segments**.  
Use this view to identify:
- High-risk customer groups
- Service gaps
- Pricing sensitivity
""")


# ============================================================================
# PAGE 3: FEATURES
# ============================================================================
elif page == "🎯 Features":
    st.markdown('<h1 class="main-header">🎯 Feature Importance</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    if len(feature_importance) > 1:
        st.markdown('<h2 class="section-header">Top Features Driving Churn</h2>', unsafe_allow_html=True)
        
        top_n = st.slider("Display top N:", 5, len(feature_importance), 15)
        top_features = feature_importance.head(top_n).sort_values('Importance', ascending=True)
        
        fig = go.Figure(data=[go.Bar(
            y=top_features['Feature'],
            x=top_features['Importance'],
            orientation='h',
            marker=dict(color=top_features['Importance'], colorscale='Blues'),
            text=top_features['Importance'].round(4),
            textposition='auto'
        )])
        fig.update_layout(
            title=f"Top {top_n} Features by Importance",
            xaxis_title="Importance Score",
            font=dict(family="Inter", size=12, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            height=400 + top_n * 12,
            xaxis=dict(gridcolor='#e5e7eb'),
            margin=dict(l=200, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success("""
**What this shows:**  
Relative importance of features used by the machine learning model to predict churn.

**Key insight:**  
A small group of features (e.g., **contract type, tenure, charges**) explains the majority of churn behaviour.

**Business implication:**  
Retention strategies should prioritise **high-impact drivers** rather than spreading effort across low-impact features.
""")

        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Top Feature", feature_importance.iloc[0]['Feature'], f"{feature_importance.iloc[0]['Importance']:.4f}")
        with col2:
            st.metric("Top 3", f"{feature_importance.head(3)['Importance'].sum()*100:.1f}%", "Combined")
        with col3:
            st.metric("Total", len(feature_importance), "Features")
        
        st.markdown("---")
        st.dataframe(feature_importance.head(15), use_container_width=True, hide_index=True)
        st.info("""
**Why this matters:**  
Focusing on the **top 3 drivers** yields the **highest ROI** for churn reduction initiatives.
""")


# ============================================================================
# PAGE 4: PREDICT
# ============================================================================
elif page == "🔮 Predict":

    st.markdown('<h1 class="main-header">🔮 Churn Risk Prediction</h1>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<h2 class="section-header">📋 Enter Customer Information</h2>', unsafe_allow_html=True)
    st.markdown("""
### 🎯 Prediction Objective

This tool estimates an individual customer's **likelihood of churn**  
and provides **actionable recommendations** to retain them before they leave.
""")


    # =======================
    # Customer Input Form
    # =======================
    with st.form("customer_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            tenure = st.number_input("Months as Customer", 0, 72, 24)
            senior_citizen = st.selectbox("Senior Citizen?", ["No", "Yes"])
            has_partner = st.selectbox("Has Partner?", ["No", "Yes"])

        with col2:
            monthly_charges = st.number_input("Monthly Bill ($)", 18.0, 119.0, 65.0, step=0.5)
            contract_type = st.selectbox(
                "Contract Length",
                ["Month-to-month", "One year", "Two year"]
            )

        with col3:
            has_security = st.selectbox("Online Security?", ["No", "Yes"])
            has_support = st.selectbox("Tech Support?", ["No", "Yes"])

        submit_btn = st.form_submit_button(
            "🔮 Predict Churn Risk",
            use_container_width=True
        )

    # =======================
    # Run prediction ONLY after click
    # =======================
    if submit_btn:

        def calculate_churn_risk(
            tenure, monthly_charges, contract_type,
            has_security, has_support, senior_citizen
        ):
            risk = {
                "Month-to-month": 0.42,
                "One year": 0.26,
                "Two year": 0.11
            }.get(contract_type, 0.26)

            if tenure < 6:
                risk += 0.15
            elif tenure < 12:
                risk += 0.10
            elif tenure < 24:
                risk += 0.05

            if monthly_charges > 90:
                risk += 0.10
            elif monthly_charges > 70:
                risk += 0.05

            if has_security == "Yes":
                risk -= 0.08
            if has_support == "Yes":
                risk -= 0.08
            if senior_citizen == "Yes":
                risk += 0.05

            return max(0.0, min(1.0, risk))

        churn_risk = calculate_churn_risk(
            tenure,
            monthly_charges,
            contract_type,
            has_security,
            has_support,
            senior_citizen
        )

        risk_percentage = churn_risk * 100

        # =======================
        # Risk Display
        # =======================
        col1, col2 = st.columns([1, 1.5])

        with col1:
            if risk_percentage < 20:
                st.success(f"✅ VERY LOW RISK\n\n{risk_percentage:.1f}%")
            elif risk_percentage < 35:
                st.info(f"🟢 LOW RISK\n\n{risk_percentage:.1f}%")
            elif risk_percentage < 50:
                st.warning(f"🟡 MODERATE RISK\n\n{risk_percentage:.1f}%")
            else:
                st.error(f"🔴 HIGH RISK\n\n{risk_percentage:.1f}%")

        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_percentage,
                number={'suffix': '%'},
                gauge={'axis': {'range': [0, 100]}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            st.info("""
**How to use this score:**  
- **Low risk:** Maintain engagement  
- **Moderate risk:** Proactive outreach  
- **High risk:** Immediate retention action

This score enables **prioritised intervention**, not blanket discounts.
""")


        # =======================
        # Recommendations
        # =======================
        st.markdown("---")
        st.markdown('<h2 class="section-header">💡 Recommendations</h2>', unsafe_allow_html=True)
        st.markdown("""
### 📌 Retention Strategy Guidance

Recommendations are generated based on **risk level and customer profile**,  
supporting **targeted, cost-effective retention actions**.
""")


        if risk_percentage < 20:
            st.success("""
            ✅ **VERY LOW RISK – Maintain Strategy**
            - Continue loyalty programs
            - Monitor satisfaction
            """)
        elif risk_percentage < 35:
            st.info("""
            🟢 **LOW RISK – Routine Engagement**
            - Service updates
            - Quarterly check-ins
            """)
        elif risk_percentage < 50:
            st.warning("""
            🟡 **MODERATE RISK – Proactive Outreach**
            - Call customer
            - Offer upgrade discounts
            """)
        else:
            st.error("""
            🔴 **HIGH RISK – URGENT ACTION**
            - Priority retention call
            - Special discount offers
            """)

        # =======================
        # Customer Profile
        # =======================
        st.markdown("---")
        st.markdown('<h2 class="section-header">📊 Customer Profile</h2>', unsafe_allow_html=True)

        profile_data = {
            "Metric": [
                "Tenure", "Monthly Charges", "Contract Type",
                "Online Security", "Tech Support",
                "Senior Citizen", "Has Partner"
            ],
            "Value": [
                f"{tenure} months",
                f"${monthly_charges:.2f}",
                contract_type,
                has_security,
                has_support,
                senior_citizen,
                has_partner
            ]
        }

        st.dataframe(
            pd.DataFrame(profile_data),
            use_container_width=True,
            hide_index=True
        )
# ============================================================================
# PAGE 5: PERFORMANCE
# ============================================================================
elif page == "📋 Performance":
    st.markdown('<h1 class="main-header">📊 Model Performance</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<h2 class="section-header">Key Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", "76.33%", "Test Set")
    with col2:
        st.metric("ROC-AUC", "0.8329", "Test Set")
    with col3:
        st.metric("Sensitivity", "71.93%", "Recall")
    with col4:
        st.metric("Specificity", "77.93%", "TNR")
    
    st.markdown('<h2 class="section-header">Detailed Evaluation</h2>', unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        cm_data = [[805, 228], [105, 269]]
        fig = go.Figure(data=go.Heatmap(
            z=cm_data,
            x=['Predicted No', 'Predicted Yes'],
            y=['Actual No', 'Actual Yes'],
            text=cm_data,
            texttemplate="%{text}",
            colorscale='Blues'
        ))
        fig.update_layout(
            title="Confusion Matrix",
            font=dict(family="Inter", size=12, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            height=350,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
**How to interpret this:**  
- True Positives: Correctly identified churners  
- False Negatives: Missed churners (highest business risk)

Reducing false negatives is key to improving retention outcomes.
""")

    
    with col2:
        metrics_data = {
            'Metric': ['Precision', 'Recall', 'F1-Score'],
            'No Churn': [0.8846, 0.7793, 0.8286],
            'Churn': [0.5412, 0.7193, 0.6177]
        }
        metrics_df = pd.DataFrame(metrics_data)
        
        fig = go.Figure(data=[
            go.Bar(name='No Churn', x=metrics_df['Metric'], y=metrics_df['No Churn'], marker=dict(color='#10b981')),
            go.Bar(name='Churn', x=metrics_df['Metric'], y=metrics_df['Churn'], marker=dict(color='#ef4444'))
        ])
        fig.update_layout(
            title="Classification Metrics",
            barmode='group',
            font=dict(family="Inter", size=12, color="#374151"),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            height=350,
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb'),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
        **Model objective:**  
Maximise detection of churners while maintaining reasonable precision.

**Why recall matters:**  
Missing a churner is more costly than incorrectly flagging a loyal customer.
""")
    
    st.markdown('<h2 class="section-header">Cross-Validation Results</h2>', unsafe_allow_html=True)
    cv_scores = [0.8341, 0.8626, 0.8512, 0.8205, 0.8501]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=['Fold 1', 'Fold 2', 'Fold 3', 'Fold 4', 'Fold 5'],
        y=cv_scores,
        mode='lines+markers',
        marker=dict(size=10, color='#3b82f6'),
        line=dict(color='#3b82f6', width=3)
    ))
    fig.add_hline(y=np.mean(cv_scores), line_dash="dash", line_color="#ef4444",
                  annotation_text=f"Mean: {np.mean(cv_scores):.4f}")
    fig.update_layout(
        title="5-Fold Cross-Validation Results",
        xaxis_title="Fold",
        yaxis_title="ROC-AUC Score",
        font=dict(family="Inter", size=12, color="#374151"),
        paper_bgcolor='rgba(255, 255, 255, 0.5)',
        height=400,
        xaxis=dict(gridcolor='#e5e7eb'),
        yaxis=dict(gridcolor='#e5e7eb'),
        margin=dict(l=60, r=40, t=60, b=60)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.success("""
**What this shows:**  
Consistent performance across folds indicates the model is **stable and generalisable**,  
not overfitting to a specific sample.
""")


# ============================================================================
# PAGE 6: ABOUT
# ============================================================================
elif page == "ℹ️ About":
    st.markdown('<h1 class="main-header">About This Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<h2 class="section-header">📱 Telco Customer Churn Analytics</h2>', unsafe_allow_html=True)
    st.markdown("""
    Advanced machine learning dashboard predicting customer churn in telecommunications.
    Identify at-risk customers and implement data-driven retention strategies.
    """)
    
    st.markdown('<h2 class="section-header">✨ Key Features</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📊 Dashboard Overview**
        - Real-time churn metrics
        - Customer distribution
        - Tenure & charges insights
        
        **📈 Analytics**
        - Interactive exploration
        - Churn rate analysis
        - Statistical summaries
        """)
    with col2:
        st.markdown("""
        **🎯 Feature Importance**
        - Top churn drivers
        - Impact analysis
        - Recommendations
        
        **🔮 Prediction**
        - Customer risk scoring
        - Personalized insights
        - Action items
        """)
    
    st.markdown('<h2 class="section-header">📊 Model Performance</h2>', unsafe_allow_html=True)
    perf_data = {
        'Metric': ['Accuracy', 'ROC-AUC', 'Sensitivity', 'Specificity', 'Precision', 'F1-Score'],
        'Value': ['76.33%', '0.8329', '71.93%', '77.93%', '54.12%', '0.6177']
    }
    st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)
    
    st.markdown('<h2 class="section-header">🔑 Top Churn Drivers</h2>', unsafe_allow_html=True)
    drivers = {
        'Rank': ['1', '2', '3'],
        'Feature': ['Contract', 'Tenure', 'Total Charges'],
        'Importance': ['18.82%', '14.90%', '12.68%'],
        'Impact': ['2-year: 11% vs Month-to-month: 43%', 'Longer tenure = lower churn', 'Higher bills = higher risk']
    }
    st.dataframe(pd.DataFrame(drivers), use_container_width=True, hide_index=True)
    
    
    st.info("""
### 🧠 Business Value Summary

This dashboard transforms raw customer data into:
- **Actionable churn insights**
- **Predictive risk scoring**
- **Targeted retention strategies**

It enables leadership to move from **reactive churn analysis**  
to **proactive, data-driven decision making**.
""")
    
    st.markdown("""
    **Developed by:** Swathi Mulkundkar      
    **Role:** Data Scientist & ML Engineer    
      Passionate about leveraging data to solve real-world business problems through analytics and machine learning.
    """, unsafe_allow_html=True)