from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, FileReadTool, PDFSearchTool

@CrewBase
class TailorResumeCrew():
    """TailorResume crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self,inputs:dict) -> None:
        super().__init__()
        self.inputs = inputs
    
    @agent
    def linkedin_pdf_cv_reader(self) -> Agent:
        
        return Agent(
            config=self.agents_config['linkedin_pdf_cv_reader'],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def job_requirements_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['job_requirements_extractor'],
            tools=[ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def resume_tailor(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_tailor'],
            allow_delegation=False,
            verbose=True,
            tools=[FileReadTool()],
        )

    # TASKS

    @task
    def pdf_to_md_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_to_md_cv_task'],
            agent=self.linkedin_pdf_cv_reader(),
            tools=[PDFSearchTool()],
            output_file=self.inputs['linkedin_md_target_resume_path']
        )

    @task
    def extract_job_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_job_requirements_task'],
            agent=self.job_requirements_extractor()
        )

    @task
    def tailor_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['tailor_resume_task'],
            agent=self.resume_tailor(),
            output_file=self.inputs['crew_generated_resume_path'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TailorResume crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
