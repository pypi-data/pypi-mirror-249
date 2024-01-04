import sys

import sensenova
from typing import Any
import json


def receive_completion_results(stream: bool, resp: Any):
    if not stream:
        resp = [resp]
    for part in resp:
        choices = part['data']["choices"]
        for c_idx, c in enumerate(choices):
            if len(choices) > 1:
                sys.stdout.write("===== Chat Completion {} =====\n".format(c_idx))
            if stream:
                delta = c.get("delta")
                if delta:
                    sys.stdout.write(delta)
            else:
                sys.stdout.write(c["text"])
                if len(choices) > 1:  # not in streams
                    sys.stdout.write("\n")
            sys.stdout.flush()


def test_completion_stream():
    stream = True
    resp = sensenova.Completion.create(
        prompt="今天天气怎么样",
        model="nova-ptc-s-v1-codecompletion",
        stream=stream,
        n=2,
        max_new_tokens=1024,
        repetition_penalty=1.05,
        stop=None,
        temperature=0.8,
        top_p=0.7
    )

    receive_completion_results(stream, resp)


def test_chat_completion_non_stream():
    stream = False
    resp = sensenova.Completion.create(
        prompt="Say this is a test!",
        model="nova-ptc-s-v1-codecompletion",
        stream=stream,
        n=2,
        max_new_tokens=1024,
        repetition_penalty=1.05,
        stop=None,
        temperature=0.8,
        top_p=0.7
    )

    receive_completion_results(stream, resp)
