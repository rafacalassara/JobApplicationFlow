
from crewai.flow.flow import Flow, listen, start

from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew
from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
from job_app_state import JobAppState
from tools.convert_resume_to_pdf import convert_md_to_pdf
from pathlib import Path
from paths import from_root

from dotenv import load_dotenv

load_dotenv()


class JobApplicationFlow(Flow[JobAppState]):
    @start()
    def init(self):
        pass

    @listen(init)
    def companies_research_crew(self):
        crew = CompaniesResearchCrew(inputs=self.state.model_dump())
        result = crew.crew().kickoff(inputs=self.state.model_dump())
        return result

    @listen(companies_research_crew)
    def tailor_resume(self):
        crew = TailorResumeCrew(inputs=self.state.model_dump())
        result = crew.crew().kickoff(inputs=self.state.model_dump())
        return result

    @listen(tailor_resume)
    def convert_resume_to_pdf(self):
        md_path = Path(self.state.crew_generated_resume_path)
        pdf_path = md_path.with_suffix('.pdf')
        css_path = from_root("src", "md-to-pdf.css")
        return convert_md_to_pdf(
            markdown_file=md_path,
            output_pdf=pdf_path,
            css_file=css_path
        )


def kickoff(inputs:dict):
    job_application_flow = JobApplicationFlow()
    job_application_flow.kickoff(inputs=inputs)


def plot():
    job_application_flow = JobApplicationFlow()
    job_application_flow.plot()


if __name__ == "__main__":
    kickoff({
        'job_posting':'https://www.linkedin.com/jobs/view/4294108202',
        'resume_language':'pt-br'
    })
    # plot()
