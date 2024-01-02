from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Sequence
from importlib.util import find_spec
import ast
from yamlstore import Document, Collection


from collections.abc import Mapping
from copy import deepcopy

# https://stackoverflow.com/a/43228384
# only works in a limited fashion
def merge(dict1, dict2):
    ''' Return a new dictionary by merging two dictionaries recursively. '''

    result = deepcopy(dict1)

    for key, value in dict2.items():
        if isinstance(value, Mapping):
            result[key] = merge(result.get(key) or {}, value)
        else:
            result[key] = deepcopy(dict2[key])

    return result


def get_module_docstring(path:Path):
    "get doc string from a python module at path"
    with open(path) as module:
        source = module.read()
    parsed = ast.parse(source)
    docstr =  ast.get_docstring(parsed)
    if not docstr:
        firstline = source.split("\n", maxsplit=1)[0].strip()
        docstr = firstline.lstrip("# ") if firstline.startswith("#") else None
    return docstr

def get_ep_docstring(ep):
    "get doc string of a python module represented by ep"
    spec = find_spec(ep.module)
    return get_module_docstring(Path(spec.origin))

def task_from_module(path:Path):
    "import task module doc string & code without running it"
    with open(path) as module:
        source = module.read()

    # log to a named debug file as required by Python
    debug = NamedTemporaryFile()
    try:
        code = compile(source, debug.name, 'exec')
    except SyntaxError as exc:
        if path.is_relative_to('.'):
            fpth = str(path.relative_to('.'))
        else:
            fpth = str(path)

        text = f" :'{exc.text.strip()}'" if exc.text else ""
        exc.msg = f"{exc.msg} in {fpth} at line {exc.lineno}{text}"
        raise exc
    return code


def get_docs(paths: Sequence[Path]):
    "get all documents in config location, or given by one or more paths"

    docs = []
    batches = []
    for pth in paths:
        if pth.is_dir():
            docs.extend([Document(doc_pth) for doc_pth in pth.glob("*.yaml")])
            batches.extend([Collection(d) for d in pth.iterdir() if len(tuple(d.glob('*.yaml'))) > 0])
        elif pth.is_file():
            docs.append(Document(pth))

    return (docs, batches)
