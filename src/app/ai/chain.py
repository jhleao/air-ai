from langchain.llms.base import BaseLLM
from langchain.chains.base import Chain
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, AgentExecutor
from typing import List
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..schema import LatLng, AirAiResponse, AirDataPoint, LocationAirData
from .parsers import PipeSeparatedListOutputParser
from .prompts import (
    AIR_QUALITY_AGENT_PROMPT,
    IDENTITY_INSTRUCTIONS,
    AQI_INSTRUCTIONS,
    FACTS_PROMPT_TEMPLATE,
)
from .tools import LocateUserTool, AskPretrainedTool, GetAirQualityTool
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

    collected_aqi_data: dict[str, List[AirDataPoint]] = {}
    """
    Request-scoped state to hold all relevant AQI data from weather API
    So we prevent trusting the LLM to juggle this data around, which is unreliable (and expensive).
    """

    agent: AgentExecutor
    agent_prompt: PromptTemplate

    facts_chain: LLMChain
    facts_chain_parser: PipeSeparatedListOutputParser

    def __init__(self, user_lat_lng: LatLng | None) -> None:
        # Dummy initialization to make Pydantic and Mypy happy at the same time.
        # TODO Find a better workaround for this.
        super().__init__(
            llm=OpenAI(),  # type: ignore
            collected_aqi_data={},  # type: ignore
            agent=initialize_agent(llm=OpenAI(), tools=[]),  # type: ignore
            agent_prompt=PromptTemplate(template="", input_variables=[]),  # type: ignore
            facts_chain=LLMChain(llm=OpenAI(), prompt=PromptTemplate(template="", input_variables=[])),  # type: ignore
            facts_chain_parser=PipeSeparatedListOutputParser(),  # type: ignore
        )

        llm = OpenAI(temperature=0, client=None)

        self.llm = llm

        self.agent = initialize_agent(
            tools=[
                LocateUserTool(user_lat_lng),
                AskPretrainedTool(llm),
                GetAirQualityTool(self.collected_aqi_data),
            ],
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
                "aqi_instructions": AQI_INSTRUCTIONS,
            },
        )

        self.facts_chain_parser = PipeSeparatedListOutputParser()

        self.facts_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                template=FACTS_PROMPT_TEMPLATE,
                input_variables=["to_justify"],
                partial_variables={
                    "separator_format_instructions": self.facts_chain_parser.get_format_instructions(
                        "`emoji``whitespace`London is foo|`emoji``whitespace`London has bar|`emoji``whitespace`baz in London|`emoji``whitespace`London buzz|`emoji``whitespace`fizz"
                    )
                },
            ),
            verbose=__DEV__,
        )

    async def acall(self, query: str) -> AirAiResponse:
        context_prompt = self.agent_prompt.format_prompt(query=query)
        if __DEV__:
            print(f"Agent prompt after fromatting\n{context_prompt.to_string()}")
        agent_answer = await self.agent.arun(context_prompt.to_string())

        auxiliary_data = self.build_auxiliary_data()

        fact_to_jusitfy = self.get_fact_to_justify()
        facts = ""
        if fact_to_jusitfy:
            facts = await self.facts_chain.arun(to_justify=fact_to_jusitfy)
        parsed_facts = self.facts_chain_parser.parse(facts)

        response = AirAiResponse(
            answer=agent_answer, facts=parsed_facts, auxiliary_data=auxiliary_data
        )

        return response

    def build_auxiliary_data(self) -> List[LocationAirData]:
        """Builds a list of LocationAirData objects from the collected_aqi_data state."""
        if len(self.collected_aqi_data) == 0:
            return []
        return [
            LocationAirData(location_name=location_name, data=data)
            for location_name, data in self.collected_aqi_data.items()
        ]

    def get_fact_to_justify(self) -> str | None:
        """Depending on what collected_aqi_data looks like, returns different fact to be justified by facts_chain"""
        places = list(self.collected_aqi_data.keys())
        if len(places) == 0:
            return None
        if len(places) < 2:
            place_name = places[0]
            place_data = self.collected_aqi_data[places[0]]
            latest_aqi = place_data[-1].aqi
            air_quality = "high" if latest_aqi > 50 else "low"
            return f"{air_quality} air pollution levels of {place_name}."
        else:
            place_names_with_aqi = [
                f"{place_name} ({data[-1].aqi} AQI)"
                for place_name, data in self.collected_aqi_data.items()
            ]
            return f"difference in air pollution levels between {', '.join(place_names_with_aqi)}."

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
