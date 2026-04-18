"""Sample emails for testing the Opportunity Inbox Copilot.

12 high-quality, varied test emails covering:
- All deadline types (hard, rolling, soft_early, relative, unknown)
- All opportunity types (scholarship, internship, fellowship, competition, research)
- Spam/newsletter examples for classification testing
"""

from typing import List, Tuple


# Email 1: HARD deadline scholarship - Google Generation Scholarship
EMAIL_1 = """Subject: Google Generation Scholarship 2025 - Applications Open!

Dear Student,

We are pleased to announce that applications for the Google Generation Scholarship 2025 are now open!

About the Scholarship:
The Google Generation Scholarship is designed to support students pursuing degrees in computer science, software engineering, or related technical fields. This scholarship aims to help students excel in technology and become future leaders in the field.

Eligibility:
- Currently enrolled in an undergraduate or graduate program
- Pursuing a Computer Science, Software Engineering, or related technical degree
- Demonstrated academic excellence with a minimum CGPA of 3.0
- Strong passion for technology and leadership

What You'll Receive:
- $10,000 USD scholarship award
- Access to Google workshops and networking events
- Mentorship from Google engineers
- Invitation to the Google Scholars Retreat

Required Documents:
- Updated resume/CV
- Unofficial transcript
- Two letters of recommendation
- Personal statement (500 words)
- Proof of enrollment

Application Deadline: March 15, 2025 at 11:59 PM PST

Apply here: https://scholarships.google.com/generation-2025

Questions? Contact scholarships@google.com

Best regards,
Google Scholarships Team
"""


# Email 2: ROLLING basis internship - Microsoft Summer Internship
EMAIL_2 = """Subject: Microsoft Summer Internship 2025 - Applications Reviewed on Rolling Basis

Hello,

Microsoft is now accepting applications for our Summer 2025 Internship Program! Join thousands of students from around the world in building innovative solutions that impact millions.

Positions Available:
- Software Engineering Intern
- Product Management Intern
- Data Science Intern
- UX Design Intern

We review applications on a rolling basis, which means positions may fill before the general deadline. We encourage you to apply as soon as possible to maximize your chances.

Requirements:
- Currently pursuing a Bachelor's, Master's, or PhD in CS, Engineering, or related field
- Expected graduation date between December 2025 and June 2027
- Strong programming skills (Python, Java, C++, or C#)
- Experience with software development projects

Location: Redmond, WA (Hybrid - 3 days in office)
Duration: 12 weeks (May/June - August 2025)
Compensation: $8,000/month + housing stipend

To apply, visit: https://careers.microsoft.com/students/internships

Best,
Microsoft University Recruiting
"""


# Email 3: SOFT_EARLY deadline - Research Fellowship with priority deadline
EMAIL_3 = """Subject: MIT AI Lab Research Fellowship - Early Applications Encouraged

Dear Prospective Fellow,

The MIT AI Laboratory is excited to announce our 2025-2026 Research Fellowship program. We are seeking exceptional graduate students interested in cutting-edge AI research.

Fellowship Details:
- Duration: 1 year (September 2025 - August 2026)
- Stipend: $45,000 per year + full tuition coverage
- Research areas: Machine Learning, NLP, Computer Vision, Robotics
- Mentorship from world-renowned faculty

Eligibility:
- Currently enrolled in or applying to a PhD program in Computer Science or related field
- Research experience in AI/ML demonstrated through publications or projects
- Strong programming background (Python, PyTorch/TensorFlow)
- GPA of 3.5 or higher preferred

Early Application Deadline: December 1, 2024
We strongly encourage early applications as we begin reviewing immediately and will make offers on a rolling basis after the priority deadline.

Final Deadline: January 15, 2025

Required Materials:
- CV with publications
- Research statement (2 pages)
- Two recommendation letters
- Code samples or GitHub portfolio

Apply: https://ai.mit.edu/fellowships/2025

Contact: ai-fellowships@mit.edu

Sincerely,
Dr. Sarah Chen, Fellowship Director
MIT AI Laboratory
"""


