import os

from acp_plugin_gamesdk.acp_plugin import AcpToken, AcpPlugin, AcpPluginOptions
from dotenv import load_dotenv

load_dotenv()


def reset_acp_states() -> None:
    """Reset plugin state for all configured ACP tokens."""
    agent_wallet_addresses = [
        os.environ.get("BUYER_AGENT_WALLET_ADDRESS"),
        os.environ.get("SELLER_AGENT_WALLET_ADDRESS")
    ]
    for agent_wallet_address in agent_wallet_addresses:
        try:
            api_key = os.environ.get("GAME_DEV_API_KEY")
            print(f"Resetting state for agent: {agent_wallet_address}")
            acp_plugin = AcpPlugin(
                options=AcpPluginOptions(
                    api_key=api_key,
                    acp_token_client=AcpToken(
                        os.environ.get("WHITELISTED_WALLET_PRIVATE_KEY"),
                        agent_wallet_address,
                        "https://base-sepolia-rpc.publicnode.com/"
                    )
                )
            )
            acp_plugin.reset_state()
            new_state = acp_plugin.acp_client.get_state()
            print(new_state)
            print(f"Successfully reset state for agent: {agent_wallet_address}")
        except Exception as e:
            print(f"Failed to reset state for agent {agent_wallet_address}: {e}")


if __name__ == "__main__":
    reset_acp_states()
