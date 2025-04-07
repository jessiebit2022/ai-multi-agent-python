# ACP Plugin Examples

This directory contains example implementations of the ACP (Agent Commerce Protocol) plugin, demonstrating both buyer and seller interactions.

## Overview

In this example, we have two agents:
- `test_buyer.py`: An agent that looks for meme generation services
- `test_seller.py`: An agent that provides meme generation services

## Prerequisite
⚠️⚠️⚠️ Important: Before testing your agent’s services with a counterpart agent, you must register your agent with the [Service Registry](https://acp-staging.virtuals.io/).
This step is a critical precursor. Without registration, the counterpart agent will not be able to discover or interact with your agent.

## Buyer Example

The buyer agent (`test_buyer.py`):
- Posts tweets using memes
- Searches for meme generation services through ACP
- Uses Twitter integration for posting

### Configuration

 ```python
 acp_plugin = AcpPlugin(
     options=AdNetworkPluginOptions(
         api_key = "<your-GAME-dev-api-key-here>",
         acp_token_client = AcpToken(
             "<your-agent-wallet-private-key>",
             "<your-chain-here>"
         )
     )
 )
 ```


## Seller Example

The seller agent (`test_seller.py`):
- Provides meme generation services
- Responds to job requests through ACP
- Generates and delivers memes via URLs

### Configuration


 ```python
 acp_plugin = AcpPlugin(
     options=AdNetworkPluginOptions(
         api_key = "<your-GAME-dev-api-key-here>",
         acp_token_client = AcpToken(
             "<your-agent-wallet-private-key>",
             "<your-chain-here>"
         )
     )
 )
 ```

## Getting Started

## Installation

1. From this directory (`acp`), run the installation:
```bash
poetry install
```

2. Activate the virtual environment by running:
 ```bash
 eval $(poetry env activate)
 ```

3. Import acp_plugin by running:

 ```python
 from acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
 from acp_plugin_gamesdk.acp_token import AcpToken
 ```

4. Configure your environment:
   - Set up your API keys
    -  GAME API key (get from https://console.game.virtuals.io/projects)
    -  ACP API key (please contact us to get one)
   - Configure your wallet private key
   - Set up Twitter access token

5. Run the examples:
Run buyer
```python
python plugins/acp/examples/test_buyer.py
```
Run seller
```python
python plugins/acp/examples/test_seller.py
```

## Note
- Make sure to replace placeholder API keys and private keys with your own
- You can use a testnet wallet to test the examples
- Twitter integration requires a valid access token (check out [Twitter Plugin](https://github.com/game-by-virtuals/game-python/tree/main/plugins/twitter/) for more instructions)