# Email 4: RELATIVE deadline - Coding Competition
EMAIL_4 = """Subject: ACM-ICPC Regional Programming Contest - Registration Closing Soon!

Hi Coders,

Get ready for the 2025 ACM-ICPC Regional Programming Contest! Test your algorithmic skills against the best student programmers in the region.

Competition Format:
- Teams of 3 students
- 5 hours of intense problem solving
- 8-12 programming problems of varying difficulty
- Languages: C++, Java, Python, Kotlin

Eligibility:
- Enrolled in a university degree program
- Have not participated in more than 2 World Finals
- Must be enrolled at least half-time

Important Dates:
Registration closes next Friday at midnight!
Competition Date: February 8, 2025
Practice Round: February 1, 2025

Prizes:
1st Place: $5,000 + Automatic advancement to World Finals
2nd Place: $3,000
3rd Place: $1,500
Top 10 teams receive swag and certificates

To register your team, visit: https://icpc.baylor.edu/regionals/2025

Don't miss this opportunity to compete with the best!

Cheers,
ACM-ICPC Organizing Committee
"""


# Email 5: UNKNOWN deadline - Scholarship with no deadline mentioned
EMAIL_5 = """Subject: Explore the Future with FutureTech Summer Research Program

Hello,

FutureTech Institute is offering exclusive research opportunities for talented undergraduate students interested in emerging technologies.

About the Program:
Our summer research program immerses students in hands-on research projects alongside leading industry researchers. You'll gain invaluable experience and contribute to cutting-edge projects.

Research Areas:
- Quantum Computing Applications
- Sustainable Technology
- Biomedical Engineering
- Renewable Energy Systems

What We Offer:
- $6,000 stipend for the summer
- Housing and meal plan provided
- Travel reimbursement up to $500
- Opportunity to present at FutureTech Symposium

Eligibility:
- Currently enrolled as an undergraduate
- GPA of 3.2 or above
- Major in Engineering, Physics, Computer Science, or related field
- US citizen or permanent resident

Interested students should submit:
- Resume
- Unofficial transcript
- Statement of purpose (300-500 words)
- One recommendation letter

Apply at: https://futuretech.org/summer-research

For questions, email: research@futuretech.org

Best,
FutureTech Admissions Team

P.S. We are accepting applications now and will review them as they arrive.
"""


# Email 6: HARD deadline with required docs - PhD Position
EMAIL_6 = """Subject: PhD Position in Machine Learning - Application Deadline June 30, 2025

Dear Prospective PhD Student,

The Department of Computer Science at Stanford University invites applications for funded PhD positions in Machine Learning, starting Fall 2025.

Position Details:
- Full funding for 5 years (tuition + $45,000 annual stipend)
- Research areas: Deep Learning, Reinforcement Learning, NLP, Computer Vision
- Access to state-of-the-art compute resources
- Collaboration with industry partners (Google, OpenAI, Meta)

Supervisor: Prof. Andrew Ng
Research Group: Stanford ML Group

Requirements:
- Bachelor's or Master's degree in Computer Science or related field
- Strong mathematical background (linear algebra, calculus, probability)
- Programming proficiency in Python
- Research experience demonstrated through projects or publications
- GRE scores (optional but recommended)
- TOEFL/IELTS for international students

Required Application Materials:
1. Online application form
2. Statement of purpose (2 pages)
3. Three letters of recommendation
4. Unofficial transcripts from all institutions attended
5. CV/Resume
6. Writing sample (optional but recommended)
7. Code sample or GitHub repository link

Application Deadline: June 30, 2025
All materials must be submitted by 11:59 PM PST on this date.

Application Portal: https://cs.stanford.edu/admissions/phd

Contact: ml-phd-admissions@stanford.edu

We look forward to receiving your application!

Best regards,
Graduate Admissions Committee
Stanford Computer Science
"""


# Email 7: ROLLING + location preference - Summer Internship
EMAIL_7 = """Subject: Summer 2025 Engineering Internship - Boston Area

Hi there,

LocalTech Solutions is hiring summer interns for our Boston office! Join our fast-growing team and work on real products used by thousands of customers.

The Role:
As a Software Engineering Intern, you'll:
- Build features for our core SaaS platform
- Work with modern tech stack (React, Node.js, PostgreSQL)
- Collaborate with senior engineers on architecture decisions
- Participate in agile ceremonies and code reviews

Qualifications:
- Currently pursuing BS/MS in Computer Science or related field
- Graduation date between December 2025 and June 2027
- Proficiency in at least one programming language
- Experience with web development a plus
- Must be able to work in Boston office (in-person required)

Details:
- Duration: 10-12 weeks (flexible start date)
- Pay: $30/hour
- Housing stipend: $1,500/month for non-local students
- Location: Boston, MA (Kendall Square area)

We are reviewing applications on a rolling basis and will close the position once we have filled our spots. Apply soon!

To apply, send your resume to: internships@localtech.com

Questions? Reply to this email.

Best,
Emily Rodriguez
Talent Acquisition
LocalTech Solutions
"""


