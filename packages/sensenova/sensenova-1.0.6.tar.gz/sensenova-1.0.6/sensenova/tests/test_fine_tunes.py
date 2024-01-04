import json
from tempfile import NamedTemporaryFile

import sensenova


def test_finetune_create():
    result = sensenova.FineTune.create(
        hyperparams={
            "training": {
                "learning_rate": 0.00002,
                "n_iters": 2000,
                "batch_size": 4
            }
        },
        model="nova-ptc-xs-v1",
        suffix="wand",
        training_file="e2f9075e-ed8d-4b79-87cd-072e974963fd"
    )
    print(result)


def test_finetune_list():
    resp = sensenova.FineTune.list()
    print(resp)

def test_finetune_cancel(id):
    resp = sensenova.FineTune.cancel(id)
    print(resp)


if __name__ == "__main__":
    id = 'ft-62e72ad8e1624bdc812cbfc71940505d'
    # test_finetune_list()
    # test_finetune_create()
    # test_finetune_list()
    print(sensenova.FineTune.retrieve(id=id))
    # test_finetune_cancel(id=id)
    # print(sensenova.FineTune.delete(sid=id))
    # test_finetune_list()
