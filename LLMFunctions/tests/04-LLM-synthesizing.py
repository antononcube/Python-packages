import unittest
from LLMFunctions.LLMFunctions import llm_synthesize
from LLMFunctions.LLMFunctions import llm_configuration
from LLMFunctions.LLMFunctions import llm_evaluator


class LLMFunctionsTests(unittest.TestCase):

    def test_synth1(self):
        s1 = llm_synthesize(["Answer as the character Yoda from Star Wars.", "Who are you?"])
        self.assertTrue(isinstance(s1, str))

    def test_synth2(self):
        s2 = llm_synthesize([lambda x: f"What is the short biography and discography of the artist {x}?", "Boris Brejcha"], e='PaLM')
        self.assertTrue(isinstance(s2, str))

    def test_synth3(self):
        s3 = llm_synthesize("What is the population of Brazil?")
        self.assertTrue(isinstance(s3, str))


if __name__ == '__main__':
    unittest.main()
