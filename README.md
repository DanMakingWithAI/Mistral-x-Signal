# Exposing a Large Language Model over Signal

This repository is for exposing a locally hosted Large Language Model over Signal. In this example, we use the Open Orca fine-tune of Mistral 7B using Ollama and expose a simple one-chat-at-a-time interface over Signal using `signal-cli`, with no advanced memory or context management.


## Getting Started

**TLDR:** Watch the video at **TBC**

1. Clone this repository by running `git clone https://github.com/DanMakingWithAI/Mistral-x-Signal.git` in your terminal.
2. Install the latest release of [signal-cli](https://github.com/AsamK/signal-cli) - unzip the latest `.tar.gz` into the same folder as this repository such that you'll have a `signal-cli/bin` folder containing the `signal-cli` executables
3. Install [Ollama](https://github.com/jmorganca/ollama) - on Windows you'll need to do this via WSL2
4. `pip install -r requirements.txt` - it's only `requests` and `python-dotenv`
5. Configure the environment variables: copy the `template.env` file to `.env` and overwrite the phone numbers in international format e.g. `+12345678901...`
6. Set up your Signal account - the [signal-cli QuickStart guide](https://github.com/AsamK/signal-cli/wiki/Quickstart) is easy enough to follow
8. Run the `signal_mistral` script to start the service. This can be done by running `python signal_mistral.py` in your terminal.
9. Optionally, run at startup. On Windows you can use Task Scheduler to add `run_mistral_x_signal.bat` to run on user login - you'll need to overwite the directory path listed in the file with whatever's right for your system - see the video for an explanation of the file and the options to use in your Task Scheduler task. On other platforms, you can use the usual patterns there to implement an equivalent.

For detailed instructions, please watch the video above.


## Donate

Making this project was quick. Documenting it so others could follow took MUCH longer 😆

If you find this project useful, consider supporting the author and future development by [donating](https://ko-fi.com/DanMakingWithAI)
