from typing import Optional, List, Dict, Tuple, Union
from .whiledb_nom import eval as _eval, exec as _exec

def eval(src: str, reg: Optional[Dict[str, int]] = None, mem: Optional[Tuple[List[Union[int, None]], Dict[int, int]]] = None) -> int:
    """Execuate the WhileDB commands `src` on the given registers `reg` and memory `mem`."""
    if reg is None: reg = {}
    if mem is None: mem = ([None], {})
    res, reg1, mem1 = _eval(src, reg, mem)
    reg.update(reg1)
    mem[0][:] = mem1[0]
    mem[1].update(mem1[1])
    return res

def exec(src: str, reg: Optional[Dict[str, int]] = None, mem: Optional[Tuple[List[Union[int, None]], Dict[int, int]]] = None) -> Tuple[Dict[str, int], Tuple[List[Union[int, None]], Dict[int, int]]]:
    """Execuate the WhileDB commands `src` on the given registers `reg` and memory `mem`."""
    if reg is None: reg = {}
    if mem is None: mem = ([None], {})
    reg1, mem1 = _exec(src=src, reg=reg, mem=mem)
    reg.update(reg1)
    mem[0][:] = mem1[0]
    mem[1].update(mem1[1])
    return reg, mem