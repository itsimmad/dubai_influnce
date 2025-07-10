import streamlit as st
st.set_page_config(layout="wide")
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
import pandas as pd
import numpy as np

# ---- Custom CSS for Premium Design ----
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove Streamlit default white blocks */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background: none !important;
        box-shadow: none !important;
    }
    
    /* Premium Card */
    .premium-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .premium-card {
        background: rgba(30, 36, 70, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        border: 1px solid rgba(255,255,255,0.10);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    .tier-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .tier-nano { background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 100%); color: #333; }
    .tier-micro { background: linear-gradient(45deg, #a8edea 0%, #fed6e3 100%); color: #333; }
    .tier-mid { background: linear-gradient(45deg, #ffecd2 0%, #fcb69f 100%); color: #333; }
    .tier-macro { background: linear-gradient(45deg, #ff9a9e 0%, #fad0c4 100%); color: #333; }
    .premium-button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .premium-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .brief-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    .market-insights {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
    }
    /* Unified input field styles */
    input, select, textarea {
        background: rgba(30, 36, 70, 0.92) !important;
        color: #fff !important;
        border: 1.5px solid #764ba2 !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        margin-bottom: 0.5rem !important;
    }
    input:focus, select:focus, textarea:focus {
        outline: none !important;
        border: 2px solid #FFD700 !important;
        background: rgba(40, 46, 90, 1) !important;
        color: #fff !important;
    }
    ::placeholder {
        color: #bdb8d7 !important;
        opacity: 1 !important;
    }
    /* Streamlit widgets */
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
        background: rgba(30, 36, 70, 0.92) !important;
        color: #fff !important;
        border-radius: 10px !important;
        border: 1.5px solid #764ba2 !important;
    }
    .stSelectbox > div > div:focus, .stNumberInput > div > div > input:focus, .stTextInput > div > div > input:focus {
        border: 2px solid #FFD700 !important;
        background: rgba(40, 46, 90, 1) !important;
        color: #fff !important;
    }
    .stMarkdown {
        color: #fff;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: white;
        font-size: 0.9rem;
    }
    .logo {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    .insight-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    /* Make tables and containers scrollable on small screens */
    .css-1l269bu, .css-1d391kg, .stDataFrame { overflow-x: auto; }
    /* Responsive padding and font size */
    @media (max-width: 600px) {
        .block-container { padding: 0.5rem 0.2rem !important; }
        body, .stTextInput input, .stButton button, .stSelectbox label, .stMarkdown { font-size: 1.08rem !important; }
        .stDataFrame { font-size: 0.95rem !important; }
    }
    /* Responsive table for influencer box */
    .premium-card .responsive-table {
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        display: block;
    }
    .premium-card table {
        border-collapse: collapse;
        width: 100%;
        font-size: 1rem;
        background: none;
    }
    .premium-card th, .premium-card td {
        padding: 0.6rem 0.5rem;
        text-align: left;
        white-space: nowrap;
    }
    .premium-card th {
        background: rgba(255,255,255,0.08);
    }
    .premium-card tr:nth-child(even) {
        background: rgba(255,255,255,0.04);
    }
    @media (max-width: 700px) {
        .premium-card table {
            font-size: 0.85rem;
            /* min-width removed */
        }
        .premium-card th, .premium-card td {
            padding: 0.3rem 0.2rem;
        }
    }
    @media (max-width: 480px) {
        .premium-card table {
            font-size: 0.72rem;
            /* min-width removed */
        }
        .premium-card th, .premium-card td {
            padding: 0.12rem 0.05rem;
            white-space: normal; /* Allow wrapping */
            word-break: break-word;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---- Enhanced Data ----
PLATFORMS = ['Instagram', 'TikTok', 'YouTube', 'LinkedIn', 'Twitter/X']
CONTENT_TYPES = ['Story', 'Reel', 'Post', 'UGC', 'Video', 'Live Stream', 'Carousel']
CAMPAIGN_GOALS = [
    'Brand Awareness & Recognition',
    'Lead Generation & Sales',
    'Product Launch & Promotion',
    'Event & Exhibition Promotion',
    'App Downloads & Engagement',
    'E-commerce & Retail Sales',
    'B2B Lead Generation',
    'Tourism & Hospitality Promotion'
]
INDUSTRIES = [
    'Luxury Fashion & Retail',
    'Real Estate & Property',
    'Technology & Innovation',
    'Hospitality & Tourism',
    'Finance & Banking',
    'Healthcare & Wellness',
    'Automotive & Transportation',
    'Food & Beverage',
    'Beauty & Cosmetics',
    'Sports & Fitness',
    'Education & Training',
    'Entertainment & Media'
]

# Premium Rate Card with Dubai Market Rates
RATE_CARD = {
    'Instagram': {
        'Nano': {'rate': 800, 'engagement': '8-12%', 'reach': '2K-5K'},
        'Micro': {'rate': 3000, 'engagement': '6-10%', 'reach': '10K-25K'},
        'Mid-tier': {'rate': 12000, 'engagement': '4-8%', 'reach': '50K-150K'},
        'Macro': {'rate': 40000, 'engagement': '2-5%', 'reach': '250K+'}
    },
    'TikTok': {
        'Nano': {'rate': 1200, 'engagement': '10-15%', 'reach': '5K-15K'},
        'Micro': {'rate': 4000, 'engagement': '8-12%', 'reach': '20K-50K'},
        'Mid-tier': {'rate': 15000, 'engagement': '5-10%', 'reach': '100K-300K'},
        'Macro': {'rate': 50000, 'engagement': '3-7%', 'reach': '500K+'}
    },
    'YouTube': {
        'Nano': {'rate': 2000, 'engagement': '5-8%', 'reach': '1K-3K'},
        'Micro': {'rate': 6000, 'engagement': '4-7%', 'reach': '5K-15K'},
        'Mid-tier': {'rate': 20000, 'engagement': '3-6%', 'reach': '25K-75K'},
        'Macro': {'rate': 80000, 'engagement': '2-4%', 'reach': '100K+'}
    },
    'LinkedIn': {
        'Nano': {'rate': 1500, 'engagement': '6-10%', 'reach': '1K-3K'},
        'Micro': {'rate': 5000, 'engagement': '5-8%', 'reach': '5K-15K'},
        'Mid-tier': {'rate': 18000, 'engagement': '4-7%', 'reach': '20K-60K'},
        'Macro': {'rate': 60000, 'engagement': '3-5%', 'reach': '100K+'}
    },
    'Twitter/X': {
        'Nano': {'rate': 600, 'engagement': '5-8%', 'reach': '2K-5K'},
        'Micro': {'rate': 2500, 'engagement': '4-7%', 'reach': '10K-25K'},
        'Mid-tier': {'rate': 10000, 'engagement': '3-6%', 'reach': '50K-150K'},
        'Macro': {'rate': 35000, 'engagement': '2-4%', 'reach': '250K+'}
    }
}

TIER_RANGES = [
    ('Nano', 1_000, 10_000),
    ('Micro', 10_001, 50_000),
    ('Mid-tier', 50_001, 250_000),
    ('Macro', 250_001, 10_000_000)
]

# Dubai Market Insights
DUBAI_INSIGHTS = {
    'market_size': 'AED 1.2B+',
    'growth_rate': '25% YoY',
    'top_industries': ['Real Estate', 'Luxury Retail', 'Tourism', 'Technology'],
    'avg_engagement': '6.8%',
    'premium_creators': '2,500+',
    'brands_active': '500+'
}

# --- Platform-based campaign types ---
PLATFORM_CAMPAIGN_TYPES = {
    'Instagram': ['Reels', 'Stories', 'Giveaways', 'Product Demo', 'UGC'],
    'TikTok': ['Challenges', 'Short-form Video', 'Duets', 'Live', 'Product Demo'],
    'YouTube': ['Product Review', 'Vlog', 'Tutorial', 'Unboxing', 'Live Stream'],
    'Facebook': ['Live', 'Event Promotion', 'Stories', 'Group Post', 'Video Ad'],
    'Twitter/X': ['Thread', 'Giveaway', 'Poll', 'Live Tweet', 'Brand Mention']
}

# --- Influencer suggestions (hardcoded for demo) ---
INFLUENCERS = {
    'Instagram': [
        {'name': 'Alya Dubai', 'handle': '@alyadxb', 'followers': '120K', 'niche': 'Fashion', 'link': 'https://instagram.com/alyadxb', 'tier': 'Micro'},
        {'name': 'Omar Eats', 'handle': '@omareats', 'followers': '80K', 'niche': 'Food', 'link': 'https://instagram.com/omareats', 'tier': 'Micro'},
        {'name': 'TechWithSara', 'handle': '@techwithsara', 'followers': '300K', 'niche': 'Tech', 'link': 'https://instagram.com/techwithsara', 'tier': 'Mid-tier'},
        {'name': 'DubaiFit', 'handle': '@dubaifit', 'followers': '25K', 'niche': 'Fitness', 'link': 'https://instagram.com/dubaifit', 'tier': 'Nano'},
        {'name': 'TravelWithZee', 'handle': '@travelwithzee', 'followers': '500K', 'niche': 'Travel', 'link': 'https://instagram.com/travelwithzee', 'tier': 'Macro'},
    ],
    'TikTok': [
        {'name': 'Lina Vlogs', 'handle': '@linavlogs', 'followers': '200K', 'niche': 'Lifestyle', 'link': 'https://tiktok.com/@linavlogs', 'tier': 'Mid-tier'},
        {'name': 'DubaiComedy', 'handle': '@dubaicomedy', 'followers': '1M', 'niche': 'Comedy', 'link': 'https://tiktok.com/@dubaicomedy', 'tier': 'Macro'},
        {'name': 'ChefRami', 'handle': '@cheframi', 'followers': '60K', 'niche': 'Food', 'link': 'https://tiktok.com/@cheframi', 'tier': 'Micro'},
        {'name': 'BeautyByNoor', 'handle': '@beautybynoor', 'followers': '35K', 'niche': 'Beauty', 'link': 'https://tiktok.com/@beautybynoor', 'tier': 'Nano'},
        {'name': 'DubaiMotors', 'handle': '@dubaimotors', 'followers': '400K', 'niche': 'Automotive', 'link': 'https://tiktok.com/@dubaimotors', 'tier': 'Mid-tier'},
    ],
    'YouTube': [
        {'name': 'Sara Reviews', 'handle': 'Sara Reviews', 'followers': '150K', 'niche': 'Tech', 'link': 'https://youtube.com/c/SaraReviews', 'tier': 'Mid-tier'},
        {'name': 'Dubai Explorer', 'handle': 'Dubai Explorer', 'followers': '500K', 'niche': 'Travel', 'link': 'https://youtube.com/c/DubaiExplorer', 'tier': 'Macro'},
        {'name': 'FitWithAli', 'handle': 'FitWithAli', 'followers': '40K', 'niche': 'Fitness', 'link': 'https://youtube.com/c/FitWithAli', 'tier': 'Micro'},
        {'name': 'TasteDXB', 'handle': 'TasteDXB', 'followers': '90K', 'niche': 'Food', 'link': 'https://youtube.com/c/TasteDXB', 'tier': 'Micro'},
        {'name': 'BeautyByLina', 'handle': 'BeautyByLina', 'followers': '20K', 'niche': 'Beauty', 'link': 'https://youtube.com/c/BeautyByLina', 'tier': 'Nano'},
    ],
    'Facebook': [
        {'name': 'Dubai Events', 'handle': '@dubaievents', 'followers': '300K', 'niche': 'Events', 'link': 'https://facebook.com/dubaievents', 'tier': 'Mid-tier'},
        {'name': 'FB Foodies', 'handle': '@fbfoodies', 'followers': '50K', 'niche': 'Food', 'link': 'https://facebook.com/fbfoodies', 'tier': 'Micro'},
        {'name': 'RealEstateDXB', 'handle': '@realestatedxb', 'followers': '120K', 'niche': 'Real Estate', 'link': 'https://facebook.com/realestatedxb', 'tier': 'Mid-tier'},
        {'name': 'DubaiMoms', 'handle': '@dubaimoms', 'followers': '25K', 'niche': 'Parenting', 'link': 'https://facebook.com/dubaimoms', 'tier': 'Nano'},
        {'name': 'TechTalksUAE', 'handle': '@techtalksuae', 'followers': '200K', 'niche': 'Tech', 'link': 'https://facebook.com/techtalksuae', 'tier': 'Mid-tier'},
    ],
    'Twitter/X': [
        {'name': 'DXB News', 'handle': '@dxbnews', 'followers': '100K', 'niche': 'News', 'link': 'https://twitter.com/dxbnews', 'tier': 'Micro'},
        {'name': 'CryptoUAE', 'handle': '@cryptouae', 'followers': '60K', 'niche': 'Finance', 'link': 'https://twitter.com/cryptouae', 'tier': 'Micro'},
        {'name': 'DubaiTrends', 'handle': '@dubaitrends', 'followers': '250K', 'niche': 'Trends', 'link': 'https://twitter.com/dubaitrends', 'tier': 'Mid-tier'},
        {'name': 'AutoDXB', 'handle': '@autodxb', 'followers': '30K', 'niche': 'Automotive', 'link': 'https://twitter.com/autodxb', 'tier': 'Nano'},
        {'name': 'HealthDXB', 'handle': '@healthdxb', 'followers': '80K', 'niche': 'Health', 'link': 'https://twitter.com/healthdxb', 'tier': 'Micro'},
    ]
}

# --- Outreach Message Generator ---
def generate_outreach_message(brief_md, influencer_name):
    # Remove Markdown formatting from the brief
    import re
    brief_plain = re.sub(r'\*\*|[#>`\-]', '', brief_md)  # Remove bold, headers, etc.
    brief_plain = re.sub(r'\n{2,}', '\n', brief_plain)   # Remove extra newlines

    return f"""Subject: Collaboration Opportunity with Dubai Influencer Pro

Hi {influencer_name},

I hope this email finds you well.

I'm reaching out from Dubai Influencer Pro regarding an upcoming campaign that we believe aligns perfectly with your audience and content style.

Campaign Details:
{brief_plain.strip()}

If you're interested, please let us know your availability and your rates. We look forward to the possibility of working together.

Best regards,
[Your Name]
Dubai Influencer Pro
"""

# ---- Helper Functions ----
def get_tier_by_budget(budget, platform):
    rates = RATE_CARD[platform]
    if budget < rates['Micro']['rate']:
        return 'Nano', rates['Nano']
    elif budget < rates['Mid-tier']['rate']:
        return 'Micro', rates['Micro']
    elif budget < rates['Macro']['rate']:
        return 'Mid-tier', rates['Mid-tier']
    else:
        return 'Macro', rates['Macro']

def get_tier_by_followers(followers):
    for tier, low, high in TIER_RANGES:
        if low <= followers <= high:
            return tier
    return 'Macro'

def generate_premium_brief(inputs):
    industry_insights = {
        'Luxury Fashion & Retail': 'Focus on exclusivity, craftsmanship, and lifestyle positioning. Target high-net-worth individuals and fashion enthusiasts.',
        'Real Estate & Property': 'Emphasize luxury living, investment opportunities, and Dubai\'s world-class infrastructure.',
        'Technology & Innovation': 'Highlight innovation, digital transformation, and cutting-edge solutions.',
        'Hospitality & Tourism': 'Showcase Dubai\'s luxury hotels, attractions, and unique experiences.',
        'Finance & Banking': 'Focus on trust, security, and financial expertise in the region.',
        'Healthcare & Wellness': 'Emphasize quality care, modern facilities, and wellness lifestyle.',
        'Automotive & Transportation': 'Highlight luxury vehicles, innovation, and premium driving experiences.',
        'Food & Beverage': 'Focus on culinary excellence, unique dining experiences, and food culture.',
        'Beauty & Cosmetics': 'Emphasize beauty standards, luxury products, and self-care.',
        'Sports & Fitness': 'Focus on active lifestyle, wellness, and performance.',
        'Education & Training': 'Highlight quality education, career advancement, and skill development.',
        'Entertainment & Media': 'Focus on entertainment, creativity, and cultural experiences.'
    }
    
    platform_strategies = {
        'Instagram': 'Visual storytelling with high-quality imagery, Stories for behind-the-scenes, and Reels for viral potential.',
        'TikTok': 'Trending content, challenges, and authentic, engaging short-form videos.',
        'YouTube': 'In-depth content, tutorials, reviews, and long-form storytelling.',
        'LinkedIn': 'Professional content, thought leadership, and B2B networking.',
        'Twitter/X': 'Real-time updates, industry insights, and engaging conversations.'
    }
    
    industry_insight = industry_insights.get(inputs['industry'], 'Focus on brand values and target audience engagement.')
    platform_strategy = platform_strategies.get(inputs['platform'], 'Create engaging, platform-specific content.')
    
    brief = f"""
## 🎯 Campaign Strategy Overview

### 📋 Executive Summary
**Campaign Goal:** {inputs['goal']}  
**Industry Focus:** {inputs['industry']}  
**Primary Platform:** {inputs['platform']}  
**Content Strategy:** {inputs['content_type']}  

### 🎨 Creative Direction
**Industry Insight:** {industry_insight}  
**Platform Strategy:** {platform_strategy}  
**Target Audience:** {inputs.get('audience', 'Dubai-based professionals and consumers')}

### 📅 Campaign Timeline
**Phase 1 (Week 1-2):** Content Creation & Influencer Selection  
**Phase 2 (Week 3-4):** Campaign Launch & Active Promotion  
**Phase 3 (Week 5-6):** Performance Monitoring & Optimization  
**Phase 4 (Week 7-8):** Results Analysis & Reporting

### 🎬 Content Deliverables
- **Primary Content:** {inputs['content_type']} on {inputs['platform']}
- **Supporting Content:** Cross-platform promotion
- **Behind-the-Scenes:** Authentic creator content
- **User-Generated Content:** Community engagement

### 📊 Key Performance Indicators (KPIs)
- **Reach & Impressions:** Target audience exposure
- **Engagement Rate:** Comments, likes, shares, saves
- **Click-Through Rate:** Website/app traffic
- **Conversion Rate:** Lead generation and sales
- **Brand Sentiment:** Positive mentions and sentiment
- **ROI:** Return on investment measurement

### 🚀 Success Metrics
- **Reach Target:** 100K+ impressions
- **Engagement Target:** 5%+ engagement rate
- **Conversion Target:** 2%+ click-through rate
- **Brand Lift:** 15%+ increase in brand awareness

### 💡 Creative Guidelines
- **Tone:** Professional yet approachable
- **Visual Style:** High-quality, premium aesthetic
- **Messaging:** Clear value proposition and call-to-action
- **Hashtags:** Industry-relevant and trending tags
- **Timing:** Optimal posting times for Dubai audience

### 🔄 Optimization Strategy
- **A/B Testing:** Content variations and messaging
- **Performance Monitoring:** Real-time analytics tracking
- **Audience Insights:** Engagement pattern analysis
- **Content Optimization:** Data-driven improvements
"""
    return brief

def create_roi_calculator(budget, platform, content_type):
    # Simulate ROI calculation
    base_engagement = RATE_CARD[platform]['Micro']['engagement']
    engagement_rate = float(base_engagement.split('-')[0].replace('%', '')) / 100
    
    estimated_reach = budget * 10  # Simplified calculation
    estimated_engagement = estimated_reach * engagement_rate
    estimated_clicks = estimated_engagement * 0.1
    estimated_conversions = estimated_clicks * 0.02
    
    return {
        'reach': estimated_reach,
        'engagement': estimated_engagement,
        'clicks': estimated_clicks,
        'conversions': estimated_conversions,
        'cpm': budget / (estimated_reach / 1000)
    }

def create_market_chart():
    # Create a sample market growth chart
    years = [2020, 2021, 2022, 2023, 2024]
    market_size = [800, 950, 1100, 1200, 1400]  # in millions AED
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=market_size,
        mode='lines+markers',
        name='Dubai Influencer Market',
        line=dict(color='#FFD700', width=5),  # Bright gold for contrast
        marker=dict(size=10, color='#fff', line=dict(width=2, color='#FFD700'))
    ))
    
    fig.update_layout(
        title='Dubai Influencer Marketing Market Growth',
        xaxis_title='Year',
        yaxis_title='Market Size (Million AED)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        title_font=dict(color='#FFD700', size=22),
        xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.2)'),
        yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.2)')
    )
    
    return fig

# ---- Main App ----
def main():
    load_custom_css()
    
    # Header
    st.markdown("""
    <div class="premium-header">
        <div class="logo">🌟 Dubai Influencer Pro</div>
        <h1 style="color: white; text-align: center; margin: 0;">Premium Rate Calculator & Campaign Builder</h1>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin: 0;">The Ultimate Tool for Dubai's Top Brands & Agencies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Market Insights Section
    with st.container():
        st.markdown("""
        <div class="market-insights">
            <h2>📊 Dubai Market Insights</h2>
            <div class="stats-grid">
                <div class="insight-card">
                    <h3>Market Size</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">AED 1.2B+</p>
                </div>
                <div class="insight-card">
                    <h3>Growth Rate</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">25% YoY</p>
                </div>
                <div class="insight-card">
                    <h3>Premium Creators</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">2,500+</p>
                </div>
                <div class="insight-card">
                    <h3>Active Brands</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">500+</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Growth Chart
    st.plotly_chart(create_market_chart(), use_container_width=True)
    
    # Main Form - All fields reset on page refresh (no session state)
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("🎯 Campaign Configuration")
        
        with st.form("premium_campaign_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                budget = st.number_input(
                    "💰 Campaign Budget (AED)",
                    min_value=1000,
                    step=1000,
                    value=None,
                    key="budget_input",
                    placeholder="Enter budget"
                )
                goal = st.selectbox(
                    "🎯 Campaign Goal",
                    [""] + CAMPAIGN_GOALS,
                    index=0,
                    key="goal_input",
                    format_func=lambda x: x if x else "Select a goal"
                )
                industry = st.selectbox(
                    "🏢 Industry/Niche",
                    [""] + INDUSTRIES,
                    index=0,
                    key="industry_input",
                    format_func=lambda x: x if x else "Select an industry"
                )
            
            with col2:
                platform = st.selectbox(
                    "📱 Primary Platform",
                    [""] + PLATFORMS,
                    index=0,
                    key="platform_input",
                    format_func=lambda x: x if x else "Select a platform"
                )
                content_type = st.selectbox(
                    "🎬 Content Type",
                    [""] + CONTENT_TYPES,
                    index=0,
                    key="content_type_input",
                    format_func=lambda x: x if x else "Select content type"
                )
                audience = st.text_input(
                    "👥 Target Audience (Optional)",
                    value="",
                    placeholder="e.g., Luxury consumers, Tech professionals",
                    key="audience_input"
                )
            
            submitted = st.form_submit_button("🚀 Generate Premium Analysis", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted:
        # Validate required fields
        if (
            budget is None or
            not goal or
            not industry or
            not platform or
            not content_type
        ):
            st.error("Please fill in all required fields before generating the analysis.")
        else:
            # Store campaign config in session state
            st.session_state['campaign_config'] = {
                'budget': budget,
                'goal': goal,
                'industry': industry,
                'platform': platform,
                'content_type': content_type,
                'audience': audience
            }
            # Influencer Tier Analysis
            tier, tier_data = get_tier_by_budget(budget, platform)
            
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.header("🤝 Influencer Tier Analysis")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Recommended Tier</h3>
                    <div class="tier-badge tier-{tier.lower()}">{tier}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Estimated Rate</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">AED {tier_data['rate']:,}</p>
                    <small>per {content_type}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Engagement Rate</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">{tier_data['engagement']}</p>
                    <small>expected range</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Reach Potential</h3>
                    <p style="font-size: 1.5rem; font-weight: bold;">{tier_data['reach']}</p>
                    <small>per post</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ROI Calculator
            roi_data = create_roi_calculator(budget, platform, content_type)
            
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.header("📈 ROI Projection")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Estimated Reach", f"{roi_data['reach']:,.0f}")
            with col2:
                st.metric("Expected Engagement", f"{roi_data['engagement']:,.0f}")
            with col3:
                st.metric("Potential Clicks", f"{roi_data['clicks']:,.0f}")
            with col4:
                st.metric("Estimated Conversions", f"{roi_data['conversions']:,.0f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Premium Campaign Brief
            inputs = {
                'goal': goal,
                'industry': industry,
                'platform': platform,
                'content_type': content_type,
                'audience': audience
            }
            
            brief_md = generate_premium_brief(inputs)
            
            st.markdown('<div class="brief-section">', unsafe_allow_html=True)
            st.header("📋 Premium Campaign Brief")
            st.markdown(brief_md)
            
            # Copy and Download buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy Brief to Clipboard", use_container_width=True):
                    st.success("Brief copied to clipboard!")
            
            with col2:
                if st.button("📥 Download as PDF", use_container_width=True):
                    st.info("PDF download feature requires wkhtmltopdf installation")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Creator Rate Estimator
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("💸 Creator Rate Estimator")
        
        with st.expander("Calculate your worth as a creator", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                creator_platform = st.selectbox("Platform", PLATFORMS, key='creator_platform_estimator')
            with col2:
                creator_followers = st.number_input("Follower Count", min_value=1000, step=1000, value=10000, key='creator_followers_estimator')
            with col3:
                creator_niche = st.selectbox("Niche", INDUSTRIES, key='creator_niche_estimator')
            
            if st.button("Calculate My Rate", use_container_width=True, key='calculate_rate_btn'):
                creator_tier = get_tier_by_followers(creator_followers)
                rate_data = RATE_CARD[creator_platform][creator_tier]
                
                st.success(f"""
                **Your Profile Analysis:**
                - **Tier:** {creator_tier}
                - **Suggested Rate:** AED {rate_data['rate']:,} per post
                - **Expected Engagement:** {rate_data['engagement']}
                - **Reach Potential:** {rate_data['reach']}
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Suggested Influencer Box (responsive table)
        if platform:
            st.markdown(f"""
            <div class="premium-card">
            <h3>👥 Suggested Influencers for {platform}</h3>
            <div class="responsive-table">
            <table>
            <tr><th>Name</th><th>Handle</th><th>Followers</th><th>Niche</th><th>Tier</th><th>Link</th></tr>
            {''.join([
                f"<tr>"
                f"<td>{inf['name']}</td>"
                f"<td>{inf['handle']}</td>"
                f"<td>{inf['followers']}</td>"
                f"<td>{inf['niche']}</td>"
                f"<td><span class='tier-badge tier-{inf['tier'].lower()}'>{inf['tier']}</span></td>"
                f"<td><a href='{inf['link']}' target='_blank'>Profile</a></td>"
                f"</tr>" for inf in INFLUENCERS.get(platform, [])
            ])}
            </table>
            </div>
            </div>
            """, unsafe_allow_html=True)

    # Outreach Message Generator (only after campaign is submitted)
    campaign_config = st.session_state.get('campaign_config')
    if campaign_config and campaign_config.get('platform'):
        st.markdown(f"<div class='premium-card'><h3>📩 Outreach Message Generator</h3></div>", unsafe_allow_html=True)
        selected_influencer = st.selectbox(
            "Select Influencer for Outreach Message",
            [inf['name'] for inf in INFLUENCERS.get(campaign_config['platform'], [])],
            key='outreach_influencer'
        )
        if st.button("Generate Email to Influencer", key="generate_email_btn"):
            brief_md = generate_premium_brief({
                'goal': campaign_config['goal'],
                'industry': campaign_config['industry'],
                'platform': campaign_config['platform'],
                'content_type': campaign_config['content_type'],
                'audience': campaign_config['audience']
            })
            message = generate_outreach_message(brief_md, selected_influencer)
            st.text_area("Copy Outreach Message", message, height=300)
            b64 = base64.b64encode(message.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="outreach_message.txt">📥 Download as .txt</a>'
            st.markdown(href, unsafe_allow_html=True)

# Footer (leave this outside the if submitted block)
st.markdown("""
<div class="footer">
    <p> Kolab - Premium Tool for Top Brands & Agencies</p>
    <p>© 2025 | Built for Dubai's Dynamic Influencer Marketing Landscape</p>
</div>
""", unsafe_allow_html=True)

    

if __name__ == "__main__":
    main()