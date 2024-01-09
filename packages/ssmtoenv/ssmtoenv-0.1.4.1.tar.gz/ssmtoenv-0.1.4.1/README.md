# ssmtoenv - SSM Parameter to .env File Utility

`ssmtoenv` is a command-line utility that allows you to fetch AWS Systems Manager (SSM) parameters and add them to a `.env` file. This tool is designed to simplify the process of retrieving and managing sensitive configuration parameters from AWS SSM Parameter Store and making them available for your applications in a local environment.

## Usage

```bash
ssmtoenv --aws-access-key <AWS_ACCESS_KEY> --aws-secret-key <AWS_SECRET_KEY> [--session-token <SESSION_TOKEN>] [--prefix <PREFIX>] [--install-completion <SHELL>] [--show-completion <SHELL>] [--help]
```

### Options

- `--aws-access-key TEXT`: AWS Access Key (required).
- `--aws-secret-key TEXT`: AWS Secret Key (required).
- `--session-token TEXT`: AWS Session Token (optional, defaults to "None").
- `--prefix TEXT`: SSM Parameter Store prefix (optional, defaults to "/cloudflaretunnel/").
- `--install-completion [bash|zsh|fish|powershell|pwsh]`: Install completion for the specified shell.
- `--show-completion [bash|zsh|fish|powershell|pwsh]`: Show completion for the specified shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

## How It Works

`ssmtoenv` interacts with AWS Systems Manager Parameter Store to retrieve configuration parameters based on the provided options. It then generates or updates a `.env` file with the retrieved parameters, making them available for your application to consume.

## Installation

You can install `ssmtoenv` using `pip`, the Python package manager:

```bash
pip install ssmtoenv
```

## Example

Suppose you have AWS SSM parameters with the prefix `/myapp/` containing database credentials, and you want to add them to a `.env` file for your application to use. You can use the following command:

```bash
ssmtoenv --aws-access-key <YOUR_AWS_ACCESS_KEY> --aws-secret-key <YOUR_AWS_SECRET_KEY> --prefix /myapp/
```

This command will fetch all parameters under the `/myapp/` prefix and update your `.env` file with the retrieved values.

## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/rahulmistri1997/ssmtoenv).


---

Note: This README provides a brief overview of the `ssmtoenv` utility. For more detailed information, options, and usage examples, please refer to the command-line help (`ssmtoenv --help`) or the source code documentation.
