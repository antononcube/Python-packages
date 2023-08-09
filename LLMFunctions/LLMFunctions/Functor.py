from typing import List, Callable, Union, Dict
import inspect


class Functor:
    llm_evaluator = None
    prompt = None
    args: Union[list, None] = None
    kwonlyargs: Union[list, None] = None

    def __init__(self, llm_evaluator, prompt):
        self.llm_evaluator = llm_evaluator
        self.prompt = prompt
        if callable(self.prompt):
            ires = inspect.getfullargspec(self.prompt)
            self.args = ires[0]
            self.kwonlyargs = ires[4]

    def __call__(self, *args, **dargs):

        # Deepcopy the evaluator
        llmEvaluatorLocal = self.llm_evaluator.copy()

        if isinstance(self.prompt, str):

            # LLM evaluate
            return llmEvaluatorLocal.eval(*args, **dargs)

        elif callable(self.prompt):

            # Filter the prompt function
            print("prompt function args: ", self.args)

            dargs2 = dict(filter(lambda x: x[0] in self.args, dargs.items()))
            promptLocal = self.prompt(*args, **dargs2)

            # LLM evaluate
            return llmEvaluatorLocal.eval(promptLocal, **dargs)

    def __str__(self):
        return str(repr(self.prompt))
