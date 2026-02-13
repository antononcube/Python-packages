import unittest
from LLMFunctionObjects.LLMFunctions import llm_configuration
from LLMFunctionObjects.LLMFunctions import llm_evaluator
from LLMFunctionObjects.Configuration import Configuration
from LLMFunctionObjects.Evaluator import Evaluator


class LLMEvaluators(unittest.TestCase):
    pre3 = 'Use to GitHub table specification of the result if possible.'

    def test_evaluator1(self):
        self.assertTrue(isinstance(llm_evaluator("openai"), Evaluator))

    def test_evaluator2(self):
        self.assertTrue(isinstance(llm_evaluator(llm_configuration("openai", prompts=self.pre3)), Evaluator))

    def test_evaluator3(self):
        self.assertTrue(isinstance(llm_evaluator(llm_evaluator('openai'), form="JSON"), Evaluator))

    def test_evaluator4(self):
        self.assertTrue(isinstance(llm_evaluator(None).to_dict(), dict))

    def test_evaluator5(self):
        self.assertTrue(isinstance(llm_evaluator(llm_configuration('openai', prompts=self.pre3)), Evaluator))

    def test_evaluator6(self):
        self.assertTrue(isinstance(llm_evaluator('Gemini', max_tokens=500), Evaluator))

    def test_evaluator7(self):
        e1 = llm_evaluator(llm_configuration('OpenAI'))
        e2 = llm_evaluator('openai')
        self.assertTrue(e1.to_dict() == e2.to_dict())

    def test_evaluator8(self):
        e = llm_evaluator(llm_configuration('OpenAI'))
        c1 = llm_configuration('OpenAI')
        c2 = llm_configuration(e)
        self.assertTrue(c1.to_dict() == c2.to_dict())


if __name__ == '__main__':
    unittest.main()
