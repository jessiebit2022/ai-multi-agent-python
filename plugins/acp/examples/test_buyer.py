import asyncio
from typing import Any, Dict
from game_sdk.game.agent import Agent, WorkerConfig
from game_sdk.game.custom_types import Function,  FunctionResult, FunctionResultStatus
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from plugins.acp.acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
from plugins.acp.acp_plugin_gamesdk.acp_token import AcpToken

async def ask_question(query: str) -> str:
    print(query, end='')
    return input()

async def post_tweet(args: Dict[str, Any], logger: callable) -> FunctionResult:
    logger("Posting tweet...")
    logger(f"Content: {args['content']}. Reasoning: {args['reasoning']}")
    
    return FunctionResult(
        FunctionResultStatus.DONE,
        "Tweet has been posted"
    )
    
async def main():
    acp_plugin = AcpPlugin(
        options=AdNetworkPluginOptions(
            api_key="apt-2e7f33d88ef994b056f2a247a5ed6168",
            acp_token_client=AcpToken(
                "0x8d2bc0d18b87b12aa435b66b2e13001ef5c395de063cdad15805c1d147fde68e",
                "base_sepolia"  # Assuming this is the chain identifier
            )
        )
    )

    def get_agent_state(_: Any, _e: Any) -> dict:
        state = acp_plugin.get_acp_state()
        return state

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
    
    acp_worker =  acp_plugin.get_worker()
    agent =  Agent(
        api_key="apt-98f312ab3078757c3682a7703455ab73",
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
    agent.run()

    while True:
        await agent.step()
        await ask_question("\nPress any key to continue...\n")

if __name__ == "__main__":
    asyncio.run(main()) 