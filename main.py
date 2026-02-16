from fastapi import Request
import os, uuid, time, asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfWriter
import uuid, os
from pypdf import PdfReader
import zipfile
from pdf2image import convert_from_path
from PIL import Image
import os, uuid
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD = "uploads"
OUTPUT = "output"

...
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/merge")
async def merge(files: list[UploadFile] = File(...)):

    writer = PdfWriter()

    paths = []
    for file in files:
        path = f"{UPLOAD}/{uuid.uuid4()}.pdf"
        with open(path, "wb") as f:
            f.write(await file.read())
        writer.append(path)
        paths.append(path)

    out = f"{OUTPUT}/{uuid.uuid4()}.pdf"
    with open(out, "wb") as f:
        writer.write(f)

    return FileResponse(out, filename="merged.pdf")
@app.post("/split")
async def split(file: UploadFile = File(...)):

    # save uploaded file
    path = f"{UPLOAD}/{uuid.uuid4()}.pdf"
    with open(path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(path)

    zip_path = f"{OUTPUT}/{uuid.uuid4()}.zip"
    zipf = zipfile.ZipFile(zip_path, 'w')

    # create each page pdf
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        page_file = f"{OUTPUT}/page_{i+1}.pdf"
        with open(page_file, "wb") as f:
            writer.write(f)

        zipf.write(page_file, f"page_{i+1}.pdf")
        os.remove(page_file)

    zipf.close()

    return FileResponse(zip_path, filename="split_pages.zip")
@app.post("/pdf-to-jpg")
async def pdf_to_jpg(file: UploadFile = File(...)):

    input_path = f"{UPLOAD}/{uuid.uuid4()}.pdf"
    with open(input_path, "wb") as f:
        f.write(await file.read())

    images = convert_from_path(input_path, poppler_path=r"C:\poppler\Library\bin")

    zip_path = f"{OUTPUT}/{uuid.uuid4()}.zip"
    zipf = zipfile.ZipFile(zip_path, 'w')

    for i, img in enumerate(images):
        img_path = f"{OUTPUT}/page_{i+1}.jpg"
        img.save(img_path, "JPEG")
        zipf.write(img_path, f"page_{i+1}.jpg")
        os.remove(img_path)

    zipf.close()

    return FileResponse(zip_path, filename="images.zip")
@app.post("/jpg-to-pdf")
async def jpg_to_pdf(files: list[UploadFile] = File(...)):

    image_paths = []

    for file in files:
        path = f"{UPLOAD}/{uuid.uuid4()}.jpg"
        with open(path, "wb") as f:
            f.write(await file.read())
        image_paths.append(path)

    images = [Image.open(p).convert("RGB") for p in image_paths]

    output_pdf = f"{OUTPUT}/{uuid.uuid4()}.pdf"
    images[0].save(output_pdf, save_all=True, append_images=images[1:])

    return FileResponse(output_pdf, filename="converted.pdf")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

FILE_LIFETIME = 60 * 60 * 24   # 24 hours (seconds)


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, name)

    with open(path, "wb") as f:
        f.write(await file.read())

    url = f"{request.base_url}download/{name}"
    return {"url": url}


@app.get("/download/{filename}")
async def download_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(path, filename=filename)

async def auto_delete():
    while True:
        now = time.time()

        for f in os.listdir(UPLOAD_DIR):
            if f.endswith(".time"):
                filepath = os.path.join(UPLOAD_DIR, f)
                with open(filepath) as t:
                    uploaded = float(t.read())

                if now - uploaded > FILE_LIFETIME:
                    realfile = filepath.replace(".time", "")
                    if os.path.exists(realfile):
                        os.remove(realfile)
                    os.remove(filepath)
                    print("Deleted:", realfile)

        await asyncio.sleep(60)  # check every minute


@app.on_event("startup")
async def start_cleanup():
    asyncio.create_task(auto_delete())
