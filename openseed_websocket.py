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

async def to_core(websocket, path):
	async for message in websocket:
		themessage = message.decode()
		if themessage.find("msg=") !=-1:
			appId = themessage.split("msg=")[1].split("<::>")[0]
			key = Account.get_priv_from_pub(appId,"App")
			message = themessage.split("msg=")[1].split("<::>")[1]
			if len(themessage.split("msg=")[1].split("<::>")) == 3:
				decrypted = Seed.simp_decrypt(key,message)
				response = Core.message(decrypted)
				encrypt = Seed.simp_crypt(key,response)
				print(Seed.simp_decrypt(key,encrypt))
				await websocket.send(encrypt)
			else:
				print('{"server":"error incomplete message"}')
				print(themessage)
				await websocket.send(str('{"server":"error incomplete message"}').encode("utf8"))

asyncio.get_event_loop().run_until_complete(websockets.serve(to_core, '0.0.0.0', 8765))
asyncio.get_event_loop().run_forever()
