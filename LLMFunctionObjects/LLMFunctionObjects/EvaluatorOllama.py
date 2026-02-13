import ollama

from LLMFunctionObjects.Evaluator import Evaluator


def _extract_ollama_text(res):
    if isinstance(res, dict):
        if "response" in res:
            return res["response"]
        if "message" in res and isinstance(res["message"], dict):
            return res["message"].get("content", res)
    if hasattr(res, "response"):
        return res.response
    return res


class EvaluatorOllama(Evaluator):
    def eval(self, texts, **args):
        confDict = self.conf.to_dict()

        echo = args.get("echo", False)
        if echo:
            print(f"Configuration: {self.conf}")

        args2 = {**self.conf.to_dict(), **args}

        # Handle argument renames
        for k, v in confDict["argument_renames"].items():
            args2[v] = args2.get(v, args2.get(k, None))

        fullPrompt = confDict["prompt_delimiter"].join(confDict["prompts"])
        prompt = self.prompt_texts_combiner(fullPrompt, texts)

        if echo:
            print(f"Prompt: {prompt}")

        model_name = args2.get("model", self.conf.model)

        known_params = set(self.conf.known_params or [])
        args3 = {k: v for k, v in args2.items() if k in known_params}
        args3["model"] = model_name
        args3["prompt"] = prompt

        self.llm_result = None
        res = ollama.generate(**args3)
        self.llm_result = res

        if echo:
            print(f"LLM result: {res}")

        return self.post_process(_extract_ollama_text(res), form=args.get("form", None))
