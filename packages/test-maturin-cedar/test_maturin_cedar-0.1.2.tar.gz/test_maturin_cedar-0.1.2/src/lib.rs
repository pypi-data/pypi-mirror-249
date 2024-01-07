use pyo3::prelude::*;
use cedar_policy as cedar;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyclass]
struct Authorizer(cedar::Authorizer);

#[pymethods]
impl Authorizer {
    #[new]
    fn new() -> Self {
        Self(cedar::Authorizer::new())
    }

    fn is_authorized(&self, request: [Option<&str>; 3], policy_set: &str) -> bool {
        let request = cedar::Request::new(
            request[0].map(|s| s.parse().expect("invalid principal")),
            request[1].map(|s| s.parse().expect("invalid action")),
            request[2].map(|s| s.parse().expect("invalid resource")),
            cedar::Context::empty(),
            None,
        ).expect("invalid request");
        let policy_set = policy_set.parse().expect("invalid policy-set");
        let response = self.0.is_authorized(&request, &policy_set, &cedar::Entities::empty());
        match response.decision() {
            cedar::Decision::Allow => true,
            _ => false,
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn test_maturin_cedar(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<Authorizer>()?;
    Ok(())
}
