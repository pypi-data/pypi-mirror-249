"""This module contains the TakeoffClient class, which is used to interact with the Takeoff server."""
# ────────────────────────────────────────────────────── Import ────────────────────────────────────────────────────── #

from typing import Any, List, Iterator
from sseclient import Event, SSEClient
import requests


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                    Takeoff Client                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class TakeoffClient:
    def __init__(self, base_url: str = "http://localhost", port: int = 3000, mgmt_port: int = None):
        """TakeoffClient is used to interact with the Takeoff server.

        Args:
            base_url (str, optional): base url that takeoff server runs on. Defaults to "http://localhost".
            port (int, optional): port that main server runs on. Defaults to 8000.
            mgmt_port (int, optional): port that management api runs on. Usually be `port + 1`. Defaults to None.
        """
        self.base_url = base_url  # "http://localhost"
        self.port = port  # 8000

        if mgmt_port is None:
            self.mgmt_port = port + 1  # 8001
        else:
            self.mgmt_port = mgmt_port

        self.url = f"{self.base_url}:{self.port}"  # "http://localhost:3000"
        self.mgmt_url = f"{self.base_url}:{self.mgmt_port}"  # "http://localhost:3001"

    def get_readers(self) -> dict:
        """Get a list of information about all readers.

        Returns:
            dict: List of information about all readers.
        """
        response = requests.get(self.mgmt_url + "/reader_groups")
        return response.json()

    def embed(self, text: str | List[str], consumer_group: str = "embed") -> dict:
        """Embed a batch of text.

        Args:
            text (str | List[str]): Text to embed.
            consumer_group (str, optional): consumer group to use. Defaults to "embed".

        Returns:
            dict: Embedding response.
        """
        response = requests.post(self.url + "/embed", json={"text": text, "consumer_group": consumer_group})

        if response.status_code != 200:
            raise Exception(f"Embedding failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}")

        return response.json()

    def generate(
        self,
        text: str | List[str],
        sampling_temperature: float = None,
        sampling_topp: float = None,
        sampling_topk: int = None,
        repetition_penalty: float = None,
        no_repeat_ngram_size: int = None,
        max_new_tokens: int = None,
        min_new_tokens: int = None,
        regex_string: str = None,
        json_schema: Any = None,
        prompt_max_tokens: int = None,
        consumer_group: str = "primary",
    ) -> dict:
        response = requests.post(
            url=self.url + "/generate",
            json={
                "text": text,
                "sampling_temperature": sampling_temperature,
                "sampling_topp": sampling_topp,
                "sampling_topk": sampling_topk,
                "repetition_penalty": repetition_penalty,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "max_new_tokens": max_new_tokens,
                "min_new_tokens": min_new_tokens,
                "regex_string": regex_string,
                "json_schema": json_schema,
                "prompt_max_tokens": prompt_max_tokens,
                "consumer_group": consumer_group,
            },
        )
        if response.status_code != 200:
            raise Exception(f"Generation failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}")

        return response.json()

    def generate_stream(
        self,
        text: str | List[str],
        sampling_temperature: float = None,
        sampling_topp: float = None,
        sampling_topk: int = None,
        repetition_penalty: float = None,
        no_repeat_ngram_size: int = None,
        max_new_tokens: int = None,
        min_new_tokens: int = None,
        regex_string: str = None,
        json_schema: Any = None,
        prompt_max_tokens: int = None,
        consumer_group: str = "primary",
    ) -> Iterator[Event]:
        response = requests.post(
            url=self.url + "/generate_stream",
            json={
                "text": text,
                "sampling_temperature": sampling_temperature,
                "sampling_topp": sampling_topp,
                "sampling_topk": sampling_topk,
                "repetition_penalty": repetition_penalty,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "max_new_tokens": max_new_tokens,
                "min_new_tokens": min_new_tokens,
                "regex_string": regex_string,
                "json_schema": json_schema,
                "prompt_max_tokens": prompt_max_tokens,
                "consumer_group": consumer_group,
            },
            stream=True,
        )
        if response.status_code != 200:
            raise Exception(f"Generation failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}")

        # return a python generator
        return SSEClient(response).events()


if __name__ == "__main__":
    pass
