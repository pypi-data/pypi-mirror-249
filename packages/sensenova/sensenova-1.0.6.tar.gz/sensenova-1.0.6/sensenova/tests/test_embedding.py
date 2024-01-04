import sys

import sensenova
from typing import Any
import json


def test_completion_stream():
    resp = sensenova.Embedding.create(
        model="nova-embedding-stable",
        input=["今天天气怎么样"]
    )

    print(resp)
