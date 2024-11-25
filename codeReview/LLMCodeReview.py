import json
import os
from typing import List

import click
import requests
from openai import OpenAI  # Modified import
from loguru import logger


def check_required_env_vars():
    """Check required environment variables"""
    required_env_vars = [
        "API_KEY",
        "GITHUB_TOKEN",
        "GITHUB_REPOSITORY",
        "GITHUB_PULL_REQUEST_NUMBER",
        "GIT_COMMIT_HASH",
    ]
    for required_env_var in required_env_vars:
        if os.getenv(required_env_var) is None:
            raise ValueError(f"{required_env_var} is not set")


def create_a_comment_to_pull_request(
        github_token: str,
        github_repository: str,
        pull_request_number: int,
        git_commit_hash: str,
        body: str):
    """Create a comment to a pull request"""
    headers = {
        "Accept": "application/vnd.github.v3.patch",
        "authorization": f"Bearer {github_token}"
    }
    data = {
        "body": body,
        "commit_id": git_commit_hash,
        "event": "COMMENT"
    }
    url = f"https://api.github.com/repos/{github_repository}/pulls/{pull_request_number}/reviews"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def chunk_string(input_string: str, chunk_size) -> List[str]:
    """Chunk a string"""
    chunked_inputs = []
    for i in range(0, len(input_string), chunk_size):
        chunked_inputs.append(input_string[i:i + chunk_size])
    return chunked_inputs


def get_review(
        diff: str,
        model: str,
        prompt_chunk_size: int
):
    """Get a review"""
    openai_api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=openai_api_key)  # Modified line

    # Chunk the prompt
    chunked_diff_list = chunk_string(input_string=diff, chunk_size=prompt_chunk_size)

    for chunked_diff in chunked_diff_list:
        prompt = f"""The following code changes were found in the pull request. Your output will be used to put inline feedback in gitlab merge request discussions.
        Diff:

        {chunked_diff}
        """

    response = client.chat.completions.create(  # Modified line
        model=model,
        messages=[
            {"role": "system", "content": "As a senior code reviewer, provide constructive feedback. Analyze the following code changes and provide constructive feedback to the developer. Your output will be used to put inline feedback in gitlab merge request discussions. Please provide a concise summary of the bug found in the code, describing its characteristics, location, and potential effects on the overall functionality and performance of the application. Present the potential issues and errors first, followed by the most important findings, in your summary. Include a block of code / diff in the summary and the line numbers where applicable."},  # noqa
            {"role": "user", "content": prompt}
        ],
    )
    review_result = response.choices[0].message.content
    
    return review_result


@click.command()
@click.option("--diff", type=click.STRING, required=True, help="Pull request diff")
@click.option("--diff-chunk-size", type=click.INT, required=False, default=3500, help="Pull request diff")
@click.option("--model", type=click.STRING, required=False, default="gpt-3.5-turbo", help="OpenAI model")
@click.option("--log-level", type=click.STRING, required=False, default="INFO", help="Log level")
def main(
        diff: str,
        diff_chunk_size: int,
        model: str,
        log_level: str
):
    # Set log level
    logger.level(log_level)
    # Check if necessary environment variables are set or not
    check_required_env_vars()

    # Request a code review
    code_review = get_review(
        diff=diff,
        model=model,
        prompt_chunk_size=diff_chunk_size
    )
   
    # Create a comment to a pull request
    create_a_comment_to_pull_request(
        github_token=os.getenv("GITHUB_TOKEN"),
        github_repository=os.getenv("GITHUB_REPOSITORY"),
        pull_request_number=int(os.getenv("GITHUB_PULL_REQUEST_NUMBER")),
        git_commit_hash=os.getenv("GIT_COMMIT_HASH"),
        body=code_review
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
