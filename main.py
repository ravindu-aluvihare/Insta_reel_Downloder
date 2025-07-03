from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import instaloader
import os
import shutil

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download_reel(url: str = Form(...)):
    try:
        shutil.rmtree(DOWNLOAD_FOLDER)
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        L = instaloader.Instaloader(dirname_pattern=DOWNLOAD_FOLDER, save_metadata=False, post_metadata_txt_pattern='')
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target='')

        video_file = None
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.endswith('.mp4'):
                video_file = os.path.join(DOWNLOAD_FOLDER, file)
                break

        if not video_file:
            return JSONResponse({"success": False, "message": "Video not found."})

        download_url = f"/getfile/{os.path.basename(video_file)}"
        return JSONResponse({"success": True, "url": download_url})

    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)})


@app.get("/getfile/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4", filename=filename)
    else:
        return JSONResponse({"success": False, "message": "File not found."})
