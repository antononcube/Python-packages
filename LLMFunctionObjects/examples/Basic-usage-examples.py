from LLMFunctionObjects import *

print(120 * "=")

# fPrompt = lambda x1, x2, x3: f'What is the {x1} if {x2} in {x3}?. Give the result as JSON object with name-value pairs.'
# print(fPrompt("GDP", "top 10 countries", "2020"))

fTxt = llm_function("What is the population of", e=llm_configuration("ChatGemini"))

print(fTxt)

print(120 * "-")

print(fTxt('Nigeria?', echo=False))

print(120 * "=")

fPrompt = lambda x1, x2, x3: f'What is the {x1} if {x2} in {x3}?. Give the result as JSON object with name-value pairs.'

fData = llm_function(fPrompt, form=sub_parser("JSON", drop=True), e=llm_configuration("ChatGPT"))

resData = fData("GDP", "top 10 countries", "2020", echo=False, max_tokens=600)

print(resData)

print(120 * "-")

print(fData.llm_result)
#
# print(120 * "=")
#
# fEx = llm_example_function({"1,000": "1000",
#                             "34,232,900": "34232900",
#                             "5.15 trillion": "5.15E12",
#                             "32.8 trillion USD": "32.8E12"},
#                            e=llm_configuration("Gemini"))
#
# print(fEx)
#
# print(fEx(resData))
