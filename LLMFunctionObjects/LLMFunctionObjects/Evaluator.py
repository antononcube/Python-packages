from LLMFunctionObjects.Configuration import Configuration
from LLMFunctionObjects.SubParser import SubParser
from LLMFunctionObjects.SubParser import sub_parser


class Evaluator:
    conf: Configuration = None
    formatron = None
    llm_result = None

    def __init__(self, conf=None, formatron='Str'):
        self.conf = conf
        self.formatron = formatron
        self.llm_result = None

    # This prompt combiner method is for the generic LLM evaluation
    # using the Evaluator class.
    def prompt_texts_combiner(self, prompt, texts, **args):
        # Make a list from prompts
        promptLocal = []
        if isinstance(prompt, list):
            promptLocal = prompt
        elif isinstance(prompt, str):
            promptLocal = [prompt, ]
        else:
            TypeError("Cannot convert prompt argument to a list of strings.")

        # Make a list from texts
        textsLocal = []
        if isinstance(texts, list):
            textsLocal = texts
        elif isinstance(texts, str):
            textsLocal = [texts, ]
        else:
            TypeError("Cannot convert texts argument to a list of strings.")

        # Result by joining the list string with the context delimiter
        return self.conf.to_dict()['prompt_delimiter'].join(promptLocal + textsLocal)

    def get_formatron(self, spec):
        if spec is None:
            return None
        elif isinstance(spec, str):
            return sub_parser(spec)
        elif callable(spec):
            return sub_parser(spec)
        elif isinstance(spec, SubParser):
            return spec
        else:
            return None

    def result_values(self, res):
        resLocal = res
        if isinstance(self.conf.response_value_keys, list):
            for k in self.conf.response_value_keys:
                resLocal = resLocal[k]
        return resLocal

    def post_process(self, res, form=None):

        resLocal = res
        if isinstance(resLocal, list) and len(resLocal) == 1:
            resLocal = resLocal[0]

        if form is None:
            reFormatter = self.get_formatron(self.formatron)
        else:
            reFormatter = self.get_formatron(form)

        if isinstance(reFormatter, SubParser):
            return reFormatter.process(resLocal)
        return resLocal

    # This is a generic LLM evaluator method
    # that works for OpenAI's text completions, and
    # PaLM's text generation.
    # The children classes override this method completely.
    # (instead of reusing it because of logging, etc.)
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
        fullPrompt = confDict['prompt_delimiter'].join(confDict['prompts'])

        if echo:
            print(f'Full prompt: {fullPrompt}')

        # Form messages
        messages = self.prompt_texts_combiner(fullPrompt, texts)

        if echo:
            print(f'Messages: {messages}')

        # Remove (last) LLM result
        self.llm_result = None

        # Invoke the LLM function
        args2["prompt"] = messages
        args2["messages"] = messages

        args2 = dict(filter(lambda x: x[0] in self.conf.known_params, args2.items()))

        res = self.conf.function(**args2)

        if echo:
            print(f'LLM result: {res}')

        # Same LLM result
        self.llm_result = res

        # Get result attribute
        if isinstance(self.conf.response_object_attribute, str):
            res = getattr(res, self.conf.response_object_attribute)

        # Get result values
        res = self.result_values(res)

        # Process the result
        formatron = args.get('formatron', args.get('form', None))
        return self.post_process(res, form=formatron)

    # ------------------------------------------------------------------
    # Copying
    # ------------------------------------------------------------------
    def copy(self):
        """Deep copy."""
        newObj = type(self)(conf=self.conf.copy(), formatron=self.formatron)
        return newObj

    def __copy__(self):
        """Deep copy."""
        return self.copy()

    def __deepcopy__(self, **kwargs):
        """Deep copy."""
        return self.copy()

    # ------------------------------------------------------------------
    # Representations
    # ------------------------------------------------------------------
    def to_dict(self):
        if self.conf is Configuration:
            res = self.conf.to_dict()
        else:
            res = {"conf": None}
        res["formatron"] = self.formatron
        return res

    def __repr__(self):
        return repr(self.to_dict())

    def __str__(self):
        return str(repr(self))
