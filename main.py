import jmcomic  # 导入此模块，需要先安装.
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello JMComic"}
@app.get("/download/{jmid}")
async def download_file(jmid: str):
    try:
        option = jmcomic.create_option_by_file('./option.yml')
        jmcomic.download_album(jmid, option)  # 传入要下载的album的id，即可下载整个album到本地.
        return {"code": 200,"message": "当前链接有效期：2小时","url": f"http://127.0.0.1:8000/pdf/{jmid}.pdf"}
    except:
        return {"code": 500, "message": "No Comic Found"}

@app.get("/pdf/{jmid}.pdf")
async def download_pdf(jmid: str):
    file_path = f"./pdf/{jmid}.pdf"
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    # Return the file as a response
    return FileResponse(file_path, media_type="application/pdf", filename=f"{jmid}.pdf")