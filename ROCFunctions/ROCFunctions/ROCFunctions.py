# ------------------------------------------------------------
# ROC predicates
# ------------------------------------------------------------
from math import sqrt


def is_roc_dict(obj):
    if isinstance(obj, dict):
        common = set.intersection(set(obj.keys()),
                                  set(["TruePositive", "FalsePositive", "TrueNegative", "FalseNegative"]))
        return len(common) == 4
    return False


def is_roc_dict_list(obj):
    return isinstance(obj, list) and all([is_roc_dict(x) for x in obj])


# ------------------------------------------------------------
# ROCs
# ------------------------------------------------------------

def _roc_map(func, obj):
    if is_roc_dict_list(obj):
        return [func(x) for x in obj]
    else:
        raise TypeError("Do not know how to process the argument.")


def TPR(obj):
    if is_roc_dict(obj):
        return (obj["TruePositive"]) / (obj["TruePositive"] + obj["FalseNegative"])
    return _roc_map(TPR, obj)


def SPC(obj):
    if is_roc_dict(obj):
        return (obj["TrueNegative"]) / (obj["FalsePositive"] + obj["TrueNegative"])
    return _roc_map(SPC, obj)


def TNR(obj):
    if is_roc_dict(obj):
        return SPC(obj)
    return _roc_map(SPC, obj)


def PPV(obj):
    if is_roc_dict(obj):
        return (obj["TruePositive"]) / (obj["TruePositive"] + obj["FalsePositive"])
    return _roc_map(PPV, obj)


def NPV(obj):
    if is_roc_dict(obj):
        return (obj["TrueNegative"]) / (obj["TrueNegative"] + obj["FalseNegative"])
    return _roc_map(NPV, obj)


def FPR(obj):
    if is_roc_dict(obj):
        return (obj["FalsePositive"]) / (obj["FalsePositive"] + obj["TrueNegative"])
    return _roc_map(FPR, obj)


def FDR(obj):
    if is_roc_dict(obj):
        return (obj["FalsePositive"]) / (obj["FalsePositive"] + obj["TruePositive"])
    return _roc_map(FDR, obj)


def FNR(obj):
    if is_roc_dict(obj):
        return (obj["FalseNegative"]) / (obj["FalseNegative"] + obj["TruePositive"])
    return _roc_map(FNR, obj)


def ACC(obj):
    if is_roc_dict(obj):
        return (obj["TruePositive"] + obj["TrueNegative"]) / sum(list(obj.values()))
    return _roc_map(ACC, obj)


def FOR(obj):
    if is_roc_dict(obj):
        return 1 - NPV(obj)
    return _roc_map(FOR, obj)


def F1(obj):
    if is_roc_dict(obj):
        return 2 * PPV(obj) * TPR(obj) / (PPV(obj) + TPR(obj))
    return _roc_map(F1, obj)


def AUROC(obj):
    if not is_roc_dict_list(obj):
        raise TypeError("The first argument is expected to be a list of ROC dictionaries.")

    fprs = FPR(obj)
    fprs.append(1)
    fprs.insert(0, 0)
    tprs = TPR(obj)
    tprs.append(1)
    tprs.insert(0, 0)

    my_sum = 0
    for i in range(len(fprs) - 1):
        my_sum += (fprs[i + 1] - fprs[i]) * (tprs[i] + (tprs[i + 1] - tprs[i]) / 2)

    return my_sum


def MCC(obj):
    if is_roc_dict(obj):
        tp = TPR(obj)
        tn = TNR(obj)
        fp = FPR(obj)
        fn = FNR(obj)

        tpfp = tp + fp
        tpfn = tp + fn
        tnfp = tn + fp
        tnfn = tn + fn

        dn = tpfp * tpfn * tnfp * tnfn
        if dn == 0:
            dn = 1

        return (tp * tn - fp * fn) / sqrt(dn)
    return _roc_map(MCC, obj)


# ------------------------------------------------------------
# ROC acronyms
# ------------------------------------------------------------

_ROC_Acronyms = {
    "TPR": "true positive rate", "TNR": "true negative rate", "SPC": "specificity",
    "PPV": "positive predictive value", "NPV": "negative predictive value", "FPR": "false positive rate",
    "FDR": "false discovery rate", "FNR": "false negative rate", "ACC": "accuracy",
    "AUROC": "area under the ROC curve", "FOR": "false omission rate", "F1": "F1 score",
    "MCC": "Matthews correlation coefficient", "Recall": "same as TPR", "Precision": "same as PPV",
    "Accuracy": "same as ACC", "Sensitivity": "same as TPR"}


def roc_acronyms_dict(*args):
    return _ROC_Acronyms.copy()


# ------------------------------------------------------------
# ROC functions
# ------------------------------------------------------------

_ROC_Functions = {
    "TPR": TPR, "TNR": SPC, "SPC": SPC, "PPV": PPV, "NPV": NPV, "FPR": FPR, "FDR": FDR,
    "FNR": FNR, "ACC": ACC, "AUROC": AUROC, "FOR": FOR, "F1": F1, "MCC": MCC, "Recall": TPR,
    "Sensitivity": TPR, "Precision": PPV, "Accuracy": ACC,
    "Specificity": SPC, "FalsePositiveRate": FPR,
    "TruePositiveRate": TPR, "FalseNegativeRate": FNR, "TrueNegativeRate": SPC,
    "FalseDiscoveryRate": FDR, "FalseOmissionRate": FOR, "F1Score": F1, "AreaUnderROCCurve": AUROC,
    "MatthewsCorrelationCoefficient": MCC}


def roc_functions(*args):
    if len(args) == 0:
        return roc_functions("Functions")
    elif isinstance(args[0], str):
        if args[0] in _ROC_Functions:
            return _ROC_Functions[args[0]]
        elif args[0].lower() == "Methods".lower():
            return ["FunctionInterpretations", "FunctionNames", "Functions", "Methods", "Properties"]
        elif args[0].lower() == "Properties".lower():
            return roc_functions("methods")
        elif args[0].lower() == "FunctionNames".lower():
            return list(roc_acronyms_dict().keys())
        elif args[0].lower() == "FunctionInterpretations".lower():
            return roc_acronyms_dict()
        elif args[0].lower() == "FunctionsAssociation".lower():
            return _ROC_Functions
        elif args[0].lower() == "Functions".lower():
            return list(_ROC_Functions.values())
        else:
            raise TypeError("Do not know how to process the argument.")
    elif isinstance(args[0], list) and all([isinstance(x, str) for x in args[0]]):
        return [roc_functions(x) for x in args[0]]
    else:
        raise TypeError("Do not know how to process the argument.")


# ------------------------------------------------------------
# To ROC hash
# ------------------------------------------------------------

def to_roc_dict(true_label: str,
                false_label: str,
                actual: list,
                predicted: list,
                sep: str = "-"):
    if not (isinstance(actual, list) and isinstance(predicted, list) and
            len(actual) == len(predicted)):
        raise TypeError("The second and third arguments are expected to be lists with the same number of elements.")

    # Empty ROC dict
    emptyROC = {}
    for x in [true_label, false_label]:
        for y in [true_label, false_label]:
            emptyROC[x + sep + y] = 0

    # Derive TruePositive, FalsePositive, TrueNegative, and FalseNegative
    res = emptyROC
    for i in range(len(actual)):
        res[actual[i] + sep + predicted[i]] += 1

    res = {
        "TruePositive": res[true_label + sep + true_label],
        "FalsePositive": res[false_label + sep + true_label],
        "TrueNegative": res[false_label + sep + false_label],
        "FalseNegative": res[true_label + sep + false_label]}

    return res
