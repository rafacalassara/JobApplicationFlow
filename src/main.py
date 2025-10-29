#!/usr/bin/env python
import os
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel, Field
from typing import Optional

from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew
from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
from job_app_state import JobAppState
from tools.convert_resume_to_pdf import convert_md_to_pdf

from dotenv import load_dotenv

load_dotenv()


class JobApplicationFlow(Flow[JobAppState]):
    def __init__(self, inputs: dict = {}, **kwargs):
        super().__init__(**kwargs)
        # Apenas o que vier de fora; defaults vivem no state.
        self.state = JobAppState(**inputs)

    @start()
    def init(self):
        pass

    @listen(init)
    def companies_research_crew(self):
        result = CompaniesResearchCrew(self.state.model_dump()).crew().kickoff(self.state.model_dump())
        return result

    @listen(companies_research_crew)
    def tailor_resume(self):
        return TailorResumeCrew(self.state.model_dump()).crew().kickoff(self.state.model_dump())

    @listen(tailor_resume)
    def convert_resume_to_pdf(self):
        return convert_md_to_pdf(
            markdown_file=self.state.crew_generated_resume_path,
            output_pdf=self.state.crew_generated_resume_path.replace(".md", ".pdf"),
            css_file="md-to-pdf.css"
        )


def kickoff(inputs:JobAppState):
    job_application_flow = JobApplicationFlow()
    job_application_flow.kickoff(inputs=inputs.model_dump())


def plot():
    job_application_flow = JobApplicationFlow()
    job_application_flow.plot()


if __name__ == "__main__":
    kickoff(JobAppState())
    # plot()
