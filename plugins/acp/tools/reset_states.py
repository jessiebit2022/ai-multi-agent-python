import os
from acp_plugin_gamesdk.acp_plugin import AcpToken, AcpPlugin, AdNetworkPluginOptions


def reset_acp_states() -> None:
    """Reset plugin state for all configured ACP tokens."""
    acp_tokens = [
        os.environ.get("ACP_TOKEN_BUYER"),
        os.environ.get("ACP_TOKEN_SELLER")
    ]

    for token in acp_tokens:
        try:
            acp_plugin = AcpPlugin(
                options=AdNetworkPluginOptions(
                    api_key=os.environ.get("GAME_DEV_API_KEY"),
                    acp_token_client=AcpToken(
                        token,
                        "https://base-sepolia-rpc.publicnode.com/"
                    )
                )
            )
            acp_plugin.reset_state()
            print(f"Successfully reset state for token: {token}")
        except Exception as e:
            print(f"Failed to reset state for token {token}: {e}")


if __name__ == "__main__":
    reset_acp_states()
