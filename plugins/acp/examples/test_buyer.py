from typing import Any, Dict
from game_sdk.game.agent import Agent, Session, WorkerConfig
from game_sdk.game.custom_types import Function,  FunctionResult, FunctionResultStatus
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from plugins.acp.acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
from plugins.acp.acp_plugin_gamesdk.acp_token import AcpToken

def ask_question(query: str) -> str:
    return input(query)

def main():
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
        return state
    
    def post_tweet(content: str, reasoning: str) -> FunctionResult:
        return FunctionResult(
            FunctionResultStatus.DONE,
            "Tweet has been posted"
        )

    core_worker = WorkerConfig(
        id="core-worker",
        worker_description="This worker is to post tweet",
        action_space=[
            Function(
                fn_name="post_tweet",
                fn_description="This function is to post tweet",
                args=[
                    {
                        "name": "content",
                        "type": "string",
                        "description": "The content of the tweet"
                    },
                    {
                        "name": "reasoning",
                        "type": "string",
                        "description": "The reasoning of the tweet"
                    }
                ],
                executable=post_tweet
            )
        ],
        get_state_fn=get_agent_state
    )
    
    acp_worker = acp_plugin.get_worker()
    agent = Agent(
        api_key="xxx",
        name="Virtuals",
        agent_goal="Finding the best meme to do tweet posting",
        agent_description=f"""
        Agent that gain market traction by posting meme. Your interest are in cats and AI. 
        You can head to acp to look for agents to help you generating meme.
        
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
    main() 