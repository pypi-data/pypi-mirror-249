/// OLS using Faer.
use faer::IntoFaer;
use faer::{prelude::*, MatRef};
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

fn list_float_output(_: &[Field]) -> PolarsResult<Field> {
    Ok(Field::new(
        "list_float",
        DataType::List(Box::new(DataType::Float64)),
    ))
}

// // Closed form. Likely don't need
// fn faer_lstsq_cf(x: MatRef<f64>, y: MatRef<f64>) -> Result<Array2<f64>, String> {
//     let xt = x.transpose();
//     let xtx = xt * &x;
//     let decomp = xtx.cholesky(Side::Lower);
//     if let Ok(cholesky) = decomp {
//         let xtx_inv = cholesky.inverse();
//         let betas = xtx_inv * xt * y;
//         Ok(betas.as_ref().into_ndarray().to_owned())
//     } else {
//         Err("Linear algebra error, likely caused by linear dependency".to_owned())
//     }
// }

fn faer_lstsq_qr(x: MatRef<f64>, y: MatRef<f64>) -> Result<Vec<f64>, String> {
    let qr = x.qr();
    let betas = qr.solve_lstsq(y);
    let mut out: Vec<f64> = Vec::with_capacity(betas.nrows());
    for i in 0..betas.nrows() {
        out.push(betas.read(i, 0));
    }
    Ok(out)
}

#[polars_expr(output_type_func=list_float_output)]
fn pl_lstsq(inputs: &[Series]) -> PolarsResult<Series> {
    // if we have nulls, automatically return NaN
    let nrows = inputs[0].len();
    let add_bias = inputs[1].bool()?;
    let add_bias: bool = add_bias.get(0).unwrap();
    let ncols = inputs[2..].len() + add_bias as usize;
    // y = inputs[0], add_bias = inputs[1]
    let y = inputs[0].f64()?;
    let y = y.rechunk();
    let y = y.to_ndarray()?.into_shape((nrows, 1)).unwrap();
    let y = y.view().into_faer();
    let mut vs: Vec<Series> = Vec::with_capacity(inputs.len() - 1);
    for (i, s) in inputs.into_iter().enumerate() {
        // Skip inputs[1] because it is just a boolean
        if (i != 1) && (s.null_count() > 0 || s.len() <= 1) {
            let mut builder: ListPrimitiveChunkedBuilder<Float64Type> =
                ListPrimitiveChunkedBuilder::new("betas", 1, ncols, DataType::Float64);
            let nan = vec![f64::NAN; ncols];
            builder.append_slice(&nan);
            let out = builder.finish();
            return Ok(out.into_series());
        } else if i >= 2 {
            let news = s
                .rechunk()
                .cast(&DataType::Float64)?
                .with_name(&i.to_string());
            vs.push(news);
        }
    }
    // Constant term
    if add_bias {
        let one = Series::from_vec("const", vec![1_f64; nrows]);
        vs.push(one);
    }

    let df_x = DataFrame::new(vs)?;
    // Copy data
    match df_x.to_ndarray::<Float64Type>(IndexOrder::Fortran) {
        Ok(x) => {
            // Solving Least Square, without bias term
            // Change this after faer updates
            let x = x.view().into_faer();
            let betas = faer_lstsq_qr(x, y); // .unwrap();
            match betas {
                Ok(b) => {
                    let mut builder: ListPrimitiveChunkedBuilder<Float64Type> =
                        ListPrimitiveChunkedBuilder::new("betas", 1, b.len(), DataType::Float64);

                    builder.append_slice(&b);
                    let out = builder.finish();
                    Ok(out.into_series())
                }
                Err(e) => Err(PolarsError::ComputeError(e.into())),
            }
        }
        Err(e) => Err(e),
    }
}
