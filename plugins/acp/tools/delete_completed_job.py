import os
from typing import Dict, Any
from pprint import pprint
from acp_plugin_gamesdk.acp_plugin import AcpToken, AcpPlugin, AcpPluginOptions

def print_completed_jobs(state: Dict[str, Any]) -> None:
    """Print all completed jobs with job ID and summary."""
    completed_jobs = state.get('jobs', {}).get('completed', [])
    if not completed_jobs:
        print("No completed jobs found.")
        return
    print(f"\n📋 Available Completed Jobs ({len(completed_jobs)} total):")
    pprint(completed_jobs)

def delete_completed_job(acp_plugin: AcpPlugin, state: Dict[str, Any]) -> None:
    """Delete completed job for all configured ACP tokens."""
    try:
        print_completed_jobs(state)
        # Prompt user to input the job ID they want to delete
        job_id = input("Enter the job ID you want to delete: ")
        acp_plugin.delete_completed_job(job_id)
        print(f"Successfully deleted completed job for token: {acp_token}")
        exit()
    except Exception as e:
        print(f"Failed to delete completed job: {e}")

def delete_all_jobs(acp_plugin: AcpPlugin, state: Dict[str, Any]):
    """Delete all completed jobs after user confirmation."""
    print_completed_jobs(state)
    confirm = input("Are you sure you want to delete ALL completed jobs? (y/n): ").strip().lower()
    if confirm == 'y':
        for job in state.get('jobs', {}).get('completed', []):
            acp_plugin.delete_completed_job(str(job.get('jobId')))
        print("✅ All completed jobs have been deleted.")
    else:
        print("❌ Operation cancelled.")

def prune_old_jobs(acp_plugin: AcpPlugin, state: Dict[str, Any]) -> None:
    """
    Deletes completed ACP jobs for the configured token,
    keeping only the n most recently updated ones.
    """
    try:
        print_completed_jobs(state)
        num_str = input("How many newest jobs do you want to keep? ").strip()
        if not num_str.isdigit() or int(num_str) < 0:
            print("❌ Invalid number. Please enter a positive integer.")
            return

        n_jobs_to_remain = int(num_str)
        completed_jobs = state.get('jobs', {}).get('completed', [])

        if not completed_jobs:
            print("No completed jobs found.")
            return

        if len(completed_jobs) <= n_jobs_to_remain:
            print(f"No pruning needed. Keeping all {len(completed_jobs)} jobs.")
            return

        # Sort jobs by 'lastUpdated' descending and keep only the most recent
        sorted_completed_jobs = sorted(
            completed_jobs, key=lambda job: job['lastUpdated'], reverse=True
        )
        jobs_to_prune = sorted_completed_jobs[n_jobs_to_remain:]

        for job in jobs_to_prune:
            job_id = job.get('jobId')
            acp_plugin.delete_completed_job(job_id)
            print(f"✅ Deleted job ID: {job_id}")

    except Exception as e:
        print(f"❌ Failed to prune jobs: {e}")

if __name__ == "__main__":
    print("Choose an operation:")
    print("1. Delete a specific job")
    print("2. Delete ALL completed jobs")
    print("3. Keep N newest jobs and delete the rest")

    choice = input("Enter your choice (1-3): ").strip()

    api_key = os.environ.get("GAME_DEV_API_KEY")
    acp_token = os.environ.get("ACP_TOKEN_BUYER")
    agent_wallet_address = os.environ.get("ACP_AGENT_WALLET_ADDRESS_BUYER")

    acp_plugin = AcpPlugin(
        options=AcpPluginOptions(
            api_key=api_key,
            acp_token_client=AcpToken(
                acp_token,
                agent_wallet_address,
                "https://base-sepolia-rpc.publicnode.com/"
            )
        )
    )
    state = acp_plugin.get_acp_state()
    pprint(state)

    if choice == "1":
        delete_completed_job(acp_plugin, state)
    elif choice == "2":
        delete_all_jobs(acp_plugin, state)
    elif choice == "3":
        prune_old_jobs(acp_plugin, state)
    else:
        print("❌ Invalid choice. Exiting.")
