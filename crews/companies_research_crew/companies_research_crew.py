from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

@CrewBase
class CompaniesResearchCrew():
	def __init__(self, inputs:dict) -> None:
		super().__init__()
		self.inputs = inputs

	"""CompaniesResearch crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
			cache=True,
			verbose=True
		) # type: ignore

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		) # type: ignore

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		) # type: ignore

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file=self.inputs['company_report_path']
		) # type: ignore

	@crew
	def crew(self) -> Crew:
		"""Creates the CompaniesResearch crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)