use std::collections::HashMap;

use pyo3::prelude::*;
use nom_learn::*;

/// Execuate the WhileDB commands `src` on the given registers `reg` and memory `mem`.
#[pyfunction]
fn exec<'a>(py: Python<'_>, src: &'a str, mut reg: HashMap<&'a str, i128>, mem: (Vec<Option<i128>>, HashMap<usize, usize>)) -> PyResult<(HashMap<&'a str, i128>, (Vec<Option<i128>>, HashMap<usize, usize>))> {
    py.allow_threads(|| {
        let mut mem = Mem { mem: mem.0, malloced: mem.1 };
        parse_cmd(&src).unwrap().1.exec(&mut reg, &mut mem);
        Ok((reg, (mem.mem, mem.malloced)))
    })
}

/// Evaluate the WhileDB expression `src` on the given registers `reg` and memory `mem`.
#[pyfunction]
fn eval<'a>(py: Python<'_>, src: &'a str, mut reg: HashMap<&'a str, i128>, mem: (Vec<Option<i128>>, HashMap<usize, usize>)) -> PyResult<(i128, HashMap<&'a str, i128>, (Vec<Option<i128>>, HashMap<usize, usize>))> {
    py.allow_threads(|| {
        let mut mem = Mem { mem: mem.0, malloced: mem.1 };
        let res = parse_expr(&src).unwrap().1.eval(&mut reg, &mut mem);
        Ok((res, reg, (mem.mem, mem.malloced)))
    })
}

#[pymodule]
fn whiledb_nom(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(exec, m)?)?;
    m.add_function(wrap_pyfunction!(eval, m)?)?;
    Ok(())
}
