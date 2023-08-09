import warnings

from LLMFunctions.Configuration import Configuration
from LLMFunctions.Evaluator import Evaluator
from LLMFunctions.Functor import Functor
import openai
import warnings


def llm_configuration(spec):
    if spec is None:
        return llm_configuration('openai')
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
            argument_renames={"stop_tokens": "stop"},
            fmt='values',
            known_params=["api_keu", "model", "prompt", "suffix", "max_tokens", "temperature", "top_p", "n", "stream",
                          "logprobs", "echo", "stop", "presence_penalty", "frequency_penalty", "best_of", "logit_bias",
                          "user"],
            response_value_keys=["choices", 0, "text"])
        return confOpenAI
    elif isinstance(spec, str) and spec.lower() == 'chatgpt':
        confChatGPT = Configuration(
            name="chatgpt",
            api_key=None,
            api_user_id='user',
            module='openai',
            model='gpt-3.5-turbo-16k-0613',
            function=openai.ChatCompletion.create,
            temperature=0.2,
            max_tokens=300,
            total_probability_cutoff=0.03,
            prompts=None,
            prompt_delimiter=' ',
            argument_renames={"stop_tokens": "stop"},
            fmt='values',
            known_params=["api_keu", "model", "messages", "functions", "function_call", "temperature", "top_p", "n",
                          "stream", "logprobs", "echo", "stop", "presence_penalty", "frequency_penalty", "logit_bias",
                          "user"],
            response_value_keys=["choices", 0, "text"]
        )
        return confChatGPT
    else:
        warnings.warn("Do not know what to do with given configuration spec.")
        return llm_configuration('openai')
    pass


def llm_evaluator(spec, frm=None):
    if spec is None:
        return Evaluator(llm_configuration(None), frm)
    elif isinstance(spec, str):
        return Evaluator(spec, frm)
    else:
        warnings.warn("Do not know what to do with given configuration spec.")
        return llm_evaluator(None, frm)
    pass


def llm_function(prompt, frm=None, e=None):
    llmEvaluator = llm_evaluator(e, frm)
    print(llmEvaluator)
    llmEvaluator.conf.prompts.append(prompt)
    print("llmEvaluator.conf.prompts: ", llmEvaluator.conf.prompts)
    # return lambda text, **kwargs: llmEvaluator.eval(text, **kwargs)
    return Functor(llmEvaluator, prompt)


def llm_example_evaluator(prompt):
    pass