# Email 8: SOFT_EARLY with financial need - Fellowship
EMAIL_8 = """Subject: NSF Graduate Research Fellowship - Priority Deadline Approaching

Dear Graduate Students,

The National Science Foundation Graduate Research Fellowship Program (GRFP) is now accepting applications for the 2025 cycle.

Award Benefits:
- $37,000 annual stipend for 3 years
- $12,000 cost of education allowance
- International research opportunities
- Access to NSF resources and networks

Eligibility:
- US citizens, nationals, or permanent residents
- Early-career graduate students (first or second year)
- Pursuing research-based Master's or PhD in STEM fields
- Must demonstrate potential for significant research achievements

Priority Consideration:
Applications submitted by the priority deadline receive full consideration for all award opportunities. While we accept applications through the final deadline, early submission is strongly encouraged.

Key Dates:
Priority Deadline: October 20, 2024
Final Deadline: October 27, 2024
Reference Letters Due: November 3, 2024

Application Components:
- Personal statement (3 pages)
- Research proposal (2 pages)
- Three reference letters
- Transcripts

Apply at: https://nsfgrfp.org

This fellowship is particularly valuable for students with financial need - it provides complete funding without requiring teaching or research assistantships.

Best of luck!
NSF GRFP Program Team
"""


# Email 9: HARD deadline with complex eligibility - Competition
EMAIL_9 = """Subject: HackMIT 2025 - Registration Opens! Deadline: September 15, 2025

Hey Hackers!

Get ready for HackMIT 2025 - MIT's premier hackathon bringing together 1,000+ students from around the world for 24 hours of hacking, learning, and innovation!

The Event:
- Date: September 27-28, 2025
- Location: MIT Campus, Cambridge, MA
- Format: 24-hour overnight hackathon
- Prize Pool: $50,000+

Eligibility Requirements:
- Must be a current student at an accredited university
- Undergraduates and graduate students welcome
- Must be 18 years or older by September 27, 2025
- Teams of 1-4 members (we can help you find teammates!)
- Prior hackathon experience NOT required - beginners welcome!
- International students welcome (travel grants available)

Tracks:
- Health & Wellness
- Sustainability & Climate
- Education & Learning
- FinTech
- Open Innovation

Prizes:
- Grand Prize: $10,000
- Track Winners: $3,000 each
- Best Beginner Hack: $2,000
- Sponsor Prizes: $25,000+ in additional prizes

Important: Registration Deadline is September 15, 2025 at 11:59 PM EDT. No late registrations accepted!

What You Get:
- Free meals throughout the event
- Swag bag with exclusive HackMIT merchandise
- Access to workshops and mentorship
- Networking with top tech companies
- Potential recruitment opportunities

Register now: https://hackmit.org/2025

Questions? Email: team@hackmit.org

Happy Hacking!
The HackMIT Team

P.S. Travel reimbursement applications close August 30, 2025!
"""


# Email 10: ROLLING with skills match - Research Assistant Position
EMAIL_10 = """Subject: Research Assistant Position - Natural Language Processing Lab

Dear Students,

The Natural Language Processing Lab at UC Berkeley is seeking undergraduate and master's students to join our team as Research Assistants.

About Us:
We are a leading research lab focusing on large language models, alignment, and multimodal AI. Our recent work includes papers at NeurIPS, ICML, and ACL.

Position: Research Assistant
Responsibilities:
- Assist with data collection and preprocessing
- Implement and evaluate NLP models
- Contribute to research papers and publications
- Collaborate with PhD students and faculty

Ideal Candidates Have:
- Strong programming skills in Python
- Experience with PyTorch or TensorFlow
- Background in NLP or machine learning
- Familiarity with transformer architectures
- Ability to work 10-20 hours per week
- Interest in pursuing graduate studies in AI

Compensation:
- $20-25/hour depending on experience
- Course credit option available
- Opportunity for co-authorship on publications
- Strong letters of recommendation for graduate applications

We are accepting applications on a continuous basis until positions are filled. If you're interested in NLP research, apply soon as these positions are competitive.

To Apply:
Send your CV, transcript, and a brief statement of interest to: nlp-jobs@berkeley.edu

Subject line: "RA Application - [Your Name]"

Best regards,
Dr. Anna Martinez
Principal Investigator
UC Berkeley NLP Lab
"""


