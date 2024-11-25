import json
import os
from typing import List

import click
import requests
from openai import OpenAI  
from loguru import logger


def check_required_env_vars():
    """Check required environment variables"""
    required_env_vars = [
        "API_KEY",
        "GITLAB_TOKEN",
        "CI_PROJECT_ID",
        "CI_MERGE_REQUEST_IID",
        "DIFF_CONTENT",
    ]
    for var in required_env_vars:
        if os.getenv(var) is None:
            raise ValueError(f"{var} is not set")


def create_a_comment_to_merge_request(
        gitlab_token: str,
        gitlab_project_id: str,
        merge_request_iid: int,
        body: str,
        gitlab_api_url: str = 'https://gitlab.com'):
    """Create a comment to a merge request in GitLab"""
    headers = {
        "PRIVATE-TOKEN": gitlab_token
    }
    data = {
        "body": body
    }
    url = f"{gitlab_api_url}/api/v4/projects/{gitlab_project_id}/merge_requests/{merge_request_iid}/notes"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 201:
        logger.error(f"Failed to create comment: {response.text}")
    else:
        logger.info("Successfully posted the code review comment.")
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

    response = client.chat.completions.create(  
        model=model,
        messages=[
            {"role": "system", "content": "As a senior code reviewer, provide constructive feedback. Analyze the following code changes and provide constructive feedback to the developer. Your output will be used to put inline feedback in gitlab merge request discussions. Please provide a concise summary of the bug found in the code, describing its characteristics, location, and potential effects on the overall functionality and performance of the application. Present the potential issues and errors first, followed by the most important findings, in your summary. Include a block of code / diff in the summary and the line numbers where applicable."},  # noqa
            {"role": "user", "content": prompt}
        ],
    )
    review_result = response.choices[0].message.content
    
    return review_result


@click.command()
@click.option("--diff-chunk-size", type=click.INT, required=False, default=3500, help="Pull request diff")
@click.option("--model", type=click.STRING, required=False, default="gpt-4o-mini", help="OpenAI model")
@click.option("--log-level", type=click.STRING, required=False, default="INFO", help="Log level")
def main(
        diff_file: str,
        diff_chunk_size: int,
        model: str,
        log_level: str
):
    # Set log level
    logger.remove()
    logger.add(lambda msg: print(msg, flush=True), level=log_level.upper())
    # Check if necessary environment variables are set or not
    check_required_env_vars()

    # Read the diff content
    with open(diff_file, "r") as file:
        diff = file.read()

    # Request a code review
    code_review = get_review(
        diff=diff,
        model=model,
        prompt_chunk_size=diff_chunk_size
    )

    # Create a comment to a merge request
    create_a_comment_to_merge_request(
        gitlab_token=os.getenv("GITLAB_TOKEN"),
        gitlab_project_id=os.getenv("CI_PROJECT_ID"),
        merge_request_iid=int(os.getenv("CI_MERGE_REQUEST_IID")),
        body=code_review
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
