from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool


@CrewBase
class EmailWriterCrew():
    """EmailWriter crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self,inputs:dict) -> None:
        super().__init__()
        self.inputs = inputs

    @agent
    def email_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['email_writer'],
            verbose=True,
        )

    @task
    def email_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_writer_task'],
            tools=[FileReadTool()],
            output_file=self.inputs['email_file_path']
        )
    
    @agent
    def application_examiner(self) -> Agent:
        return Agent(
            config=self.agents_config['application_examiner'],
            verbose=True,
        )

    @task
    def application_examiner_task(self) -> Task:
        return Task(
            config=self.tasks_config['application_examiner_task'],
            output_file=self.inputs['reviewed_email_file_path']
        )

    @ crew
    def crew(self) -> Crew:
        """Creates the EmailWriter crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
