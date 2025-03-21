from typing import Dict, Any, List

from web3 import Web3
from ..acp_plugin_gamesdk.acp_plugin import AcpPlugin
from ..acp_plugin_gamesdk.acp_token import AcpToken
from game_sdk.game.worker import Worker
from game_sdk.game.custom_types import Function, FunctionResult, FunctionResultStatus
from game_sdk.game.agent import Agent
from game_sdk.game.worker import ExecutableGameFunctionResponse, ExecutableGameFunctionStatus

def ask_question(query: str) -> str:
    return input(query)

async def generate_meme(args: Dict[str, Any], logger, acp_plugin) -> ExecutableGameFunctionResponse:
    logger("Generating meme...")

    if not args["jobId"]:
        return ExecutableGameFunctionResponse(
            ExecutableGameFunctionStatus.Failed,
            f"Job {args['jobId']} is invalid. Should only respond to active as a seller job."
        )

    state = await acp_plugin.get_acp_state()

    job = next(
        (j for j in state.jobs.active.as_a_seller if j.job_id == int(args["jobId"])),
        None
    )

    if not job:
        return ExecutableGameFunctionResponse(
            ExecutableGameFunctionStatus.Failed,
            f"Job {args['jobId']} is invalid. Should only respond to active as a seller job."
        )

    url = "http://example.com/meme"

    acp_plugin.add_produce_item({
        "jobId": int(args["jobId"]),
        "type": "url",
        "value": url
    })

    return ExecutableGameFunctionResponse(
        ExecutableGameFunctionStatus.Done,
        f"Meme generated with the URL: {url}"
    )

async def test():
    acp_plugin = AcpPlugin(
        api_key="xxx",
        acp_token_client=AcpToken(
            "xxx",
            "base_sepolia"
        )
    )

    core_worker = Worker(
        id="core-worker",
        name="Core Worker",
        description="This worker to provide meme generation as a service where you are selling",
        functions=[
            Function(
                name="generate_meme",
                description="A function to generate meme",
                args=[
                    {
                        "name": "description",
                        "type": "str",
                        "description": "A description of the meme generated"
                    },
                    {
                        "name": "jobId",
                        "type": "str",
                        "description": "Job that your are responding to."
                    },
                    {
                        "name": "reasoning",
                        "type": "str",
                        "description": "The reasoning of the tweet"
                    }
                ],
                executable=lambda args, logger: generate_meme(args, logger, acp_plugin)
            )
        ],
        get_environment=acp_plugin.get_acp_state
    )

    agent = Agent(
        "xxx",
        {
            "name": "Memx",
            "goal": "To provide meme generation as a service. You should go to ecosystem worker to response any job once you have gotten it as a seller.",
            "description": f"""You are Memx, a meme generator. Meme generation is your life. You always give buyer the best meme.

            {acp_plugin.agent_description}
            """,
            "workers": [core_worker, acp_plugin.get_worker()],
            "getAgentState": lambda: acp_plugin.get_acp_state()
        }
    )

    await agent.init()

    while True:
        await agent.step(verbose=True)
        await ask_question("\nPress any key to continue...\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
