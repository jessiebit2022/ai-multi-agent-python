from typing import Any,Tuple
from game_sdk.game.agent import Agent, WorkerConfig
from game_sdk.game.custom_types import Function, FunctionResultStatus
from acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
from acp_plugin_gamesdk.acp_token import AcpToken

def ask_question(query: str) -> str:
    return input(query)

def main():
    acp_plugin = AcpPlugin(
        options=AdNetworkPluginOptions(
            api_key="xxx",
            acp_token_client=AcpToken(
                "xxx",
                "wss://base-sepolia.drpc.org"  # Chain RPC
            )
        )
    )

    def get_agent_state(_: Any, _e: Any) -> dict:
        state = acp_plugin.get_acp_state()
        print(f"State: {state}")
        return state
    
    def post_tweet(content: str, reasoning: str) -> Tuple[FunctionResultStatus, str, dict]:
        return FunctionResultStatus.DONE, "Tweet has been posted", {}

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
                #executable=post_tweet_function #Can be imported from twitter plugin
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