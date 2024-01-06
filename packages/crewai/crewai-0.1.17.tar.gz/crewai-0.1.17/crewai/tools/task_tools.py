import inspect
from typing import List

from langchain.tools import Tool
from pydantic import BaseModel, Field

from crewai.agent import Agent


class TaskTools(BaseModel):
	"""Default tools around task outcomes retrieval"""

	outcomes: dict = Field(description="List of tasks outcomes.")

	def tools(self):
		return [
			Tool.from_function(
				func=self.retrieve_outcome,
				name="Retrieve previous tasks outcome",
				description=inspect.cleandoc(f"""Useful to retrieve the outcome of a previously completed task.
				The input to this tool should be one of the available task.
				Available tasks:
				{self.__format_outcomes()}
				"""
				),
			),
		]

	def retrieve_outcome(self, description):
			"""Useful to retrieve the outcome of a completed task."""
			if not description:
				return "\nError using tool. Missing the task input."

			if description not in self.outcomes.keys():
				return inspect.cleandoc(f"""\
						Error using tool. Task not found, use one of the available tasks.
						Available tasks:
						{self.__format_outcomes()}
					""")

			return self.outcomes[description]

	def __format_outcomes(self):
			"""Format outcomes dict to string."""
			return "\n".join([f"- {key}" for key in self.outcomes.keys()])