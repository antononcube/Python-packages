from collections.abc import Iterable
from LLMFunctions.Configuration import Configuration
import openai


class Evaluator:
    conf: Configuration = None
    formatron = None

    def __init__(self, conf=None, formatron='Str'):
        self.conf = conf
        self.formatron = formatron

    def clone(self, **kwargs):
        return Evaluator(conf=self.conf.copy(), **kwargs)

    def prompt_texts_combiner(self, prompt, texts, **args):
        if isinstance(texts, list):
            textsLocal = texts
        elif isinstance(texts, str):
            textsLocal = [texts]
        else:
            TypeError("Cannot convert")

        if isinstance(prompt, list):
            promptLocal = prompt
        elif isinstance(prompt, str):
            promptLocal = [prompt]
        else:
            TypeError("Cannot convert")
        return self.conf.to_dict()['prompt_delimiter'].join(promptLocal + textsLocal)

    def get_formatron(self, spec):
        if spec is None:
            return None

    def post_process(self, res, form=None):

        resLocal = res
        if isinstance(resLocal, list) and len(resLocal) == 1:
            resLocal = resLocal[0]

        if form is None:
            reformater = self.get_formatron(self.formatron)
        else:
            reformater = self.get_formatron(form)

        if callable(reformater):
            return reformater.process(resLocal)
        return resLocal

    def eval(self, texts, **args):

        confDict = self.conf.to_dict()

        echo = args.get('echo', False)

        if echo:
            print(f"Configuration: {self.conf}")

        args2 = {**self.conf.to_dict(), **args}

        # Handling the argument renaming
        for k, v in confDict['argument_renames'].items():
            args2[v] = args2.get(v, args2.get(k, None))

        # Make the full prompt
        prompt = confDict['prompts'] + [confDict['prompt_delimiter'], ]

        if echo:
            print(f'Full prompt: {prompt}')

        # Form messages
        messages = self.prompt_texts_combiner(prompt, texts)

        if echo:
            print(f'Messages: {messages}')

        print(sorted(args2.keys()))
        print(args2)

        # Invoke the LLM function
        args2["prompt"] = messages
        args2["messages"] = messages

        args2 = dict(filter(lambda x: x[0] in self.conf.known_params, args2.items()))

        res = self.conf.function(**args2)

        if isinstance(self.conf.response_value_keys, list):
            for k in self.conf.response_value_keys:
                res = res[k]

        # Process the result
        return self.post_process(res, form=args.get('form', None))

    def __repr__(self):
        if self.conf is Configuration:
            res = self.conf.to_dict()
        else:
            res = {"conf": None}
        res["formatron"] = self.formatron
        return repr(res)

    def __str__(self):
        return str(repr(self))
