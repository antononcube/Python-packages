# Assuming Data_TypeSystem_Examiner is a Python class defined elsewhere
#from collections.abc import dict_values, dict_keys

from DataTypeSystem.Examiner import Examiner


# ===========================================================
# Determines if given data is reshapable.
# (For example, a list of dictionaries in Python.)
def is_reshapable(data, iterable_type=None, record_type=None):
    if iterable_type is not None and record_type is not None:
        return Examiner().is_reshapable(data, iterable_type=iterable_type, record_type=record_type)
    else:
        return Examiner().is_reshapable(data)


# ===========================================================
# Returns the record types of the given argument.
def record_types(data):
    return Examiner().record_types(data)


# ===========================================================
# Deduces the type of the given argument.
# :max_enum_elems -- Max number of enum elements.
# :max_struct_elems -- Max number of struct elements.
# :max_tuple_elems -- Max number of tuple elements.
# :tally -- should tally be returned or not?
def deduce_type(data, max_enum_elems=6, max_struct_elems=16, max_tuple_elems=16, tally=False):
    ts = Examiner(max_enum_elems, max_struct_elems, max_tuple_elems)
    if (type(data) is {}.keys().__class__ or
            type(data) is {}.values().__class__ or
            type(data) is {}.items().__class__):
        return ts.deduce_type(list(data), tally=tally)
    return ts.deduce_type(data, tally=tally)
