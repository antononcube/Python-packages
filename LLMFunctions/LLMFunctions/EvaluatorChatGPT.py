from LLMFunctions.EvaluatorChat import EvaluatorChat


class EvaluatorChatGPT(EvaluatorChat):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def prompt_texts_combiner(self, prompt, texts, **kwargs):
        messages = super().prompt_texts_combiner(prompt, texts, **kwargs)

        # At this point the messages are key-value pairs.
        # We convert them into records expected by OpenAI.
        # See https://platform.openai.com/docs/api-reference/chat/create?lang=python
        res_messages = []

        for d in messages:
            for k, v in d.items():
                res_messages.append({"role": k, "content": v})

        return res_messages

    def prompt_texts_combiner_first(self, prompt, texts, **args):
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
