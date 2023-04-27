# get a token: https://replicate.com/account
from getpass import getpass
import os
import replicate
import matplotlib.pyplot as plt
import numpy as np
import requests


class ImageReplicator():
    def __init__(self) -> None:
        self.token = os.environ.get("REPLICATE_TOKEN") or getpass(
            "Enter your Replicate token: ")
        self.model = "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478"
        self.prompt = "an iguana on the beach, pointillism"
        self.output = replicate.run(
            "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
            input={"prompt": "an iguana on the beach, pointillism"}
        )

    
