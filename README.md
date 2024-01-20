# Exposing a Large Language Model over Signal

This repository is for exposing a locally hosted Large Language Model over Signal. In this example, we use the Open Orca fine-tune of Mistral 7B using Ollama and expose a simple one-chat-at-a-time interface over Signal using `signal-cli`, with no advanced memory or context management.


## Getting Started

**TLDR:** Watch the video at **TBC**

1. Clone this repository by running `git clone https://github.com/DanMakingWithAI/Mistral-x-Signal.git` in your terminal.
2. Install the latest release of `signal-cli` which you can find at `https://github.com/AsamK/signal-cli` - unzip the latest `.tar.gz` into the same folder as this repository such that you'll have a `signal-cli/bin` folder containing the `signal-cli` executables
3. Install Ollama - on Windows you'll need to do this via WSL2
3. Configure the environment variables. This involves setting up your Signal account and other necessary configurations.
4. Run the signal_mistral script to start the service. This can be done by running `python signal_mistral.py` in your terminal.
5. Optionally, run at startup. On Windows you can use Task Scheduler to add `run_mistral_x_signal.bat` to run on user login - see video for explanation of options. On other platforms, use the usual patterns there to implement an equivalent to the bat file.

For detailed instructions, please refer to the video above.


## Donate

If you find this project useful, consider supporting its development by donating at [https://ko-fi.com/DanMakingWithAI](https://ko-fi.com/danmakingwithai).
