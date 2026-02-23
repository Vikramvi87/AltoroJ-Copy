from pptx import Presentation
from pptx.util import Inches, Pt

def create_appscan_presentation():
    prs = Presentation()

    # Slide content: (Title, Content List)
    slides_data = [
        ("HCL AppScan 360 Implementation", 
         ["Securing the Future of our eCommerce & Loyalty Platforms", 
          "Vision: Transitioning to a Tech-First Organization"]),
        
        ("The Business Case – Why Now?", 
         ["Problem: Manual, fragmented security is a bottleneck.",
          "Risk: Brand damage to new Loyalty/eCommerce programs.",
          "Goal: Move from 'Reactionary' to 'Proactive' Resilience.",
          "Solution: Unified 360-degree view of risk."]),
        
        ("Our Vision – Becoming a Tech Company", 
         ["Continuous Development: Supporting 'Daily Releases'.",
          "In-House Ownership: We own the code and the liability.",
          "Strategy: Shift Left (fix at the desk) and Automation (guardrails)."]),
        
        ("HCL AppScan 360 – The Unified Ecosystem", 
         ["One Platform: Merging SAST, DAST, SCA, and IAST.",
          "Cloud Native: Scalable via Containers/Kubernetes.",
          "Data Sovereignty: Private Cloud or On-Prem deployment options."]),
        
        ("Protecting the eCommerce Engine (SAST & DAST)", 
         ["SAST: Scans proprietary logic before compilation.",
          "DAST: Tests the live site from a 'Hacker-view'.",
          "AI Edge: IFA filters out 98% of false positives."]),
        
        ("The Loyalty Platform & Open Source (SCA)", 
         ["Risk: 80% of modern apps use open-source libraries.",
          "SCA: Identifies vulnerable 3rd-party components.",
          "Compliance: Automatically generates SBOM (Software Bill of Materials)."]),
        
        ("Handling the 'Year 1' Stabilization", 
         ["Incremental Scanning: Test only what changed today.",
          "API Security: Auto-discover new endpoints as they are built.",
          "Speed: Matches the velocity of our internal dev team."]),
        
        ("Empowering Developers (Not Blocking)", 
         ["IDE Integration: Feedback inside VS Code / IntelliJ.",
          "AI Auto-Remediation: Actual code fix suggestions.",
          "CI/CD Ready: Jenkins, GitHub Actions, and GitLab integration."]),
        
        ("Executive Dashboard & Governance", 
         ["Single Pane of Glass: Risk view across all platforms.",
          "Compliance: Out-of-the-box PCI-DSS and GDPR reporting.",
          "Scorecards: Track security improvement during Year 1."]),
        
        ("Conclusion & Next Steps", 
         ["Finalize eCommerce tech stack requirements.",
          "Launch 30-day PoC on Loyalty sub-module.",
          "Integrate into the main CI/CD pipeline."])
    ]

    for title_text, bullet_points in slides_data:
        # Using a standard bullet point layout
        slide_layout = prs.slide_layouts[1] 
        slide = prs.slides.add_slide(slide_layout)
        
        # Set Title
        title = slide.shapes.title
        title.text = title_text
        
        # Set Body
        tf = slide.placeholders[1].text_frame
        tf.word_wrap = True
        
        for point in bullet_points:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
            p.space_after = Pt(10)

    # Save the presentation
    file_name = "HCL_AppScan_360_Business_Case.pptx"
    prs.save(file_name)
    print(f"Presentation saved as {file_name}")

if __name__ == "__main__":
    create_appscan_presentation()