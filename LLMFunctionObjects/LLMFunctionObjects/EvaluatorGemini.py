import importlib
import os
import warnings

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


def _import_google_genai():
    try:
        return importlib.import_module("google.genai")
    except ImportError:
        return None


def _import_google_generativeai():
    try:
        return importlib.import_module("google.generativeai")
    except ImportError:
        return None


def _gemini_config_from_args(args2, system_instruction=None, tools=None, tool_config=None):
    config = {}
    generation_config = args2.get("generation_config", None)
    if isinstance(generation_config, dict):
        config.update(generation_config)

    if args2.get("temperature", None) is not None:
        config["temperature"] = args2.get("temperature")
    if args2.get("max_tokens", None) is not None and "max_output_tokens" not in config:
        config["max_output_tokens"] = args2.get("max_tokens")
    if args2.get("stop_tokens", None) and "stop_sequences" not in config:
        config["stop_sequences"] = args2.get("stop_tokens")
    if args2.get("safety_settings", None) is not None:
        config["safety_settings"] = args2.get("safety_settings")
    if system_instruction:
        config["system_instruction"] = system_instruction
    if tools is not None:
        config["tools"] = tools
    if tool_config is not None:
        config["tool_config"] = tool_config

    return config if len(config) > 0 else None


def _resolve_gemini_key(args2):
    return args2.get("api_key", None) or os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY"))


def _generate_with_google_genai(model_name, contents, args2, system_instruction=None, tools=None, tool_config=None):
    google_genai = _import_google_genai()
    if google_genai is None:
        return None, None

    api_key = _resolve_gemini_key(args2)
    client = google_genai.Client(api_key=api_key)
    config = _gemini_config_from_args(args2, system_instruction=system_instruction, tools=tools, tool_config=tool_config)

    if args2.get("stream", False):
        chunks = client.models.generate_content_stream(model=model_name, contents=contents, config=config)
        text_chunks = []
        last_chunk = None
        for chunk in chunks:
            last_chunk = chunk
            chunk_text = _extract_gemini_text(chunk)
            if isinstance(chunk_text, str):
                text_chunks.append(chunk_text)
        return last_chunk, "".join(text_chunks)

    res = client.models.generate_content(model=model_name, contents=contents, config=config)
    return res, _extract_gemini_text(res)


def _generate_with_google_generativeai(model_name, contents, args2, system_instruction=None, tools=None, tool_config=None):
    genai = _import_google_generativeai()
    if genai is None:
        raise ImportError(
            "Neither 'google.genai' nor 'google.generativeai' is available. "
            "Install 'google-genai' to use Gemini."
        )

    warnings.warn(
        "Using deprecated 'google.generativeai'. Install 'google-genai' to use the supported Gemini SDK.",
        DeprecationWarning,
        stacklevel=2,
    )

    api_key = _resolve_gemini_key(args2)
    if api_key is not None:
        genai.configure(api_key=api_key)

    model_init_args = {}
    if system_instruction:
        model_init_args["system_instruction"] = system_instruction
    if tools is not None:
        model_init_args["tools"] = tools
    if tool_config is not None:
        model_init_args["tool_config"] = tool_config

    try:
        model = genai.GenerativeModel(model_name, **model_init_args)
    except TypeError:
        model = genai.GenerativeModel(model_name)
        if system_instruction and isinstance(contents, str):
            contents = f"{system_instruction}\n\n{contents}"

    model_args = {
        "generation_config": args2.get("generation_config", None),
        "safety_settings": args2.get("safety_settings", None),
        "tools": None,
        "tool_config": None,
        "stream": args2.get("stream", None),
        "request_options": args2.get("request_options", None),
    }
    model_args = {k: v for k, v in model_args.items() if v is not None}
    res = model.generate_content(contents, **model_args)
    return res, _extract_gemini_text(res)


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
        tools = args2.get("tools", None)
        tool_config = args2.get("tool_config", None)

        # Invoke Gemini
        self.llm_result = None
        res, text = _generate_with_google_genai(
            model_name=model_name,
            contents=prompt,
            args2=args2,
            system_instruction=system_instruction,
            tools=tools,
            tool_config=tool_config,
        )
        if res is None:
            res, text = _generate_with_google_generativeai(
                model_name=model_name,
                contents=prompt,
                args2=args2,
                system_instruction=system_instruction,
                tools=tools,
                tool_config=tool_config,
            )
        self.llm_result = res

        if echo:
            print(f"LLM result: {res}")

        return self.post_process(text, form=args.get("form", None))
