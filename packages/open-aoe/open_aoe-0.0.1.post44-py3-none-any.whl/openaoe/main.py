from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi.responses import FileResponse
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import argparse

from openaoe.backend.api.route_minimax import router as minimax
from openaoe.backend.api.route_openai import router as openai
from openaoe.backend.api.route_google import router as google
from openaoe.backend.api.route_claude import router as claude
from openaoe.backend.api.route_xunfei import router as xunfei
from openaoe.backend.api.route_internlm import router as internlm
from openaoe.backend.util.log import log
from openaoe.backend.util.exception import OpenAIException, is_openai_key_limited
from openaoe.backend.model.dto.ReturnBase import ReturnBase
from openaoe.backend.config.biz_config import app_abs_path, img_out_path
from openaoe.backend.util.str_util import safe_join
from openaoe.backend.config.biz_config import load_config


logger = log(__name__)
# define global variable
API_VER = 'v1'
base_dir = app_abs_path()
STATIC_RESOURCE_DIR = os.path.join(base_dir, "frontend/dist")
CSS_PATH_LIB = f"{STATIC_RESOURCE_DIR}/assets"
IMG_PATH_LIB = f"{STATIC_RESOURCE_DIR}/assets"
JS_PATH_LIB = f"{STATIC_RESOURCE_DIR}/js"
path = img_out_path()
OUT_IMG_PATH_LIB = f"{path}"

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_RESOURCE_DIR), name="static")
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def server():
    return FileResponse(f"{STATIC_RESOURCE_DIR}/index.html")


@app.get("/assets/css/{path:path}")
async def build_resource(path: str):
    build_file = safe_join(CSS_PATH_LIB, path)
    return FileResponse(build_file)


@app.get("/{path:path}")
async def build_resource(path: str):
    static_file = safe_join(STATIC_RESOURCE_DIR, path)
    return FileResponse(static_file)


# add middlewares here if need
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add api routers
app.include_router(minimax, prefix=f"/{API_VER}/minimax")
app.include_router(openai, prefix=f"/{API_VER}/openai")
app.include_router(google, prefix=f"/{API_VER}/google")
app.include_router(claude, prefix=f"/{API_VER}/claude")
app.include_router(xunfei, prefix=f"/{API_VER}/xunfei")
app.include_router(internlm, prefix=f"/{API_VER}/internlm")


@app.exception_handler(OpenAIException)
# 统一处理openai请求时的异常，对于需要轮转的key，设置轮转标记（在后续middleware中统一处理)
async def openai_exceptioxn_handler(request: Request, exc: OpenAIException):
    logger.warning(f"{exc}")
    is_limited, reason = is_openai_key_limited(exc.model, exc.error)
    if is_limited:
        logger.info("is limited")

    if 'stream' in request.url.path:
        return
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(ReturnBase(
            msg="error",
            msgCode="-1",
            data=str(exc.error)
        )))


def main():
     # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Example app using a YAML config file.")
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the YAML config file.')

    # 解析命令行参数
    config_path = parser.parse_args()

    logger.info(f"your config file is: {config_path.file}")
    # load config.yaml
    load_config(config_path.file)

    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=10099,
        timeout_keep_alive=600,
        workers=1
    )


if __name__ == "__main__":
    main()
