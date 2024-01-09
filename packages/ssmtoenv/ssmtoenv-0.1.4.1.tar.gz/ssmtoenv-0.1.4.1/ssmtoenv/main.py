"""
Fetch SSM parameters and add them to a .env file.
"""

import typer
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import set_key, find_dotenv
from typing import Optional, Literal

app = typer.Typer()


def fetch_ssm_parameters(prefix, aws_access_key, aws_secret_key, session_token) -> list:
    """
    Fetch SSM parameters from AWS Parameter Store.

    Args:
        prefix (str): SSM Parameter Store prefix.

        aws_access_key (str): AWS Access Key.

        aws_secret_key (str): AWS Secret Key.

        session_token (str): AWS Session Token.

    Returns:

        ssm_secrets (list): List of SSM parameter dictionaries.
    """
    if session_token == "None":
        session_token = None

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=session_token,
    )
    ssm_client = session.client("ssm")

    try:
        parameters = []
        next_token: Literal[""] = ""
        while True:
            response = ssm_client.get_parameters_by_path(
                Path=prefix, Recursive=True, WithDecryption=True, NextToken=next_token
            )
            parameters.extend(response.get("Parameters", []))
            next_token = response.get("NextToken")
            if not next_token:
                break
        return parameters
    except NoCredentialsError:
        typer.echo(
            "AWS credentials not found. Make sure you have configured your credentials."
        )
        raise typer.Exit(code=1)


class TyperOptionFetch:
    @staticmethod
    def aws_access_key() -> typer.Option:
        """
        The function `aws_access_key()` returns the AWS Access Key.
        :return: The function `aws_access_key()` is returning a `typer.Option` object.
        """
        return typer.Option(
            ...,
            prompt=True,
            hide_input=True,
            confirmation_prompt=False,
            help="AWS Access Key",
        )

    @staticmethod
    def aws_secret_key() -> typer.Option:
        """
        The function `aws_secret_key()` prompts the user to enter their AWS Secret Key and hides the
        input for security purposes.
        """
        return typer.Option(
            ...,
            prompt=True,
            hide_input=True,
            confirmation_prompt=False,
            help="AWS Secret Key",
        )

    @staticmethod
    def session_token() -> typer.Option:
        """
        The function `session_token()` returns an AWS Session Token, with a default value of "None" if
        not provided.
        :return: a `typer.Option` object.
        """
        return typer.Option(
            "None",
            prompt=True,
            hide_input=True,
            confirmation_prompt=False,
            help="AWS Session Token, if not provided will default to None",
        )

    @staticmethod
    def prefix() -> typer.Option:
        """
        The `prefix` function returns a `typer.Option` object with default values and prompts for user
        input.
        :return: a `typer.Option` object.
        """
        return typer.Option(
            "/cloudflaretunnel/",
            prompt=True,
            confirmation_prompt=False,
            help="SSM Parameter Store prefix",
        )


@app.command()
def fetch_and_add_to_env(
    aws_access_key: str = TyperOptionFetch.aws_access_key(),
    aws_secret_key: str = TyperOptionFetch.aws_secret_key(),
    session_token: Optional[str] = TyperOptionFetch.session_token(),
    prefix: str = TyperOptionFetch.prefix(),
) -> None:
    """
    Fetch SSM parameters and add them to a .env file.

    Args:
        aws_access_key (str): AWS Access Key.
        aws_secret_key (str): AWS Secret Key.
        session_token (str, optional): AWS Session Token. Defaults to "None".
        prefix (str): SSM Parameter Store prefix.
    """
    typer.echo(f"Fetching SSM parameters with prefix: {prefix}")

    parameters = fetch_ssm_parameters(
        prefix, aws_access_key, aws_secret_key, session_token
    )

    if len(parameters) == 0:
        typer.echo("No parameters found with the given prefix")
        raise typer.Exit(code=1)

    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path == "":
        dotenv_path = ".env"
        with open(dotenv_path, "w") as f:
            f.write("")

    dotenv_path = find_dotenv(usecwd=True)

    for parameter in parameters:
        parameter_name = parameter["Name"].split("/")[-1]
        parameter_value = parameter["Value"]
        set_key(dotenv_path, parameter_name, parameter_value)
        typer.echo(f"Added parameter: {parameter_name}")


if __name__ == "__main__":
    app()
