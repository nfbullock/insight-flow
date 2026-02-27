#!/usr/bin/env python3
"""Test the shim print API directly"""

import os
import requests
from pathlib import Path

# Load auth token
shim_env_path = Path.home() / '.openclaw/workspace-fred/.shim-env'
if shim_env_path.exists():
    with open(shim_env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"')

token = os.environ.get('SHIM_AUTH_TOKEN')
pdf_path = "/home/sand/.openclaw/workspace-fred/insight-flow/kids/test_dahlia.pdf"

# Try the print endpoint
print(f"Testing print API with: {pdf_path}")
print(f"Token length: {len(token)}")

with open(pdf_path, 'rb') as f:
    # Try with 'file' key
    files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(
        'https://shim.bullock.im/print', 
        files=files, 
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")