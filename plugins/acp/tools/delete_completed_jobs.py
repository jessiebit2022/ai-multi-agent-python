import os
import time
from typing import Dict, Any
from pprint import pprint
from acp_plugin_gamesdk.acp_plugin import AcpToken, AcpPlugin, AcpPluginOptions
from acp_plugin_gamesdk.configs import BASE_SEPOLIA_CONFIG, BASE_MAINNET_CONFIG
from dotenv import load_dotenv

load_dotenv()

def print_completed_jobs(state: Dict[str, Any]) -> bool:
    """Print all completed jobs with job ID and summary."""
    completed_jobs = state.get('jobs', {}).get('completed', [])
    if not completed_jobs:
        print("No completed jobs found.")
        return False
    print(f"\n📋 Available Completed Jobs ({len(completed_jobs)} total):")
    pprint(completed_jobs)
    print()
    return True

def delete_completed_job(acp_plugin: AcpPlugin, state: Dict[str, Any]) -> None:
    """Delete completed job for all configured ACP tokens."""
    try:
        has_completed_jobs = print_completed_jobs(state)
        if has_completed_jobs:
            # Prompt user to input the job ID they want to delete
            job_id = input("Enter the job ID you want to delete: ")
            if not job_id.isdigit() or int(job_id) < 0:
                print("❌ Invalid number. Please enter a positive integer.")
                return

            acp_plugin.delete_completed_job(int(job_id))
            print(f"Successfully deleted completed job for agent: {agent_wallet_address}\n")
    except Exception as e:
        print(f"Failed to delete completed job: {e}")

def delete_all_jobs(acp_plugin: AcpPlugin, state: Dict[str, Any]):
    """Delete all completed jobs after user confirmation."""
    has_completed_jobs = print_completed_jobs(state)
    if has_completed_jobs:
        confirm = input("Are you sure you want to delete ALL completed jobs? (y/n): ").strip().lower()
        if confirm == 'y':
            for job in state.get('jobs', {}).get('completed', []):
                acp_plugin.delete_completed_job(job.get('jobId'))
            print("✅ All completed jobs have been deleted.")
        else:
            print("❌ Operation cancelled.")

def prune_old_jobs(acp_plugin: AcpPlugin, state: Dict[str, Any]) -> None:
    """
    Deletes completed ACP jobs for the configured token,
    keeping only the n most recently updated ones.
    """
    try:
        has_completed_jobs = print_completed_jobs(state)
        if has_completed_jobs:
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
    api_key = os.environ.get("GAME_DEV_API_KEY")
    whitelisted_wallet_private_key = os.environ.get("WHITELISTED_WALLET_PRIVATE_KEY")
    agent_wallet_address = os.environ.get("BUYER_AGENT_WALLET_ADDRESS")

    acp_plugin = AcpPlugin(
        options=AcpPluginOptions(
            api_key=api_key,
            acp_token_client=AcpToken(
                whitelisted_wallet_private_key,
                agent_wallet_address,
                BASE_MAINNET_CONFIG # Use BASE_SEPOLIA_CONFIG for testing; switch to BASE_MAINNET_CONFIG for production
            )
        )
    )

    while True:
        state = acp_plugin.get_acp_state()
        print()
        pprint(state)

        print("\nChoose an operation:")
        print("1. Reset State")
        print("2. Delete a specific job")
        print("3. Delete ALL completed jobs")
        print("4. Keep N newest jobs and delete the rest")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            print("Resetting state...")
            acp_plugin.reset_state()
        elif choice == "2":
            delete_completed_job(acp_plugin, state)
        elif choice == "3":
            delete_all_jobs(acp_plugin, state)
        elif choice == "4":
            prune_old_jobs(acp_plugin, state)
        elif choice == "5":
            print("Exiting...")
            exit()
        else:
            print("❌ Invalid choice.")

        time.sleep(1)
