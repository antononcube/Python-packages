from LLMPrompts import *
from LLMFunctions import *
import random

# Ingest prompt data
aPromptData = ingest_prompt_data()
for rec in random.sample(aPromptData["records"], 3):
    print(rec)

print(120 * "=")
# ========================================================================================================================
# Get a specified prompts
p1 = llm_prompt_data("^N.*e$", fields="whatever")
print(p1)

print(120 * "=")
# ========================================================================================================================
# Get a constant prompt
p2 = llm_prompt("Yoda")
print(p2)

print(120 * "=")
# ========================================================================================================================
# Get function
p2 = llm_prompt("ShortLineIt")
print(p2)

print(120 * "-")
print(p2(30, 'THIS TEXT'))

print(120 * "=")
# ========================================================================================================================
# Get function
p3 = llm_prompt("CallToActionSuggest")
print(p3)

print(120 * "-")
print(p3(Text='THIS TEXT'))

print(120 * "=")
# ========================================================================================================================
# Get a random prompt
p4 = llm_prompt("Yoda")
print(p4)

print(120 * "=")
# ========================================================================================================================
#  LLM function
f1 = llm_function(llm_prompt("FTFY"))

print(f1)

print(f1("Where does he works now?"))
