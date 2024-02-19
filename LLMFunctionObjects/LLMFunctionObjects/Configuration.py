import pickle
from copy import deepcopy
from typing import List, Callable, Union, Dict


class Configuration:
    def __init__(self,
                 name: str,
                 api_key: Union[str, None] = None,
                 api_user_id: Union[str, None] = None,
                 module: str = '',
                 model: str = '',
                 function: Union[Callable, None] = None,
                 temperature: float = 0,
                 total_probability_cutoff: float = 0,
                 max_tokens: int = 64,
                 fmt: Union[str, None] = None,
                 prompts=None,
                 prompt_delimiter: str = ' ',
                 stop_tokens: Union[list, None] = None,
                 tools=None,
                 tool_prompt: str = '',
                 tool_request_parser: Union[Callable, None] = None,
                 tool_response_insertion_function: Union[Callable, None] = None,
                 argument_renames=None,
                 evaluator: Union = None,
                 known_params: Union[list, None] = None,
                 response_object_attribute: Union[str, None] = None,
                 response_value_keys: Union[list, None] = None,
                 llm_evaluator=None
                 ):
        if argument_renames is None:
            argument_renames = {}
        if known_params is None:
            known_params = []
        if tools is None:
            tools = []
        if prompts is None:
            prompts = []
        # if stop_tokens is None:
        #    stop_tokens = ['.', '?', '!']
        self.name = name
        self.api_key = api_key
        self.api_user_id = api_user_id
        self.module = module
        self.model = model
        self.function = function
        self.temperature = temperature
        self.total_probability_cutoff = total_probability_cutoff
        self.max_tokens = max_tokens
        self.fmt = fmt

        self.prompts = []
        if isinstance(prompts, list):
            self.prompts = prompts.copy()
        elif isinstance(prompts, str):
            self.prompts = [prompts, ]
        elif prompts is not None:
            TypeError("The argument prompts is expected to be a string, a list of strings, or None.")

        self.prompt_delimiter = prompt_delimiter

        self.stop_tokens = None
        if isinstance(stop_tokens, list):
            self.stop_tokens = stop_tokens.copy()
        elif isinstance(stop_tokens, str):
            self.stop_tokens = [stop_tokens, ]
        elif stop_tokens is not None:
            TypeError("The argument stop_tokens is expected to be a string, a list of strings, or None.")

        self.tools = None
        if isinstance(tools, list):
            self.tools = tools.copy()
        elif tools is not None:
            TypeError("The argument tools is expected to a list or None.")

        self.tool_prompt = tool_prompt
        self.tool_request_parser = tool_request_parser
        self.tool_response_insertion_function = tool_response_insertion_function

        argument_renames = {}
        if isinstance(argument_renames, dict):
            self.argument_renames = argument_renames.copy()
        elif argument_renames is None:
            self.argument_renames = {}
        else:
            TypeError("The argument argument_renames is expected to a dictionary or None.")

        self.evaluator = evaluator
        self.known_params = known_params

        self.response_object_attribute = None
        if isinstance(response_object_attribute, str):
            self.response_object_attribute = response_object_attribute
        elif response_object_attribute is not None:
            TypeError("The argument response_object_attribute is expected to a string or None.")

        self.response_value_keys = None
        if isinstance(response_value_keys, list):
            self.response_value_keys = response_value_keys.copy()
        elif response_value_keys is not None:
            TypeError("The argument response_value_keys is expected to a list or None.")

        self.llm_evaluator = llm_evaluator

    # ------------------------------------------------------------------
    # Copying
    # ------------------------------------------------------------------
    def copy(self):
        """Deep copy."""
        newObj = type(self)(
            name=self.name,
            api_key=self.api_key,
            api_user_id=self.api_user_id,
            module=self.module,
            model=self.model,
            function=self.function,
            temperature=self.temperature,
            total_probability_cutoff=self.total_probability_cutoff,
            max_tokens=self.max_tokens,
            fmt=self.fmt,
            prompts=self.prompts,
            prompt_delimiter=self.prompt_delimiter,
            stop_tokens=self.stop_tokens,
            tools=self.tools,
            tool_prompt=self.tool_prompt,
            tool_request_parser=self.tool_request_parser,
            tool_response_insertion_function=self.tool_response_insertion_function,
            argument_renames=self.argument_renames,
            evaluator=self.evaluator,
            known_params=self.known_params,
            response_object_attribute=self.response_object_attribute,
            response_value_keys=self.response_value_keys,
            llm_evaluator=self.llm_evaluator
        )

        return newObj

    def __copy__(self):
        """Deep copy."""
        return self.copy()

    def __deepcopy__(self, **kwargs):
        """Deep copy."""
        return self.copy()

    def combine(self, conf):
        if isinstance(conf, Configuration):
            return self.combine(conf.to_dict())
        elif isinstance(conf, dict):
            # newArgs = self.to_dict() | conf
            newArgs = {**self.to_dict(), **conf}
            return Configuration(**newArgs)
        else:
            TypeError("The first argument is expected to a Configuration object or a dictionary")

    # ------------------------------------------------------------------
    # Representations
    # ------------------------------------------------------------------
    def to_dict(self):
        return {
            'name': self.name,
            'api_key': self.api_key,
            'api_user_id': self.api_user_id,
            'module': self.module,
            'model': self.model,
            'function': self.function,
            'temperature': self.temperature,
            'total_probability_cutoff': self.total_probability_cutoff,
            'max_tokens': self.max_tokens,
            'fmt': self.fmt,
            'prompts': self.prompts,
            'prompt_delimiter': self.prompt_delimiter,
            'stop_tokens': self.stop_tokens,
            'tools': self.tools,
            'tool_prompt': self.tool_prompt,
            'tool_request_parser': self.tool_request_parser,
            'tool_response_insertion_function': self.tool_response_insertion_function,
            'argument_renames': self.argument_renames,
            'evaluator': self.evaluator,
            'known_params': self.known_params,
            'response_object_attribute': self.response_object_attribute,
            'response_value_keys': self.response_value_keys,
            'llm_evaluator': self.llm_evaluator
        }

    def __str__(self):
        return self.repr()

    def repr(self):
        return repr(self.to_dict())
