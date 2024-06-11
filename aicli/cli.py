import click
import logging
import json
import os
import subprocess
from aicli.nlp_module import interpret_command, get_gpt_solution, explain_output
from aicli.roles import has_permission

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Set higher logging level for httpx and openai to suppress INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# Get the username from environment variable, default to 'user' if not set
USERNAME = os.getenv('AICLI_USERNAME', 'user')

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load custom commands from JSON file
custom_commands_path = os.path.join(script_dir, 'custom_commands.json')
with open(custom_commands_path, 'r') as f:
    custom_commands = json.load(f).get('custom_commands', {})

@click.group()
def cli():
    """AI-driven Kubernetes CLI assistant."""
    pass

def run_kubectl_command(kubectl_command):
    try:
        result = subprocess.run(kubectl_command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        logging.error(f"Command failed with error: {error_message}")
        return f"Command failed with error: {error_message}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

@click.command(name='list-contexts', help="List available Kubernetes contexts.")
def list_contexts():
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    output = run_kubectl_command("kubectl config get-contexts -o name")
    click.echo(output)

@click.command(name='set-context', help="Set the current Kubernetes context.")
@click.argument('context')
def set_context(context):
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    output = run_kubectl_command(f"kubectl config use-context {context}")
    click.echo(output)

@click.command(name='list-namespaces', help="List available namespaces in the current context.")
def list_namespaces():
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    output = run_kubectl_command("kubectl get namespaces -o json")
    try:
        namespaces = [ns['metadata']['name'] for ns in json.loads(output)['items']]
        click.echo("Available namespaces:")
        for ns in namespaces:
            click.echo(f"- {ns}")
    except json.JSONDecodeError as e:
        click.echo(f"Failed to parse JSON output: {str(e)}")
        logging.error(f"Failed to parse JSON output: {str(e)}")

@click.command(help="Execute a Kubernetes command using natural language input.")
@click.argument('command', nargs=-1)
def execute(command):
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    user_input = " ".join(command)
    kubectl_command = interpret_command(user_input)
     #logging.info(f"User input: {user_input}")
    #logging.info(f"Interpreted command: {kubectl_command}")
    click.echo(f"Executing: {kubectl_command}")

    output = run_kubectl_command(kubectl_command)
    click.echo(output)
    if "error" in output.lower():
        solution = get_gpt_solution(kubectl_command, output)
        click.echo(f"Suggested solution: {solution}")

@click.command(name='custom', help="Execute a custom Kubernetes command.")
@click.argument('custom_command')
@click.option('--pod_name', default='', help='Name of the pod')
@click.option('--namespace', default='default', help='Namespace of the resource')
def custom(custom_command, pod_name, namespace):
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    command_template = custom_commands.get(custom_command)
    if not command_template:
        click.echo(f"No custom command found with the name: {custom_command}")
        return

    kubectl_command = command_template.format(pod_name=pod_name, namespace=namespace)
    logging.info(f"Executing custom command: {kubectl_command}")

    output = run_kubectl_command(kubectl_command)
    click.echo(output)
    if "error" in output.lower():
        solution = get_gpt_solution(kubectl_command, output)
        click.echo(f"Suggested solution: {solution}")

@click.command(help="Explain the output of a Kubernetes command.")
@click.argument('output')
def explain(output):
    if not has_permission(USERNAME, 'explain'):
        click.echo("You do not have permission to explain this command output.")
        return

    explanation = explain_output(output)
    click.echo(explanation)

@click.command(name='monitor-pods', help="Monitor CPU and memory usage of all pods in a namespace.")
@click.option('--namespace', default='default', help='Namespace to monitor')
def monitor_pods(namespace):
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    output = run_kubectl_command(f"kubectl top pods -n {namespace}")
    click.echo(output)

@click.command(name='monitor-nodes', help="Monitor CPU and memory usage of all nodes.")
def monitor_nodes():
    if not has_permission(USERNAME, 'execute'):
        click.echo("You do not have permission to execute this command.")
        return

    output = run_kubectl_command("kubectl top nodes")
    click.echo(output)

@click.command(name='list-roles', help="List roles for the current user.")
def list_roles():
    if not has_permission(USERNAME, 'view_roles'):
        click.echo("You do not have permission to view roles.")
        return

    output = run_kubectl_command("kubectl get clusterrolebindings -o json")
    try:
        roles = json.loads(output)
        for role in roles['items']:
            click.echo(f"Role: {role['metadata']['name']}")
            for subject in role['subjects']:
                if subject['kind'] == 'User' and subject['name'] == USERNAME:
                    click.echo(f"  User: {subject['name']} (matched)")
    except json.JSONDecodeError as e:
        click.echo(f"Failed to parse JSON output: {str(e)}")
        logging.error(f"Failed to parse JSON output: {str(e)}")

# Register all commands
cli.add_command(list_contexts)
cli.add_command(set_context)
cli.add_command(list_namespaces)
cli.add_command(execute)
cli.add_command(custom)
cli.add_command(explain)
cli.add_command(monitor_pods)
cli.add_command(monitor_nodes)
cli.add_command(list_roles)

if __name__ == "__main__":
    cli()

