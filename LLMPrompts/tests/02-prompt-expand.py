import re
import unittest
from LLMPrompts import llm_prompt, llm_prompt_expand


class LLMPromptsTests(unittest.TestCase):

    def test_1(self):
        self.assertEqual(
            llm_prompt_expand('This is a simple prompt'),
            'This is a simple prompt')

    def test_2(self):
        spec2 = """
         @Yoda 
        """
        self.assertEqual(
            llm_prompt_expand(spec2).strip(),
            llm_prompt('Yoda').strip())

    def test_3(self):
        spec3 = """
        !Translated|German
        """
        self.assertEqual(
            llm_prompt_expand(spec3).strip(),
            llm_prompt('Translated')('German').strip())

    def test_4(self):
        self.assertEqual(
            llm_prompt_expand('@Yoda The summer is gone.'),
            llm_prompt('Yoda') + "\n The summer is gone.")

    def test_5(self):
        self.assertEqual(
            llm_prompt_expand('@CodeWriterX|HTML Random table with 5 rows and 4 columns.'),
            llm_prompt('CodeWriterX')('HTML') + "\n Random table with 5 rows and 4 columns.")

    def test_6(self):
        spec5 = 'The summer is gone, school is coming soon.'
        self.assertEqual(
            llm_prompt_expand(f"{spec5} #HaikuStyled").strip(),
            (spec5 + ' ' + llm_prompt('HaikuStyled')).strip())

    def test_7(self):
        spec5 = 'The summer is gone, school is coming soon.'
        self.assertEqual(
            (spec5 + ' ' + llm_prompt('HaikuStyled') + "\n " + llm_prompt('Translated')()).strip(),
            llm_prompt_expand(f"{spec5} #HaikuStyled #Translated").strip())

    def test_8(self):
        spec5 = 'The summer is gone, school is coming soon.'
        self.assertEqual(
            (spec5 + ' ' + llm_prompt('HaikuStyled') + "\n " + llm_prompt('Translated')('German')).strip(),
            llm_prompt_expand(f"{spec5} #HaikuStyled #Translated|German").strip())

    def test_9(self):
        self.assertEqual(
            ('Generate a scary story. ' + llm_prompt('ShortLineIt')(50)).strip(),
            llm_prompt_expand("Generate a scary story. #ShortLineIt|50").strip())

    def test_10(self):
        self.assertEqual(
            'Generate a scary story. ' + llm_prompt('ShortLineIt')(50, 'text'),
            llm_prompt_expand("Generate a scary story. #ShortLineIt|50|text").strip())

    def test_11(self):
        spec5 = 'The summer is gone, school is coming soon.'
        self.assertEqual(
            (llm_prompt('Translate')('Russian') + spec5).strip(),
            llm_prompt_expand(f"&Translate|Russian {spec5}").strip())

    def test_12(self):
        spec5 = 'The summer is gone, school is coming soon.'
        self.assertEqual(
            (llm_prompt('Translate')('High German') + spec5).strip(),
            llm_prompt_expand(f"!Translate|'High German' {spec5}"))

    def test_13(self):
        spec8 = 'The cat chased the mouse.'
        self.assertEqual(
            re.sub("\s+", " ", llm_prompt('FormalRephrase')(spec8)),
            re.sub("\s+", " ", llm_prompt_expand(f"!FormalRephrase {spec8}")))

    def test_14(self):
        spec8 = 'The cat chased the mouse.'
        self.assertEqual(
            llm_prompt('FormalRephrase')(spec8),
            llm_prompt_expand(f"!FormalRephrase>{spec8}"))

    def test_15(self):
        messages12 = ['some1', 'some2']
        self.assertEqual(
            llm_prompt('FormalRephrase')('some2').strip(),
            llm_prompt_expand("\n\n!FormalRephrase^\n\n", messages=messages12).strip())

    def test_16(self):
        messages12 = ['some1', 'some2']
        self.assertEqual(
            llm_prompt_expand("&FormalRephrase^^", messages=messages12, sep="\n;;\n"),
            llm_prompt('FormalRephrase')("\n;;\n".join(messages12)))

    def test_17(self):
        self.assertEqual(
            llm_prompt('ShortLineIt')('  40').strip(),
            llm_prompt_expand("\n\n!ShortLineIt>  40").strip())

    def test_18(self):
        self.assertEqual(
            llm_prompt_expand("\n\n!ShortLineIt|40 some long text").strip(),
            llm_prompt('ShortLineIt')(40, 'some long text').strip())

    def test_19(self):
        messages19 = ['tomorrow', 'future']
        self.assertEqual(
            llm_prompt('Translate')('German', 'future').strip(),
            llm_prompt_expand("\n\n!Translate|German^\n\n", messages=messages19).strip())


if __name__ == '__main__':
    unittest.main()
