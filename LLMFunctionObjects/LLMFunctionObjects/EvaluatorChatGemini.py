import google.generativeai as genai

from LLMFunctionObjects.EvaluatorChat import EvaluatorChat
from LLMFunctionObjects.EvaluatorGemini import _extract_gemini_text


class EvaluatorChatGemini(EvaluatorChat):
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

        if echo:
            print(f"Context: {context}")

        # Form messages
        messages = self.prompt_texts_combiner(prompt="", texts=texts, context=context)

        if echo:
            print(f"Messages: {messages}")

        # Extract system instruction if present
        system_instruction = None
        if messages and list(messages[0].keys())[0] == self.system_role:
            system_instruction = list(messages[0].values())[0]
            messages = messages[1:]

        # Map roles to Gemini format
        res_messages = []
        for d in messages:
            role, content = list(d.items())[0]
            if role == self.assistant_role:
                role = "model"
            elif role == self.user_role:
                role = "user"
            res_messages.append({"role": role, "parts": [content]})

        model_name = args2.get("model", self.conf.model)
        tools = args2.get("tools", None)
        tool_config = args2.get("tool_config", None)
        model_init_args = {}
        if system_instruction:
            model_init_args["system_instruction"] = system_instruction
        if tools is not None:
            model_init_args["tools"] = tools
        if tool_config is not None:
            model_init_args["tool_config"] = tool_config

        model = genai.GenerativeModel(model_name, **model_init_args)

        model_args = {
            "generation_config": args2.get("generation_config", None),
            "safety_settings": args2.get("safety_settings", None),
            "tools": None,
            "tool_config": None,
            "stream": args2.get("stream", None),
            "request_options": args2.get("request_options", None),
        }
        model_args = {k: v for k, v in model_args.items() if v is not None}

        self.llm_result = None
        res = model.generate_content(res_messages, **model_args)
        self.llm_result = res

        if echo:
            print(f"LLM result: {res}")

        return self.post_process(_extract_gemini_text(res), form=args.get("form", None))
