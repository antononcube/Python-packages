from LLMFunctionObjects import *
import LLMFunctionObjects

# print(120 * "=")
#
# eObj = LLMFunctionObjects.EvaluatorChatGPT(conf=llm_configuration("ChatGPT"))
#
# fTxt = llm_function("What is the population of", e=eObj)
#
# print(fTxt)
#
# print(120 * "-")
#
# print(fTxt('Nigeria?', echo=False))
#
# print(120 * "=")

s1 = llm_synthesize(["Answer as the character Yoda from Star Wars.", "Who are you?"], e='ChatPaLM')

print(s1)
