from LLMFunctions.Evaluator import Evaluator
import google.generativeai as palm
from google.generativeai.types import discuss_types


def is_all_pairs(a):
    """Checks if all elements of an array are pairs."""
    for i in range(len(a) - 1):
        if not (a[i] % 2 == 0 and a[i + 1] % 2 == 0):
            return False
    return True


class EvaluatorChatPaLM(Evaluator):

    def __init__(self, conf=None, formatron='Str'):
        Evaluator.__init__(self, conf=conf, formatron=formatron)

    def prompt_texts_combiner(self, prompt, texts, **args):

        # Default role
        role = 'user'
        if 'role' in args.keys():
            role = args['role']

        # Make texts
        textsLocal = None
        if isinstance(texts, str):
            textsLocal = texts
        elif isinstance(texts, list):
            textsLocal = self.conf.to_dict()['prompt_delimiter'].join(texts)

        if not isinstance(textsLocal, str):
            TypeError("Cannot convert texts argument to a single strings.")

        # Make PaLM message object
        message = discuss_types.MessageDict(author=role, content=textsLocal, citation_metadata=None)

        # Result
        return message


    # The eval implementation follows the description and examples in:
    # https://developers.generativeai.google/tutorials/chat_quickstart
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
        messages = self.prompt_texts_combiner(prompt='', texts=texts)

        if echo:
            print(f'Messages: {messages}')

        # Remove (last) LLM result
        self.llm_result = None

        # Invoke the LLM function
        knownParamsLocal = self.conf.known_params + ['context', 'messages']
        args2 = dict(filter(lambda x: x[0] in knownParamsLocal, args2.items()))

        res = palm.chat(
            context=fullPrompt,
            messages=messages,
            **args2
        )

        if echo:
            print(f'LLM result: {res}')

        # Same LLM result
        self.llm_result = res

        # Get result attribute
        res = res.to_dict()["messages"][len(res.messages)-1]["content"]

        # Process the result
        return self.post_process(res, form=args.get('form', None))
