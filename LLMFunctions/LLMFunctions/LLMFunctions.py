import warnings
import os
from LLMFunctions.Configuration import Configuration
from LLMFunctions.Evaluator import Evaluator
from LLMFunctions.EvaluatorChatPaLM import EvaluatorChatPaLM
from LLMFunctions.Functor import Functor
from LLMFunctions.Chat import Chat
import openai
import google.generativeai
import warnings


# ===========================================================
# Configuration creation
# ===========================================================
def llm_configuration(spec, **kwargs):
    if spec is None:
        return llm_configuration('openai', **kwargs)
    elif isinstance(spec, Configuration):
        return spec.combine(kwargs)
    elif isinstance(spec, str) and spec.lower() == 'openai':
        confOpenAI = Configuration(
            name="openai",
            api_key=None,
            api_user_id='user',
            module='openai',
            model='text-davinci-003',  # 'gpt-3.5-turbo-instruct',
            function=openai.Completion.create,
            temperature=0.2,
            max_tokens=300,
            total_probability_cutoff=0.03,
            prompts=None,
            prompt_delimiter=' ',
            stop_tokens=None,
            argument_renames={"stop_tokens": "stop"},
            fmt='values',
            known_params=["api_key", "model", "prompt", "suffix", "max_tokens", "temperature", "top_p", "n", "stream",
                          "logprobs", "stop", "presence_penalty", "frequency_penalty", "best_of", "logit_bias",
                          "user"],
            response_value_keys=["choices", 0, "text"],
            llm_evaluator=Evaluator)
        if len(kwargs) > 0:
            confOpenAI = confOpenAI.combine(kwargs)
        return confOpenAI
    elif isinstance(spec, str) and spec.lower() == 'chatgpt':
        confChatGPT = llm_configuration("openai",
                                        name="chatgpt",
                                        module='openai',
                                        model='gpt-3.5-turbo-0613',
                                        function=openai.ChatCompletion.create,
                                        known_params=["api_key", "model", "messages", "functions", "function_call",
                                                      "temperature", "top_p", "n",
                                                      "stream", "logprobs", "stop", "presence_penalty",
                                                      "frequency_penalty", "logit_bias",
                                                      "user"],
                                        response_value_keys=["choices", 0, "message"])
        if len(kwargs) > 0:
            confChatGPT = confChatGPT.combine(kwargs)
        return confChatGPT
    elif isinstance(spec, str) and spec.lower() == 'PaLM'.lower():

        # Set key
        apiKey = os.environ.get("PALM_API_KEY")
        google.generativeai.configure(api_key=apiKey)

        # Configuration
        confPaLM = Configuration(
            name="palm",
            api_key=None,
            api_user_id="user",
            module="google.generativeai",
            model="models/text-bison-001",
            function=google.generativeai.generate_text,
            temperature=0.2,
            max_tokens=300,
            total_probability_cutoff=0.03,
            prompts=None,
            prompt_delimiter=" ",
            stop_tokens=None,
            argument_renames={"max_tokens": "max_output_tokens",
                              "stop_tokens": "stop_sequences"},
            fmt="values",
            known_params=[
                "model", "prompt", "temperature", "candidate_count", "max_output_tokens", "top_p", "top_k",
                "safety_settings", "stop_sequences", "client"
            ],
            response_object_attribute="result",
            response_value_keys=[],
            llm_evaluator=Evaluator)

        # Modify by additional arguments
        if len(kwargs) > 0:
            confPaLM = confPaLM.combine(kwargs)

        # Result
        return confPaLM

    elif isinstance(spec, str) and spec.lower() == 'ChatPaLM'.lower():

        # Start as PaLM text completion configuration
        confChatPaLM = llm_configuration("PaLM")

        # Default PaLM chat model
        confChatPaLM.model = 'models/chat-bison-001'

        # The parameters are taken from here:
        #   https://github.com/google/generative-ai-python/blob/f370f5ab908a095282a0cdd946385db23c695498/google/generativeai/discuss.py#L210
        # and used in EvaluatorChatPaLM.eval
        confChatPaLM.known_params = [
            "model", "context", "examples", "temperature", "candidate_count", "top_p", "top_k", "prompt"
        ]

        # Adding it this for consistency
        confChatPaLM.response_value_keys = ["messages", -1, "content"]

        # Evaluator class
        confChatPaLM.llm_evaluator = EvaluatorChatPaLM

        # Combine with given additional parameters (if any)
        if len(kwargs) > 0:
            confChatPaLM = confChatPaLM.combine(kwargs)

        return confChatPaLM
    else:
        warnings.warn("Do not know what to do with given configuration spec.")
        return llm_configuration('OpenAI', **kwargs)
    pass


# ===========================================================
# Evaluator creation
# ===========================================================
def llm_evaluator(spec, form=None):
    if spec is None:
        return Evaluator(conf=llm_configuration(None), formatron=form)
    elif isinstance(spec, str):
        return Evaluator(conf=llm_configuration(spec), formatron=form)
    elif isinstance(spec, Configuration):
        evaluatorClass = Evaluator
        if spec.llm_evaluator is not None:
            evaluatorClass = spec.llm_evaluator
        return evaluatorClass(conf=spec, formatron=form)
    else:
        warnings.warn("Do not know what to do with the given configuration spec.")
        return llm_evaluator(None, form)
    pass


# ===========================================================
# Function creation
# ===========================================================
def llm_function(prompt, form=None, e=None):
    llmEvaluator = llm_evaluator(spec=e, form=form)
    return Functor(llmEvaluator, prompt)


# ===========================================================
# Example function creation
# ===========================================================

def llm_example_function(rules, form=None, e=None):
    if isinstance(rules, dict):
        pre = ""
        for (k, v) in rules.items():
            pre = f'Input: {k}\nOutput: {v}\n\n'

        prompt = lambda x: pre + f"\nInput {x}\nOutput:"

        return llm_function(prompt, form=form, e=e)

    else:
        TypeError("The first argument is expected to be a dictionary.")


# ===========================================================
# Chat object creation
# ===========================================================

def llm_chat(prompt, chat_id="", e=None):
    llmEvaluator = llm_evaluator(spec=e)
    return Chat(prompt=prompt, chat_id=chat_id, llm_evaluator=llmEvaluator)
