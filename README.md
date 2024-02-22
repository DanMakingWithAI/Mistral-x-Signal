# Exposing a Locally Hosted Large Language Model over Signal

In this example, we use the Open Orca fine-tune of Mistral 7B using Ollama and expose a simple one-chat-at-a-time interface over Signal using `signal-cli`, with no advanced memory or context management.


**TLDR:** Watch the video on [YouTube](https://youtu.be/FoDRF-1hWco)

## Edits
### 22/02/2024:
- WSL2 no longer required as Ollama now has a native Window installation - `run_mistral_x_signal.bat` updated to reflect this.
- The bat file also handles signal-cli errors better now, creating `signal-cli-error.log` if an error was encountered e.g. an out of date binary due to updates of Signal services
- I'm aware that there is now an Ollama Python library. I may migrate to in future, but it still works fine as-is for now.

## Getting Started
1. Clone this repository by running `git clone https://github.com/DanMakingWithAI/Mistral-x-Signal.git` in your terminal.
2. Install the latest release of [signal-cli](https://github.com/AsamK/signal-cli) - unzip the latest `.tar.gz` into the same folder as this repository such that you'll have a `signal-cli/bin` folder containing the `signal-cli` executables
3. Install [Ollama](https://github.com/jmorganca/ollama) - there is now a Windows native installation available (no need to follow the installation instructions in the video for installing on WSL2 any more)
4. `pip install -r requirements.txt` - it's only `requests` and `python-dotenv`
5. Configure the environment variables: copy the `template.env` file to `.env` and overwrite the phone numbers in international format e.g. `+12345678901...`
6. Set up your Signal account - the [signal-cli QuickStart guide](https://github.com/AsamK/signal-cli/wiki/Quickstart) is easy enough to follow
8. Run the `signal_mistral` script to start the service. This can be done by running `python signal_mistral.py` in your terminal.
9. Optionally, run at startup. On Windows you can use Task Scheduler to add `run_mistral_x_signal.bat` to run on user login - you'll need to overwite the directory path listed in the file with whatever's right for your system - see the video for an explanation of the file and the options to use in your Task Scheduler task. On other platforms, you can use the usual patterns there to implement an equivalent.

For detailed instructions, please watch the video above.


## Donate

Making this project was quick. Documenting it so others could follow took MUCH longer 😆

If you find this project useful, consider supporting the author and future development by [donating](https://ko-fi.com/DanMakingWithAI)
