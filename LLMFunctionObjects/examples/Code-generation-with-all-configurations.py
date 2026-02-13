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
print('ChatGemini')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='ChatGemini')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))

# =====================================================================================================================
print(120 * "=")
print('ChatOllama')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='ChatOllama')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))

# =====================================================================================================================
print(120 * "=")
print('Ollama')
print(120 * "-")

fcw = llm_function(llm_prompt("CodeWriterX")("Python"), e='Ollama')

print(fcw.prompt)
# ---------------------------------------------------------------------------------------------------------------------
print(120 * "-")

print(fcw("Random walk simulation.", echo=False))
