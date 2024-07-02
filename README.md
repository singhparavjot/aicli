# aicli

Welcome to `aicli`, an AI-driven command-line interface that enhances your interactions with Kubernetes by leveraging advanced natural language processing. `aicli` simplifies Kubernetes operations, making it accessible to users without in-depth knowledge of kubectl commands. Whether you're managing pods, contexts, or namespaces, `aicli` provides intuitive command execution powered by OpenAI's GPT technology.



[Screencast from 2024-06-11 20-59-37.webm](https://github.com/singhparavjot/aicli/assets/41161923/4adbd322-5bef-40f2-9ccf-2054b618e059)




## Installation

`aicli` is easy to install and can be done with just a few commands. Follow these steps to get started:

```bash
pip install aicli
```

This command will fetch the latest version of `aicli` from PyPI and install it along with its dependencies.

## Setting Up Your Environment

To ensure `aicli` operates correctly, you must configure an environment variable for the OpenAI API key. This key enables `aicli` to communicate with OpenAI's services for processing natural language inputs.

### Configuring API Key on Linux or macOS:

Add the following line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

Then, apply the changes with:

```bash
source ~/.bashrc   # or the appropriate file for your shell
```

### Configuring API Key on Windows:

For persistent configuration, use the Command Prompt:

```cmd
setx OPENAI_API_KEY "your-openai-api-key"
```

For a temporary setup, valid for the session of your command prompt:

```cmd
set OPENAI_API_KEY=your-openai-api-key
```

### Verifying the Setup:

You can check if the environment variable is set by running:

```bash
echo $OPENAI_API_KEY   # On Linux or macOS
echo %OPENAI_API_KEY%  # On Windows
```

## Detailed Usage Guide

### Basic Commands

- **List Kubernetes Contexts**:
  Understand your current Kubernetes setup and available contexts.

  ```bash
  aicli list-contexts
  ```

- **Switch Kubernetes Contexts**:
  Change your active Kubernetes context to manage different clusters.

  ```bash
  aicli set-context my-context
  ```

- **List Namespaces**:
  Display all namespaces available in the current context to manage scoped resources.

  ```bash
  aicli list-namespaces
  ```

### Advanced Interaction

- **Natural Language Execution**:
  Use plain English to perform Kubernetes operations without remembering specific syntax.

  ```bash
  aicli execute "show me all pods in the default namespace"
  ```

- **Custom Commands**:
  Define and use bespoke commands tailored to your operational needs.

  ```bash
  aicli custom list_all_pods --pod_name mypod --namespace default
  ```

### Resource Monitoring

- **Monitor Pod Resources**:
  Check real-time CPU and memory usage of pods to manage resource allocation effectively.

  ```bash
  aicli monitor-pods --namespace default
  ```

- **Monitor Node Resources**:
  Gain insights into the overall resource usage of nodes in your cluster.

  ```bash
  aicli monitor-nodes
  ```

### Role Management

- **Check User Roles**:
  Display Kubernetes roles associated with your user to understand your permissions and scope of access.

  ```bash
  aicli list-roles
  ```

## Contributing

Contributions to `aicli` are welcome! Here's how you can contribute:

1. **Fork the Repository**: Create a copy of this project to your GitHub account.
2. **Create a Feature Branch**: Make a new branch in your forked repository.
3. **Make Changes**: Add new features or improvements to your branch.
4. **Submit a Pull Request**: Open a PR to the original repository with a concise description of what changes you've made.

Your contributions will be reviewed as soon as possible. Please ensure your code is clean, well-documented, and includes tests where applicable.

## Questions or Issues?

If you encounter any problems or have questions about using `aicli`, please open an issue on the GitHub repository. Provide detailed information about your problem or question to help us understand and address it promptly.

## Further Information

For more details about configuring and using `aicli`, visit [GitHub repository](https://github.com/singhparavjot/aicli) or the documentation page. Stay updated with the latest releases and features by watching our repository on GitHub.

