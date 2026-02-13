import ollama

from LLMFunctionObjects.EvaluatorChat import EvaluatorChat
from LLMFunctionObjects.EvaluatorOllama import _extract_ollama_text


class EvaluatorChatOllama(EvaluatorChat):
    def _to_ollama_messages(self, messages):
        res_messages = []
        for d in messages:
            for k, v in d.items():
                res_messages.append({"role": k, "content": v})
        return res_messages

    def eval(self, texts, **args):
        confDict = self.conf.to_dict()

        echo = args.get("echo", False)
        if echo:
            print(f"Configuration: {self.conf}")

        args2 = {**self.conf.to_dict(), **args}

        # Handle argument renames
        for k, v in confDict["argument_renames"].items():
            args2[v] = args2.get(v, args2.get(k, None))

        # Build context
        delim = confDict["prompt_delimiter"] or "\n"
        context = self.context or ""
        fullPrompt = delim.join(confDict["prompts"])
        if fullPrompt and context:
            context = delim.join([fullPrompt, context])
        elif fullPrompt:
            context = fullPrompt

        # Form messages
        messages = self.prompt_texts_combiner(prompt="", texts=texts, context=context)
        res_messages = self._to_ollama_messages(messages)

        if echo:
            print(f"Messages: {res_messages}")

        model_name = args2.get("model", self.conf.model)

        known_params = set(self.conf.known_params or [])
        args3 = {k: v for k, v in args2.items() if k in known_params}
        args3["model"] = model_name
        args3["messages"] = res_messages

        self.llm_result = None
        res = ollama.chat(**args3)
        self.llm_result = res

        if echo:
            print(f"LLM result: {res}")

        return self.post_process(_extract_ollama_text(res), form=args.get("form", None))
