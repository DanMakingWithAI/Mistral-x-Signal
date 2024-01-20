#!/usr/bin/env python
"""Assumes re have already run: ./signal-cli/bin/signal-cli -a SIGNAL_PHONE_NUMBER_TO_SEND_FROM daemon --http localhost:11535 --receive-mode=manual"""
"""Assumes we are already running Ollama (uses mistral-openorca with default other settings)"""

import time
from signal_jsonrpc import send_signal_read_receipt, send_signal_typing_indicator_start, send_signal_typing_indicator_stop, send_signal_message, raise_exception_if_signal_cli_daemon_is_down, poll_for_incoming_messages
from ollama_chat import generate_system_message, get_chat_completion, print_conversation_turns

def handle_incoming_messages(message, timestamps, thread):
  # print(message)
  send_signal_read_receipt(timestamps)
  send_signal_typing_indicator_start()
  
  # Message routing, could add /command handling here
  conversation_finished = False
  if (message.lower() == "goodbye" or message.lower() == "thanks"):
    send_signal_typing_indicator_stop()
    send_signal_message("👍")
    del thread[1:]
    # print('Thread reset')
    conversation_finished = True
  else:
    # print('Passing in thread: ', thread)
    get_chat_completion(prompt=message, thread=thread)
    # print(thread)
    send_signal_typing_indicator_stop()
    send_signal_message(thread[-1]['content'])

  return conversation_finished

def main():
  # Check the signal-cli daemon available
  raise_exception_if_signal_cli_daemon_is_down()

  # Polling loop
  thread = generate_system_message("You are a helpful assistant. You speak in very succinct sentences suitable for instant messaging.")
  loop_num = 0
  while True:
    loop_num = loop_num + 1
    # print(f"Waiting ({loop_num})")
    poll_for_incoming_messages(handle_incoming_messages, thread)
    time.sleep(5)

if __name__ == "__main__":
  main()
