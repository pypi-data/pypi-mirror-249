import argparse
import sys


def cli():
    parser = argparse.ArgumentParser(description="Swarms CLI")
    parser.add_argument(
        "file_name", help="Python file containing Swarms code to run"
    )
    # Help message for the -h flag is automatically generated by argparse
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 0.1.0"
    )

    # Check deployments for a given model
    parser.add_argument(
        "-c", "--check", help="Check deployments for a given agent"
    )

    # Generate an API key for a given agent
    parser.add_argument(
        "-g",
        "--generate",
        help="Generate an API key for a given agent",
    )

    # Signin to swarms with a given API key
    parser.add_argument(
        "-s", "--signin", help="Signin to swarms with a given API key"
    )

    # Signout of swarms
    parser.add_argument("-o", "--signout", help="Signout of swarms")

    # List all agents
    parser.add_argument("-l", "--list", help="List all agents")

    # List all deployments
    parser.add_argument(
        "-d", "--deployments", help="List all deployments"
    )

    # Pricing information
    parser.add_argument("-p", "--pricing", help="Pricing information")

    # Run a deployment
    parser.add_argument("-r", "--run", help="Run a deployment")

    # Stop a deployment
    parser.add_argument("-t", "--stop", help="Stop a deployment")

    # Delete a deployment
    parser.add_argument("-x", "--delete", help="Delete a deployment")

    # Get a deployment
    parser.add_argument("-e", "--get", help="Get a deployment")

    # Get a deployment's logs
    parser.add_argument(
        "-z", "--logs", help="Get a deployment's logs"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Execute the specified file
    try:
        with open(args.file_name, "r") as file:
            exec(file.read(), globals())
    except FileNotFoundError:
        print(f"Error: File '{args.file_name}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing file '{args.file_name}': {e}")
        sys.exit(1)
