"""This module contains utils functions to parse the response from the server"""

# ────────────────────────────────────────────────────── Import ────────────────────────────────────────────────────── #

import re
import requests


def parse_sse_stream_response(response: requests.Response):
    """Stream the response from the server to a streamlit text area

    Args:
        response (requests.Response): Response object from the server
    """
    # Regular expression to match lines that start with 'data:'
    data_pattern = re.compile(rb"^data:")

    # return a python generator
    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk and data_pattern.match(chunk):
                text = chunk.split(b"data:", 1)[1].strip().decode("utf-8")
                yield text

    return generate()
