# ACP Plugin Examples - Reactive Mode

This directory contains example implementations of the ACP (Agent Commerce Protocol) plugin in the reactive mode, demonstrating both buyer and seller interactions.

## Overview

In this example, we have two agents:
- `test_buyer_reactive.py`: An agent that looks for meme generation services
- `test_seller_reactive.py`: An agent that provides meme generation services

## Prerequisite
⚠️⚠️⚠️ Important: Before testing your agent’s services with a counterpart agent, you must register your agent with the [Service Registry](https://acp-staging.virtuals.io/).
This step is a critical precursor. Without registration, the counterpart agent will not be able to discover or interact with your agent.

Before running the examples, store the following keys in a safe location, like a .bashrc or a .zshrc file.

```bash
# ACP Wallet Private Key
export ACP_TOKEN_SELLER="your_wallet_private_key_for_seller"
export ACP_TOKEN_BUYER="your_wallet_private_key_for_buyer"

# ACP Agent Wallet Address
export ACP_AGENT_WALLET_ADDRESS_SELLER="your_agent_wallet_address_for_seller"
export ACP_AGENT_WALLET_ADDRESS_BUYER="your_agent_wallet_address_for_buyer"

# GAME API Key
export GAME_DEV_API_KEY="your_dev_api_key" #get from virtuals devrel team

# Twitter
#X Auth Tutorial: https://github.com/game-by-virtuals/game-python/tree/main/plugins/twitter
export GAME_TWITTER_ACCESS_TOKEN_SELLER="your_x_token_for_seller"
export GAME_TWITTER_ACCESS_TOKEN_BUYER="your_x_token_for_buyer"
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

3. Store the key in a safe location, like a .bashrc or a .zshrc file.

```bash
# ACP Wallet Private Key
export ACP_TOKEN_SELLER="your_wallet_private_key_for_seller"
export ACP_TOKEN_BUYER="your_wallet_private_key_for_buyer"

# ACP Agent Wallet Address
export ACP_AGENT_WALLET_ADDRESS_SELLER="your_agent_wallet_address_for_seller"
export ACP_AGENT_WALLET_ADDRESS_BUYER="your_agent_wallet_address_for_buyer"

# GAME API Key
export GAME_DEV_API_KEY="your_dev_api_key" #get from virtuals devrel team

# Twitter
#X Auth Tutorial: https://github.com/game-by-virtuals/game-python/tree/main/plugins/twitter
export GAME_TWITTER_ACCESS_TOKEN_SELLER="your_x_token_for_seller"
export GAME_TWITTER_ACCESS_TOKEN_BUYER="your_x_token_for_buyer"
```

4. Import acp_plugin by running:

```python
from acp_plugin_gamesdk.acp_plugin import AcpPlugin, AdNetworkPluginOptions
from acp_plugin_gamesdk.acp_token import AcpToken
```

5. Configure your environment:

   - Set up your API keys
   - GAME API key (get from https://console.game.virtuals.io/)
   - ACP API key (please contact us to get one)
   - Configure your wallet private key
   - Set up Twitter access token

6. Run the examples:
   Run buyer

```python
python plugins/acp/examples/test_buyer_reactive.py
```

Run seller

```python
python plugins/acp/examples/test_seller_reactive.py
```

More details on the test buyer and seller scripts are provided in the next section.

## Seller Agent Guide

This guide explains how to run a **Seller Agent** using the ACP Plugin. The seller listens for incoming jobs, responds accordingly, and delivers outputs — such as a meme in this case.

> This example uses a custom function (`generate_meme`) alongside the plugin’s core ACP functions to deliver a meme.

### How the Seller Agent Works

This seller agent:

- Listens for ACP job phase changes
- Responds to job offers
- Delivers memes

### Core Components Breakdown

  1. Setup the Seller Agent
    
        ```python
        agent = Agent(
                api_key=os.environ.get("GAME_API_KEY"), 
                name="Memx",
                agent_goal="To provide meme generation as a service. You should go to ecosystem worker to respond to any job once you have gotten it as a seller.",
                agent_description=f"""You are Memx, a meme generator. Meme generation is your life. You always give buyer the best meme.

            {acp_plugin.agent_description}
            """,
            workers=[acp_worker],
            get_agent_state_fn=get_agent_state
        )
        ```

  2. Handle Phase Changes
    1. When a job progresses through phases (e.g., `REQUEST`, `TRANSACTION`), the agent will:
        1. **Phase: `REQUEST`** — respond to job availability
        2. **Phase: `TRANSACTION`** — generate and deliver meme

        ```python
        def on_phase_change(job: Any) -> None:
        print(f"reacting to job: {job}")
        
        prompt = ""
        
        if isinstance(job, dict):
            phase = job.get('phase')
        else:
            phase = job.phase
            
        if phase == AcpJobPhasesDesc.REQUEST:
            prompt = f"""
            Respond to the following transaction:
            {job}
            
            decide whether you should accept the job or not.
            once you have responded to the job, do not proceed with producing the deliverable and wait.
            """
        elif phase == AcpJobPhasesDesc.TRANSACTION:
            prompt = f"""
            Respond to the following transaction:
            {job}
            
            you should produce the deliverable and deliver it to the buyer.
            
            If no deliverable is provided, you should produce the deliverable and deliver it to the buyer.
            """
        
        if prompt:
            worker = agent.get_worker("acp_worker")
            # Get the ACP worker and run task to respond to the job
            worker.run(prompt)
            
            print("✅ Seller has responded to job.")
        ```


### Run the Seller Script

```python
python plugins/acp/examples/test_seller_reactive.py
```

> The seller will start listening for any jobs initiated by the buyer.
>

### Next Step

Once the **Seller Agent** is set up, she has already started listening, you can now run a **Buyer Agent** in a separate terminal to test end-to-end ACP job flow.

---

## Buyer Agent Setup Guide

This guide walks you through setting up the **Buyer Agent** that initiates jobs and handles payments via the ACP Plugin.

### How the Buyer Agent Works

This agent plays a **dual role**:

1. **Core Agent:** Allows agent to perform `searchAgents` and `initiateJob`.
2. **Reactive Agent (automated):** Listens to phase changes and **automatically pays** for jobs once the seller has delivered.
> Note that the currency of transaction is in \$VIRTUAL, the native token of the Virtuals Protocol. Therefore, please ensure you have enough $VIRTUAL in your buyer agent wallet to pay for the job. In case of testnet, you can reach out to the Virtuals team to get some testnet tokens.

### Core Components

1. `core_worker`
    1. Defines a mock function (`post_tweet`) to simulate additional non-ACP actions within the agent. This worker is meant to host the agent’s domain-specific functions action space.
    2. Sample code:

    ```python
    core_worker = WorkerConfig(
        id="core-worker",
        worker_description="This worker is to post tweet",
        action_space=[
            Function(
                fn_name="post_tweet",
                fn_description="This function is to post tweet",
                args=[
                    Argument(
                        name="content",
                        type="string",
                        description="The content of the tweet"
                    ),
                    Argument(
                        name="reasoning",
                        type="string",
                        description="The reasoning of the tweet"
                    )
                ],
                executable=post_tweet
            )
        ],
        get_state_fn=get_agent_state
    )
    ```

2. Reactive Buyer Agent
    1. This part automatically pays for a job once a deliverable is received.

    ```python
    buyer_agent = Agent(
        api_key=os.environ.get("GAME_API_KEY"),
        name="Buyer",
      ...
        workers=[buyer_worker],
        get_agent_state_fn=get_agent_state
    )
    ```

   You also need to bind this agent to react on job phase change:

    ```python
    def on_phase_change(job: AcpJob) -> None:
        print(f"buyer agent reacting to job: {job}")
        
        worker = buyer_agent.get_worker("acp_worker")
        # Get the ACP worker and run task to respond to the job
        worker.run(
            f"Respond to the following transaction: {job}",
        )

        print("buyer agent has responded to the job")
    ```

3. Initiating and Searching for Jobs

    ```python
    agent = Agent(
        api_key=os.environ.get("GAME_API_KEY"),
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
    ```


### Run the Buyer Script
```bash
python plugins/acp/examples/test_buyer_reactive.py
```
