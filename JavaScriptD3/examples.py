from DSLTranslation import *

print(dsl_translation("use dfTitanic; group by passengerSex; counts", fmt="json"))

print(dsl_translation("use dfTitanic; group by passengerSex;what are the counts", fmt="code", fallback=False))

print(dsl_translation("use dfTitanic; group by passengerSex;what are the counts", fmt="code", fallback=True))
