from langchain.llms.base import BaseLLM
from langchain.chains.base import Chain
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, AgentExecutor
from typing import List
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..schema import LatLng, AirAiResponse
from .prompts import AIR_QUALITY_AGENT_PROMPT, IDENTITY_INSTRUCTIONS
from .tools import LocateUserTool, AskPretrainedTool
from datetime import datetime
import os

__DEV__ = os.getenv("ENV_NAME") == "dev"


class AirAiChain(Chain):
    """
    Receives natural language asks and returns full responses in the form of AirAiResponse.

    This is only partially implements the Chain interface.
    TODO Complete as needed
    """

    llm: BaseLLM

    agent: AgentExecutor
    agent_prompt: PromptTemplate

    def __init__(self, user_lat_lng: LatLng | None) -> None:
        # Dummy initialization to make Pydantic and Mypy happy at the same time.
        # TODO Find a better workaround for this.
        super().__init__(
            llm=OpenAI(),  # type: ignore
            agent=initialize_agent(llm=OpenAI(), tools=[]),  # type: ignore
            agent_prompt=PromptTemplate(template="", input_variables=[]),  # type: ignore
        )

        llm = OpenAI(temperature=0.1, client=None)

        self.llm = llm

        self.agent = initialize_agent(
            tools=[LocateUserTool(user_lat_lng), AskPretrainedTool(llm)],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=__DEV__,
            max_execution_time=30,
        )

        # LangChain doesn't seem to have chains that link Agents and Prompts together
        # TODO write something to encapsulate this
        self.agent_prompt = PromptTemplate(
            template=AIR_QUALITY_AGENT_PROMPT,
            input_variables=["query"],
            partial_variables={
                "date": datetime.utcnow().strftime("%B %d, %Y"),
                "identity": IDENTITY_INSTRUCTIONS,
            },
        )

    async def acall(self, query: str) -> AirAiResponse:
        context_prompt = self.agent_prompt.format_prompt(query=query)
        if __DEV__:
            print(f"Agent prompt after fromatting\n{context_prompt.to_string()}")
        agent_answer = await self.agent.arun(context_prompt.to_string())

        response = AirAiResponse(answer=agent_answer, facts=[], auxiliary_data=[])

        return response

    @property
    def input_keys(self) -> List[str]:
        return []

    @property
    def output_keys(self) -> List[str]:
        return []

    def run(self):
        raise NotImplementedError()

    def call(self, query: str):
        raise NotImplementedError()

    def _call(self):
        raise NotImplementedError()

    def _acall(self, args):
        raise NotImplementedError()
