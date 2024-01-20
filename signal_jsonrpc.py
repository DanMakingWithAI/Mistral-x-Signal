#!/usr/bin/env python
"""Assumes re have already run: ./signal-cli -a YOURNUM daemon --http localhost:11535 --receive-mode=manual"""

import requests, time, os

from dotenv import load_dotenv
load_dotenv()
SIGNAL_PHONE_NUMBER_TO_SEND_FROM = os.getenv('SIGNAL_PHONE_NUMBER_TO_SEND_FROM')
SIGNAL_PHONE_NUMBER_TO_SEND_TO = os.getenv('SIGNAL_PHONE_NUMBER_TO_SEND_TO')

signal_cli_daemon_check_url = "http://localhost:11535/api/v1/check"
signal_cli_daemon_jsonrpc_url = "http://localhost:11535/api/v1/rpc"
signal_cli_deamon_headers = {
  "Content-Type": "application/json",
  "Accept": "application/json"
}

def raise_exception_if_signal_cli_daemon_is_down():
  r = requests.get(signal_cli_daemon_check_url, headers=signal_cli_deamon_headers)
  if r.status_code != 200:
    raise ConnectionAbortedError('Signal CLI daemon unavailable', r.status_code)

def send_signal_message(message):
  data = {
    "jsonrpc":"2.0",
    "method":"send",
    "params": {
      "recipient": [SIGNAL_PHONE_NUMBER_TO_SEND_TO],
      "message": message
    },
    "id": int(time.time())
  }
  r = requests.post(signal_cli_daemon_jsonrpc_url, headers=signal_cli_deamon_headers, json=data)
  if r.status_code != 200:
    raise ConnectionAbortedError('Signal CLI daemon unavailable - Message sending aborted', r.status_code)

def receive_signal_messages():
  data = {
    "jsonrpc":"2.0",
    "method":"receive",
    "params": {},
    "id": int(time.time())
  }
  r = requests.post(signal_cli_daemon_jsonrpc_url, headers=signal_cli_deamon_headers, json=data)
  if r.status_code != 200:
    raise ConnectionAbortedError('Signal CLI daemon unavailable - Message receiving aborted', r.status_code)
  response = r.json()
  # print(response)
  all_messages = [
    {
      'source': item.get('envelope', {}).get('sourceNumber', None),
      'message': item.get('envelope', {}).get('dataMessage', {}).get('message', None),
      'timestamp': item.get('envelope', {}).get('dataMessage', {}).get('timestamp', None)
    }
    for item in response['result']
  ]
  all_messages_from_given_number = [ message_object for message_object in all_messages if message_object['source'] == SIGNAL_PHONE_NUMBER_TO_SEND_TO ]
  all_messages_with_content = [ message_object for message_object in all_messages_from_given_number if message_object['message'] ]
  all_message_contents = [ message_object['message'] for message_object in all_messages_with_content ]
  all_message_timestamps = [ message_object['timestamp'] for message_object in all_messages_with_content ]
  concatenated_message = '\n'.join(all_message_contents)
  return { 'message': concatenated_message, 'timestamps': all_message_timestamps }

def send_signal_read_receipt(timestamps):
  data = {
    "jsonrpc":"2.0",
    "method":"sendReadReceipt",
    "params": {
      "recipient": [SIGNAL_PHONE_NUMBER_TO_SEND_TO],
      "targetSentTimestamp": timestamps
    },
    "id": int(time.time())
  }
  r = requests.post(signal_cli_daemon_jsonrpc_url, headers=signal_cli_deamon_headers, json=data)
  if r.status_code != 200:
    raise ConnectionAbortedError('Signal CLI daemon unavailable - Read receipt sending aborted', r.status_code)
  
def send_signal_typing_indicator(true_if_sending_stop):
  data = {
    "jsonrpc":"2.0",
    "method":"sendTyping",
    "params": {
      "recipient": [SIGNAL_PHONE_NUMBER_TO_SEND_TO],
      "stop": true_if_sending_stop
    },
    "id": int(time.time())
  }
  r = requests.post(signal_cli_daemon_jsonrpc_url, headers=signal_cli_deamon_headers, json=data)
  if r.status_code != 200:
    raise ConnectionAbortedError('Signal CLI daemon unavailable - Typing indicator sending aborted', r.status_code)
  
def send_signal_typing_indicator_start():
  send_signal_typing_indicator(False)

def send_signal_typing_indicator_stop():
  send_signal_typing_indicator(True)

def echo_and_encourage_continuation_until_goodbye(message, timestamps, thread):
  print(message)
  send_signal_read_receipt(timestamps)
  send_signal_typing_indicator_start()
  time.sleep(5) # Artificial delay, as a demo
  send_signal_typing_indicator_stop()

  # Message routing, could add /command handling here
  conversation_finished = False
  if (message == "Goodbye"):
    send_signal_message("Goodbye!")
    conversation_finished = True
  else:
    send_signal_message(f"It's funny you should say '{message}' - I was just thinking that. Go on...")

  return conversation_finished

def poll_for_incoming_messages(message_handler, thread=[]):
  result = receive_signal_messages()
  message = result['message']
  conversation_finished = False
  if message:
    conversation_finished = message_handler(message, result['timestamps'], thread)
  return conversation_finished

def main():
  # Check the signal-cli daemon available
  raise_exception_if_signal_cli_daemon_is_down()

  # Polling loop
  loop_num = 0
  conversation_finished = False
  while not conversation_finished:
    loop_num = loop_num + 1
    print(f"Waiting ({loop_num})")
    conversation_finished = poll_for_incoming_messages(echo_and_encourage_continuation_until_goodbye)
    time.sleep(5)

if __name__ == "__main__":
  main()