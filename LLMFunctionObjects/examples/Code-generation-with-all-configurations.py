from LLMFunctionObjects import *
from LLMPrompts import *

# =====================================================================================================================
print(120 * "=")
print('ChatGPT')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='ChatGPT')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))

# =====================================================================================================================
print(120 * "=")
print('OpenAI')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='OpenAI')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))

# =====================================================================================================================
print(120 * "=")
print('ChatGemini')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='ChatGemini')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))

# =====================================================================================================================
print(120 * "=")
print('Gemini')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='Gemini')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))
