from typing import List, Dict, Tuple, Union

def exec(src: str, reg: Dict[str, int], mem: Tuple[List[Union[int, None]], Dict[int, int]]) -> Tuple[Dict[str, int], Tuple[List[Union[int, None]], Dict[int, int]]]:
    """Execuate the WhileDB commands `src` on the given registers `reg` and memory `mem`."""

def eval(src: str, reg: Dict[str, int], mem: Tuple[List[Union[int, None]], Dict[int, int]]) -> Tuple[int, Dict[str, int], Tuple[List[Union[int, None]], Dict[int, int]]]:
    """Evaluate the WhileDB expression `src` on the given registers `reg` and memory `mem`."""