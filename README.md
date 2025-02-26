# ALT Works AI

Welcome to **ALT Works AI**, a streamlined dashboard designed to showcase the innovative projects of AlphaTech Logics. This app dynamically pulls data from the organization's GitHub repositories and displays each project with modern, interactive cards. Each card features clickable icons linking to the GitHub repository and the live demo of the project, along with a short description that appears on hover.

---

## Features

- **Dynamic Data Fetching:** Retrieves real-time project data using the GitHub API.
- **Interactive Dashboard:** Displays projects in a responsive grid layout with modern card designs.
- **Icon-Based Navigation:** Uses FontAwesome icons for intuitive navigation to GitHub and live demos.
- **Custom Tooltips:** Each project card shows a short description on hover for quick insights.
- **Easy Demo URL Management:** Manually map demo URLs for each project to ensure accurate linking.

---

## Technologies Used

- **[Streamlit](https://streamlit.io/):** For creating the interactive web application.
- **Python:** The core programming language.
- **GitHub API:** For fetching repository data dynamically.
- **FontAwesome:** For stylish, scalable icons.

---

## Setup & Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/alphatechlogics/Atlworks.ai.git
   cd Atlworks.ai
   ```

2. **Create a Virtual Environment & Install Dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

4. **Customize Demo URLs:**
   - Update the `demo_urls` dictionary in the code with your live demo links for each repository.

---

## Application Structure

- **app.py:** Main Streamlit application file that fetches GitHub data and renders the dashboard.
- **README.md:** This file, providing an overview and setup instructions.
- **requirements.txt:** Lists all Python dependencies.

---

## Contact

For any questions or suggestions, feel free to contact us at [contact@alphatechlogics.com](mailto:contact@alphatechlogics.com).

---

**ALT Works AI** is proudly developed by **AlphaTech Logics** – accelerating business development through scalable digital products powered by Artificial Intelligence.
