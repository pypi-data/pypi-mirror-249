import sensenova
import sys
import json


def test_chat_session():
    result = sensenova.ChatSession.create()
    print(result)
    result = sensenova.ChatSession.create(system_prompt=[
        {
            "role": "system",
            "content": "You are a translation expert."
        }
    ])
    print(result)


def test_chat_conversation():
    result = sensenova.ChatConversation.create(
        action="next",
        content="地球的直径是多少米?",
        model="nova-ptc-xl-v1",
        session_id="55b1f0815c76000",
        stream=False,
        know_ids=[]
    )
    print(result)


def test_chat_conversation_stream():
    resp = sensenova.ChatConversation.create(
        action="next",
        content="地球的直径是多少米?",
        model="nova-ptc-xl-v1",
        session_id="55b1f0815c76000",
        stream=True,
        know_ids=[]
    )
    for part in resp:
        print(part["data"]["delta"])


def test_chat_completion_associated_knowledge():
    session_result = sensenova.ChatSession.create()
    stream = False
    resp = sensenova.ChatConversation.create(
        session_id=session_result["session_id"],
        action="next",
        content="aasda是什么",
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
                "search_enable": False,
                "result_enable": True
            },
        }
    )

    print(json.dumps(resp, ensure_ascii=False))
