# AI Resume Analyzer & Career Copilot
# 12-Page Presentation Slide Deck Generator using ReportLab

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI_Resume_Analyzer_Presentation.pdf")

# Custom Canvas for High-End Presentation Background & Footer
class PresentationCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_pages):
        page_num = self._pageNumber
        w, h = landscape(A4)

        # 1. Dark Theme Background
        self.saveState()
        self.setFillColor(colors.HexColor("#090d16"))
        self.rect(0, 0, w, h, fill=1, stroke=0)

        # 2. Subtle Glowing Accents in Corners
        self.setFillColor(colors.HexColor("#1e1b4b"))
        self.circle(w + 30, h + 30, 160, fill=1, stroke=0)
        self.circle(-30, -30, 140, fill=1, stroke=0)

        # Slide 1 (Title slide) has special layout, others have standard header/footer
        if page_num > 1:
            # Top accent line
            self.setStrokeColor(colors.HexColor("#312e81"))
            self.setLineWidth(1)
            self.line(40, h - 35, w - 40, h - 35)

            # Bottom footer line
            self.setStrokeColor(colors.HexColor("#1e293b"))
            self.line(40, 36, w - 40, 36)

            # Footer Left Text
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#818cf8"))
            self.drawString(40, 22, "AI RESUME ANALYZER & CAREER COPILOT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(225, 22, "|   5th Semester Major Project   |   Author: Anupam Chatterjee")

            # Footer Right: Slide Page Number
            self.setFont("Helvetica-Bold", 9)
            self.setFillColor(colors.HexColor("#94a3b8"))
            page_str = f"Slide {page_num:02d} / {total_pages:02d}"
            self.drawRightString(w - 40, 22, page_str)

        self.restoreState()


def build_pdf():
    w, h = landscape(A4)
    # 40pt margins, top 45pt, bottom 45pt
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(A4),
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    style_badge = ParagraphStyle(
        'Badge',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#a5b4fc"),
        backColor=colors.HexColor("#1e1b4b"),
        borderPadding=(4, 8, 4, 8),
        borderRadius=4,
        spaceAfter=6
    )

    style_title = ParagraphStyle(
        'SlideTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#ffffff"),
        spaceAfter=3
    )

    style_subtitle = ParagraphStyle(
        'SlideSubtitle',
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#94a3b8"),
        spaceAfter=14
    )

    style_card_title = ParagraphStyle(
        'CardTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#ffffff"),
        spaceAfter=6
    )

    style_body = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#cbd5e1")
    )

    style_body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#ffffff")
    )

    style_bullet = ParagraphStyle(
        'BulletDark',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#cbd5e1"),
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # SLIDE 1: COVER / TITLE SLIDE
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("<font color='#818cf8'><b>⚡ 5TH SEMESTER MAJOR PROJECT PRESENTATION</b></font>", ParagraphStyle('H1B', fontName='Helvetica-Bold', fontSize=10, leading=12, alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("AI Resume Analyzer &amp; Career Copilot", ParagraphStyle('CoverT', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=colors.HexColor('#ffffff'), alignment=1)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Intelligent Resume Parsing, Automated ATS Scoring, Domain Classification &amp; Smart Learning Paths", ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=12, leading=16, textColor=colors.HexColor('#a5b4fc'), alignment=1)))
    story.append(Spacer(1, 35))

    # Presenter Details Card
    presenter_data = [
        [
            Paragraph("<b>Presented By:</b><br/><font color='#ffffff'><b>Anupam Chatterjee</b></font><br/><font color='#94a3b8'>Dept. of Computer Science &amp; Engineering</font>", style_body),
            Paragraph("<b>Core Technologies:</b><br/><font color='#38bdf8'><b>Python 3.9  |  SpaCy NLP  |  Streamlit  |  PDFMiner3</b></font><br/><font color='#94a3b8'>Dual Database Architecture: MySQL + SQLite Fallback</font>", style_body)
        ]
    ]
    t_presenter = Table(presenter_data, colWidths=[350, 390])
    t_presenter.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131a2a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#312e81')),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 18),
        ('RIGHTPADDING', (0,0), (-1,-1), 18),
    ]))
    story.append(t_presenter)

    story.append(Spacer(1, 35))
    story.append(Paragraph("<font color='#64748b'>Live Cloud Application: </font><font color='#38bdf8'><b>https://airesumeanalyzer-ezeedzgjxmv3jgm3e95rrj.streamlit.app/</b></font>", ParagraphStyle('CoverRepo', fontName='Helvetica', fontSize=9, leading=12, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    story.append(Paragraph("01. CONTEXT &amp; CHALLENGE", style_badge))
    story.append(Paragraph("Problem Statement &amp; Industry Motivation", style_title))
    story.append(Paragraph("Why manual resume screening fails and how candidates fall through the cracks", style_subtitle))

    p2_c1 = [
        Paragraph("<font color='#a5b4fc'><b>⏳ RECRUITER OVERLOAD</b></font>", style_card_title),
        Paragraph("<font size='24' color='#ffffff'><b>7 Seconds</b></font><br/><font color='#818cf8'><b>Average Human Screening Time</b></font>", style_body),
        Spacer(1, 8),
        Paragraph("Corporate job openings receive an average of 250+ resumes within 48 hours. Human recruiters are overwhelmed, leading to fatigue, unconscious bias, and high false-rejection rates.", style_body)
    ]
    p2_c2 = [
        Paragraph("<font color='#f59e0b'><b>🚫 THE ATS BLACKBOX</b></font>", style_card_title),
        Paragraph("<font size='24' color='#ffffff'><b>75% Filtered</b></font><br/><font color='#f59e0b'><b>Automated Algorithm Rejection</b></font>", style_body),
        Spacer(1, 8),
        Paragraph("Over 75% of resumes are discarded by Applicant Tracking Systems (ATS) before human review due to missing keywords, non-standard section headers, and formatting parsing errors.", style_body)
    ]
    p2_c3 = [
        Paragraph("<font color='#10b981'><b>💡 THE GUIDANCE VOID</b></font>", style_card_title),
        Paragraph("<font size='24' color='#ffffff'><b>Zero Feedback</b></font><br/><font color='#10b981'><b>Unaddressed Skill Gaps</b></font>", style_body),
        Spacer(1, 8),
        Paragraph("Rejected job applicants receive standard automated rejection letters with zero explanation. They are left without actionable guidance on what technical skills or certifications to acquire.", style_body)
    ]

    t_p2 = Table([[p2_c1, p2_c2, p2_c3]], colWidths=[240, 240, 240])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p2)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES & VISION
    # =========================================================================
    story.append(Paragraph("02. GOALS &amp; VISION", style_badge))
    story.append(Paragraph("Project Objectives &amp; Proposed Solution", style_title))
    story.append(Paragraph("A dual-sided ecosystem bridging applicant self-readiness and recruiter intelligence", style_subtitle))

    p3_left = [
        Paragraph("<b>🎯 Primary Technical Objectives</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("• <b>Automated PDF Information Ingestion:</b> Accurately extract raw text, contact information, degrees, and technical skills from PDF resumes without manual entry.", style_bullet),
        Paragraph("• <b>Objective ATS Compatibility Scoring:</b> Implement a clear, deterministic 100-point rubric assessing 9 vital resume sections.", style_bullet),
        Paragraph("• <b>Predictive Domain Classification:</b> Map parsed technical competencies to appropriate industry career tracks (Data Science, Web, Android, iOS, UI/UX).", style_bullet),
        Paragraph("• <b>Personalized Upskilling Engine:</b> Recommend missing domain keywords and university-grade certification courses to bridge candidate gaps.", style_bullet)
    ]

    p3_right = [
        Paragraph("<b>🌟 Key Innovations &amp; Architectural Strengths</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("• <b>Dual-Mode Resilient Database:</b> Auto-detects local MySQL servers; gracefully falls back to embedded SQLite for zero-crash cloud deployments.", style_bullet),
        Paragraph("• <b>Modern Interactive Presentation:</b> High-impact circular Plotly ATS gauge, visual checklist badges, and non-intrusive PDF previews.", style_bullet),
        Paragraph("• <b>Recruiter Intelligence Portal:</b> Secure administrative suite with searchable candidate rosters, CSV export, and Plotly analytics.", style_bullet),
        Paragraph("• <b>Permanent 24/7 Cloud Hosting:</b> Hosted on Google Cloud infrastructure via Streamlit Community Cloud with instant accessibility.", style_bullet)
    ]

    t_p3 = Table([[p3_left, p3_right]], colWidths=[365, 365])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#111827')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#131a2e')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#1f2937')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#312e81')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 18),
        ('RIGHTPADDING', (0,0), (-1,-1), 18),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p3)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & DATA FLOW
    # =========================================================================
    story.append(Paragraph("03. ARCHITECTURAL DESIGN", style_badge))
    story.append(Paragraph("System Architecture &amp; Data Pipeline", style_title))
    story.append(Paragraph("Modular 4-stage data pipeline orchestrating ingestion, extraction, intelligence, and presentation", style_subtitle))

    p4_cards = [
        [
            Paragraph("<font color='#818cf8'><b>STAGE 01</b></font><br/><b>PDF Ingestion Layer</b>", style_card_title),
            Paragraph("<font color='#818cf8'><b>STAGE 02</b></font><br/><b>NLP Extraction Engine</b>", style_card_title),
            Paragraph("<font color='#818cf8'><b>STAGE 03</b></font><br/><b>Intelligence &amp; Scoring</b>", style_card_title),
            Paragraph("<font color='#818cf8'><b>STAGE 04</b></font><br/><b>Presentation &amp; DB</b>", style_card_title)
        ],
        [
            Paragraph("• PDF file upload via Streamlit<br/>• File byte-buffer caching<br/>• <b>pdfminer3</b> layout preservation<br/>• Raw text stream extraction", style_body),
            Paragraph("• SpaCy <b>en_core_web_sm</b><br/>• Linguistic tokenization<br/>• Noun chunk phrase extraction<br/>• Regex Matcher for contact info<br/>• Skills lexicon lookup", style_body),
            Paragraph("• 9-Section ATS evaluation<br/>• 100-point score computation<br/>• Experience level prediction<br/>• Keyword domain clustering<br/>• Curated course matching", style_body),
            Paragraph("• Dual DB (MySQL / SQLite)<br/>• Plotly circular gauge meter<br/>• 4 Tabbed candidate insights<br/>• Admin BI dashboard<br/>• One-click CSV export", style_body)
        ]
    ]
    t_p4 = Table(p4_cards, colWidths=[180, 180, 180, 180])
    t_p4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p4)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: TECHNOLOGY STACK & LIBRARIES
    # =========================================================================
    story.append(Paragraph("04. IMPLEMENTATION TOOLING", style_badge))
    story.append(Paragraph("Technology Stack &amp; Libraries Used", style_title))
    story.append(Paragraph("Carefully chosen production tools ensuring performance, accuracy, and maintainability", style_subtitle))

    p5_c1 = [
        Paragraph("<b>🐍 Language &amp; NLP Stack</b>", style_card_title),
        Paragraph("• <b>Python 3.9.13:</b> Core runtime with universal C-extension wheel compatibility.", style_bullet),
        Paragraph("• <b>SpaCy 2.3.5:</b> Ultra-fast industrial NLP engine written in Cython.", style_bullet),
        Paragraph("• <b>en_core_web_sm:</b> Pre-trained English linguistic model for statistical entity recognition.", style_bullet),
        Paragraph("• <b>pdfminer3:</b> Accurate layout extraction tool parsing native PDF text streams.", style_bullet),
        Paragraph("• <b>NLTK:</b> Stopwords filtering and English lexical analysis.", style_bullet)
    ]
    p5_c2 = [
        Paragraph("<b>🖥️ Frontend &amp; Visualization</b>", style_card_title),
        Paragraph("• <b>Streamlit:</b> Reactive Python web framework with stateful component re-rendering.", style_bullet),
        Paragraph("• <b>Plotly Express &amp; GO:</b> Interactive circular gauges, donut charts, and histograms.", style_bullet),
        Paragraph("• <b>Custom CSS Injection:</b> Modern typography (Plus Jakarta Sans) and glassmorphism cards.", style_bullet),
        Paragraph("• <b>Streamlit Tags:</b> Interactive chip badges rendering extracted and suggested skills.", style_bullet)
    ]
    p5_c3 = [
        Paragraph("<b>🗄️ Persistence &amp; Cloud Infra</b>", style_card_title),
        Paragraph("• <b>PyMySQL:</b> High-performance connector for local relational database servers.", style_bullet),
        Paragraph("• <b>SQLite3:</b> Embedded ACID-compliant database for zero-downtime cloud hosting.", style_bullet),
        Paragraph("• <b>Streamlit Cloud:</b> Containerized Debian Linux hosting on Google Cloud infra.", style_bullet),
        Paragraph("• <b>Git &amp; GitHub:</b> Version control and automated continuous deployment.", style_bullet)
    ]

    t_p5 = Table([[p5_c1, p5_c2, p5_c3]], colWidths=[240, 240, 240])
    t_p5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p5)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: NATURAL LANGUAGE PROCESSING PIPELINE
    # =========================================================================
    story.append(Paragraph("05. CORE NLP ARCHITECTURE", style_badge))
    story.append(Paragraph("Natural Language Processing (NLP) Engine", style_title))
    story.append(Paragraph("Converting freeform, unstructured resume text into standardized structured JSON data", style_subtitle))

    p6_left = [
        Paragraph("<b>🔬 Technical NLP Methodologies Employed</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Statistical Entity Recognition (NER):</b> Identifies applicant names and academic organizations using SpaCy's transition-based statistical parser.", style_bullet),
        Paragraph("• <b>Syntactic Noun Chunking:</b> Rather than naive word tokenization, noun chunks group compound technical entities (e.g. <i>'Convolutional Neural Networks'</i>, <i>'Relational Database Management'</i>).", style_bullet),
        Paragraph("• <b>Pattern Matching via Rule Matcher:</b> <code>spacy.matcher.Matcher</code> regex patterns extract mobile numbers, international dialing codes, and email addresses.", style_bullet),
        Paragraph("• <b>Skills Dictionary Cross-Referencing:</b> Cleaned tokens are matched against an exhaustive technical skills database (<code>skills.csv</code>).", style_bullet)
    ]

    p6_right = [
        Paragraph("<b>📄 Sample Parsed Output Structure</b>", style_card_title),
        Paragraph(
            "<font color='#38bdf8'><b>{</b></font><br/>"
            "&nbsp;&nbsp;<font color='#a5b4fc'>\"name\"</font>: <font color='#34d399'>\"Anupam Chatterjee\"</font>,<br/>"
            "&nbsp;&nbsp;<font color='#a5b4fc'>\"email\"</font>: <font color='#34d399'>\"anupam@example.com\"</font>,<br/>"
            "&nbsp;&nbsp;<font color='#a5b4fc'>\"mobile_number\"</font>: <font color='#34d399'>\"+91 9876543210\"</font>,<br/>"
            "&nbsp;&nbsp;<font color='#a5b4fc'>\"degree\"</font>: <font color='#34d399'>[\"B.Tech in Computer Science\"]</font>,<br/>"
            "&nbsp;&nbsp;<font color='#a5b4fc'>\"no_of_pages\"</font>: <font color='#f59e0b'>2</font>,<br/>"
            "&nbsp;&nbsp;<font color='#a5b4fc'>\"skills\"</font>: <font color='#34d399'>[\"Python\", \"Machine Learning\", \"TensorFlow\", \"Docker\", \"SQL\"]</font><br/>"
            "<font color='#38bdf8'><b>}</b></font>",
            ParagraphStyle('CodeBlock', fontName='Courier', fontSize=9, leading=14, textColor=colors.HexColor('#ffffff'), backColor=colors.HexColor('#090d16'), borderPadding=(10,12,10,12), borderRadius=6)
        )
    ]

    t_p6 = Table([[p6_left, p6_right]], colWidths=[400, 330])
    t_p6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p6)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: PREDICTIVE ATS SCORING MODEL
    # =========================================================================
    story.append(Paragraph("06. SCORING MECHANISM", style_badge))
    story.append(Paragraph("Predictive ATS Compatibility Scoring Model", style_title))
    story.append(Paragraph("Deterministic 100-point rubric assessing 9 vital recruiter evaluation checkpoints", style_subtitle))

    table_data = [
        [Paragraph("<b>Resume Section</b>", style_body_bold), Paragraph("<b>Weight</b>", style_body_bold), Paragraph("<b>Recruiter Evaluation Focus</b>", style_body_bold)],
        [Paragraph("Projects Portfolio", style_body), Paragraph("<font color='#34d399'><b>+19 pts</b></font>", style_body), Paragraph("Demonstrates real-world problem solving and applied knowledge", style_body)],
        [Paragraph("Work Experience", style_body), Paragraph("<font color='#34d399'><b>+16 pts</b></font>", style_body), Paragraph("Validates corporate delivery, teamwork, and accountability", style_body)],
        [Paragraph("Achievements &amp; Honors", style_body), Paragraph("<font color='#34d399'><b>+13 pts</b></font>", style_body), Paragraph("Signals competitive excellence and peer recognition", style_body)],
        [Paragraph("Educational Credentials", style_body), Paragraph("<font color='#34d399'><b>+12 pts</b></font>", style_body), Paragraph("Confirms formal academic qualifications and foundations", style_body)],
        [Paragraph("Certifications &amp; Courses", style_body), Paragraph("<font color='#34d399'><b>+12 pts</b></font>", style_body), Paragraph("Proves ongoing self-initiative and specialized domain skills", style_body)],
        [Paragraph("Interests &amp; Extracurriculars", style_body), Paragraph("<font color='#34d399'><b>+9 pts</b></font>", style_body), Paragraph("Provides insight into personality and cultural team fit", style_body)],
        [Paragraph("Technical Skills Section", style_body), Paragraph("<font color='#34d399'><b>+7 pts</b></font>", style_body), Paragraph("Core requirement for automated keyword matching queries", style_body)],
        [Paragraph("Career Objective / Summary", style_body), Paragraph("<font color='#34d399'><b>+6 pts</b></font>", style_body), Paragraph("Communicates clear professional intent and immediate focus", style_body)],
        [Paragraph("Internship Experience", style_body), Paragraph("<font color='#34d399'><b>+6 pts</b></font>", style_body), Paragraph("Validates transitional capability from academia to industry", style_body)],
    ]
    t_scoring = Table(table_data, colWidths=[200, 90, 440])
    t_scoring.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#111827')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1f2937')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#111827'), colors.HexColor('#131d2e')]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_scoring)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: DOMAIN CLASSIFICATION & SMART COURSES
    # =========================================================================
    story.append(Paragraph("07. INTELLIGENT RECOMMENDATION", style_badge))
    story.append(Paragraph("Domain Classification &amp; Smart Course Engine", style_title))
    story.append(Paragraph("Taxonomy-based skill clustering and dynamic course recommendation from top platforms", style_subtitle))

    p8_left = [
        Paragraph("<b>🗂️ Keyword Taxonomy Clustering</b>", style_card_title),
        Paragraph("• <b>Data Science &amp; AI:</b> <i>TensorFlow, Keras, PyTorch, Scikit-learn, Machine Learning, Deep Learning, Streamlit, Pandas.</i>", style_bullet),
        Paragraph("• <b>Web Development:</b> <i>React, Django, Node.js, Express, JavaScript, HTML/CSS, Flask, C#, PHP, TypeScript.</i>", style_bullet),
        Paragraph("• <b>Android Development:</b> <i>Kotlin, Android Studio, Flutter, Java, XML, Room, Jetpack Compose, Coroutines.</i>", style_bullet),
        Paragraph("• <b>iOS Development:</b> <i>Swift, SwiftUI, Xcode, Cocoa Touch, Objective-C, Combine, CoreData.</i>", style_bullet),
        Paragraph("• <b>UI / UX Design:</b> <i>Figma, Adobe XD, Wireframing, User Research, Prototyping, Zeplin, Design Systems.</i>", style_bullet)
    ]

    p8_right = [
        Paragraph("<b>🎓 Personalized Learning Recommendations</b>", style_card_title),
        Paragraph("• <b>Top Curated Certifications:</b> Pulls relevant courses directly from Google Developers, Coursera (Andrew Ng), Udacity Nanodegrees, and LinkedIn Learning.", style_bullet),
        Paragraph("• <b>Domain-Specific Gap Filling:</b> Highlights specific missing keywords that candidates can add to boost ATS keyword match rates.", style_bullet),
        Paragraph("• <b>Embedded Video Masterclasses:</b> Automatically streams curated video masterclasses covering high-impact resume writing and technical interview preparation.", style_bullet)
    ]

    t_p8 = Table([[p8_left, p8_right]], colWidths=[365, 365])
    t_p8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p8)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: MODERN USER INTERFACE & EXPERIENCE
    # =========================================================================
    story.append(Paragraph("08. USER EXPERIENCE (UX)", style_badge))
    story.append(Paragraph("Modernized User Interface &amp; Candidate Portal", style_title))
    story.append(Paragraph("Engineered as a clean, responsive SaaS dashboard with real-time feedback mechanisms", style_subtitle))

    p9_c1 = [
        Paragraph("<b>🚀 Candidate Workspace</b>", style_card_title),
        Paragraph("• 3-column responsive input for Name, Email, and Phone.<br/>• Drag-and-drop PDF dropzone with instantaneous state recognition.<br/>• Collapsible PDF preview accordion preventing page clutter.<br/>• Automatic IP, Hostname, and Geolocation capture.", style_body)
    ]
    p9_c2 = [
        Paragraph("<b>📈 Visual Dashboard</b>", style_card_title),
        Paragraph("• <b>4 Top KPI Cards:</b> Score, Domain, Level, and Page count.<br/>• <b>Circular Plotly Gauge Meter:</b> Color-coded safety bands (Red 0-40, Amber 40-70, Green 70-100).<br/>• Extracted profile summary card.", style_body)
    ]
    p9_c3 = [
        Paragraph("<b>📋 4 Interactive Tabs</b>", style_card_title),
        Paragraph("• <b>Skill Alignment:</b> Detected tags vs booster keywords.<br/>• <b>ATS Checklist Audit:</b> Green/amber breakdown cards.<br/>• <b>Recommended Courses:</b> 2-column card links.<br/>• <b>Career Masterclasses:</b> Embedded video players.", style_body)
    ]

    t_p9 = Table([[p9_c1, p9_c2, p9_c3]], colWidths=[240, 240, 240])
    t_p9.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p9)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: ADMIN INTELLIGENCE HUB & ANALYTICS
    # =========================================================================
    story.append(Paragraph("09. ENTERPRISE RECRUITER PORTAL", style_badge))
    story.append(Paragraph("Admin Intelligence Hub &amp; Visual Analytics", style_title))
    story.append(Paragraph("Empowering recruitment teams with data-driven insights over applicant pools", style_subtitle))

    p10_left = [
        Paragraph("<b>🔐 Secure Candidate Management</b>", style_card_title),
        Paragraph("• <b>Authentication Gate:</b> Protected by administrator credentials (<code>admin</code> / <code>admin@resume-analyzer</code>).", style_bullet),
        Paragraph("• <b>Unified Candidate Database Grid:</b> Searchable table tracking Candidate Name, Email, Contact, ATS Score, Predicted Domain, Experience Level, and Timestamps.", style_bullet),
        Paragraph("• <b>One-Click CSV Export:</b> Generates <code>Candidate_Intelligence_Report.csv</code> for direct import into enterprise HRMS systems.", style_bullet),
        Paragraph("• <b>Feedback Testimonials:</b> Reviews user ratings and qualitative feedback entries.", style_bullet)
    ]

    p10_right = [
        Paragraph("<b>📊 Real-Time Plotly Analytics</b>", style_card_title),
        Paragraph("• <b>Domain Distribution Pie Chart:</b> Visualizes applicant share across Data Science, Web, Android, iOS, and UI/UX.", style_bullet),
        Paragraph("• <b>Experience Level Proportions:</b> Tracks applicant ratios between Freshers, Intermediate, and Experienced engineers.", style_bullet),
        Paragraph("• <b>Applicant Score Distribution:</b> Identifies high-scoring talent pools meeting hiring criteria.", style_bullet),
        Paragraph("• <b>Geographic Origin Tracking:</b> Displays applicant origins across cities and states.", style_bullet)
    ]

    t_p10 = Table([[p10_left, p10_right]], colWidths=[365, 365])
    t_p10.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p10)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 11: DEPLOYMENT & TESTING RESULTS
    # =========================================================================
    story.append(Paragraph("10. RELIABILITY &amp; DEPLOYMENT", style_badge))
    story.append(Paragraph("Deployment Architecture &amp; System Testing", style_title))
    story.append(Paragraph("Ensuring robust offline execution and permanent 24/7 global cloud availability", style_subtitle))

    p11_c1 = [
        Paragraph("<b>🌐 24/7 Cloud Deployment</b>", style_card_title),
        Paragraph("Hosted on Google Cloud infrastructure via <b>Streamlit Community Cloud</b>.<br/><br/>Live URL:<br/><font color='#38bdf8'><b>https://airesumeanalyzer-ezeedzgjxmv3jgm3e95rrj.streamlit.app/</b></font>", style_body)
    ]
    p11_c2 = [
        Paragraph("<b>🛡️ Dual-Mode Database</b>", style_card_title),
        Paragraph("Auto-detects MySQL server availability. If offline (or in cloud containers), automatically connects to embedded <b>SQLite</b> (<code>cv_database.db</code>) with zero crashes.", style_body)
    ]
    p11_c3 = [
        Paragraph("<b>🧪 Rigorous Testing</b>", style_card_title),
        Paragraph("• Verified across multiple resume formats (Fresher, Intermediate, Senior).<br/>• Tested offline local launcher (<code>RUN_APP.bat</code>).<br/>• Validated cross-browser UI responsiveness.", style_body)
    ]

    t_p11 = Table([[p11_c1, p11_c2, p11_c3]], colWidths=[240, 240, 240])
    t_p11.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p11)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("<font color='#818cf8'><b>11. SUMMARY &amp; ROADMAP</b></font>", ParagraphStyle('CBadge', fontName='Helvetica-Bold', fontSize=9, leading=11, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Conclusion &amp; Future Scope", ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=colors.HexColor('#ffffff'), alignment=1)))
    story.append(Spacer(1, 20))

    p12_c1 = [
        Paragraph("<b>🔍 OCR Integration</b>", style_card_title),
        Paragraph("Incorporating <b>Tesseract OCR</b> to parse scanned graphic image resumes and non-selectable PDF formats.", style_body)
    ]
    p12_c2 = [
        Paragraph("<b>🤖 Transformer Semantic Matching</b>", style_card_title),
        Paragraph("Fine-tuning <b>BERT / RoBERTa</b> embeddings for cosine similarity matching against specific employer Job Descriptions.", style_body)
    ]
    p12_c3 = [
        Paragraph("<b>🎙️ Dynamic AI Mock Interviewer</b>", style_card_title),
        Paragraph("Generating custom viva and technical interview questions based directly on the candidate's extracted project experience.", style_body)
    ]
    t_p12 = Table([[p12_c1, p12_c2, p12_c3]], colWidths=[240, 240, 240])
    t_p12.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1f2937')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p12)

    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Thank You! Any Questions?</b>", ParagraphStyle('TY', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor('#ffffff'), alignment=1)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<font color='#94a3b8'>Project Developer: <b>Anupam Chatterjee</b>  |  GitHub: <font color='#38bdf8'>AnupamMax-10</font></font>", ParagraphStyle('TY2', fontName='Helvetica', fontSize=10, leading=14, alignment=1)))

    # Build the PDF document
    doc.build(story, canvasmaker=PresentationCanvas)
    print("PDF build successful:", PDF_PATH)

if __name__ == "__main__":
    build_pdf()
