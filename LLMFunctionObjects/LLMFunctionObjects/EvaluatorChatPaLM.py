from LLMFunctionObjects.EvaluatorChat import EvaluatorChat
import google.generativeai as palm
from google.generativeai.types import discuss_types


def is_all_pairs(a):
    """Checks if all elements of an array are pairs."""
    for i in range(len(a) - 1):
        if not (a[i] % 2 == 0 and a[i + 1] % 2 == 0):
            return False
    return True


class EvaluatorChatPaLM(EvaluatorChat):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Process context
        self.user_role = kwargs.get('user_role', 'user')
        self.assistant_role = kwargs.get('assistant_role', 'assistant')
        self.system_role = kwargs.get('system_role', 'context')

    def prompt_texts_combiner(self, prompt, texts, **kwargs):

        messages = super().prompt_texts_combiner(prompt, texts, **kwargs)

        res_messages = []

        for d in messages:
            for k, v in d.items():
                # Make PaLM message object
                if k != self.system_role:
                    m = discuss_types.MessageDict(author=k, content=v, citation_metadata=None)
                    res_messages.append(m)

        # Result
        return res_messages


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

        # Just in case make None object into strings
        delim = confDict['prompt_delimiter']
        if delim is None:
            delim = "\n"

        context = self.context
        if context is None:
            context = ""

        # Make the full prompt
        fullPrompt = delim.join(confDict['prompts'])
        fullPrompt = delim.join([fullPrompt, context])

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
