from typing import List, Callable, Union, Dict

from LLMFunctionObjects.Evaluator import Evaluator
from LLMFunctionObjects.Configuration import Configuration


class EvaluatorChat(Evaluator):
    context: Union[str, None] = None
    examples: Union[str, None] = None
    user_role: str = 'user'
    assistant_role: str = 'assistant'
    system_role: str = 'system'

    def __init__(self,
                 conf=None,
                 formatron='Str',
                 context=None,
                 examples=None,
                 user_role='user',
                 assistant_role='assistant',
                 system_role='system'):
        super().__init__(conf, formatron)
        self.context = context
        self.examples = examples
        self.user_role = user_role
        self.assistant_role = assistant_role
        self.system_role = system_role

        if (isinstance(self.conf, Configuration) and
                len(self.conf.prompts) > 0 and
                all(isinstance(prompt, str) for prompt in self.conf.prompts)):
            context_local = self.conf.prompt_delimiter.join(self.conf.prompts)
            self.context = context_local
            self.conf.prompts = []

    def combine_role_messages(self, messages):
        # Ensure that all elements of messages are pairs (i.e., key-value pairs)
        if not all(isinstance(message, dict) for message in messages):
            raise ValueError("All messages should be key-value pairs")

        # Initialize resMessages with the first message
        res_messages = [messages[0]]

        # Iterate through the remaining messages
        for message in messages[1:]:
            if list(message.keys())[0] == list(res_messages[-1].keys())[0]:
                last_message = res_messages.pop()
                combined_value = self.conf.prompt_delimiter.join(
                    [list(last_message.values())[0], list(message.values())[0]])
                res_messages.append({list(message.keys())[0]: combined_value})
            else:
                res_messages.append(message)

        return res_messages

    def process_examples(self, messages, **kwargs):
        examples_local = kwargs.get('examples', self.examples)

        # Check if examples_local is not an instance of the 'Whatever' class
        # This 'Whatever' class doesn't have an exact equivalent in Python.
        # So, I am assuming that you'd either define it or we need to modify this check accordingly.
        if examples_local is not None:
            # Check if examples_local is a list of single key-value pair dictionaries
            if not (isinstance(examples_local, list) and all(
                    isinstance(ex, dict) and len(ex) == 1 for ex in examples_local)):
                raise ValueError(
                    "When examples spec is provided it is expected to be a list of single key-value pair dictionaries.")

            examples_local = "\n".join(
                [f"Input: {list(ex.keys())[0]} \n Output: {list(ex.values())[0]} \n" for ex in examples_local])

            # Assuming `prepend` adds the string at the beginning of the list
            messages.insert(0, examples_local)

        return messages

    def prompt_texts_combiner(self, prompt, texts, **kwargs):
        # Handle different cases of texts
        if all(isinstance(text, str) for text in texts):
            messages = [{self.user_role: text} for text in texts]
        elif all(isinstance(text, dict) and len(text) == 1 for text in texts):
            messages = texts
        elif all(isinstance(text, dict) for text in texts):
            messages = [{text['role']: text['content']} for text in texts]
        else:
            raise ValueError('Unknown form of the second argument (texts).')

        # Filter out messages with key 'examples'
        messages = [msg for msg in messages if list(msg.keys())[0] != 'examples']

        # Add prompt
        if prompt:
            messages.insert(0, {self.user_role: prompt})

        # Combine role messages (assuming you've implemented this method as per previous conversion)
        messages = self.combine_role_messages(messages)

        # Process context
        context_local = messages[0].get('context', kwargs.get('context', self.context))

        if context_local is not None:
            if not isinstance(context_local, str):
                raise ValueError("When context spec is provided it is expected to be string.")
            messages.insert(0, {self.system_role: context_local})

        # Process examples (assuming you've implemented this method as per previous conversion)
        messages = self.process_examples(messages, **kwargs)

        # Result
        return messages

    # ------------------------------------------------------------------
    # Representations
    # ------------------------------------------------------------------
    def to_dict(self):
        res = super().to_dict()
        res["context"] = self.context
        res["examples"] = self.examples
        res["context"] = self.context
        res["user_role"] = self.user_role
        res["assistant_role"] = self.assistant_role
        res["system_role"] = self.system_role
        return res

    def __repr__(self):
        return repr(self.to_dict())
