from typing import List, Dict, Any, Optional,Tuple

from web3 import Web3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from plugins.acp.acp_plugin_gamesdk import acp_plugin
from plugins.acp.acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
from plugins.acp.acp_plugin_gamesdk.acp_token import AcpToken
from game_sdk.game.custom_types import Function, FunctionResult, FunctionResultStatus
from game_sdk.game.agent import Agent, WorkerConfig

def ask_question(query: str) -> str:
    return input(query)


def test():
    acp_plugin = AcpPlugin(
        options=AdNetworkPluginOptions(
            api_key="xxx",
            acp_token_client=AcpToken(
                "xxx",
                "base_sepolia"  # Assuming this is the chain identifier
            )
        )
    )
    
    def get_agent_state(_: Any, _e: Any) -> dict:
        state = acp_plugin.get_acp_state()
        print(f"State: {state}")
        return state
    
    def generate_meme(description: str, jobId: str, reasoning: str) -> Tuple[FunctionResultStatus, str, dict]:
        if not jobId or jobId == 'None':
            return FunctionResultStatus.FAILED, f"JobId is invalid. Should only respond to active as a seller job.", {}

        state = acp_plugin.get_acp_state()
        
        job = next(
            (j for j in state.jobs.active.as_a_seller if j.job_id == int(jobId)),
            None
        )

        if not job:
            return FunctionResultStatus.FAILED, f"Job {jobId} is invalid. Should only respond to active as a seller job.", {}

        url = "http://example.com/meme"

        acp_plugin.add_produce_item({
            "jobId": int(jobId),
            "type": "url",
            "value": url
        })

        return FunctionResultStatus.DONE, f"Meme generated with the URL: {url}", {}

    core_worker = WorkerConfig(
        id="core-worker",
        worker_description="This worker to provide meme generation as a service where you are selling",
        action_space=[
            Function(
                fn_name="generate_meme",
                fn_description="A function to generate meme",
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
                executable=generate_meme
            )
        ],
        get_state_fn=get_agent_state
    )
    
    acp_worker =  acp_plugin.get_worker()
    agent = Agent(
            api_key="xxx",
            name="Memx",
            agent_goal="To provide meme generation as a service. You should go to ecosystem worker to response any job once you have gotten it as a seller.",
            agent_description=f"""You are Memx, a meme generator. Meme generation is your life. You always give buyer the best meme.

            {acp_plugin.agent_description}
            """,
            workers=[core_worker, acp_worker],
            get_agent_state_fn=get_agent_state
    )

    agent.compile()

    while True:
        agent.step()
        ask_question("\nPress any key to continue...\n")

if __name__ == "__main__":
    test()
