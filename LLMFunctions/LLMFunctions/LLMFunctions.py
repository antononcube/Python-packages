import warnings
import os
from LLMFunctions.Configuration import Configuration
from LLMFunctions.Evaluator import Evaluator
from LLMFunctions.Functor import Functor
import openai
import google.generativeai
import warnings


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
                          "logprobs", "echo", "stop", "presence_penalty", "frequency_penalty", "best_of", "logit_bias",
                          "user"],
            response_value_keys=["choices", 0, "text"])
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
                                                      "stream", "logprobs", "echo", "stop", "presence_penalty",
                                                      "frequency_penalty", "logit_bias",
                                                      "user"],
                                        response_value_keys=["choices", 0, "text"])
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
            response_object_attribute = "result",
            response_value_keys=[])

        # Modify by additional arguments
        if len(kwargs) > 0:
            confPaLM = confPaLM.combine(kwargs)

        # Result
        return confPaLM

    elif isinstance(spec, str) and spec.lower() == 'ChatPaLM'.lower():
        confChatPaLM = llm_configuration("PaLM")
        if len(kwargs) > 0:
            confChatPaLM = confChatPaLM.combine(kwargs)
        return confChatPaLM
    else:
        warnings.warn("Do not know what to do with given configuration spec.")
        return llm_configuration('OpenAI', **kwargs)
    pass


def llm_evaluator(spec, form=None):
    if spec is None:
        return Evaluator(conf=llm_configuration(None), formatron=form)
    elif isinstance(spec, str):
        return Evaluator(conf=llm_configuration(spec), formatron=form)
    elif isinstance(spec, Configuration):
        return Evaluator(conf=spec, formatron=form)
    else:
        warnings.warn("Do not know what to do with the given configuration spec.")
        return llm_evaluator(None, form)
    pass


def llm_function(prompt, form=None, e=None):
    llmEvaluator = llm_evaluator(spec=e, form=form)
    return Functor(llmEvaluator, prompt)


def llm_example_function(rules, form=None, e=None):
    if isinstance(rules, dict):
        pre = ""
        for (k, v) in rules.items():
            pre = f'Input: {k}\nOutput: {v}\n\n'

        prompt = lambda x: pre + f"\nInput {x}\nOutput:"

        return llm_function(prompt, form=form, e=e)

    else:
        TypeError("The first argument is expected to be a dictionary.")
