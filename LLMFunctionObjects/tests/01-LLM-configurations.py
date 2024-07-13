import unittest
from LLMFunctionObjects.LLMFunctions import llm_configuration
from LLMFunctionObjects.Configuration import Configuration


class LLMConfigurations(unittest.TestCase):
    pre3 = 'Use to GitHub table specification of the result if possible.'

    def test_config1(self):
        self.assertTrue(isinstance(llm_configuration(None).to_dict(), dict))

    def test_config2(self):
        self.assertTrue(isinstance(llm_configuration("openai"), Configuration))

    def test_config3(self):
        self.assertTrue(isinstance(llm_configuration(llm_configuration('openai', prompts=self.pre3)), Configuration))

    def test_config4(self):
        self.assertTrue(isinstance(llm_configuration('openai', prompts=self.pre3), Configuration))

    def test_config5(self):
        c1 = llm_configuration('OpenAI')
        c2 = llm_configuration('openai')
        self.assertTrue(c1.to_dict() == c2.to_dict())

    def test_config6(self):
        c6 = llm_configuration('openai', prompts=self.pre3)
        self.assertEqual(c6.prompts, [self.pre3, ])

    def test_config7(self):
        c7 = llm_configuration('chatgpt', temperature=1.1)
        self.assertEqual(c7.temperature, 1.1)
        self.assertEqual(c7.name, 'chatgpt')
        self.assertEqual(c7.model, 'gpt-3.5-turbo')


if __name__ == '__main__':
    unittest.main()
