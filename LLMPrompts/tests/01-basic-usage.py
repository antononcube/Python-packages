import unittest
from LLMPrompts.LLMPrompts import ingest_prompt_data
from LLMPrompts.LLMPrompts import llm_prompt_data
from LLMPrompts.LLMPrompts import llm_prompt


class LLMPromptsBasicUsage(unittest.TestCase):
    pre3 = 'Use to GitHub table specification of the result if possible.'

    def test_ingest1(self):
        self.assertTrue(isinstance(ingest_prompt_data(), dict))
        self.assertTrue("records" in ingest_prompt_data().keys())
        self.assertTrue("categories" in ingest_prompt_data().keys())
        self.assertTrue("topics" in ingest_prompt_data().keys())

    def test_prompt_data1(self):
        self.assertTrue(isinstance(llm_prompt_data(), dict))

    def test_prompt_data2(self):
        self.assertTrue(isinstance(llm_prompt_data('Y'), dict))
        self.assertTrue(isinstance(llm_prompt_data(r'^Y.*E$'), dict))

    def test_prompt_data3(self):
        self.assertTrue(isinstance(llm_prompt_data('Y', None), dict))
        self.assertTrue(isinstance(llm_prompt_data(r'^Y.*E$', "Description"), dict))
        self.assertTrue(isinstance(llm_prompt_data(r'^Y.*E$', ["Description", "Categories"]), dict))

    def test_prompt1(self):
        self.assertTrue(isinstance(llm_prompt('Yoda'), str))
        self.assertTrue(callable(llm_prompt('ShortLineIt')))
        self.assertTrue(callable(llm_prompt('CallToActionSuggest')))

    def test_prompt2(self):
        self.assertTrue(llm_prompt('YodaSodaModaCoda98e9x994239201') is None)


if __name__ == '__main__':
    unittest.main()
