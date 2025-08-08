# Import the necessary libraries
import streamlit as st
import google.generativeai as genai
import os

# --- Step 1: Configure the API Key ---
# It's best practice to set your API key as an environment variable.
# For this example, we will use Streamlit's secrets management, which is secure.
# If that fails, we'll try a direct paste for testing.

try:
    # Recommended: Use Streamlit's secrets management
    # To use this, create a file .streamlit/secrets.toml and add:
    # GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
    API_KEY = st.secrets["your api key"]
except:
    # Fallback for testing: Paste your key directly
    # WARNING: Do not share your code publicly with the key pasted here.
    API_KEY = "your api key"

# If the API_KEY is still the placeholder, show an error.
if API_KEY == "PASTE_YOUR_API_KEY_HERE" or not API_KEY:
    st.error("🛑 API Key not found! Please paste your Gemini API key in the code.")
    st.stop() # Stop the app if the key is missing

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error configuring the Gemini API: {e}")
    st.stop()


# --- Step 2: Function to Call the AI Model ---
def generate_resume_content(name, job_title, email, phone, linkedin, degree, college, grad_year, experience, skills, projects):
    """
    Generates resume content by sending a detailed prompt to the Gemini API.
    """
    # This is the detailed instruction for the AI model
    prompt = f"""
    Act as an expert resume writer and career coach. Your task is to generate a professional, complete, and well-formatted resume in Markdown format based on the user's provided details.

    *User's Provided Details:*
    - *Name:* {name}
    - *Desired Job Title:* {job_title}
    - *Contact:* Email: {email}, Phone: {phone}, LinkedIn: {linkedin}
    - *Education:* {degree} from {college}, Graduated: {grad_year}
    - *Skills:* {skills}
    - *Work Experience:*
    {experience}
    - *Projects:*
    {projects}

    *Instructions:*
    1.  *Format:* Create a full resume in clean, professional Markdown.
    2.  *Contact Information:* Display the user's provided contact information neatly under their name.
    3.  *Professional Summary:* Write a compelling 3-4 sentence summary tailored to the desired job title, incorporating the user's skills and experience.
    4.  *Skills Section:* Neatly format the skills provided by the user into a bulleted list.
    5.  *Experience Section:* Take the user's raw experience text and re-write it professionally. For each role, use action verbs to start each bullet point. Focus on achievements and responsibilities.
    6.  *Projects Section:* If the user has provided project details, create a "Projects" section. Format it similarly to the experience section, highlighting the project's goal and the user's role. If the projects field is empty, omit this section.
    7.  *Education Section:* Format the user's degree, college, and graduation year clearly.

    Ensure the final output is a polished, professional resume ready for job applications.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the resume: {e}"


# --- Step 3: Build the Streamlit User Interface (UI) ---

st.set_page_config(page_title="Smart Resume Generator", page_icon="📄")

st.title("📄 Smart Resume Generator")
st.write("Fill in your details below and let AI craft a professional resume for you.")

# Input form for user details
with st.form("resume_form"):
    st.header("Personal Information")
    name = st.text_input("Your Full Name")
    job_title = st.text_input("Your Desired Job Title (e.g., 'Data Scientist')")
    email = st.text_input("Your Email Address")
    phone = st.text_input("Your Phone Number")
    linkedin = st.text_input("Your LinkedIn Profile URL (Optional)")
    
    st.header("Education")
    degree = st.text_input("Your Degree (e.g., 'Bachelor of Technology in Electronics')")
    college = st.text_input("Your College/University Name")
    grad_year = st.text_input("Your Graduation Year (e.g., '2024')")

    st.header("Experience")
    experience = st.text_area("Describe your work experience and internships. List different jobs, responsibilities, and achievements.", height=200)

    st.header("Projects")
    projects = st.text_area("Describe your personal or academic projects. (Optional)", height=150)

    st.header("Skills")
    skills = st.text_input("List your key skills, separated by commas (e.g., Python, SQL, Machine Learning, Communication)")

    # The submit button for the form
    submitted = st.form_submit_button("Generate My Resume")
    # --- Step 4: Handle Form Submission ---

if submitted:
    # Check for required fields
    if name and job_title and email and phone and degree and college and grad_year and experience and skills:
        with st.spinner(f"Crafting a resume for a {job_title}..."):
            generated_resume = generate_resume_content(name, job_title, email, phone, linkedin, degree, college, grad_year, experience, skills, projects)
            
            st.markdown("---")
            st.header("Your AI-Generated Resume")
            st.markdown(generated_resume)
    else:
        # If any required field is missing, show a warning message

        st.warning("Please fill in all required fields to generate your resume. LinkedIn and Projects are optional.")
