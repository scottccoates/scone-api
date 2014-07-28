# http://stackoverflow.com/a/485368/173957
import ast
import textwrap


def invert_dict(dict_to_invert):
  inv_map = {}

  for k, v in dict_to_invert.items():
    inv_map.setdefault(v, []).append(k)

  return inv_map


def get_dict_from_string(string):
  return ast.literal_eval(textwrap.dedent(string))
