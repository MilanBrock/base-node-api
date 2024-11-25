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
        temperature: float,
        max_tokens: int,
        model: str,
        prompt_chunk_size: int
):
    """Get a review"""
    openai_api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=openai_api_key)  # Modified line

    # Chunk the prompt
    chunked_diff_list = chunk_string(input_string=diff, chunk_size=prompt_chunk_size)
    chunked_reviews = []

    for chunked_diff in chunked_diff_list:
        prompt = f"""Provide a concise summary of the bug found in the code, describing its characteristics, 
location, and potential effects on the overall functionality and performance of the application.
Present the potential issues and errors first, followed by the most important findings, in your summary.
Include a block of code / diff in the summary and the line numbers where applicable.

Diff:

{chunked_diff}
"""

        response = client.chat.completions.create(  # Modified line
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        review_result = response["choices"][0]["message"]["content"]
        chunked_reviews.append(review_result)

    # If the chunked reviews are only one, return it
    if len(chunked_reviews) == 1:
        return chunked_reviews, chunked_reviews[0]

    # Summarize the chunked reviews
    changes_text = "\n".join(chunked_reviews)
    summary_prompt = f"""Summarize the following file changes in a pull request, focusing on major modifications, 
additions, deletions, and any significant updates within the files. Include a block of code / diff 
and line numbers.

Changes:
{changes_text}
"""
    summary_response = client.chat.completions.create(  # Modified line
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": summary_prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    summarized_review = summary_response["choices"][0]["message"]["content"]
    return chunked_reviews, summarized_review


def format_review_comment(summarized_review: str, chunked_reviews: List[str]) -> str:
    """Format reviews"""
    if len(chunked_reviews) == 1:
        return summarized_review
    unioned_reviews = "\n".join(chunked_reviews)
    review = f"""<details>
<summary>{summarized_review}</summary>
{unioned_reviews}
</details>
"""
    return review


@click.command()
@click.option("--diff", type=click.STRING, required=True, help="Pull request diff")
@click.option("--diff-chunk-size", type=click.INT, required=False, default=3500, help="Pull request diff")
@click.option("--model", type=click.STRING, required=False, default="gpt-3.5-turbo", help="OpenAI model")
@click.option("--temperature", type=click.FLOAT, required=False, default=0.1, help="Temperature")
@click.option("--max-tokens", type=click.INT, required=False, default=250, help="Max tokens")
@click.option("--log-level", type=click.STRING, required=False, default="INFO", help="Log level")
def main(
        diff: str,
        diff_chunk_size: int,
        model: str,
        temperature: float,
        max_tokens: int,
        log_level: str
):
    # Set log level
    logger.level(log_level)
    # Check if necessary environment variables are set or not
    check_required_env_vars()

    # Request a code review
    chunked_reviews, summarized_review = get_review(
        diff=diff,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
        prompt_chunk_size=diff_chunk_size
    )
    logger.debug(f"Summarized review: {summarized_review}")
    logger.debug(f"Chunked reviews: {chunked_reviews}")

    # Format reviews
    review_comment = format_review_comment(summarized_review=summarized_review,
                                           chunked_reviews=chunked_reviews)
    # Create a comment to a pull request
    create_a_comment_to_pull_request(
        github_token=os.getenv("GITHUB_TOKEN"),
        github_repository=os.getenv("GITHUB_REPOSITORY"),
        pull_request_number=int(os.getenv("GITHUB_PULL_REQUEST_NUMBER")),
        git_commit_hash=os.getenv("GIT_COMMIT_HASH"),
        body=review_comment
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
