#!/usr/bin/env python
from crewai.flow.flow import Flow, listen, start

from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew
from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
from crews.email_writer_crew.email_writer_crew import EmailWriterCrew

from dotenv import load_dotenv

load_dotenv()

class JobApplicationFlow(Flow):
    def __init__(self, inputs:dict={}, **kwargs):
        super().__init__(**kwargs)        

        self.inputs = {
            "base_resume": "inputs/base_resume.md",

            "linkedin_md_target_resume_path": "outputs/linkedin_md_target_resume.md",
            "crew_generated_resume_path": "outputs/crew_generated_resume.md",
            
            "company_report_path": "outputs/company_report.md",
            
            "email_file_path": "outputs/email.md",
            "reviewed_email_file_path": "outputs/reviewed_email.md",
            "job_posting": 'https://www.linkedin.com/jobs/view/4060688413/',
            "linkedin_source_resume_path": "inputs/source_resume.pdf",

            # Hard coded inputs
            "company": "L3 IT is about People",
            "company_url" : "https://l3.com.br/",
            "company_location": "São Paulo, São Paulo",
            "user_considerations_for_resume_crew": "If the person dont have a needed hability, dont include.",
            "user_considerations_for_companies_research_crew": "",
            "user_considerations_for_email_crew": """
                Include the fact that the user wrote the email based on a search on the company made by a crew of artificial inteligence agents.
                Write the email in Portuguese.
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
    def email_writer(self):
        return EmailWriterCrew(self.inputs).crew().kickoff(self.inputs)


def kickoff():
    job_application_flow = JobApplicationFlow()
    job_application_flow.kickoff()


def plot():
    job_application_flow = JobApplicationFlow()
    job_application_flow.plot()


if __name__ == "__main__":
    kickoff()
    # plot()