# Email 11: SPAM - Newsletter disguised as opportunity
EMAIL_11 = """Subject: AMAZING OPPORTUNITY! Change Your Life Today!

Hi Friend,

Are you tired of missing out on opportunities? Do you want to unlock your full potential and achieve financial freedom?

INTRODUCING: The Ultimate Success Newsletter

Join 50,000+ successful people who read our weekly newsletter and transform their lives!

What You'll Get:
- Exclusive tips from millionaires
- Secrets they don't teach in college
- Networking opportunities
- Free e-books worth $500
- Access to our private community

Normally $99/month, but TODAY ONLY get 80% OFF!

Use code: SUCCESS80

Limited spots available! Act now before this offer expires!

Click here to subscribe: https://success-newsletter.com/limited-offer

Don't let this life-changing opportunity pass you by!

To your success,
The Success Team

P.S. This is a limited time offer. We can't hold these spots forever!

---
You're receiving this because you subscribed to our mailing list.
Unsubscribe here: https://success-newsletter.com/unsubscribe
---
"""


# Email 12: SPAM - Unrelated job offer
EMAIL_12 = """Subject: Immediate Hire - Work From Home Opportunity!

Dear Candidate,

We found your profile and think you'd be perfect for our Work From Home position!

Earn $5,000-$10,000 per week working just 2-3 hours daily!

No experience needed!
No degree required!
Start immediately!

We are looking for:
- Data entry specialists
- Virtual assistants
- Social media managers
- Marketing representatives

Requirements:
- Basic computer skills
- Internet connection
- 18 years or older

What We Offer:
- Flexible hours
- Weekly payment
- Full training provided
- Benefits after 90 days

Hurry! We only have 7 positions left in your area!

Reply with your full name, phone number, and email to claim your spot.

Or call now: 1-800-SCAM-NOW (waiting for you!)

Don't miss this once-in-a-lifetime opportunity!

Best,
Sarah Johnson
Hiring Manager
Global Opportunities Inc.

P.S. Positions are filling fast! Apply NOW!
"""


# Collection of all sample emails
SAMPLE_EMAILS: List[Tuple[str, str]] = [
    ("Google Generation Scholarship (HARD deadline)", EMAIL_1),
    ("Microsoft Summer Internship (ROLLING)", EMAIL_2),
    ("MIT AI Fellowship (SOFT_EARLY deadline)", EMAIL_3),
    ("ACM-ICPC Competition (RELATIVE deadline)", EMAIL_4),
    ("FutureTech Research Program (UNKNOWN deadline)", EMAIL_5),
    ("Stanford PhD Position (HARD deadline)", EMAIL_6),
    ("LocalTech Internship (ROLLING + location)", EMAIL_7),
    ("NSF Fellowship (SOFT_EARLY + financial need)", EMAIL_8),
    ("HackMIT Competition (HARD deadline)", EMAIL_9),
    ("Berkeley NLP Research Assistant (ROLLING + skills)", EMAIL_10),
    ("SPAM: Success Newsletter", EMAIL_11),
    ("SPAM: Work From Home Scam", EMAIL_12),
]


def get_sample_emails() -> List[Tuple[str, str]]:
    """Returns all sample emails with their descriptions."""
    return SAMPLE_EMAILS


def get_opportunity_emails() -> List[Tuple[str, str]]:
    """Returns only genuine opportunity emails (excludes spam)."""
    return [(desc, email) for desc, email in SAMPLE_EMAILS if not desc.startswith("SPAM")]


def get_spam_emails() -> List[Tuple[str, str]]:
    """Returns only spam emails."""
    return [(desc, email) for desc, email in SAMPLE_EMAILS if desc.startswith("SPAM")]
