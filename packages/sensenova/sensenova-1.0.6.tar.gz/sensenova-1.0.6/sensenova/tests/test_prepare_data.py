import json
import subprocess
from tempfile import NamedTemporaryFile


def test_prepare_data() -> None:
    unprepared_training_data = [
        {
            "instruction": "我们如何在日常生活中减少用水？",
            "input": "",
            "output": "1. 使用节水装置，如节水淋浴喷头和水龙头。 \n2. 使用水箱或水桶收集家庭废水，例如洗碗和洗浴。 \n3. 在社区中提高节水意识。 \n4. 检查水管和灌溉系统的漏水情况，并及时修复它们。 \n5. 洗澡时间缩短，使用低流量淋浴头节约用水。 \n6. 收集雨水，用于园艺或其他非饮用目的。 \n7. 刷牙或擦手时关掉水龙头。 \n8. 减少浇水草坪的时间。 \n9. 尽可能多地重复使用灰水（来自洗衣机、浴室水槽和淋浴的水）。 \n10. 只购买能源效率高的洗碗机和洗衣机。"
        },
        {
            "instruction": "编辑文章，使其更吸引读者。",
            "input": "自主机器人是计算机控制的机器，被编程执行特定任务而不需要任何人类输入。自主机器人在各个行业中被越来越广泛地应用，从制造业到医疗保健再到安全。",
            "output": "自主机器人是计算机控制的机器，被编程执行特定任务而不需要任何人类输入，从而实现了新的效率、精确度和可靠性水平。自主机器人在各个行业中被越来越广泛地应用，从制造业，它们可以使用精度和一致的质量组装复杂的组件，到医疗保健，可以协助进行医疗测试和处理，再到安全，可以监控大面积地区，保障人们和财产的安全。自主机器人还可以减少在危险或有害环境中的错误和增加安全，在工业流程的检查或维修期间等。由于其多样性，自主机器人将彻底改变我们工作方式的方式，使任务变得更加简单、快速，最终更加愉悦。"
        },
        {
            "instruction": "政府可以采取哪些策略来减少空气污染？",
            "input": "",
            "output": "1. 实施强制的车辆排放标准和基于激励的计划，以降低车辆的碳足迹。\n2. 增加公共交通工具，减少公众对车辆的依赖。\n3. 增加对空气污染的影响的认识，鼓励市民减少污染物的生成。\n4. 投资于可再生能源的研究和开发，如太阳能和风能。\n5. 在工厂和发电厂安装空气污染控制装置，例如洗涤器。\n6. 对车辆和工厂使用清洁燃料。\n7. 实施更好的城市规划和控制拓展。\n8. 改善农业效率，减少化肥和杀虫剂的使用。\n9. 种植更多的树木以减少空气污染。\n10. 减少木材、煤炭和生物质的燃烧。"
        },
        {
            "instruction": "我们如何在日常生活中减少用水？",
            "input": "",
            "output": "1. 使用节水装置，如节水淋浴喷头和水龙头。 \n2. 使用水箱或水桶收集家庭废水，例如洗碗和洗浴。 \n3. 在社区中提高节水意识。 \n4. 检查水管和灌溉系统的漏水情况，并及时修复它们。 \n5. 洗澡时间缩短，使用低流量淋浴头节约用水。 \n6. 收集雨水，用于园艺或其他非饮用目的。 \n7. 刷牙或擦手时关掉水龙头。 \n8. 减少浇水草坪的时间。 \n9. 尽可能多地重复使用灰水（来自洗衣机、浴室水槽和淋浴的水）。 \n10. 只购买能源效率高的洗碗机和洗衣机。"
        }
    ]

    with NamedTemporaryFile(suffix=".json", mode="w") as training_data:
        training_data.write(json.dumps(unprepared_training_data, ensure_ascii=False))
        training_data.flush()

        prepared_data_cmd_output = subprocess.run(
            [f"sensenova tools fine_tunes.prepare_data -f {training_data.name}"],
            # ['ls'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            shell=True,
        )

        return prepared_data_cmd_output.stdout


if __name__ == '__main__':
    test_prepare_data()
