import unittest
from LLMFunctions.LLMFunctions import llm_function
from LLMFunctions.LLMFunctions import llm_configuration
from LLMFunctions.LLMFunctions import llm_evaluator


class LLMFunctionsTests(unittest.TestCase):

    def test_func1(self):
        f1 = llm_function("Answer as the character Yoda from Star Wars.")
        self.assertTrue(callable(f1))

    def test_func2(self):
        f2 = llm_function(lambda x: f"What is the short biography and discography of the artist {x}?", e='PaLM')
        self.assertTrue(callable(f2))

    def test_func3(self):
        f3 = llm_function(lambda x: f"What is the short biography and discography of the artist {x}?",
                          e=llm_configuration('PaLM', max_tokens=500))
        self.assertTrue(callable(f3))

    def test_func4(self):
        f4 = llm_function()
        self.assertTrue(callable(f4))


if __name__ == '__main__':
    unittest.main()
