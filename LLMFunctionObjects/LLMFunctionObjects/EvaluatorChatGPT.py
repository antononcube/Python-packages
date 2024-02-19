from LLMFunctionObjects.EvaluatorChat import EvaluatorChat


class EvaluatorChatGPT(EvaluatorChat):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def result_values(self, res):
        resLocal = res.choices[0].message.content
        return resLocal
