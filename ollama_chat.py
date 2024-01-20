#!/usr/bin/env python
"""Assumes we are already running Ollama (uses mistral-openorca with default other settings)"""

import requests, json

ollama_chat_url = "http://localhost:11434/api/chat"

STATUS_REQUEST_RECEIVED = 'REQUEST_RECEIVED'
STATUS_REQUEST_SENT = 'REQUEST_SENT'
STATUS_RESPONSE_STARTED = 'RESPONSE_STARTED'
STATUS_RESPONSE_PART_RECEIVED = 'RESPONSE_PART_RECEIVED'
STATUS_RESPONSE_COMPLETED = 'RESPONSE_COMPLETED'

# Generate initial system message (not required)
def generate_system_message(system_prompt="You are a helpful assistant.", new_thread=[]):
  new_thread = [
    {
      'role': 'system',
      'content': system_prompt
    }
  ]
  return new_thread

# Simple status callback, prints all status updates
def print_status(status, content=None):
  print(f'{status}: {content}')

# Simple status callback, prints the final conversation
def print_conversation_turns(status, content=None):
  if status == STATUS_REQUEST_RECEIVED:
    print(f'User: {content}')
  elif status == STATUS_RESPONSE_COMPLETED:
    print(f'Assistant: {content}')

# Simple status callback, prints the final conversation, as it streams
def print_conversation_turns_streaming(status, content=None):
  if status == STATUS_REQUEST_RECEIVED:
    print(f'User: {content}')
  elif status == STATUS_RESPONSE_STARTED:
    print(f'Assistant: ', end='', flush=True)
  elif status == STATUS_RESPONSE_PART_RECEIVED:
    print(content, end='', flush=True)
  elif status == STATUS_RESPONSE_COMPLETED:
    print('')


# Get Completion
def get_chat_completion(prompt='Hello', thread=[], status_callback=None):

  # Start by noting the received prompt
  if status_callback is not None:
    status_callback(STATUS_REQUEST_RECEIVED, prompt)

  # Add the user message
  thread.append(
    {
      'role': 'user',
      'content': prompt
    }
  )

  # Harcoded as mistral-openorca for now
  ollama_request = {
    'model': 'mistral-openorca',
    'messages': thread
  }

  # Make a POST request for a streaming response
  r = requests.post(ollama_chat_url, stream=True, data=json.dumps(ollama_request))
  if status_callback is not None:
    status_callback(STATUS_REQUEST_SENT, prompt)

  # Loop over all chunks as they are received
  full_response = ''
  response_started = False
  first_response = True

  for chunk in r.iter_content(1024):
    if chunk:
      
      # Note the start of a response
      if not response_started:
        response_started = True
        if status_callback is not None:
          status_callback(STATUS_RESPONSE_STARTED)
      
      # Assume complete if no successful JSON decoding
      try:
        data = json.loads(chunk.decode('utf-8'))
        
        # Complete when done = true is received
        if data['done'] == True:
          break

        # Else record this chunk
        this_response_chunk = data['message']['content']

      except json.JSONDecodeError:
        break

      # Remove any initial space if it's a first response
      if first_response:
        first_response = False
        if this_response_chunk.startswith(' '):
          this_response_chunk = this_response_chunk[1:]
      
      # Note progress
      if status_callback is not None:
        status_callback(STATUS_RESPONSE_PART_RECEIVED, this_response_chunk)
      
      # Accumulate the completed response as necessary
      full_response = full_response + this_response_chunk

  # Note the end of the response
  if status_callback is not None:
    status_callback(STATUS_RESPONSE_COMPLETED, full_response)

  # For convenience, return the new message history
  thread.append({
    'role': 'assistant',
    'content': full_response
  })
  return thread


def main():
  thread = generate_system_message()
  get_chat_completion(prompt='Mary had a little lamb', thread=thread, status_callback=print_conversation_turns)
  get_chat_completion(prompt='I am hungry - should I cook and eat the lamb?', thread=thread, status_callback=print_conversation_turns)

if __name__ == "__main__":
  main()
