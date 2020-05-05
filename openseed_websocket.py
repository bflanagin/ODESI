#!/usr/bin/env python

import asyncio
import websockets
import openseed_seedgenerator as Seed
import openseed_account as Account
import json
import time
import openseed_core as Core
import subprocess
import sys
import os

async def echo(websocket, path):
	async for message in websocket:
		response = Core.message(message)
		await websocket.send(response)

asyncio.get_event_loop().run_until_complete(
	websockets.serve(echo, '0.0.0.0', 8765))
asyncio.get_event_loop().run_forever()
