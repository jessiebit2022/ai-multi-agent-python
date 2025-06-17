# Twitter Plugin for GAME SDK

The **Twitter Plugin** provides a lightweight interface for integrating Twitter (X) functionality into your GAME SDK agents. Built on top of [`virtuals_tweepy`](https://pypi.org/project/virtuals-tweepy/) by the Virtuals team — a maintained fork of [`Tweepy`](https://pypi.org/project/tweepy/)) — this plugin lets you easily post tweets, fetch data, and execute workflows through agent logic.

## 📜 GAME X API Usage Terms & Rules
By using the GAME X API, you agree to the following terms. Violation of any rule may result in immediate revocation of access. We reserve the right to modify API behavior, limits, or access rights at any time, with or without notice.

### ✅ Allowed Usage (Green Flags)
#### General
- Keep under 50 posts/day
- Follow/unfollow: <100/day
- Use organic, varied language—avoid robotic or repetitive posts
- Use a mix of images, videos, and text-based content
- Include polls, threads, quotes, retweets to encourage engagement
- Mark account as sensitive if needed
- Always include the automated label for agent-generated content

#### Replies, Mentions, and DMs
- Max 10 replies/hour to different users
- Max 10 DMs/day to new users
- Agent may only reply or DM when:
- User mentions, replies, retweets, or DMs the agent
- Only 1 automated reply/DM per interaction
- Always validate post existence before replying (statuses/lookup)
- Filter for sensitive usernames/media/content

#### ✉️ DM Rules
- DMs must be triggered by valid user interaction

Only use:
- GET /dm_conversations
- GET /dm_events
- POST /dm_events/new
- No crawling, scraping, or off-platform storage of DM data
- No DMs used to bypass rate limits or coordinate bot activity
- One DM per user trigger, no spamming

### 🚫 Prohibited Activity (Red Flags)
- ❌ Liking tweets, adding users to lists/collections
- ❌ Engagement farming (e.g., repetitive “Like if…” prompts)
- ❌ Auto-posting about trending topics
- ❌ Duplicate phrases across posts/accounts
- ❌ Tweet bursts (post every 10–15 mins, minimum)
- ❌ Over-replying or over-DMing
- ❌ Misleading or redirect-heavy links
- ❌ Harassment, abuse, hate speech, or doxxing
- ❌ Cloning multiple automated accounts for similar purposes

## 🚀 API Access Tiers
### Tier 1 — Default
- Basic access
- Standard rate limits

### Tier 2 — Elevated
- Higher rate limits
- Request access via Discord → @virtualsio
- Requires verification

---
Use it standalone or compose multiple Twitter actions as part of a larger agent job.

## Installation

You can install the plugin using either `poetry` or `pip`:

```bash
# Using Poetry (from the plugin directory)
poetry install
```
or
```bash
# Using pip (recommended for integration projects)
pip install twitter_plugin_gamesdk
```

---

## Authentication Methods
Virtuals sponsors the community with a **Twitter Enterprise API access plan**, using OAuth 2.0 with PKCE. This provides:

- Higher rate limits: **35 calls / 5 minutes**
- Smoother onboarding
- Free usage via your `GAME_API_KEY`

#### 1. Get Your Access Token

Run the following command to authenticate using your `GAME_API_KEY`:

```bash
poetry run twitter-plugin-gamesdk auth -k <GAME_API_KEY>
```

This will prompt:

```bash
Waiting for authentication...

Visit the following URL to authenticate:
https://x.com/i/oauth2/authorize?...

Authenticated! Here's your access token:
apx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 2. Store Your Access Token

We recommend storing environment variables in a `.env` file:

```
# .env

GAME_TWITTER_ACCESS_TOKEN=apx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Then, use `load_dotenv()` to load them:

```python
import os
from dotenv import load_dotenv
from twitter_plugin_gamesdk.twitter_plugin import TwitterPlugin

load_dotenv()

options = {
    "credentials": {
        "game_twitter_access_token": os.environ.get("GAME_TWITTER_ACCESS_TOKEN")
    }
}

twitter_plugin = TwitterPlugin(options)
client = twitter_plugin.twitter_client

client.create_tweet(text="Tweeting with GAME Access Token!")
```
---

## Examples

Explore the [`examples/`](./examples) directory for sample scripts demonstrating how to:

- Post tweets
- Reply to mentions
- Quote tweets
- Fetch user timelines
- And more!

---

## API Reference

This plugin wraps [`virtuals_tweepy`](https://pypi.org/project/virtuals-tweepy/), which is API-compatible with [Tweepy’s client interface](https://docs.tweepy.org/en/stable/client.html). Refer to their docs for supported methods and parameters.

---
