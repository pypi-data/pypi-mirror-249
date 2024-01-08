import os

from dotenv import load_dotenv

from parea import Experiment, init
from parea.evals.utils import call_openai
from parea.schemas.log import Log
from parea.utils.trace_utils import trace

load_dotenv()

init(api_key=os.getenv("PAREA_API_KEY"))


def is_between_1_and_n(log: Log) -> float:
    """Evaluates if the number is between 1 and n"""
    n = log.inputs["n"]
    try:
        return 1.0 if 1.0 <= float(log.output) <= float(n) else 0.0
    except ValueError:
        return 0.0


@trace(eval_funcs=[is_between_1_and_n])
def generate_random_number(n: str) -> str:
    return call_openai(
        [
            {"role": "user", "content": f"Generate a number between 1 and {n}."},
        ],
        model="gpt-3.5-turbo",
    )


Experiment(
    name="Testing",
    data=[
        {"n": "10"},
    ],
    func=generate_random_number,
)
