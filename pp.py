import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_detailed_presentation():
    prs = Presentation()

    # Helper function to create a slide
    def add_slide(title, subtitle=None, content_list=None):
        # Use a layout with a title and content (Layout index 1 usually)
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        
        # Set Title
        title_shape = slide.shapes.title
        title_shape.text = title
        
        # Set Body Content
        body_shape = slide.shapes.placeholders[1]
        tf = body_shape.text_frame
        tf.word_wrap = True
        
        if subtitle:
            p = tf.add_paragraph()
            p.text = subtitle
            p.font.bold = True
            p.font.size = Pt(22)
            p.font.color.rgb = None # Reset color if needed
            
        if content_list:
            for item in content_list:
                p = tf.add_paragraph()
                p.text = item
                p.font.size = Pt(18)
                p.level = 0

    # --- Slide 1: Title ---
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "HCL AppScan 360: Security for Our Digital Future"
    slide.placeholders[1].text = "Enabling High-Velocity Development for eCommerce & Loyalty\n[Date] | [Presenter Name]"

    # --- Slide 2: Pain Points ---
    add_slide(
        "The 'Why': Friction Between Speed and Security",
        "The Security Gap in Our Transformation:",
        [
            "• The Pen-Test Bottleneck: Manual testing (1-2 weeks) cannot match our daily release goal.",
            "• Blind Spots: No visibility into 3rd-party open-source risks (SCA) in our Loyalty app.",
            "• Developer Friction: Security reports are currently 'thrown over the wall' as PDFs.",
            "• Risk: We are building faster than we can secure."
        ]
    )

    # --- Slide 3: Vision ---
    add_slide(
        "Our Vision: 'Secure by Design'",
        "Building a DevSecOps Culture:",
        [
            "• Shift Left: Move security to the Code/Build phase (Fixing bugs at $10 vs $10,000).",
            "• Guardrails, Not Gates: Automated checks that guide developers rather than stopping them.",
            "• Compliance as Code: Automating PCI-DSS checks for our new financial data flows.",
            "• Zero Trust: Verifying every line of code, proprietary or open-source."
        ]
    )

    # --- Slide 4: Solution Deep Dive ---
    add_slide(
        "The Solution: HCL AppScan 360",
        "A Unified Enterprise Platform:",
        [
            "• Centralized '360' Visibility: Single dashboard for C-Suite risk management.",
            "• SAST (Static): Scans source code for logic errors (e.g., SQL Injection).",
            "• DAST (Dynamic): Simulates hacker attacks on the running application.",
            "• SCA (Composition): Identifies vulnerable open-source libraries (e.g., Log4j).",
            "• Deployment: On-premise control to keep our proprietary IP and data secure."
        ]
    )

    # --- Slide 5: Innovation ---
    add_slide(
        "Technological Edge: Intelligent Analytics",
        "Solving the 'Noise' Problem:",
        [
            "• The Challenge: Traditional scanners flood developers with False Positives.",
            "• Intelligent Finding Analytics (IFA): Uses Machine Learning to filter out 90%+ of noise.",
            "• Result: Developers only see issues that are real and exploitable.",
            "• Scalability: Containerized architecture grows automatically with our build volume."
        ]
    )

    # --- Slide 6: Developer Focus ---
    add_slide(
        "Empowering Developers: 'Fix Groups'",
        "Solving Problems, Not Just Finding Them:",
        [
            "• Fix Groups: Groups 1,000 issues into 1 'Root Cause' (e.g., 1 validation fix resolves 500 alerts).",
            "• IDE Integration: Plugins for VS Code/IntelliJ let devs scan while they write.",
            "• Educational Support: Provides code snippets and 'How-to-Fix' guides directly in the tool.",
            "• Reduced Friction: Security becomes a helper, not a blocker."
        ]
    )

    # --- Slide 7: Critical Use Case ---
    add_slide(
        "Protecting the eCommerce Launch",
        "Specific Risks We Must Mitigate:",
        [
            "• PCI-DSS Compliance: Built-in templates to ensure payment page security.",
            "• API Security: DAST specifically tests the heavy API usage in our Loyalty platform.",
            "• Data Leakage: Detects hardcoded secrets (passwords/keys) before they commit to Git.",
            "• Brand Reputation: Prevents breaches during our high-visibility launch."
        ]
    )

    # --- Slide 8: CI/CD Integration ---
    add_slide(
        "Integration: The 'Quality Gate'",
        "Automated Pipeline Workflow:",
        [
            "1. Code Commit: Developer pushes code.",
            "2. Auto-Scan: Jenkins/GitLab triggers AppScan 360.",
            "3. The Gate: If Critical Vulnerability found -> BUILD FAILS.",
            "4. Feedback: Developer gets instant alert with fix details.",
            "• Outcome: No critical vulnerability ever reaches Production."
        ]
    )

    # --- Slide 9: ROI ---
    add_slide(
        "ROI & Business Justification",
        "Why This Investment Pays Off:",
        [
            "• Cost Efficiency: Drastically lowers remediation costs by finding bugs early.",
            "• Productivity: 'Fix Groups' reduce developer triage time by up to 70%.",
            "• Automation: Saves ~20 hours/week of manual security review time.",
            "• Market Trust: Positions our platform as 'Enterprise Secure' for partners."
        ]
    )

    # --- Slide 10: Next Steps ---
    add_slide(
        "Conclusion & Roadmap",
        "The Path Forward:",
        [
            "• Phase 1 (Month 1): Deploy AppScan 360 On-Prem. Integrate with eCommerce Pilot.",
            "• Phase 2 (Month 3): Enforce 'Quality Gates'. Enable SCA for open-source.",
            "• Phase 3 (Month 6): Full rollout to Loyalty platform and legacy apps.",
            "• Ask: Approval for procurement and PoC kickoff."
        ]
    )

    prs.save('HCL_AppScan_360_Detailed_Case.pptx')
    print("Presentation saved as 'HCL_AppScan_360_Detailed_Case.pptx'")

if __name__ == "__main__":
    try:
        create_detailed_presentation()
    except ImportError:
        print("Error: python-pptx library not found. Run: pip install python-pptx")