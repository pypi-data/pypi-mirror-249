import sys

import sensenova
from typing import Any
import json


def receive_chat_completion_results(stream: bool, resp: Any):
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
                sys.stdout.write(c["message"])
                if len(choices) > 1:  # not in streams
                    sys.stdout.write("\n")
            sys.stdout.flush()


def test_chat_completion_stream():
    stream = True
    resp = sensenova.ChatCompletion.create(
        messages=[{"role": "user", "content": "Say this is a test!"}],
        model="nova-ptc-xs-v1",
        stream=stream,
    )

    receive_chat_completion_results(stream, resp)


def test_chat_completion_non_stream():
    stream = False
    resp = sensenova.ChatCompletion.create(
        messages=[{"role": "user", "content": "Say this is a test!"}],
        model="nova-ptc-xs-v1",
        stream=stream,
    )

    receive_chat_completion_results(stream, resp)


def test_chat_completion_associated_knowledge():
    stream = False
    resp = sensenova.ChatCompletion.create(
        messages=[{"role": "user", "content": "aasda是什么"}],
        model="nova-ptc-xl-v1",
        stream=stream,
        max_new_tokens=1024,
        n=1,
        repetition_penalty=1.05,
        temperature=0.8,
        top_p=0.7,
        user="sensenova-python-test-user",
        knowledge_config={
            "control_level": "normal",
            "knowledge_base_result": True
        },
        plugins={
            "associated_knowledge": {
                "content": "aasda是一个大电影院。",
                "mode": "concatenate"
            },
            "web_search": {
                "search_enable": True,
                "result_enable": True
            },
        }
    )

    print(json.dumps(resp, ensure_ascii=False))


def test_chat_completion_knowledge_base_configs():
    stream = False
    resp = sensenova.ChatCompletion.create(
        messages=[{"role": "user", "content": "如代发工资录入时提示“业务编号不匹配"}],
        model="nova-ptc-xl-v1",
        stream=stream,
        know_ids=["s76f9273aba56488ba8569a8134574b6b"],
        max_new_tokens=1024,
        n=1,
        repetition_penalty=1.05,
        temperature=0.8,
        top_p=0.7,
        user="sensenova-python-test-user",
        knowledge_config={
            "control_level": "normal",
            "knowledge_base_result": True,
            "knowledge_base_configs": [
                {
                    "know_id": "sfa06ed682460495f982fe56b9b4c3e22",
                    "faq_threshold": 0.9
                }
            ]
        },
        plugins={}
    )
    print()
    print(json.dumps(resp, ensure_ascii=False))
    print(resp.headers()["X-Request-Id"])
    print(type(resp.headers()))
    print(resp.headers())


def test_chat_completion_with_errors():
    try:
        stream = False
        resp = sensenova.ChatCompletion.create(
            messages=[{"role": "user", "content": "如代发工资录入时提示“业务编号不匹配"}],
            model="nova-ptc-xl-v1",
            stream=stream,
            know_ids=["s76f9273aba56488ba8569a8134574b6b"],
            max_new_tokens=1024,
            n=1,
            repetition_penalty=1.05,
            temperature=0.8,
            top_p=0.7,
            user="sensenova-python-test-user",
            knowledge_config={
                "control_level": "normal",
                "knowledge_base_result": True,
                "knowledge_base_configs": [
                    {
                        "know_id": "sfa06ed682460495f982fe56b9b4c3e22",
                        "faq_threshold": 0.9
                    }
                ]
            },
            plugins={}
        )
        print()
        print(json.dumps(resp, ensure_ascii=False))
        print(resp.headers())
    except sensenova.AuthenticationError as e:
        print(e.headers)
    except sensenova.InvalidRequestError as e:
        print(e.headers)
        print(e.http_body)
        print(e.code)
    except sensenova.APIError as e:
        print(e.headers)
    except sensenova.TryAgain as e:
        print(e.headers)
    except sensenova.PermissionError as e:
        print(e.headers)
    except sensenova.SensenovaError as e:
        print(e.headers)




