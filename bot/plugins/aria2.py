# GOAL:
# getting track for logging

import logging

LOGGER = logging.getLogger(__name__)

# GOAL:
# create aria2 handler class

import asyncio
import aria2p

class aria2(aria2p.API):
    __api =  None
    __config = {
        "dir" : "downloads",
        "daemon" : "true",
        "max-connection-per-server" : "16",
        "max-overall-upload-limit" : "1K",
        "max-concurrent-downloads" : "3",
        "bt-max-peers" : "0",
        "rpc-listen-all" : "false",
        "rpc-listen-port": "6800",
        "seed-ratio" : "0",
        "seed-time" : "0.01"
    }
    __process = None

    def __init__(self, config={}):
        self.__config.update(config)

    async def start(self):
        if not self.__process:
            cmd = [
                "aria2c",
                "--enable-rpc"
            ]
            for key in self.__config:
                cmd.append(f"--{key}={self.__config[key]}")
            LOGGER.info(cmd)
            self.__process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await self.__process.communicate()
            LOGGER.info(stderr or stdout)
        if not self.__api:
            self.__api = aria2p.API(
                aria2p.Client(
                    host="http://localhost",
                    port=int(self.__config['rpc-listen-port'])
                )
            )
    
    def __getattr__(self, name):
        return getattr(self.__api, name)
