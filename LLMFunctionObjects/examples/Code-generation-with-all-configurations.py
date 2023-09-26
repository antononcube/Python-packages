from LLMFunctions import *
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
print('ChatPaLM')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='ChatPaLM')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))

# =====================================================================================================================
print(120 * "=")
print('PaLM')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='PaLM')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))