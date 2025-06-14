import os
import streamlit as st
import requests
import base64
import re
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple

# Load environment variables from .env file
load_dotenv()

# Configuration
ORG_NAME = 'alphatechlogics'
REPOS_PER_PAGE = 8  # 2 columns × 4 rows
COLS_PER_ROW = 2

class GitHubProjectsDashboard:
    def __init__(self):
        self.github_token = self._get_github_token()
        self.headers = self._setup_headers()
        
    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from environment variable or Streamlit secrets"""
        token = os.getenv("GITHUB_TOKEN")
        try:
            secret_token = st.secrets.get("GITHUB_TOKEN")
            if secret_token:
                token = secret_token
        except Exception:
            pass
        return token
    
    def _setup_headers(self) -> Dict[str, str]:
        """Set up headers for GitHub API requests"""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        return headers
    
    def fetch_repositories(self) -> List[Dict]:
        """Fetch all repositories (public and private) from GitHub"""
        all_repos = []
        page = 1
        
        while True:
            # Fetch both public and private repos
            url = f'https://api.github.com/orgs/{ORG_NAME}/repos'
            params = {
                'type': 'all',  # Include both public and private
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 100,
                'page': page
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                st.error(f"Failed to fetch repositories: {response.status_code}")
                if response.status_code == 401:
                    st.error("Authentication failed. Please check your GitHub token.")
                break
            
            repos = response.json()
            if not repos:
                break
                
            all_repos.extend(repos)
            page += 1
        
        return all_repos
    
    def extract_readme_info(self, repo_name: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract Streamlit URL and first image from README.md file"""
        readme_url = f'https://api.github.com/repos/{ORG_NAME}/{repo_name}/readme'
        
        try:
            response = requests.get(readme_url, headers=self.headers)
            if response.status_code == 200:
                readme_data = response.json()
                # Decode base64 content
                content = base64.b64decode(readme_data['content']).decode('utf-8')
                
                # Look for Streamlit URLs in various formats
                streamlit_url = None
                streamlit_patterns = [
                    r'https://[^.]+\.streamlit\.app[^\s\)]*',
                    r'https://share\.streamlit\.io/[^\s\)]*',
                    r'\[.*?\]\((https://[^.]+\.streamlit\.app[^\)]*)\)',
                    r'\[.*?\]\((https://share\.streamlit\.io[^\)]*)\)'
                ]
                
                for pattern in streamlit_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        streamlit_url = matches[0]
                        break
                
                # Look for images in README
                image_url = None
                image_patterns = [
                    r'!\[.*?\]\((https://[^\)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)',
                    r'!\[.*?\]\(([^)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)',
                    r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>',
                ]
                
                for pattern in image_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        img_url = matches[0]
                        # Convert relative URLs to absolute
                        if not img_url.startswith('http'):
                            if img_url.startswith('./'):
                                img_url = img_url[2:]
                            image_url = f'https://raw.githubusercontent.com/{ORG_NAME}/{repo_name}/main/{img_url}'
                        else:
                            image_url = img_url
                        break
                
                return streamlit_url, image_url
                
        except Exception as e:
            pass  # Silently handle errors to avoid cluttering the UI
        
        return None, None
    
    def get_base64_image(self, image_path: str) -> str:
        """Convert an image to a Base64 string"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except FileNotFoundError:
            # Return a placeholder or empty string if image not found
            return ""
    
    def render_custom_css(self, logo_base64: str):
        """Render custom CSS styles"""
        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
            }}

            .main > div {{
                padding-top: 2rem;
            }}

            .header {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                background-image: url("data:image/png;base64,{logo_base64}");
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;
                color: white;
                padding: 60px 40px;
                text-align: center;
                border-radius: 20px;
                margin-bottom: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }}

            .org-info {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                padding: 40px;
                border-radius: 20px;
                margin-bottom: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
            }}
            
            .org-info h2, .org-info h3 {{
                color: #6366f1;
                font-weight: 600;
            }}

            .filter-container {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
            }}

            .filter-row {{
                display: flex;
                gap: 20px;
                align-items: end;
                flex-wrap: wrap;
                margin-top: 20px;
            }}

            .filter-group {{
                display: flex;
                flex-direction: column;
                gap: 8px;
                min-width: 150px;
            }}

            .filter-label {{
                font-weight: 600;
                color: #374151;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}

            .search-container {{
                margin-bottom: 25px;
            }}

            .search-container input {{
                width: 100% !important;
                padding: 16px 20px !important;
                border: 2px solid #e5e7eb !important;
                border-radius: 12px !important;
                font-size: 16px !important;
                background: rgba(255,255,255,0.9) !important;
                transition: all 0.3s ease !important;
            }}

            .search-container input:focus {{
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
                outline: none !important;
            }}

            .repo-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                padding: 20px;
                margin: 15px 10px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                overflow: hidden;
                height: 320px;
                display: flex;
                flex-direction: column;
                border: 1px solid rgba(255,255,255,0.2);
                position: relative;
            }}
            
            .repo-card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 20px 50px rgba(0,0,0,0.15);
            }}

            .repo-image {{
                width: 100%;
                height: 100px;
                object-fit: cover;
                border-radius: 12px;
                margin-bottom: 12px;
                background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9ca3af;
                font-size: 12px;
                border: 2px dashed #d1d5db;
                flex-shrink: 0;
            }}

            .repo-image img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 12px;
            }}

            .repo-content {{
                display: flex;
                flex-direction: column;
                flex-grow: 1;
                min-height: 0;
            }}
            
            .repo-card h3 {{
                margin: 0 0 8px 0;
                color: #1f2937;
                font-size: 16px;
                font-weight: 600;
                line-height: 1.3;
                display: flex;
                align-items: center;
                gap: 8px;
                flex-shrink: 0;
            }}
            
            .repo-description {{
                color: #6b7280;
                font-size: 13px;
                line-height: 1.4;
                flex-grow: 1;
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                margin-bottom: 12px;
                min-height: 60px;
            }}
            
            .repo-description.no-description {{
                color: #9ca3af;
                font-style: italic;
            }}

            .repo-footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: auto;
                padding-top: 12px;
                border-top: 1px solid #e5e7eb;
                flex-shrink: 0;
            }}

            .icons {{
                display: flex;
                gap: 10px;
                margin-left: auto;
            }}
            
            .icons a {{
                color: #6366f1;
                transition: all 0.2s ease;
                font-size: 16px;
                text-decoration: none;
                padding: 6px;
                border-radius: 6px;
                background: rgba(99, 102, 241, 0.1);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 32px;
                height: 32px;
            }}
            
            .icons a:hover {{
                color: white;
                background: #6366f1;
                transform: scale(1.1);
            }}
            
            .icons span {{
                font-size: 16px;
                color: #d1d5db;
                padding: 6px;
                border-radius: 6px;
                background: rgba(209, 213, 219, 0.1);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 32px;
                height: 32px;
            }}
            
            .pagination {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 40px 0;
                gap: 15px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .pagination-info {{
                color: #6b7280;
                font-size: 14px;
                font-weight: 500;
                margin: 0 25px;
                background: rgba(99, 102, 241, 0.1);
                padding: 8px 16px;
                border-radius: 20px;
            }}
            
            .private-badge {{
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
                margin-left: auto;
            }}
            
            .public-badge {{
                background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                color: white;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
                margin-left: auto;
            }}

            .projects-title {{
                color: #1f2937;
                font-size: 32px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 30px;
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            /* Streamlit specific overrides */
            .stSelectbox > div > div > div {{
                background: rgba(255,255,255,0.9) !important;
                border: 2px solid #e5e7eb !important;
                border-radius: 12px !important;
                padding: 8px 12px !important;
            }}

            .stSelectbox > div > div > div:focus-within {{
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            }}

            .stButton > button {{
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 10px 20px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
            }}

            .stButton > button:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
            }}

            div[data-testid="stSidebar"] {{
                display: none;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    def render_header(self):
        """Render the header section"""
        st.markdown(
            """
            <div class="header">
                <h1></h1>
                <h1></h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    def render_org_info(self):
        """Render organization information section"""
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
    
    def render_repository_card(self, repo: Dict, bg_color: str):
        """Render a single repository card"""
        repo_name = repo.get('name', 'Unnamed Repository')
        repo_url = repo.get('html_url', '#')
        
        # Handle missing descriptions safely
        description = repo.get('description')
        if description is None or (isinstance(description, str) and not description.strip()):
            description = '📝 No description provided yet. Click to explore the repository!'
            description_class = 'no-description'
        else:
            description = description.strip()
            description_class = ''
        
        is_private = repo.get('private', False)
        
        # Extract Streamlit URL and image from README
        streamlit_url, image_url = self.extract_readme_info(repo_name)
        
        # Create privacy badge
        privacy_badge = f'<span class="private-badge">Private</span>' if is_private else f'<span class="public-badge">Public</span>'
        
        # Create demo link
        if streamlit_url:
            demo_link = f'<a href="{streamlit_url}" target="_blank" title="View Live Demo"><i class="fas fa-external-link-alt"></i></a>'
        else:
            demo_link = '<span title="No demo available"><i class="fas fa-external-link-alt"></i></span>'
        
        # Create image section
        if image_url:
            image_section = f'<div class="repo-image"><img src="{image_url}" alt="{repo_name} preview" onerror="this.parentElement.innerHTML=\'📷 Preview not available\'"></div>'
        else:
            image_section = '<div class="repo-image">📷 No preview available</div>'
        
        st.markdown(
            f"""
            <div class="repo-card">
                {image_section}
                <div class="repo-content">
                    <h3>{repo_name}</h3>
                    <div class="repo-description {description_class}">{description}</div>
                    <div class="repo-footer">
                        {privacy_badge}
                        <div class="icons">
                            <a href="{repo_url}" target="_blank" title="View on GitHub"><i class="fab fa-github"></i></a>
                            {demo_link}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def apply_filter_and_sort(self, repos: List[Dict], sort_option: str, privacy_filter: str, search_query: str) -> List[Dict]:
        """Apply filtering and sorting to repositories"""
        # First, filter out forks if they don't have descriptions
        filtered_repos = [repo for repo in repos if repo.get('description') or not repo.get('fork', True)]
        
        # Apply privacy filter
        if privacy_filter == "Public Only":
            filtered_repos = [repo for repo in filtered_repos if not repo.get('private', False)]
        elif privacy_filter == "Private Only":
            filtered_repos = [repo for repo in filtered_repos if repo.get('private', False)]
        # "All" doesn't need additional filtering
        
        # Apply search filter
        if search_query:
            search_query_lower = search_query.lower()
            filtered_repos = [
                repo for repo in filtered_repos 
                if (search_query_lower in repo.get('name', '').lower()) or 
                   (repo.get('description') and isinstance(repo.get('description'), str) and search_query_lower in repo.get('description', '').lower())
            ]
        
        # Apply sorting
        if sort_option == "Latest":
            return sorted(filtered_repos, key=lambda x: x.get('updated_at', ''), reverse=True)
        elif sort_option == "Oldest":
            return sorted(filtered_repos, key=lambda x: x.get('updated_at', ''))
        elif sort_option == "A-Z":
            return sorted(filtered_repos, key=lambda x: x.get('name', '').lower())
        elif sort_option == "Z-A":
            return sorted(filtered_repos, key=lambda x: x.get('name', '').lower(), reverse=True)
        else:
            return filtered_repos
    
    def render_filter_section(self) -> Tuple[str, str, str]:
        """Render the filter section and return selected filters"""
        st.markdown('<h2 class="projects-title">Our Projects</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        
        # Search bar
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_query = st.text_input(
            "",
            placeholder="🔍 Search repositories by name or description...",
            key="search_input",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter row
        st.markdown('<div class="filter-row">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.markdown('<div class="filter-group">', unsafe_allow_html=True)
            st.markdown('<div class="filter-label">Sort By</div>', unsafe_allow_html=True)
            sort_options = ["Latest", "Oldest", "A-Z", "Z-A"]
            selected_sort = st.selectbox(
                "",
                sort_options,
                index=0,
                key="repo_sort",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="filter-group">', unsafe_allow_html=True)
            st.markdown('<div class="filter-label">Visibility</div>', unsafe_allow_html=True)
            privacy_options = ["All", "Public Only", "Private Only"]
            selected_privacy = st.selectbox(
                "",
                privacy_options,
                index=0,
                key="privacy_filter",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown("")  # Spacer
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close filter-row
        st.markdown('</div>', unsafe_allow_html=True)  # Close filter-container
        
        return selected_sort, selected_privacy, search_query
            
    
    def render_pagination(self, current_page: int, total_pages: int, total_repos: int):
        """Render pagination controls"""
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if current_page > 1:
                if st.button("← Previous"):
                    st.session_state.current_page = current_page - 1
                    st.rerun()
        
        with col2:
            if current_page > 1:
                if st.button("First"):
                    st.session_state.current_page = 1
                    st.rerun()
        
        with col3:
            st.markdown(
                f'<div class="pagination-info">Page {current_page} of {total_pages} ({total_repos} repositories)</div>',
                unsafe_allow_html=True
            )
        
        with col4:
            if current_page < total_pages:
                if st.button("Last"):
                    st.session_state.current_page = total_pages
                    st.rerun()
        
        with col5:
            if current_page < total_pages:
                if st.button("Next →"):
                    st.session_state.current_page = current_page + 1
                    st.rerun()
    
    def run(self):
        """Main function to run the dashboard"""
        # Set page configuration
        st.set_page_config(page_title="AlphaTech Logics Dashboard", layout="wide")
        
        # Get Base64 string of the logo image
        logo_base64 = self.get_base64_image("black_without-tagline.png")
        
        # Render custom CSS
        self.render_custom_css(logo_base64)
        
        # Render header and organization info
        self.render_header()
        self.render_org_info()
        
        # Render filter section and get selected filters
        selected_sort, selected_privacy, search_query = self.render_filter_section()
        
        # Initialize session state for pagination
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Reset page when filters change
        filter_key = f"{selected_sort}_{selected_privacy}_{search_query}"
        if 'previous_filter_key' not in st.session_state:
            st.session_state.previous_filter_key = filter_key
        elif st.session_state.previous_filter_key != filter_key:
            st.session_state.current_page = 1
            st.session_state.previous_filter_key = filter_key
        
        # Fetch repositories
        with st.spinner("Loading repositories..."):
            repos = self.fetch_repositories()
        
        if not repos:
            st.error("No repositories found or failed to fetch repositories.")
            return
        
        # Apply filters and sorting
        filtered_repos = self.apply_filter_and_sort(repos, selected_sort, selected_privacy, search_query)
        
        # Check if no repositories match the filter
        if not filtered_repos:
            st.warning("No repositories match your current filters. Try adjusting your search criteria.")
            return
        
        # Calculate pagination
        total_repos = len(filtered_repos)
        total_pages = (total_repos + REPOS_PER_PAGE - 1) // REPOS_PER_PAGE
        current_page = st.session_state.current_page
        
        # Ensure current page is within bounds
        if current_page > total_pages:
            st.session_state.current_page = 1
            current_page = 1
        
        # Get repositories for current page
        start_idx = (current_page - 1) * REPOS_PER_PAGE
        end_idx = start_idx + REPOS_PER_PAGE
        page_repos = filtered_repos[start_idx:end_idx]
        
        # Display repositories in grid layout
        light_colors = ["#f7f7f7", "#e6f7ff", "#e8ffe8", "#fff0e6", "#f0f8ff", "#fdfd96"]
        
        # Create rows of repositories
        rows_list = [page_repos[i:i + COLS_PER_ROW] for i in range(0, len(page_repos), COLS_PER_ROW)]
        
        card_index = 0
        for row in rows_list:
            cols = st.columns(COLS_PER_ROW)
            for idx, repo in enumerate(row):
                bg_color = light_colors[card_index % len(light_colors)]
                card_index += 1
                with cols[idx]:
                    self.render_repository_card(repo, bg_color)
        
        # Render pagination if there are multiple pages
        if total_pages > 1:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_pagination(current_page, total_pages, total_repos)

# Run the dashboard
if __name__ == "__main__":
    dashboard = GitHubProjectsDashboard()
    dashboard.run()