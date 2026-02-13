import warnings

from LLMFunctionObjects.EvaluatorChatGemini import EvaluatorChatGemini


class EvaluatorChatPaLM(EvaluatorChatGemini):
    def __init__(self, **kwargs):
        warnings.warn(
            "PaLM is deprecated and has been replaced with Gemini. "
            "Use EvaluatorChatGemini or llm_configuration('ChatGemini').",
            DeprecationWarning,
        )
        super().__init__(**kwargs)
