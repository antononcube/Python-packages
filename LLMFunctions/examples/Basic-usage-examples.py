from LLMFunctions.LLMFunctions import llm_configuration
from LLMFunctions.LLMFunctions import llm_evaluator
from LLMFunctions.LLMFunctions import llm_function

print(120 * "=")

#fPrompt = lambda x1, x2, x3: f'What is the {x1} if {x2} in {x3}?. Give the result as JSON object with name-value pairs.'
#print(fPrompt("GDP", "top 10 countries", "2020"))

fTxt = llm_function("What is the population of:")

print(fTxt)

print(120 * "-")

print(fTxt('Brazil'))
