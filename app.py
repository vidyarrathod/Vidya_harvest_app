import streamlit as st
import random
import pandas as pd
from PIL import Image
import time
from datetime import datetime
import plotly.express as px
from plotly import graph_objects as go


# Page Configuration
st.set_page_config(
    page_title="Harvest Pay Credit System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Custom CSS for Full-Page Coverage and Metrics Styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .st-emotion-cache-1jicfl2 {
        width: 100%;
        padding: 6rem 1rem 10rem;
        min-width: auto;
        max-width: initial;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
def create_sidebar():
    with st.sidebar:
        # Sidebar Image
        try:
            st.image("credit.jpg", caption="Harvest Pay")
        except:
            st.image("https://via.placeholder.com/150", caption="Harvest Pay")
        
        selected = st.radio(
            "Navigate to",
            ["Home", "About", "Features", "Dashboard", "Analytics", "Contact"]
        )
        
        st.divider()
        
        # Login/Logout Section
        if st.session_state.get('logged_in', False):
            st.success(f"Welcome, {st.session_state.get('user_name', 'User')} ({st.session_state.get('user_role', 'Role')})")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.pop('user_name', None)
                st.session_state.pop('user_id', None)
                st.session_state.pop('user_role', None)
                st.rerun()
        else:
            with st.expander("Login"):
                # Role Selection
                role = st.selectbox("Login as", ["Select", "Admin", "Farmer", "Contributor"], key="login_role")
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                if st.button("Login"):
                    if role != "Select" and username and password:
                        st.session_state.logged_in = True
                        st.session_state.user_name = username
                        st.session_state.user_id = random.randint(1, 1000)
                        st.session_state.user_role = role
                        st.rerun()
                    else:
                        st.error("Please select a role and enter both username and password.")
        
        return selected.lower().replace(" ", "_") if st.session_state.get('logged_in', False) else "login"

# Home Page
def home():
    # Main Layout
    col1, col2 = st.columns([2, 1])

    # Left Column: Welcome Message
    with col1:
        st.title("🌟 Welcome to Harvest Pay Credit Card System")

        # Role-based Welcome Message
        role = st.session_state.get('user_role', 'Guest')
        if role == "Admin":
            st.subheader("You have administrative access to manage the system.")
        elif role == "Farmer":
            st.subheader("Explore tailored credit options designed for farmers.")
        elif role == "Contributor":
            st.subheader("Contribute to building a better credit system.")
        else:
            st.subheader("Please log in to access personalized features.")

        # User Interaction
        user_name = st.text_input("Enter your name to personalize your experience", key="user_name")
        if user_name:
            st.success(f"Hello, {user_name}! Let's explore your credit options.")

        # Interactive Features Showcase
        with st.expander("🌟 Why Choose Us?"):
            st.markdown("""
            - **AI-Powered Credit Scoring**: Leverage innovative algorithms to assess creditworthiness.
            - **Instant Approval Process**: Get your loans approved within minutes.
            - **Zero Annual Fees**: Enjoy benefits without additional costs.
            - **24/7 Customer Support**: Always available for your queries.
            """)

    # Right Column: Dynamic Live Statistics
    with col2:
        st.subheader("📊 Live Statistics")

        if role == "Admin":
            st.metric("📈 Active Users", f"{random.randint(1000, 5000):,}")
            st.metric("📊 Average Credit Score", random.randint(700, 800))
            st.metric("💰 Total Credit Issued", f"₹{random.randint(10_000_000, 50_000_000):,}")
        elif role == "Contributor":
            st.metric("💵 Amount Invested", f"₹{random.randint(500_000, 5_000_000):,}")
            st.metric("📉 Rate of Interest Allocated", f"{random.uniform(5.0, 12.0):.2f}%")
            st.metric("📈 Profit Made", f"₹{random.randint(100_000, 500_000):,}")
        elif role == "Farmer":
            st.metric("💳 Credit Limit", f"₹{random.randint(50_000, 300_000):,}")
            st.metric("📉 Rate of Interest", f"{random.uniform(3.0, 8.0):.2f}%")
            st.metric("📊 Credit Amount", f"₹{random.randint(15_000, 200_000):,}")
        else:
            st.info("Log in to view role-specific statistics.")

    # Horizontal Divider
    st.divider()

    # Additional Features Section
    st.subheader("🌟 Additional Features")
    col1, col2, col3 = st.columns(3)

    # Feature 1: Apply for Credit Card
    with col1:
        if st.button("🌱 Crop Rotation and Soil Health Advisor"):
            st.write("### 🌾 Optimize Your Crop Rotation")
            st.write("Get recommendations for the next crop to grow based on soil health and the last planted crop.")

        # Input Fields
        last_crop = st.selectbox("Select Last Planted Crop", ["Wheat", "Rice", "Maize", "Sugarcane", "Cotton"])
        soil_type = st.selectbox("Select Soil Type", ["Loamy", "Sandy", "Clayey", "Silty", "Peaty"])
        irrigation = st.radio("Do you have irrigation facilities?", ["Yes", "No"])
        organic_matter = st.slider("Organic Matter Content (%)", min_value=1, max_value=100, value=50)
        
        # Logic for Recommendations
        recommendations = {
            "Wheat": {"Loamy": "Maize", "Sandy": "Peanuts", "Clayey": "Rice"},
            "Rice": {"Loamy": "Sugarcane", "Sandy": "Cotton", "Clayey": "Wheat"},
            "Maize": {"Loamy": "Beans", "Sandy": "Millets", "Clayey": "Rice"},
            "Sugarcane": {"Loamy": "Soybeans", "Sandy": "Groundnuts", "Clayey": "Cotton"},
            "Cotton": {"Loamy": "Wheat", "Sandy": "Sunflower", "Clayey": "Rice"}
        }
        
        next_crop = recommendations.get(last_crop, {}).get(soil_type, "No recommendation available")
        
        # Display Results
        st.write("### Recommendations")
        st.write(f"**Last Planted Crop:** {last_crop}")
        st.write(f"**Soil Type:** {soil_type}")
        st.write(f"**Organic Matter Content:** {organic_matter}%")
        st.write(f"**Irrigation Available:** {irrigation}")
        st.write(f"**Recommended Next Crop:** {next_crop}")
        
        # Visualization with Gauge
        soil_health_score = organic_matter + (20 if irrigation == "Yes" else 0)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=soil_health_score,
            title={"text": "Soil Health Score"},
            gauge={
                "axis": {"range": [0, 120]},
                "steps": [
                    {"range": [0, 40], "color": "red"},
                    {"range": [40, 80], "color": "yellow"},
                    {"range": [80, 120], "color": "green"},
                ],
                "bar": {"color": "blue"}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)


    # Feature 2: View Loan Details
    with col2:
        if st.button("📑 View Loan Details"):
            st.write("**Your Current Loans**")
            st.write("""
            | Loan ID | Amount (₹) | Interest Rate (%) | Status |
            |---------|------------|-------------------|--------|
            | 10101   | 2,50,000   | 08.0            | Active |
            | 10102   | 1,00,000   | 08.0              | Paid   |
            """)
            st.info("📊 Visit your loan dashboard for more details.")

    # Feature 3: Customer Support
    with col3:
        if st.button("🛠 Customer Support"):
            st.write("**Contact Our Support Team**")
            st.write("""
            - **Email**: support@vidyacredit.com
            - **Phone**: +91-9876543210
            - **Working Hours**: 24/7
            """)
            st.write("🗨️ Chat with us [here](#).")

    # Footer Section
    st.divider()
    st.caption("© 2024 Vidya's Credit Card System. All rights reserved.")
# About Page
def about():
    st.title("🌟About HarvestPay Credit System")
    
    # Mission and Vision Section
    st.markdown(
        """
        <div style="background-color:#f0f4f7; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
            <h2 style="color:#4CAF50; text-align:center;">Our Mission</h2>
            <p style="font-size:16px; text-align:center; line-height:1.6;">
                To provide affordable institutional credit to financially excluded citizens 
                through innovative AI-powered credit scoring.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # What We Do Section
    st.markdown(
        """
        <div style="background-color:#e9f5ff; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
            <h2 style="color:#2196F3; text-align:center;">What We Do</h2>
            <p style="font-size:16px; text-align:center; line-height:1.6;">
                We leverage artificial intelligence and machine learning to evaluate creditworthiness 
                using alternative data points, making credit accessible to those without traditional credit history.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Key Impact Metrics Section
    st.markdown(
        """
        <div style="background-color:#fff3e0; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
            <h2 style="color:#FF5722; text-align:center;">Impact At a Glance</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌍 Lives Impacted", "250M+")
    with col2:
        st.metric("🤝 Lending Partners", "55+")
    with col3:
        st.metric("📄 Loan Applications", "25M+")

    # Interactive Story Section
    st.markdown(
        """
        <div style="background-color:#f4f4f4; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-top:20px;">
            <h2 style="color:#9C27B0; text-align:center;">Our Journey</h2>
            <p style="font-size:16px; text-align:center; line-height:1.6;">
                Starting with a vision to revolutionize credit accessibility, Vidya's Credit Card System 
                has grown into a platform that bridges financial gaps and empowers underserved communities.
            </p>
            <div style="text-align:center; margin-top:20px;">
                <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-size:16px;">
                    Learn More About Us
                </button>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Features Page
def features():
    st.title("🌟 Key Features")

    # Smart Credit Scoring Feature in a Box
    st.markdown(
        """
        <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
            <h3 style="color:#4CAF50;">💡 Smart Credit Scoring</h3>
            <ul>
                <li><b>AI-powered creditworthiness assessment</b>: Predicts eligibility with high accuracy.</li>
                <li><b>Digital footprint analysis</b>: Evaluates online behavior for better credit decisions.</li>
                <li><b>Behavioral data evaluation</b>: Provides insights from past actions.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Loan Benefits Feature in a Box
    st.markdown(
        """
        <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
            <h3 style="color:#2196F3;">💰 Loan Benefits</h3>
            <ul>
                <li><b>Loan range</b>: ₹15,000 - ₹3,00,000</li>
                <li><b>Competitive interest rates</b>: Starting at 8%.</li>
                <li><b>Quick processing and approval</b>: Get loans without hassle.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Security Features in a Box
    st.markdown(
        """
        <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
            <h3 style="color:#FF5722;">🔒 Security Features</h3>
            <ul>
                <li><b>Advanced fraud detection</b>: Safeguards against suspicious activities.</li>
                <li><b>Secure transaction processing</b>: Ensures all data is encrypted.</li>
                <li><b>Real-time monitoring</b>: Keeps your account safe 24/7.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Feature Comparison Section
    st.write("### Compare Features")
    feature_comparison = {
        "Feature": ["AI Credit Scoring", "Loan Benefits", "Security"],
        "User Rating (⭐)": [4.8, 4.6, 4.9],
        "Benefit Level": ["High", "Moderate", "Very High"]
    }
    st.dataframe(feature_comparison)

    # Interactive Button
    st.markdown(
        """
        <div style="text-align:center; margin-top:20px;">
            <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-size:16px;">
                Explore More Features
            </button>
        </div>
        """, 
        unsafe_allow_html=True
    )
#def dashbooard            
def dashboard():
    st.title("📊 User Dashboard")
    
    # Retrieve the user's role from session state
    role = st.session_state.get("user_role", "Guest")  # Default to 'Guest' if not set

    if role == "Admin":
        st.subheader("Admin Dashboard")
        # Graph: Active Users Over Time
        st.write("### Active Users Over Time")
        active_users_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Active Users": [random.randint(1000, 5000) for _ in range(6)]
        })
        st.line_chart(active_users_data.set_index("Month"))

        # Graph: Pending Applications by Type
        st.write("### Pending Applications by Type")
        pending_apps_data = pd.DataFrame({
            "Type": ["Loan Approval", "KYC Verification", "Fraud Check"],
            "Count": [random.randint(50, 200) for _ in range(3)]
        })
        st.bar_chart(pending_apps_data.set_index("Type"))

    elif role == "Contributor":
        st.subheader("Contributor Dashboard")
        # Graph: Investments in Different Sectors
        st.write("### Investments in Different Sectors")
        investment_data = pd.DataFrame({
            "Sector": ["Agriculture", "Retail", "Technology", "Healthcare"],
            "Amount Invested (₹)": [random.randint(100000, 500000) for _ in range(4)]
        })
        st.bar_chart(investment_data.set_index("Sector"))

        # Graph: Monthly Profits
        st.write("### Monthly Profits")
        profit_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr"],
            "Profit (₹)": [random.randint(10000, 50000) for _ in range(4)]
        })
        st.line_chart(profit_data.set_index("Month"))

    elif role == "Farmer":
        st.subheader("Farmer Dashboard")
        # Graph: Loan Usage Breakdown
        st.write("### Loan Usage Breakdown")
        usage_data = pd.DataFrame({
            "Category": ["Seeds", "Equipment", "Fertilizers", "Labor"],
            "Amount Used (₹)": [random.randint(10000, 50000) for _ in range(4)]
        })
        st.bar_chart(usage_data.set_index("Category"))

        # Graph: Monthly Payments
        st.write("### Monthly Payments")
        payment_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr"],
            "Payment (₹)": [random.randint(5000, 20000) for _ in range(4)]
        })
        st.line_chart(payment_data.set_index("Month"))

    else:
        st.info("Please log in to view your dashboard.")
# Analytics Page
def analytics():
    st.title("Analytics Dashboard")
    time_period = st.selectbox("Select Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Transaction Analytics")
        st.write("• Transaction success rates")
        st.write("• Usage patterns by merchant category")
        st.write("• Card activation trends")
        chart_data = pd.DataFrame({
            'Category': ['Shopping', 'Travel', 'Food', 'Bills'],
            'Amount': [45000, 30000, 25000, 20000]
        })
        st.bar_chart(chart_data.set_index('Category'))
    with col2:
        st.subheader("Customer Insights")
        st.write("• Spending behavior analysis")
        st.write("• Customer segmentation")
        st.write("• Risk assessment metrics")
        st.metric("Average Transaction Value", "₹15,000", "+12%")
        st.metric("Active Users", "25,000", "+5%")

# Contact Page
def contact():
    # Background color for the page
    st.markdown(
        """
        <style>
        .contact-section {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }
        .contact-header {
            color: #2a9d8f;
            text-align: center;
        }
        .form-container {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
        }
        .submit-button {
            background-color: #2a9d8f;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .submit-button:hover {
            background-color: #1b7f69;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="contact-section">', unsafe_allow_html=True)

    st.title("📞 Contact Us")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💬 Customer Support")
        st.write("24/7 Toll-Free Numbers:")
        st.write("📞 1800-425-7744")
        st.write("📞 1800-425-9992")
        st.subheader("📧 Email Support")
        st.write("📩 support@vidyacredit.com")
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        with st.form("contact_form"):
            st.subheader("✉️ Send us a message")
            name = st.text_input("Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            message = st.text_area("Message", placeholder="Write your message here...")
            submitted = st.form_submit_button("Submit", help="Click to send your message")
            if submitted:
                st.success("✅ Thank you for your message. We'll get back to you soon!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Main Function
import os

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    page = create_sidebar()
    
    # Define the image path
    image_path = "crop_image.jpg"
    
    # If not logged in, show the login page with the image
    if not st.session_state.get('logged_in', False):
        st.markdown("""
            <div style="text-align:center; margin-top:50px;">
                <h1>Welcome to Harvest Pay Credit System</h1>
            </div>
        """, unsafe_allow_html=True)

        # Display image
        if os.path.exists(image_path):
            st.image(image_path, caption="Secure Credit Card Services", use_container_width=True)
        else:
            st.error("Image not found. Please check the file path.")
    elif page == "home":
        home()
    elif page == "about":
        about()
    elif page == "features":
        features()
    
    elif page == "dashboard":
        dashboard()
    elif page == "analytics":
        analytics()
    elif page == "contact":
        contact()
    else:
        st.error("Page not found.")

# Run the application
if __name__ == "__main__":
    main()

