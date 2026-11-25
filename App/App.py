# Developed by Anupam Chatterjee [https://github.com/AnupamMax-10]
# AI Resume Analyzer & Career Copilot - Modernized UI Edition

import os
import sys

# Ensure both App directory and Repository Root are in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

###### Packages Used ######
import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
import pymysql
import sqlite3
import socket
import platform
import geocoder
import secrets
import io
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
from Courses import (
    ds_course, web_course, android_course, ios_course,
    uiux_course, resume_videos, interview_videos
)
import nltk

try:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception:
    pass

###### Page Configuration ######
logo_icon = os.path.join(BASE_DIR, 'Logo', 'recommend.png')
st.set_page_config(
    page_title="AI Resume Analyzer & Career Copilot",
    page_icon=logo_icon if os.path.exists(logo_icon) else "📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

###### Preprocessing Functions ######

def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-btn">{text}</a>'

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf" style="border-radius:12px; border:1px solid #e2e8f0;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.markdown("### 👨‍🎓 Curated Learning Path & Certifications")
    rec_course = []
    no_of_reco = st.slider('Select Number of Recommended Courses:', 1, 10, 6)
    shuffled = course_list.copy()
    random.shuffle(shuffled)
    cols = st.columns(2)
    for idx, (c_name, c_link) in enumerate(shuffled[:no_of_reco]):
        rec_course.append(c_name)
        with cols[idx % 2]:
            st.markdown(f'''
            <div style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 14px 16px; margin-bottom: 12px;">
                <div style="font-weight: 600; font-size: 14px; margin-bottom: 8px;">🎓 {c_name}</div>
                <a href="{c_link}" target="_blank" style="display: inline-block; font-size: 12px; font-weight: 600; color: #4f46e5; text-decoration: none; padding: 5px 12px; background: rgba(99, 102, 241, 0.12); border-radius: 6px;">Enroll / View Course ↗</a>
            </div>
            ''', unsafe_allow_html=True)
    return rec_course

###### Database Configuration ######

DB_IS_SQLITE = False
connection = None
cursor = None

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='anupam1605',
        db='cv',
        connect_timeout=2
    )
    cursor = connection.cursor()
    DB_IS_SQLITE = False
except Exception:
    db_path = os.path.join(BASE_DIR, 'cv_database.db')
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    DB_IS_SQLITE = True

def insert_data(sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country, act_name, act_mail, act_mob, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses, pdf_name):
    DB_table_name = 'user_data'
    if DB_IS_SQLITE:
        placeholders = ', '.join(['?'] * 23)
        insert_sql = f"INSERT INTO {DB_table_name} VALUES (NULL, {placeholders})"
    else:
        placeholders = ', '.join(['%s'] * 23)
        insert_sql = f"INSERT INTO {DB_table_name} VALUES (0, {placeholders})"
    rec_values = (
        str(sec_token), str(ip_add), str(host_name), str(dev_user), str(os_name_ver),
        str(latlong), str(city), str(state), str(country), str(act_name), str(act_mail),
        str(act_mob), str(name), str(email), str(res_score), str(timestamp),
        str(no_of_pages), str(reco_field), str(cand_level), str(skills),
        str(recommended_skills), str(courses), str(pdf_name)
    )
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def insertf_data(feed_name, feed_email, feed_score, comments, Timestamp):
    DBf_table_name = 'user_feedback'
    if DB_IS_SQLITE:
        placeholders = ', '.join(['?'] * 5)
        insertfeed_sql = f"INSERT INTO {DBf_table_name} VALUES (NULL, {placeholders})"
    else:
        placeholders = ', '.join(['%s'] * 5)
        insertfeed_sql = f"INSERT INTO {DBf_table_name} VALUES (0, {placeholders})"
    rec_values = (str(feed_name), str(feed_email), str(feed_score), str(comments), str(Timestamp))
    cursor.execute(insertfeed_sql, rec_values)
    connection.commit()

