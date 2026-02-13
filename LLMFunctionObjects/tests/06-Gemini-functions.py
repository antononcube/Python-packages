import os
import unittest
from LLMFunctionObjects.LLMFunctions import llm_configuration, llm_evaluator, llm_example_function, llm_function

class GeminiExamFuncs(unittest.TestCase):

    def test_exam1(self):
        gemini_api_key = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY"))

        confGemini = llm_configuration("Gemini", api_key=gemini_api_key)

        pu = llm_example_function(
            {'11,042 m/s': '11_042 * u.m / u.s")',
             '4,380,042 J': '4_380_042 * u.J")',
             '304.342 m/s^2': '304.342 * u.m / u.s**2'},
            e=confGemini)

        fs = llm_function(lambda a, b: f"What is the average speed of {a} in the units of {b}?", e=confGemini)

        self.assertTrue(callable(fs))

        rs1 = fs('rocket leaving Earth', 'meters per second')
        #print(rs1)

        self.assertTrue(isinstance(rs1, str))

    def test_func1(self):
        gemini_api_key = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY"))

        confGemini = llm_configuration("Gemini", api_key=gemini_api_key)

        text = llm_function('', e=llm_configuration(confGemini, max_tokens=500))("What is Boris Brejcha's bio and discography?")
        #print(text)

        self.assertTrue(isinstance(text, str))


if __name__ == '__main__':
    unittest.main()
