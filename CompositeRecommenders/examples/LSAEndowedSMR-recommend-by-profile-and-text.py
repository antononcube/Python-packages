from SparseMatrixRecommender.SparseMatrixRecommender import *
from SparseMatrixRecommender.DataLoaders import *
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import *
from CompositeRecommenders.LSAEndowedSMR import LSAEndowedSMR
from CompositeRecommenders.SMR_to_LSA import SMR_to_LSA

# -----------------------------------------------------------
# dfMushroom = load_mushroom_data_frame()
dfTitanic = load_titanic_data_frame()

smrObj = (SparseMatrixRecommender()
          .create_from_wide_form(data=dfTitanic,
                                 columns=None,
                                 item_column_name="id",
                                 add_tag_types_to_column_names=True,
                                 tag_value_separator=":")
          .apply_term_weight_functions(global_weight_func="IDF",
                                       local_weight_func="None",
                                       normalizer_func="Cosine"))

print(smrObj.take_M().column_names())

# profile1 = ["cap-Color:gray", "odor:foul", "not-in-tag"]
profile1 = ["passengerSex:female", "passengerClass:1st"]

recs1 = (smrObj
         .recommend_by_profile(profile=profile1, normalize=False, ignore_unknown=True)
         .take_value())

print(recs1)

# -----------------------------------------------------------

lsaObj = SMR_to_LSA(smr=smrObj, number_of_topics=3)

print(lsaObj.echo_topics_interpretation(wide_form=True))

# -----------------------------------------------------------

smatWords = lsaObj.take_doc_term_mat().copy()
smatWords = smatWords.set_column_names(["Word:" + c for c in smatWords.column_names()], )

smatTopics = lsaObj.take_W().copy()
smatTopics = smatTopics.set_column_names(["Topic:" + c for c in smatTopics.column_names()])

smrObj = smrObj.annex_sub_matrices(mats={"Word": smatWords, "Topic": smatTopics})
smrObj = smrObj.apply_term_weight_functions("None", "None", "Cosine")
smrEndowed = LSAEndowedSMR(smrObj, lsaObj)

recs2 = smrEndowed.recommend_by_profile_and_text([], "male 3rd survived", ignore_unknown=True).take_value()

print(recs2)

# -----------------------------------------------------------
#
# print("=" * 120)
#
# print(smrEndowed)
#
# print("-" * 120)
#
# print(repr(smrEndowed))
#
# -----------------------------------------------------------
#
# print("=" * 120)
#
# print(smrEndowed.to_dict())