###### Custom CSS Injection ######

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Global Card styling */
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        border-radius: 20px;
        padding: 32px 36px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 15px 35px -10px rgba(49, 46, 129, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.15);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    
    .download-btn {
        display: inline-block;
        padding: 10px 22px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
    }
    
    /* Modern Section Header */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-top: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Checklist Items */
    .checklist-card {
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-size: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .checklist-pass {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #065f46;
    }
    .checklist-fail {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        color: #92400e;
    }
    
    /* Button refinement */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    /* Tab refinement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

###### Main Execution Flow ######

def run():
    inject_custom_css()

    ###### Sidebar Navigation & Branding ######
    with st.sidebar:
        img_path = os.path.join(BASE_DIR, 'Logo', 'RESUM.png')
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)
        else:
            st.title("🎯 AI Resume Copilot")

        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        activities = [
            "🚀 Candidate Workspace",
            "💬 Feedback & Ratings",
            "ℹ️ System Architecture",
            "🔐 Admin Intelligence Hub"
        ]
        choice = st.selectbox("Explore Section:", activities, index=0)
        
        st.markdown("---")
        st.markdown('''
        <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 14px; text-align: center;">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #4f46e5; letter-spacing: 0.05em;">Lead Developer</div>
            <div style="font-size: 15px; font-weight: 700; margin: 4px 0 2px 0;">Anupam Chatterjee</div>
            <a href="https://github.com/AnupamMax-10" target="_blank" style="font-size: 12px; color: #6366f1; text-decoration: none; font-weight: 600;">github.com/AnupamMax-10 ↗</a>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
            <div style="text-align: center; margin-top: 16px; font-size: 12px; color: #94a3b8;">
                Visitors Count <img src="https://counter9.stat.ovh/private/freecounterstat.php?c=t2xghr8ak6lfqt3kgru233378jya38dy" title="Free Counter" alt="web counter" width="55px" style="vertical-align: middle;" />
            </div>
        ''', unsafe_allow_html=True)

    ###### Database Schema Verification ######
    if not DB_IS_SQLITE:
        cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                ID INT NOT NULL AUTO_INCREMENT,
                sec_token varchar(20) NOT NULL,
                ip_add varchar(50) NULL,
                host_name varchar(50) NULL,
                dev_user varchar(50) NULL,
                os_name_ver varchar(50) NULL,
                latlong varchar(50) NULL,
                city varchar(50) NULL,
                state varchar(50) NULL,
                country varchar(50) NULL,
                act_name varchar(50) NOT NULL,
                act_mail varchar(50) NOT NULL,
                act_mob varchar(20) NOT NULL,
                Name varchar(500) NOT NULL,
                Email_ID VARCHAR(500) NOT NULL,
                resume_score VARCHAR(8) NOT NULL,
                Timestamp VARCHAR(50) NOT NULL,
                Page_no VARCHAR(5) NOT NULL,
                Predicted_Field BLOB NOT NULL,
                User_level BLOB NOT NULL,
                Actual_skills BLOB NOT NULL,
                Recommended_skills BLOB NOT NULL,
                Recommended_courses BLOB NOT NULL,
                pdf_name varchar(50) NOT NULL,
                PRIMARY KEY (ID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback (
                ID INT NOT NULL AUTO_INCREMENT,
                feed_name varchar(50) NOT NULL,
                feed_email VARCHAR(50) NOT NULL,
                feed_score VARCHAR(5) NOT NULL,
                comments VARCHAR(100) NULL,
                Timestamp VARCHAR(50) NOT NULL,
                PRIMARY KEY (ID)
            );
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                sec_token TEXT NOT NULL,
                ip_add TEXT,
                host_name TEXT,
                dev_user TEXT,
                os_name_ver TEXT,
                latlong TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                act_name TEXT NOT NULL,
                act_mail TEXT NOT NULL,
                act_mob TEXT NOT NULL,
                Name TEXT NOT NULL,
                Email_ID TEXT NOT NULL,
                resume_score TEXT NOT NULL,
                Timestamp TEXT NOT NULL,
                Page_no TEXT NOT NULL,
                Predicted_Field TEXT NOT NULL,
                User_level TEXT NOT NULL,
                Actual_skills TEXT NOT NULL,
                Recommended_skills TEXT NOT NULL,
                Recommended_courses TEXT NOT NULL,
                pdf_name TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                feed_name TEXT NOT NULL,
                feed_email TEXT NOT NULL,
                feed_score TEXT NOT NULL,
                comments TEXT,
                Timestamp TEXT NOT NULL
            );
        """)
        connection.commit()

    ###### Hero Banner (Global) ######
    st.markdown('''
    <div class="hero-card">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="display: inline-block; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(8px); padding: 4px 14px; border-radius: 9999px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                    ⚡ AI Resume Analyzer & Career Copilot v2.0
                </div>
                <h1 style="margin: 0; font-size: 32px; font-weight: 800; letter-spacing: -0.02em; color: #ffffff;">
                    Transform Your Resume with Smart Career AI
                </h1>
                <p style="margin: 8px 0 0 0; font-size: 15px; color: #c7d2fe; max-width: 680px; line-height: 1.5;">
                    Real-time Natural Language Processing, predictive ATS scoring, domain alignment, and intelligent skill gap recommendations.
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 12px; color: #a5b4fc; margin-bottom: 4px;">Engineered by</div>
                <div style="font-size: 17px; font-weight: 700; color: #ffffff;">Anupam Chatterjee</div>
                <a href="https://github.com/AnupamMax-10" target="_blank" style="display: inline-block; margin-top: 6px; font-size: 12px; color: #ffffff; background: rgba(255,255,255,0.18); padding: 4px 12px; border-radius: 6px; text-decoration: none; font-weight: 600;">GitHub Profile ↗</a>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    ###### 1. CANDIDATE WORKSPACE ######
    if "Candidate" in choice:
        st.markdown("### 📝 Candidate Details & Document Upload")
        st.markdown("Please input your contact information and submit your resume in PDF format for real-time NLP analysis.")

        col_inp1, col_inp2, col_inp3 = st.columns(3)
        with col_inp1:
            act_name = st.text_input('Full Name *', placeholder='e.g. John Doe')
        with col_inp2:
            act_mail = st.text_input('Email Address *', placeholder='e.g. john@example.com')
        with col_inp3:
            act_mob = st.text_input('Contact Number *', placeholder='e.g. +91 9876543210')

        sec_token = secrets.token_urlsafe(12)
        try:
            host_name = socket.gethostname()
            ip_add = socket.gethostbyname(host_name)
        except Exception:
            host_name = 'cloud-host'
            ip_add = '127.0.0.1'

        try:
            dev_user = os.getlogin()
        except Exception:
            dev_user = os.environ.get('USER', os.environ.get('USERNAME', 'web_user'))

        os_name_ver = f"{platform.system()} {platform.release()}"

        try:
            g = geocoder.ip('me')
            latlong = g.latlng
            geolocator = Nominatim(user_agent="ai_resume_analyzer", timeout=5)
            location = geolocator.reverse(latlong, language='en') if latlong else None
            address = location.raw['address'] if location else {}
            city = address.get('city', '')
            state = address.get('state', '')
            country = address.get('country', '')
        except Exception:
            latlong = [0.0, 0.0]
            city = 'NA'
            state = 'NA'
            country = 'NA'

        st.markdown("---")
        pdf_file = st.file_uploader("📂 Select Resume (PDF Format)", type=["pdf"], help="Upload your resume document in PDF format to receive instant ATS evaluation and course recommendations.")

        if pdf_file is not None:
            with st.spinner('🤖 AI Engine is extracting entities, matching skills, and computing ATS metrics...'):
                upload_dir = os.path.join(BASE_DIR, 'Uploaded_Resumes')
                os.makedirs(upload_dir, exist_ok=True)
                save_image_path = os.path.join(upload_dir, pdf_file.name)
                pdf_name = pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                
                resume_data = ResumeParser(save_image_path).get_extracted_data()
                resume_text = pdf_reader(save_image_path)

            if resume_data:
                # Experience Level Determination
                cand_level = ''
                if resume_data.get('no_of_pages', 0) < 1:
                    cand_level = "Fresher"
                elif any(term in resume_text for term in ['INTERNSHIP', 'INTERNSHIPS', 'Internship', 'Internships']):
                    cand_level = "Intermediate"
                elif any(term in resume_text for term in ['EXPERIENCE', 'WORK EXPERIENCE', 'Experience', 'Work Experience']):
                    cand_level = "Experienced"
                else:
                    cand_level = "Fresher"

                # Skills & Field Prediction
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit']
                web_keyword = ['react', 'django', 'node js', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'asp.net', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'photoshop', 'illustrator', 'after effects', 'premier pro', 'indesign', 'user research']

                recommended_skills = []
                reco_field = 'General Technology'
                rec_course = []

                user_skills = [s.lower() for s in (resume_data.get('skills') or [])]
                
                if any(k in user_skills for k in ds_keyword):
                    reco_field = 'Data Science & AI'
                    recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'ML Algorithms', 'Pytorch', 'Scikit-learn', 'Tensorflow', 'Streamlit', 'Deep Learning', 'Big Data']
                    rec_course_list = ds_course
                elif any(k in user_skills for k in web_keyword):
                    reco_field = 'Web Development'
                    recommended_skills = ['React JS', 'Node JS', 'TypeScript', 'Next.js', 'GraphQL', 'Tailwind CSS', 'Docker', 'PostgreSQL', 'API Development']
                    rec_course_list = web_course
                elif any(k in user_skills for k in android_keyword):
                    reco_field = 'Android Development'
                    recommended_skills = ['Kotlin', 'Jetpack Compose', 'Flutter', 'Room Database', 'Coroutines', 'Clean Architecture', 'CI/CD Pipelines']
                    rec_course_list = android_course
                elif any(k in user_skills for k in ios_keyword):
                    reco_field = 'iOS Development'
                    recommended_skills = ['Swift', 'SwiftUI', 'Combine', 'CoreData', 'CocoaPods', 'XCTest', 'App Store Deployment']
                    rec_course_list = ios_course
                elif any(k in user_skills for k in uiux_keyword):
                    reco_field = 'UI / UX Design'
                    recommended_skills = ['Figma Design Systems', 'User Research', 'Interactive Prototyping', 'Usability Testing', 'Wireframing', 'Design Sprint', 'Micro-interactions']
                    rec_course_list = uiux_course
                else:
                    reco_field = 'General Software Engineering'
                    recommended_skills = ['Data Structures & Algorithms', 'System Design', 'Git Version Control', 'Cloud Fundamentals (AWS/GCP)', 'Unit Testing']
                    rec_course_list = ds_course

                # ATS Checklist & Resume Scoring
                checklist = [
                    ("Career Objective / Summary", any(t in resume_text for t in ['Objective', 'Summary']), 6, "Clarifies immediate career direction to recruiters"),
                    ("Educational Credentials", any(t in resume_text for t in ['Education', 'School', 'College', 'Degree']), 12, "Confirms formal academic qualification"),
                    ("Work Experience", any(t in resume_text for t in ['EXPERIENCE', 'Experience', 'Work Experience']), 16, "Demonstrates practical industry contributions"),
                    ("Internships", any(t in resume_text for t in ['INTERNSHIP', 'INTERNSHIPS', 'Internship', 'Internships']), 6, "Reflects real-world team project involvement"),
                    ("Technical Skills Section", any(t in resume_text for t in ['SKILLS', 'SKILL', 'Skills', 'Skill']), 7, "Essential for ATS keyword scanner matching"),
                    ("Project Showcase", any(t in resume_text for t in ['PROJECTS', 'PROJECT', 'Projects', 'Project']), 19, "Proof of execution and applied knowledge"),
                    ("Certifications & Accreditations", any(t in resume_text for t in ['CERTIFICATIONS', 'Certifications', 'Certification']), 12, "Signals specialized domain excellence"),
                    ("Achievements & Honors", any(t in resume_text for t in ['ACHIEVEMENTS', 'Achievements']), 13, "Competitive differentiator from other candidates"),
                    ("Interests & Extracurriculars", any(t in resume_text for t in ['HOBBIES', 'Hobbies', 'INTERESTS', 'Interests']), 9, "Gives insight into personality and culture fit")
                ]

                resume_score = sum(pts for _, found, pts, _ in checklist if found)

                # Save record to database
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = f"{cur_date}_{cur_time}"

                insert_data(
                    str(sec_token), str(ip_add), str(host_name), str(dev_user), str(os_name_ver),
                    str(latlong), str(city), str(state), str(country), str(act_name), str(act_mail),
                    str(act_mob), str(resume_data.get('name') or act_name), str(resume_data.get('email') or act_mail),
                    str(resume_score), timestamp, str(resume_data.get('no_of_pages', 1)), reco_field, cand_level,
                    str(resume_data.get('skills') or []), str(recommended_skills), str([c[0] for c in rec_course_list[:5]]), pdf_name
                )

                ###### Dashboard Overview Cards ######
                st.markdown(f"## 🎉 Resume Intelligence Report for {resume_data.get('name') or act_name or 'Candidate'}")
                
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("🎯 ATS Resume Score", f"{resume_score} / 100", delta="High Impact" if resume_score >= 70 else "Needs Polish")
                with m2:
                    st.metric("💼 Predicted Field", reco_field)
                with m3:
                    st.metric("📈 Experience Level", cand_level)
                with m4:
                    st.metric("📄 Page Length", f"{resume_data.get('no_of_pages', 1)} Page(s)")

                st.markdown("---")

                # Circular Gauge Meter for ATS Score
                col_gauge, col_quickinfo = st.columns([1.2, 1.8])
                with col_gauge:
                    gauge_color = "#10b981" if resume_score >= 75 else ("#f59e0b" if resume_score >= 50 else "#ef4444")
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=resume_score,
                        number={'suffix': "/100", 'font': {'size': 32, 'family': 'Plus Jakarta Sans', 'color': gauge_color}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                            'bar': {'color': gauge_color, 'thickness': 0.28},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 1,
                            'bordercolor': "rgba(226, 232, 240, 0.4)",
                            'steps': [
                                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.15)'},
                                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
                            ],
                            'threshold': {
                                'line': {'color': "#4f46e5", 'width': 4},
                                'thickness': 0.75,
                                'value': 85
                            }
                        }
                    ))
                    fig_gauge.update_layout(
                        height=240,
                        margin=dict(l=20, r=20, t=30, b=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family='Plus Jakarta Sans, sans-serif')
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)

                with col_quickinfo:
                    st.markdown("#### 👤 Extracted Candidate Profile")
                    st.markdown(f"""
                    - **Candidate Name:** `{resume_data.get('name') or 'Not Detected'}`
                    - **Email Address:** `{resume_data.get('email') or 'Not Detected'}`
                    - **Contact Number:** `{resume_data.get('mobile_number') or 'Not Detected'}`
                    - **Qualification / Degree:** `{resume_data.get('degree') or 'Not Detected'}`
                    """)
                    
                    with st.expander("📄 Click to Preview Uploaded Resume Document"):
                        show_pdf(save_image_path)

                ###### Interactive Tabs for In-Depth Analysis ######
                tab_skills, tab_audit, tab_courses, tab_videos = st.tabs([
                    "💡 Skill Alignment",
                    "📋 ATS Checklist Audit",
                    "🎓 Recommended Courses",
                    "📹 Career Masterclasses"
                ])

                with tab_skills:
                    st.markdown("#### 🛠️ Skills Extracted by Natural Language Parser")
                    if resume_data.get('skills'):
                        st_tags(label='Current Skills Detected:', text='Extracted from your resume content', value=resume_data['skills'], key='extracted_skills_tags')
                    else:
                        st.info("No specific technical skills were automatically extracted. Adding a dedicated 'Skills' section will significantly improve ATS discovery.")

                    st.markdown(f"#### 🚀 System Recommended Skills for **{reco_field}**")
                    st.markdown("Incorporate these high-frequency keywords to maximize ATS score and pass screening algorithms:")
                    st_tags(label='Recommended Skills for Target Domain:', text='Skills recommended by System', value=recommended_skills, key='rec_skills_tags')

                with tab_audit:
                    st.markdown("#### 🔍 Resume Section Coverage & Scoring Breakdown")
                    st.markdown("Here is how your resume measures against standard Applicant Tracking System (ATS) parsing requirements:")
                    
                    col_aud1, col_aud2 = st.columns(2)
                    for idx, (title, passed, points, tip) in enumerate(checklist):
                        target_col = col_aud1 if idx % 2 == 0 else col_aud2
                        with target_col:
                            if passed:
                                st.markdown(f'''
                                <div class="checklist-card checklist-pass">
                                    <div><b>✅ {title}</b><br><small style="color:#047857;">{tip}</small></div>
                                    <span style="font-weight:700; color:#065f46;">+{points} pts</span>
                                </div>
                                ''', unsafe_allow_html=True)
                            else:
                                st.markdown(f'''
                                <div class="checklist-card checklist-fail">
                                    <div><b>⚠️ {title} (Missing)</b><br><small style="color:#b45309;">{tip}</small></div>
                                    <span style="font-weight:700; color:#92400e;">0 / {points} pts</span>
                                </div>
                                ''', unsafe_allow_html=True)

                with tab_courses:
                    course_recommender(rec_course_list)

                with tab_videos:
                    st.markdown("### 📹 Handpicked Masterclasses for You")
                    col_v1, col_v2 = st.columns(2)
                    with col_v1:
                        st.markdown("#### ✍️ High-Impact Resume Writing")
                        resume_vid = random.choice(resume_videos)
                        st.video(resume_vid)
                    with col_v2:
                        st.markdown("#### 🎯 Technical Interview Preparation")
                        interview_vid = random.choice(interview_videos)
                        st.video(interview_vid)

                st.balloons()
            else:
                st.error('Could not extract text from the uploaded PDF document. Please verify the file is a readable text-based PDF.')

    ###### 2. FEEDBACK & RATINGS ######
    elif "Feedback" in choice:
        st.markdown("### 💬 User Feedback & Rating Portal")
        st.markdown("We are committed to continuously improving this AI tool. Please leave your rating and feedback below.")

        with st.form("feedback_form"):
            feed_name = st.text_input('Your Name', placeholder='e.g. John Doe')
            feed_email = st.text_input('Your Email', placeholder='e.g. john@example.com')
            feed_score = st.slider('How would you rate your experience? (1 = Poor, 5 = Excellent)', 1, 5, 5)
            comments = st.text_area('Comments & Suggestions', placeholder='Share your thoughts on the recommendations and analysis...')
            submitted = st.form_submit_button("Submit Feedback 🚀")
            
            if submitted:
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = f"{cur_date}_{cur_time}"
                insertf_data(feed_name, feed_email, feed_score, comments, timestamp)
                st.success("Thank you! Your feedback has been recorded successfully.")
                st.balloons()

        st.markdown("---")
        query = 'select * from user_feedback'
        plotfeed_data = pd.read_sql(query, connection)

        if not plotfeed_data.empty and 'feed_score' in plotfeed_data.columns and len(plotfeed_data) > 0:
            col_chart, col_table = st.columns([1, 1.2])
            with col_chart:
                st.markdown("#### 📊 Past User Ratings Distribution")
                labels = plotfeed_data.feed_score.value_counts().index
                values = plotfeed_data.feed_score.value_counts().values
                fig = px.pie(
                    names=labels,
                    values=values,
                    hole=0.45,
                    color_discrete_sequence=px.colors.sequential.Purp
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family='Plus Jakarta Sans, sans-serif'),
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_table:
                st.markdown("#### 💬 Recent User Testimonials")
                cursor.execute('select feed_name, comments, Timestamp from user_feedback order by ID desc limit 10')
                plfeed_cmt_data = cursor.fetchall()
                if plfeed_cmt_data:
                    dff = pd.DataFrame(plfeed_cmt_data, columns=['Candidate', 'Feedback Note', 'Timestamp'])
                    st.dataframe(dff, use_container_width=True)
        else:
            st.info("No ratings have been submitted yet. Be the first to share your thoughts above!")

    ###### 3. SYSTEM ARCHITECTURE (ABOUT) ######
    elif "Architecture" in choice:
        st.markdown("### ℹ️ AI Resume Analyzer System Architecture")
        
        st.markdown("""
        The **AI Resume Analyzer & Career Copilot** is a modular Natural Language Processing system engineered to automate resume screening, evaluate ATS compatibility, and provide personalized career upskilling recommendations.
        """)

        col_arch1, col_arch2, col_arch3 = st.columns(3)
        with col_arch1:
            st.markdown("""
            <div style="background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.2); border-radius:14px; padding:20px; height:100%;">
                <h4 style="margin-top:0;">1. Text Ingestion & OCR</h4>
                <p style="font-size:14px; color:#475569; line-height:1.5;">
                    Extracts raw text streams and font layout boundaries from PDF resumes using <code>pdfminer3</code>, handling multi-column formats and complex character encodings.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_arch2:
            st.markdown("""
            <div style="background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.2); border-radius:14px; padding:20px; height:100%;">
                <h4 style="margin-top:0;">2. Named Entity Recognition</h4>
                <p style="font-size:14px; color:#475569; line-height:1.5;">
                    Utilizes customized <code>spaCy</code> language models and noun chunk tokenizers to isolate applicant entities: Name, Email, Contact, Academic Degrees, and Core Competencies.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_arch3:
            st.markdown("""
            <div style="background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.2); border-radius:14px; padding:20px; height:100%;">
                <h4 style="margin-top:0;">3. Predictive Recommendation</h4>
                <p style="font-size:14px; color:#475569; line-height:1.5;">
                    Clusters extracted skills into specialized professional domains (Data Science, Web, Mobile, UI/UX) and calculates an ATS compatibility score based on standard recruiter criteria.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🛠️ Tech Stack & Technologies Used")
        st.markdown("""
        - **Frontend & App Framework:** Streamlit (Python) with custom CSS & Plotly Visualizations
        - **Natural Language Processing:** SpaCy v2.3.5, PyResParser, NLTK (Stopwords/Wordnet)
        - **Document Parsing:** PDFMiner3, PDFPageInterpreter
        - **Database Layer:** Dual-Mode Architecture (MySQL for production servers, embedded SQLite for 24/7 cloud hosting)
        - **Deployment:** Streamlit Community Cloud (Containerized Debian Linux)
        """)

        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3>Designed & Developed with 🤍 by <b>Anupam Chatterjee</b></h3>
            <p>Connect and explore the code on GitHub:</p>
            <a href="https://github.com/AnupamMax-10/AI_RESUME_ANALYZER" target="_blank" class="download-btn">View GitHub Repository ↗</a>
        </div>
        """, unsafe_allow_html=True)

    ###### 4. ADMIN INTELLIGENCE HUB ######
    else:
        st.markdown("### 🔐 Admin Intelligence Hub")
        st.markdown("Authorized administrative access to candidate records, ATS scoring logs, and analytics.")

        ad_user = st.text_input("Administrator Username", placeholder="Enter admin username")
        ad_password = st.text_input("Administrator Password", type='password', placeholder="Enter admin password")

        if st.button('Login to Admin Portal 🔓'):
            if ad_user == 'admin' and ad_password == 'admin@resume-analyzer':
                st.success("Authentication successful! Welcome, Anupam.")

                if DB_IS_SQLITE:
                    cursor.execute('''SELECT ID, ip_add, resume_score, Predicted_Field, User_level, city, state, country from user_data''')
                else:
                    cursor.execute('''SELECT ID, ip_add, resume_score, convert(Predicted_Field using utf8), convert(User_level using utf8), city, state, country from user_data''')
                datanalys = cursor.fetchall()
                plot_data = pd.DataFrame(datanalys, columns=['Idt', 'IP_add', 'resume_score', 'Predicted_Field', 'User_Level', 'City', 'State', 'Country'])

                if DB_IS_SQLITE:
                    cursor.execute('''SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob, Predicted_Field, Timestamp, Name, Email_ID, resume_score, Page_no, pdf_name, User_level, Actual_skills, Recommended_skills, Recommended_courses, city, state, country, latlong, os_name_ver, host_name, dev_user from user_data''')
                else:
                    cursor.execute('''SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob, convert(Predicted_Field using utf8), Timestamp, Name, Email_ID, resume_score, Page_no, pdf_name, convert(User_level using utf8), convert(Actual_skills using utf8), convert(Recommended_skills using utf8), convert(Recommended_courses using utf8), city, state, country, latlong, os_name_ver, host_name, dev_user from user_data''')
                data = cursor.fetchall()

                df = pd.DataFrame(data, columns=[
                    'ID', 'Token', 'IP Address', 'Candidate Name', 'Email', 'Contact', 'Predicted Domain',
                    'Timestamp', 'Extracted Name', 'Extracted Email', 'ATS Score', 'Pages', 'File Name',
                    'Experience Level', 'Extracted Skills', 'Recommended Skills', 'Courses',
                    'City', 'State', 'Country', 'Coordinates', 'OS Version', 'Host Name', 'Dev User'
                ])

                # KPI Metrics
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.metric("Total Resumes Analyzed", len(df))
                with k2:
                    avg_score = round(pd.to_numeric(df['ATS Score'], errors='coerce').mean(), 1) if not df.empty else 0
                    st.metric("Average ATS Score", f"{avg_score}/100")
                with k3:
                    top_field = df['Predicted Domain'].mode()[0] if not df.empty and not df['Predicted Domain'].empty else "N/A"
                    st.metric("Top Candidate Domain", top_field)
                with k4:
                    exp_count = (df['Experience Level'] == 'Experienced').sum() if not df.empty else 0
                    st.metric("Experienced Candidates", exp_count)

                st.markdown("---")
                tab_table, tab_charts = st.tabs(["👥 Candidate Records", "📊 Visual Analytics"])

                with tab_table:
                    st.markdown("#### Detailed Candidate Database")
                    st.dataframe(df, use_container_width=True)
                    st.markdown(get_csv_download_link(df, 'Candidate_Intelligence_Report.csv', '📥 Download Full Data (CSV)'), unsafe_allow_html=True)

                with tab_charts:
                    if not plot_data.empty:
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("##### 🎯 Predicted Domain Distribution")
                            fig_field = px.pie(
                                plot_data,
                                names='Predicted_Field',
                                color_discrete_sequence=px.colors.sequential.Viridis,
                                hole=0.35
                            )
                            fig_field.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family='Plus Jakarta Sans'))
                            st.plotly_chart(fig_field, use_container_width=True)

                        with c2:
                            st.markdown("##### 📈 Candidate Experience Levels")
                            fig_exp = px.pie(
                                plot_data,
                                names='User_Level',
                                color_discrete_sequence=px.colors.sequential.Sunset,
                                hole=0.35
                            )
                            fig_exp.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family='Plus Jakarta Sans'))
                            st.plotly_chart(fig_exp, use_container_width=True)
                    else:
                        st.info("No candidate records found yet to generate visual charts.")
            else:
                st.error("Invalid administrator credentials provided.")

if __name__ == '__main__':
    run()
