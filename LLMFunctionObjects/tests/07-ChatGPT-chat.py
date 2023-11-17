import unittest
from LLMFunctionObjects.LLMFunctions import llm_chat
from LLMFunctionObjects.Chat import Chat


class PaLMChats(unittest.TestCase):
    prompt = """
    You are Yoda. 
    Respond to ALL inputs in the voice of Yoda from Star Wars. 
    Be sure to ALWAYS use his distinctive style and syntax. Vary sentence length.
    """
    def test_chat1(self):
        chatObj = llm_chat(self.prompt, conf="ChatGPT")

        self.assertTrue(chatObj, Chat)

        self.assertTrue(chatObj.prompt(), self.prompt)

        self.assertTrue(isinstance(chatObj.eval("Hi! Who are you?"), str))

        self.assertTrue(isinstance(chatObj.eval("How many students did you have?"), str))


if __name__ == '__main__':
    unittest.main()
