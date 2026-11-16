from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

file_router = APIRouter(tags=["File"])

# 파일 저장 경로 설정
FILE_DIR = Path(__file__).resolve().parent.parent / "static" / "files"
FILE_DIR.mkdir(parents=True, exist_ok=True)

# 파일 업로드 구현
@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = Path(file.filename).name
    if not filename:
        raise HTTPException(status_code=400, detail="파일명이 없습니다")

    with open(FILE_DIR / filename, "wb") as f:
        f.write(await file.read())
    return {"filename": filename, "message": "업로드 완료"}

#파일 다운로드 구현
@file_router.get("/download")
def download_file(filename: str):
    file_path = FILE_DIR / Path(filename).name
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="파일이 없습니다")
    return FileResponse(
        file_path, media_type="application/octet-stream", filename=file_path.name
    )

#파일 리스트로 나열
@file_router.get("")
def list_files() -> dict:
    files = sorted(p.name for p in FILE_DIR.iterdir() if p.is_file())
    return {"count": len(files), "files": files}
