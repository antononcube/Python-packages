import google.generativeai as genai

from LLMFunctionObjects.Evaluator import Evaluator


def _extract_gemini_text(res):
    if hasattr(res, "text") and res.text is not None:
        return res.text
    if isinstance(res, dict):
        if "text" in res and res["text"] is not None:
            return res["text"]
    if hasattr(res, "candidates") and res.candidates:
        cand = res.candidates[0]
        if hasattr(cand, "content") and hasattr(cand.content, "parts"):
            parts = cand.content.parts
            if parts:
                if isinstance(parts[0], str):
                    return "".join(parts)
                if hasattr(parts[0], "text"):
                    return "".join([p.text for p in parts if hasattr(p, "text")])
    return res


class EvaluatorGemini(Evaluator):
    def eval(self, texts, **args):
        confDict = self.conf.to_dict()

        echo = args.get("echo", False)
        if echo:
            print(f"Configuration: {self.conf}")

        args2 = {**self.conf.to_dict(), **args}

        # Handle argument renames
        for k, v in confDict["argument_renames"].items():
            args2[v] = args2.get(v, args2.get(k, None))

        # Build prompt
        fullPrompt = confDict["prompt_delimiter"].join(confDict["prompts"])
        prompt = self.prompt_texts_combiner(fullPrompt, texts)

        if echo:
            print(f"Prompt: {prompt}")

        # Configure model
        model_name = args2.get("model", self.conf.model)
        system_instruction = args2.get("system_instruction", None)
        if system_instruction:
            model = genai.GenerativeModel(model_name, system_instruction=system_instruction)
        else:
            model = genai.GenerativeModel(model_name)

        model_args = {
            "generation_config": args2.get("generation_config", None),
            "safety_settings": args2.get("safety_settings", None),
            "tools": args2.get("tools", None),
            "tool_config": args2.get("tool_config", None),
            "stream": args2.get("stream", None),
            "request_options": args2.get("request_options", None),
        }
        model_args = {k: v for k, v in model_args.items() if v is not None}

        # Invoke Gemini
        self.llm_result = None
        res = model.generate_content(prompt, **model_args)
        self.llm_result = res

        if echo:
            print(f"LLM result: {res}")

        return self.post_process(_extract_gemini_text(res), form=args.get("form", None))
