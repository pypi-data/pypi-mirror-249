import sys

import sensenova
from typing import Any
import json

def test_character_chat_completion():
    resp = sensenova.CharacterChatCompletion.create(
        model="nova-ptc-s-v1-character",
        n=2,
        max_new_tokens=300,
        character_settings=[
            {
                "name": "y",
                "gender": "男",
                "nickname": "铁老师",
                "other_setting": "特别喜欢钱,主播赚的钱都是我的."
            },
            {
                "name": "d",
                "gender": "男",
                "nickname": "卖菜员"
            }
        ],
        role_setting={
            "user_name": "d",
            "primary_bot_name": "y"
        },
        messages=[
            {
                "name": "d",
                "content": "请问铁老师,我为公司赚了几百亿,我能分多少钱."
            }
        ]
    )

    print(resp["data"]["reply"])
    print(resp.headers())
    choices = resp['data']["choices"]
    for c_idx, c in enumerate(choices):
        if len(choices) > 1:
            sys.stdout.write("===== Character Chat Completion {} =====\n".format(c_idx))

        sys.stdout.write(c["message"])
        if len(choices) > 1:  # not in streams
            sys.stdout.write("\n")
        sys.stdout.flush()
