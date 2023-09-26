import logging
import time
from typing import List, Callable, Union, Dict
import inspect
from LLMFunctionObjects.EvaluatorChat import EvaluatorChat


class Chat:
    chat_id: str = ''
    llm_evaluator: EvaluatorChat
    messages: list = []
    examples: list = []
    lmm_result = None

    # ------------------------------------------------------
    def __init__(self, chat_id=None, llm_evaluator=None, messages=None, examples=None):
        if chat_id is None:
            self.chat_id = ''
        else:
            self.chat_id = chat_id
        if examples is None:
            examples = []
        if messages is None:
            messages = []
        self.llm_evaluator = llm_evaluator
        self.messages = messages
        self.examples = examples

    # ------------------------------------------------------
    def prompt(self):
        promptLocal = self.llm_evaluator.conf.prompts

        if len(promptLocal) == 0:
            promptLocal = self.llm_evaluator.context

        if isinstance(promptLocal, list):
            promptLocal = self.llm_evaluator.conf.prompt_delimiter.join(promptLocal)
        return promptLocal

    # ------------------------------------------------------
    def make_message(self,
                     role: Union[str, None] = None,
                     message: str = '',
                     timestamp=None):
        roleLocal = role
        if roleLocal is None:
            roleLocal = 'user'
        timestampLocal = timestamp
        if timestampLocal is None:
            timestampLocal = time.time()
        return {"role": roleLocal, "content": message, "timestamp": timestampLocal}

    # ------------------------------------------------------
    import logging

    def eval(self, message, role=None, **args):
        """Evaluates a message using a large language model.

        Args:
          message: The message to evaluate.
          role: The role of the user who is issuing the message.
          **args: Additional arguments to be passed to the large language model.

        Returns:
          The evaluation result from the large language model.
        """

        # Process role argument
        roleLocal = role
        if roleLocal is None:
            roleLocal = self.llm_evaluator.user_role
        else:
            self.llm_evaluator.user_role = roleLocal

        # Make and store message struct
        if self.messages is None:
            self.messages = []
        self.messages.append(self.make_message(role=roleLocal, message=message))

        # Get LLM result
        res = None
        try:
            res = self.llm_evaluator.eval(self.messages, **args)
        except Exception as ex:
            logging.error('Failure while evaluating the message. Message and response are not logged.')
            raise ex

        # Try to convert LLM response into a string
        msg_res = None
        try:
            msg_res = str(res)
        except Exception as ex:
            logging.error("Cannot store as a string the LLM response: '%s'.", res)
            msg_res = res

        # Make and store message response
        self.messages.append(self.make_message(role=self.llm_evaluator.assistant_role, message=msg_res))

        return res

    # ------------------------------------------------------
    def print(self):
        print("Chat ID: " + self.chat_id)
        print(60 * "-")
        print("Prompt:")
        print(self.prompt())
        for m in self.messages:
            print(60 * "-")
            print(m)

    # ------------------------------------------------------
    def to_dict(self):
        return {'id': self.chat_id, 'type': 'chat', 'prompt': repr(self.prompt()), 'messages': len(self.messages)}

    def __repr__(self):
        return repr(self.to_dict())

    # ------------------------------------------------------
    def __str__(self):
        return str(repr(self))
