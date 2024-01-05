extern crate core;

mod parser;
mod ast;

use pyo3::prelude::*;

use pyo3::exceptions::PySyntaxError;
use crate::ast::{T3dObject, T3dReference};
use crate::parser::parse_t3d;

#[pyfunction]
fn read_t3d(contents: &str) -> PyResult<Vec<T3dObject>> {
    match parse_t3d(contents) {
        Ok(objects) => {
            Ok(objects)
        },
        Err(err) => {
            Err(PySyntaxError::new_err(format!("{:?}", err)))
        }
    }
}

#[pymodule]
fn t3dpy(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<T3dObject>()?;
    m.add_class::<T3dReference>()?;
    m.add_function(wrap_pyfunction!(read_t3d, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::fs::File;
    use std::io::Read;
    use super::*;

    #[test]
    fn it_works() -> Result<(), String> {
        let mut contents = String::new();
        match File::open("src/tests/data/terraininfo.t3d") {
            Ok(mut file) => {
                match file.read_to_string(&mut contents) {
                    Ok(_) => {
                        let result = parser::parse_t3d(contents.as_str());
                        match result {
                            Ok(_) => {
                                Ok(())
                            }
                            Err(error) => {
                                print!("{}", error.to_string().as_str());
                                Err("Syntax error".to_string())
                            }
                        }
                    }
                    Err(_) => {
                        Err("Failed to file contents".to_string())
                    }
                }
            }
            Err(_) => {
                Err("Failed to open file".to_string())
            }
        }
    }
}
