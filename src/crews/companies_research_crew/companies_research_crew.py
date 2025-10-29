import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import ScrapeWebsiteTool
from tools.ddgs_tool import DuckDuckGoSearchTool

@CrewBase
class CompaniesResearchCrew():
	"""CompaniesResearch crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	llm_model : LLM = None
	inputs:dict = None
	
	def __init__(self, inputs:dict, model:str=None):
		self.llm_config(model)
		self.inputs = inputs

	def llm_config(self, model:str) -> LLM:
		self.llm_model = LLM(
			model=os.getenv('RESEARCH_LLM_MODEL', 'gpt-5-mini') if not model else model,
		)
		return self.llm_model

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[DuckDuckGoSearchTool(), ScrapeWebsiteTool()],
			llm=self.llm_model,
			verbose=True
		) # type: ignore

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			llm=self.llm_model,
			verbose=True,
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