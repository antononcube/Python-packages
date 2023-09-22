from typing import List, Callable, Union, Dict
import inspect


class Functor:
    llm_evaluator = None
    prompt = None
    args: Union[list, None] = None
    kwOnlyArgs: Union[list, None] = None
    lmm_result = None

    def __init__(self, llm_evaluator, prompt):
        self.llm_evaluator = llm_evaluator
        self.prompt = prompt
        if callable(self.prompt):
            ires = inspect.getfullargspec(self.prompt)
            self.args = ires[0]
            self.kwOnlyArgs = ires[4]
        self.lmm_result = None

    def __call__(self, *args, **dargs):

        # Deepcopy the evaluator
        llmEvaluatorLocal = self.llm_evaluator.copy()

        res = ''
        if isinstance(self.prompt, str):

            args2 = [self.prompt, ] + list(args)

            # LLM evaluate
            res = llmEvaluatorLocal.eval(args2, **dargs)

        elif callable(self.prompt):

            # Filter the prompt function
            dargs2 = dict(filter(lambda x: x[0] in self.args, dargs.items()))

            # Compute the actual prompt given to LLM
            promptLocal = self.prompt(*args, **dargs2)

            # LLM evaluate
            res = llmEvaluatorLocal.eval(promptLocal, **dargs)

        # Save "raw" LLM result
        self.llm_result = llmEvaluatorLocal.llm_result

        # Result
        return res

    def __repr__(self):
        return str({'type': 'functor', 'prompt': repr(self.prompt), 'llm_evaluator': self.llm_evaluator})

    def __str__(self):
        return str(repr(self))
