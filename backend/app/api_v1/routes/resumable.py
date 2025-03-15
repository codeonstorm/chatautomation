from fastapi import FastAPI, Request, UploadFile, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse, HTMLResponse
from pathlib import Path
import os

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resumable.js + FastAPI</title>
    <script src="https://cdn.jsdelivr.net/npm/resumablejs/resumable.js"></script>
</head>
<body>
    <h1>Upload Files</h1>
    <button id="browseButton">Select Files</button>
    <div id="fileList"></div>

    <script>
        const r = new Resumable({
            target: 'http://127.0.0.1:8000/api/v1/uploads',
            chunkSize: 1 * 1024 * 1024, // 1MB
            simultaneousUploads: 3,
            testChunks: true,
        });

        r.assignBrowse(document.getElementById('browseButton'));

        r.on('fileAdded', function(file) {
            const fileList = document.getElementById('fileList');
            const listItem = document.createElement('div');
            listItem.id = `file-${file.uniqueIdentifier}`;
            listItem.innerHTML = `<strong>${file.fileName}</strong> (${file.size} bytes) <span id="progress-${file.uniqueIdentifier}">0%</span>`;
            fileList.appendChild(listItem);
            r.upload();
        });

        r.on('fileProgress', function(file) {
            const progress = Math.floor(file.progress() * 100);
            document.getElementById(`progress-${file.uniqueIdentifier}`).innerText = `${progress}%`;
        });

        r.on('fileSuccess', function(file) {
            document.getElementById(`progress-${file.uniqueIdentifier}`).innerText = 'Completed';
        });

        r.on('fileError', function(file, message) {
            document.getElementById(`progress-${file.uniqueIdentifier}`).innerText = `Error: ${message}`;
        });
    </script>
</body>
</html>

'''

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.get("")
async def check_chunk(resumableIdentifier: str, resumableFilename: str, resumableChunkNumber: int):
    chunk_file = UPLOAD_DIR / f"{resumableIdentifier}_{resumableChunkNumber}"
    if chunk_file.exists():
        return JSONResponse(status_code=200, content={"status": "found"})
    return JSONResponse(status_code=404, content={"status": "not found"})

@router.post("")
async def upload_chunk(request: Request):
    form = await request.form()
    chunk_number = int(form.get("resumableChunkNumber"))
    identifier = form.get("resumableIdentifier")
    filename = form.get("resumableFilename")
    chunk = form.get("file")

    if not all([chunk_number, identifier, filename, chunk]):
        raise HTTPException(status_code=400, detail="Missing upload parameters")

    chunk_file = UPLOAD_DIR / f"{identifier}_{chunk_number}"
    with chunk_file.open("wb") as f:
        f.write(await chunk.read())

    # Check if all chunks are uploaded
    total_chunks = int(form.get("resumableTotalChunks"))
    if all((UPLOAD_DIR / f"{identifier}_{i}").exists() for i in range(1, total_chunks + 1)):
        with open(UPLOAD_DIR / filename, "wb") as final_file:
            for i in range(1, total_chunks + 1):
                chunk_file = UPLOAD_DIR / f"{identifier}_{i}"
                with chunk_file.open("rb") as cf:
                    final_file.write(cf.read())
                os.remove(chunk_file)

    return JSONResponse(status_code=200, content={"status": "chunk uploaded"})

@router.get("/file", response_class=HTMLResponse)
async def upload_file():
    """
    Get the chat UI
    """
    return HTMLResponse(content=html)
