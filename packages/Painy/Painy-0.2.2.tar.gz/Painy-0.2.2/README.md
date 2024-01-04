# Painy

    Comments for this repository commits are written with Painy itself.

*Star the repository to support the project.*

## Features

- Painy is a simple tool which allows you to automatically generate commit messages with the help of OpenAI models. It automatically check the staged changes in your repository and generate a commit message based on the changes.

- Works well with Jupyter Notebooks (`.ipynb` files) by using `nbdime` for diffing.

- Painy is capable of reviewing past commits and creating new ones that follow the same style.

- You can add your own rules/requests as additional prompts for model. For example, set maximum number of characters/sentences in the commit message.

- Interactive mode.

## Prerequisites

- OpenAI API key. You can get one [here](https://platform.openai.com).

- Python 3.7.1 or higher and `pip` package manager.

## Installation

- Install the package via pip:

    ```bash
    pip install painy
    ```

- Set the environment variable `OPENAI_API_KEY` to your OpenAI API key.

- By default, Painy will use the `gpt-3.5-turbo` (ChatGPT), if you want to use a different model, set the environment variable `OPENAI_MODEL_NAME` to the model you want to use. You must have access to the model you want to use.

- Max context length depends on the model you use. Try to use the tool on not too big changes, ideally on a single file.

## Usage

- (Recommended) Go to the folder with your repository and run the following command:

  - Add something to stage:

    ```bash
    git add <files>
    ```

  - Then use Painy:

    ```bash
    painy comment
    ```

  - Or with the environment variable `OPENAI_API_KEY` set inplace:

    ```bash
    OPENAI_API_KEY=<your-openai-api-key> painy comment
    ```

    This will generate a commit message based on the staged changes in your repository.

- Commit staged changes with a generated commit message:

```bash
painy commit
```

- Interactive mode:

```bash
painy <comment|commit> -i
```

This will generate a commit message based on the staged changes in your repository and will ask you if you want to regenerate the commit message.

- If you want to generate a commit message for all the changes in your repository, run the following command (this files must be registered in git before in order to have a diff to compare):

```bash
painy <comment|commit> --check-all
```

- By default the `use_commit_history_style` is set to `True`. If you want to disable it, run the following command:

    ```bash
    painy config --set use-commit-history-style False
    ```

- To get the actual value of config option run the following command:

    ```bash
    painy config --get use-commit-history-style
    ```

- List of options:
  - `use_commit_history_style` - whether to use the style of the former commits in the repository. By default it is set to `false`. (Experimental)
  - `max_num_commits_style` - the maximum number of last commits to use for the style. By default it is set to `5`.
  - `max_characters` (used as a property in one of default rules) - the desired maximum number of characters in the commit message. By default it is set to `100`.

- To get the list of rules run the following command:

    ```bash
    painy rules
    ```

  - To add a new rule run the following command:

    ```bash
    painy rules --add "Your own rule"
    ```

  - To remove i-th rule from the list run the following command:

    ```bash
    painy rules --remove <i>
    ```
