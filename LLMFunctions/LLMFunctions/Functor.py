from collections.abc import Iterable
from LLMFunctions.Configuration import Configuration
from LLMFunctions.Evaluator import Evaluator

class Functor:
    llm_evaluator = None
    prompt = None

    def __init__(self, llm_evaluator, prompt):
        self.llm_evaluator = llm_evaluator
        self.prompt = prompt

    def __call__(self, *args, **dargs):
        return self.llm_evaluator.eval(*args, **dargs)

    def __str__(self):
        return str(repr(self.prompt))
