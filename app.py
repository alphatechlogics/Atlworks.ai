import os
import streamlit as st
import requests
import base64

# Function to convert an image to a Base64 string


def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Get Base64 string of the logo image
logo_base64 = get_base64_image("black_without-tagline.png")

# Set page configuration
st.set_page_config(page_title="AlphaTech Logics Dashboard", layout="wide")

# Load FontAwesome for icons
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)

# Inject custom CSS with Times New Roman font style
st.markdown(
    f"""
    <style>
    body {{
        background-color: #f0f2f6;
        font-family: 'Times New Roman', Times, serif;
    }}

    /* Header with a black background and centered logo */
    .header {{
        background: #000000 url("data:image/png;base64,{logo_base64}") no-repeat center;
        background-size: contain;
        color: white;
        padding: 40px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 30px;
    }}

    /* Organization info section styling */
    .org-info {{
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    /* Headings in your brand color */
    .org-info h2, .org-info h3 {{
        color: #A917FE;
    }}

    /* Repository card styling */
    .repo-card {{
        /* The background-color will be overridden by inline style */
        padding: 20px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        overflow: hidden;
    }}
    .repo-card:hover {{
        transform: translateY(-5px);
    }}
    .repo-card h3 {{
        margin-top: 0;
        color: #A917FE;
        font-size: 1.5em;
    }}

    .icons {{
        margin-top: 10px;
    }}
    .icons a {{
        margin-right: 15px;
        color: #A917FE;
        transition: color 0.2s;
        font-size: 1.75em;
    }}
    .icons a:hover {{
        color: #A917FE;
    }}

    .tooltip {{
        display: none;
        pointer-events: none;
        position: absolute;
        bottom: 10px;
        left: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.75);
        color: #fff;
        padding: 8px;
        border-radius: 5px;
        font-size: 0.9em;
        line-height: 1.2;
        z-index: 10;
    }}
    .repo-card:hover .tooltip {{
        display: block;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section with only the logo (no text)
st.markdown(
    """
    <div class="header">
        <h1></h1>
        <h1></h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Organization Information Section
st.markdown(
    """
    <div class="org-info">
        <h2>About Us</h2>
        <p>
            At AlphaTech Logics, we specialize in accelerating business development through scalable digital products powered by Artificial Intelligence.
            Our expertise spans AI-driven solutions, modernizing applications, and securing systems to ensure your business thrives in an increasingly digital world.
        </p>
        <h3>Our Core Services:</h3>
        <ul>
            <li>🤖 <strong>AI</strong>: Harness AI to spur creativity, automate tasks, and uncover new insights.</li>
            <li>🔐 <strong>Cyber Security</strong>: Fortify your defenses and ensure data security.</li>
            <li>💻 <strong>Application Development</strong>: Build or enhance high-performing, scalable digital products.</li>
            <li>⚙️ <strong>Application Modernization</strong>: Maximize system performance and optimize user experience.</li>
            <li>🧑‍💻 <strong>Discovery Workshops</strong>: Define project scopes, clarify technology strategies, and craft execution plans.</li>
            <li>☁️ <strong>Cloud Engineering & Migration</strong>: Seamlessly migrate to the cloud for efficiency and scalability.</li>
        </ul>
        <h3>What We Do</h3>
        <p>
            We streamline applications for cost savings and cloud efficiency, help businesses evolve through AI, and ensure robust defense with cutting-edge cyber security solutions.
        </p>
        <h3>Key Achievements & Stats</h3>
        <ul>
            <li>📉 <strong>Knowles Case Study</strong>: Reduced costs by 40% and improved inquiry response time by 60%.</li>
            <li>⏱️ <strong>Time to Market</strong>: Minimized development time, ensuring your product stands out.</li>
            <li>🏆 10+ Years of driving growth</li>
            <li>👨‍💻 100+ Technical Experts</li>
            <li>🚀 150+ Projects Delivered</li>
            <li>⭐ 50+ Satisfied Customers</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Display Projects Section Title
st.markdown("<h2 style='color:#A917FE;'>Our Projects</h2>",
            unsafe_allow_html=True)

# GitHub API endpoint for organization repositories
ORG_NAME = 'alphatechlogics'
GITHUB_API_URL = f'https://api.github.com/orgs/{ORG_NAME}/repos'

# Get GitHub token from environment variable or Streamlit secrets
github_token = os.getenv("GITHUB_TOKEN")
try:
    token = st.secrets.get("GITHUB_TOKEN")
    if token:
        github_token = token
except Exception:
    pass

# Set up headers to use authentication if a token is available
headers = {}
if github_token:
    headers["Authorization"] = f"Bearer {github_token}"
    headers["Accept"] = "application/vnd.github+json"
    headers["X-GitHub-Api-Version"] = "2022-11-28"

# Fetch repositories data from GitHub
response = requests.get(GITHUB_API_URL, headers=headers)
all_repos = response.json()

# Mapping of repository names to their demo URLs
demo_urls = {
    "AIAvatar": "https://aiavatar.streamlit.app/",
    "Alpha-navigator": "https://alpha-navigator.streamlit.app/",
    "BiomedicalLiteratureHelperWithBioGPT": "https://biomedicalliteratureapperwithbiogpt-dem0.streamlit.app/",
    "BlogCraft": "https://blogcrafts.streamlit.app/",
    "BrainTumorPrediction": "https://braintumorpredictions.streamlit.app/",
    "BreastCancerDetection-": "https://breastcancerdetection-demo.streamlit.app/",
    "CarNumberPlateDetection": "https://carnumberplatedetection-demo.streamlit.app/",
    "ConstrucSafe": "https://construcsafe-demo.streamlit.app/",
    "Doctor-AI": "https://doctor-ai-demo.streamlit.app/",
    "FraudulentDetection": "https://fraudulentdetection-demo.streamlit.app/",
    "garbage-sorting-image-classification": "https://garbage-sorting-image-classification-demo.streamlit.app/",
    "HandWrittenDigitalsClassification": "https://handwrittendigitalsclassification-demo.streamlit.app/",
    "ICUMonitorScreenReader": "https://icu-monitor-screenreader-demo.streamlit.app/",
    "LangGraphAgent": "https://langgraphagent.streamlit.app/",
    "MathTutor": "https://math-tutor1.streamlit.app/",
    "MedicalDiseasePredictionRecommendation": "https://medicaldiseasepredictionrecommendation.streamlit.app/",
    "RAG": "https://multimodal-rag-demo.streamlit.app/",
    "PlantLeafDiseaseDetection": "https://plantleafdiseasedetection-demo.streamlit.app/",
    "QandA-System": "https://questionanswerssystem.streamlit.app/",
    "StockMarketPricePrediction": "https://stockmarketpriceprediction-demo1.streamlit.app/",
    "Text-Classification": "https://text-classification-dpkxu7ytn9vdg7yqj9fpsk.streamlit.app/",
    "Text-Summarization": "https://text-summarization-demo.streamlit.app/",
    "Text-to-Image-Generation-via-DALL-E3-StableDiffusion": "https://text-to-image-generation-via-dall-e3-stablediffusion.streamlit.app/"
}

# Manually provided descriptions for specific repositories
manual_descriptions = {
    "ICUMonitorScreenReader": "Welcome to the ICU Monitor Data Extraction app! This app utilizes OpenAI's Vision API to analyze ICU monitor images, extract vital signs like heart rate (HR), blood pressure (BP), oxygen saturation (SpO2), respiratory rate (RR), temperature, and more. The app displays these vital signs in a user-friendly table format.",
    "StockMarketPricePrediction": "Welcome to the Stock Price Prediction App, an interactive web application designed to forecast future stock prices using advanced time-series modeling techniques. This application leverages an intuitive interface, real-time data retrieval, and an AI-based forecasting library to provide quick and accessible insights for users interested in analyzing and predicting stock market behavior.",
    "CarNumberPlateDetection": "Welcome to the Vehicle Number Plate Detection System! 🚗 This project leverages the powerful YOLOv8 framework to accurately detect vehicle number plates in images. Whether you're developing traffic management solutions, parking lot systems, or security surveillance tools, this system provides a robust foundation for your computer vision applications.",
    "BreastCancerDetection-": "Welcome to the Breast Tumor Detection project! This project demonstrates how to build, train, and deploy a deep learning model that detects breast tumors from mammogram images.",
    "BrainTumorPrediction": "This tutorial will guide you through setting up the MRI 🩺 Image Classification app locally. The app allows users to upload MRI images, predict classifications, and visualize results, including tumor contouring. 🎨",
    "HandWrittenDigitalsClassification": "Welcome to the MNIST Digit Recognition project! This repository demonstrates a complete workflow for building, training, and deploying a neural network to recognize handwritten digits from the MNIST dataset. Additionally, it includes an interactive Streamlit web app for showcasing the model's capabilities.",
    "BiomedicalLiteratureHelperWithBioGPT": "Welcome to the Biomedical Literature Helper with BioGPT! This Streamlit application leverages the power of the BioGPT language model to assist researchers, clinicians, and enthusiasts in generating and mining biomedical texts efficiently. Whether you're drafting research papers, summarizing complex biomedical information, or exploring new hypotheses, this tool is here to streamline your workflow.",
    "AIAvatar": "Welcome to the LightX AI Services app! This Streamlit application lets you transform your personal photo into either a personalized AI Avatar or a professional full-body cartoon character using the LightX APIs."
}

# --- Safe Filtering of Repositories ---
if isinstance(all_repos, list):
    safe_repos = [repo for repo in all_repos if isinstance(
        repo, dict) and 'name' in repo]
    repos = [repo for repo in safe_repos if repo['name'] in demo_urls]
    # Sort repositories alphabetically (case-insensitive)
    repos = sorted(repos, key=lambda x: x['name'].lower())
else:
    st.error("GitHub API response is not a list. Response:")
    st.write(all_repos)
    repos = []

# Define grid layout for project cards (4 per row)
cols_per_row = 4
rows_list = [repos[i: i + cols_per_row]
             for i in range(0, len(repos), cols_per_row)]

# List of light background colors
light_colors = ["#f7f7f7", "#e6f7ff",
                "#e8ffe8", "#fff0e6", "#f0f8ff", "#fdfd96"]
card_index = 0

for row in rows_list:
    cols = st.columns(cols_per_row)
    for idx, repo in enumerate(row):
        bg_color = light_colors[card_index % len(light_colors)]
        card_index += 1
        with cols[idx]:
            repo_name = repo['name']
            repo_url = repo['html_url']
            demo_url = demo_urls.get(repo_name, "#")
            # Use the manual description if available; otherwise, fallback to the repo's description or a default message.
            description = manual_descriptions.get(repo_name, repo.get(
                'description') or "No description provided.")
            st.markdown(
                f"""
                <div class="repo-card" style="background-color: {bg_color};">
                    <h3>{repo_name}</h3>
                    <div class="icons">
                        <a href="{repo_url}" target="_blank" title="View on GitHub"><i class="fab fa-github"></i></a>
                        <a href="{demo_url}" target="_blank" title="View Demo"><i class="fas fa-external-link-alt"></i></a>
                    </div>
                    <div class="tooltip">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
