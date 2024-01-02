mod utils;
use utils::{AST, cmd2ast};
use pyo3::{exceptions::PyRuntimeError, types::PyTuple};
use pyo3::prelude::*;
use whiledb::{SrcError, parse as whiledb_parse, interpreter, interpreter::Result};
use std::{rc::Rc, collections::VecDeque, cell::RefCell};

/// parse the `src` string
#[pyfunction]
fn parse(src: String) -> PyResult<AST> {
    match whiledb_parse(&src) {
        Ok(tree) => {
            Ok(cmd2ast(&tree))
        },
        Err(err) => {
            let msg = match err {
                SrcError::LexerError(_, msg) => msg,
                SrcError::ParseError(_, msg) => msg,
                SrcError::SelfError(msg) => msg,
                SrcError::SelfWarning(_, msg) => msg,
            };
            Err(PyRuntimeError::new_err(msg))
        },
    }
}

fn py_buildin_print(args: VecDeque<interpreter::Any>, state: interpreter::Any) -> Result<interpreter::Any> {
    let mut print_args = vec![];
    for arg in args.into_iter() {
        print_args.push(interpreter::utils::convert2string(arg, state.clone())?);
    }
    Python::with_gil(|py| -> PyResult<()> {
        let builtins = py.import("builtins")?;
        let print_func: PyObject = builtins.getattr("print")?.into();
        let args = PyTuple::new(py, print_args);
        print_func.call1(py, args)?;
        Ok(())
    })?;
    interpreter::utils::get_buildin_var("None", state)
}

/// execuate the WhileDB code
#[pyfunction]
fn exec(src: String) -> PyResult<()> {
    match whiledb_parse(&src) {
        Ok(res) => {
            let state = interpreter::init_state()?;
            interpreter::utils::set_attr(state.clone(), "print", Rc::new(RefCell::new(
                interpreter::WdAny::Func("print".to_string(), interpreter::Function::BuildInFunction(interpreter::BuildInFunction(py_buildin_print)))
            )))?;
            let state = interpreter::utils::local_state(state.clone());
            interpreter::exec(Rc::new(res), state)?;
            Ok(())
        },
        Err(err) => {
            let msg = match err {
                SrcError::LexerError(_, msg) => msg,
                SrcError::ParseError(_, msg) => msg,
                SrcError::SelfError(msg) => msg,
                SrcError::SelfWarning(_, msg) => msg,
            };
            Err(PyRuntimeError::new_err(msg))
        },
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn whiledb_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(exec, m)?)?;
    Ok(())
}
