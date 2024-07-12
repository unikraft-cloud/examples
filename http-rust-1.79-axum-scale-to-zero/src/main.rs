use std::convert::Infallible;
use std::time::Duration;

use axum::extract::Path;
use axum::http::StatusCode;
use axum::response::sse::{Event, KeepAlive};
use axum::response::{IntoResponse, Sse};
use axum::routing::{get, post};
use axum::Router;
use futures_util::stream::{self, Stream};
use tokio::fs;
use tokio_stream::StreamExt as _;

const LIBUKP_FILE: &str = "/uk/libukp/scale_to_zero_disable";

enum Error {
    IoError(std::io::Error),
}

impl IntoResponse for Error {
    fn into_response(self) -> axum::response::Response {
        let (status, message) = match self {
            Error::IoError(e) => (StatusCode::INTERNAL_SERVER_ERROR, format!("I/O error: {e}")),
        };

        (status, message).into_response()
    }
}

impl From<std::io::Error> for Error {
    fn from(value: std::io::Error) -> Self {
        Self::IoError(value)
    }
}

async fn read_libukp_disable() -> std::io::Result<String> {
    fs::read_to_string(LIBUKP_FILE).await
}

async fn write_libukp_disable(content: impl AsRef<[u8]>) -> std::io::Result<String> {
    fs::write(LIBUKP_FILE, content).await?;
    read_libukp_disable().await
}

async fn counter_set(Path(value): Path<u32>) -> Result<String, Error> {
    Ok(write_libukp_disable(&format!("={value}")).await?)
}

async fn counter_inc() -> Result<String, Error> {
    Ok(write_libukp_disable("+").await?)
}

async fn counter_add(Path(adj): Path<u32>) -> Result<String, Error> {
    Ok(write_libukp_disable(&format!("+{adj}")).await?)
}

async fn counter_dec() -> Result<String, Error> {
    Ok(write_libukp_disable("-").await?)
}

async fn counter_sub(Path(adj): Path<u32>) -> Result<String, Error> {
    Ok(write_libukp_disable(&format!("-{adj}")).await?)
}

async fn counter_get() -> Result<String, Error> {
    Ok(read_libukp_disable().await?)
}

async fn sse(Path(sec): Path<u32>) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let stream = stream::repeat_with(|| Event::default().data("ping"))
        .map(Ok)
        .throttle(Duration::from_secs(sec.into()));

    Sse::new(stream).keep_alive(KeepAlive::default())
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(counter_get))
        .route("/sse/:sec", get(sse))
        .route("/set/:value", post(counter_set))
        .route("/add", post(counter_inc))
        .route("/add/:adj", post(counter_add))
        .route("/sub", post(counter_dec))
        .route("/sub/:adj", post(counter_sub));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
