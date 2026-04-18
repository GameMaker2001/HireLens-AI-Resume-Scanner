# HireLens-AI-Resume-Scanner
A high precision career dashboard that uses GPT-4o to show you where your resume is and where it needs to be.

I built this because "good enough" isn't actually good enough when you're gunning for top tier roles. Whether it's AI, engineering or music, you want the mix to be perfect. So it doesn't just tell you that you're a "match", it breaks down exactly where your skill gaps are and gives you the "Quick Fixes" needed to lock in that 100% score.

You can try the production version of the dashboard here:  
[Live App Link](https://hirelens-ai-resume-scanner-sdekhksarnkobkejyvfgn5.streamlit.app/)  
*(Note: You'll need your own OpenAI API key to run a scan on the live demo for security reasons. Submit your job description and a resume.

### How to Run It (In your IDE for recreational purposes):
1. Clone the repo.
2. Add your `OPENAI_API_KEY` to a `.env` file (don't push this to GitHub!).
3. Install the requirements: `pip install -r requirements.txt`
4. Run the app: `streamlit run Main.py`
5. Upload job description
6. Upload resume document and see your progress


### What’s Under the Hood?
* **LLM Analysis:** Powered by GPT-4o for high context document comparison.
* **Skill Overlap Wheel:** A dynamic Plotly radar chart that visualizes your Technical, Soft Skill, and Experience alignment.
* **Precision Extraction:** Custom regex and PyPDF2 logic to clean up messy PDF text before the AI even touches it.
* **Streamlit UI:** A low contrast, dark-mode interface designed for high-end performance monitoring.

---
*Built by [Ezra Bakatubia] | 2026*
