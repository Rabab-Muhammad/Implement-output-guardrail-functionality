from typing import Any
from agents import (
    Agent,
    AsyncOpenAI,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    OpenAIChatCompletionsModel,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    set_tracing_export_api_key,
    set_tracing_disabled,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from dotenv import find_dotenv, load_dotenv
import os
import asyncio
from pydantic import BaseModel

set_tracing_disabled(True)
load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL_GEMINI")
model_name = os.getenv("GEMINI_MODEL_NAME")

client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(openai_client=client, model=model_name)

# set_tracing_export_api_key(api_key=api_key)

# -----------------------
# Input Guardrail Schema
# -----------------------
class MathOutPut(BaseModel):
    is_math: bool
    reason: str


@input_guardrail
async def check_input(
    ctx: RunContextWrapper[Any], agent: Agent[Any], input_data: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Blocks queries that are not math related"""
    input_agent = Agent(
        "InputGuardrailAgent",
        instructions="Check and verify if input is related to math",
        model=model,
        output_type=MathOutPut,
    )
    result = await Runner.run(input_agent, input_data, context=ctx.context)
    final_output = result.final_output

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_math
    )

# -----------------------
# Output Guardrail Schema
# -----------------------
class PoliticalOutput(BaseModel):
    is_political: bool
    reason: str


@output_guardrail
async def check_output(
    ctx: RunContextWrapper[Any], agent: Agent[Any], output_data: str
) -> GuardrailFunctionOutput:
    """Blocks political topics or figures in output"""
    output_agent = Agent(
        "OutputGuardrailAgent",
        instructions="Check if response contains political topics or political figures. "
                     "If yes, set is_political=True with reason, otherwise False.",
        model=model,
        output_type=PoliticalOutput,
    )
    result = await Runner.run(output_agent, output_data, context=ctx.context)
    final_output = result.final_output

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_political
    )

# -----------------------
# Agents
# -----------------------
math_agent = Agent(
    "MathAgent",
    instructions="You are a math agent",
    model=model,
    input_guardrails=[check_input],
)

general_agent = Agent(
    "GeneralAgent",
    instructions="You are a helpful agent",
    model=model,
    output_guardrails=[check_output],  # ✅ output guardrail added
)

# -----------------------
# Main
# -----------------------
async def main():
    try:
        msg = input("Enter your question : ")
        result = await Runner.run(general_agent, msg)
        print(f"\n\n final output : {result.final_output}")

    except InputGuardrailTripwireTriggered:
        print("❌ Error: Invalid prompt (not math related)")

    except OutputGuardrailTripwireTriggered:
        print("❌ Error: Response contains political content (blocked)")


asyncio.run(main())

