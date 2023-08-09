import pickle
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
                 stop_tokens: Union[list, None]=None,
                 tools=None,
                 tool_prompt: str = '',
                 tool_request_parser: Union[Callable, None] = None,
                 tool_response_insertion_function: Union[Callable, None] = None,
                 argument_renames=None,
                 evaluator: Union = None,
                 known_params: Union[list, None] = None,
                 response_value_keys: Union[list, None] = None):
        if argument_renames is None:
            argument_renames = {}
        if known_params is None:
            known_params = []
        if tools is None:
            tools = []
        if prompts is None:
            prompts = []
        #if stop_tokens is None:
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
        self.prompts = prompts.copy()
        self.prompt_delimiter = prompt_delimiter
        if isinstance(stop_tokens, list):
            self.stop_tokens = stop_tokens.copy()
        else:
            self.stop_tokens = stop_tokens
        self.tools = tools.copy()
        self.tool_prompt = tool_prompt
        self.tool_request_parser = tool_request_parser
        self.tool_response_insertion_function = tool_response_insertion_function
        self.argument_renames = argument_renames.copy()
        self.evaluator = evaluator
        self.known_params = known_params
        self.response_value_keys = response_value_keys

    # ------------------------------------------------------------------
    # Copying
    # ------------------------------------------------------------------
    def copy(self):
        """Deep copy."""
        return pickle.loads(pickle.dumps(self, -1))

    def __copy__(self):
        """Deep copy."""
        return pickle.loads(pickle.dumps(self, -1))

    def __deepcopy__(self, memodict={}):
        """Deep copy."""
        return pickle.loads(pickle.dumps(self, -1))

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
            'known_params': self.known_params
        }

    def __str__(self):
        return self.repr()

    def repr(self):
        return repr(self.to_dict())
