#!/usr/bin/env python
from datetime import datetime
from crewai.flow.flow import Flow, listen, start

from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew
from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
from crews.email_writer_crew.email_writer_crew import EmailWriterCrew
from tools.convert_resume_to_pdf import convert_md_to_pdf

from dotenv import load_dotenv

load_dotenv()


class JobApplicationFlow(Flow):
    def __init__(self, inputs: dict = {}, **kwargs):
        super().__init__(**kwargs)

        self.inputs = {
            "base_resume": "inputs/base_resume.md",

            "linkedin_md_target_resume_path": "outputs/linkedin_md_target_resume.md",
            "crew_generated_resume_path": "outputs/crew_generated_resume.md",

            "company_report_path": "outputs/company_report.md",

            "email_file_path": "outputs/email.md",
            "reviewed_email_file_path": "outputs/reviewed_email.md",
            "linkedin_source_resume_path": "inputs/Profile.pdf",
            "current_date": datetime.now().strftime("%Y-%m-%d"),

            # Hard coded inputs
            "job_posting": 'https://www.linkedin.com/jobs/view/4177412562/',
            "company": "Dayos",
            "company_url": "https://www.dayos.com/",
            "company_location": "Downtown Core, Central Region",
            "resume_language": "en",
            "user_considerations_for_resume_crew": """
                If the person dont have a needed hability, dont include or fake information, only highlight the user habilities.
                Put an emphasis on the fact that the user is a developer with a knack for AI agentic systems.
                Remember to remove the company name from the resume.
                Remember to include all the certifications and degrees.
            """,
            "user_considerations_for_companies_research_crew": "",
            "user_considerations_for_email_crew": """
                Write the email in EN.
            """,
            **inputs
        }

    @start()
    def init(self):
        return self.inputs

    @listen(init)
    def companies_research_crew(self):
        result = CompaniesResearchCrew(self.inputs).crew().kickoff(self.inputs)
        return result

    @listen(companies_research_crew)
    def tailor_resume(self):
        return TailorResumeCrew(self.inputs).crew().kickoff(self.inputs)

    @listen(tailor_resume)
    def convert_resume_to_pdf(self):
        return convert_md_to_pdf(
            markdown_file=self.inputs["crew_generated_resume_path"],
            output_pdf=self.inputs["crew_generated_resume_path"].replace(".md", ".pdf"),
            css_file="md-to-pdf.css"
        )

    # @listen(tailor_resume)
    # def email_writer(self):
    #     return EmailWriterCrew(self.inputs).crew().kickoff(self.inputs)

def kickoff():
    job_application_flow = JobApplicationFlow()
    job_application_flow.kickoff()


def plot():
    job_application_flow = JobApplicationFlow()
    job_application_flow.plot()


if __name__ == "__main__":
    kickoff()
    # plot()
