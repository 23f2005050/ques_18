from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request
from fastapi.responses import JSONResponse
import csv
import io
from collections import Counter

app = FastAPI()

# ✅ Correct CORS headers (UPDATED to your required token header)
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Upload-Token-4748",
    "Access-Control-Expose-Headers": "Access-Control-Allow-Origin",
}

VALID_TOKEN = "mhhv4fmvj2xjn5n5"
MAX_FILE_SIZE = 54 * 1024
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt"}


# ✅ Handle Preflight Request
@app.options("/upload")
async def options_upload():
    return JSONResponse(content={}, headers=CORS_HEADERS)


@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "Upload endpoint: POST /upload with header X-Upload-Token-4748 and form file 'file'",
            "allowedMethods": ["POST", "OPTIONS"]
        },
        headers=CORS_HEADERS
    )


@app.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    x_upload_token_4748: str = Header(None)
):

    # 1️⃣ Authentication
    if x_upload_token_4748 != VALID_TOKEN:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"},
            headers=CORS_HEADERS
        )

    # 2️⃣ File Type Validation
    filename = file.filename
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid file type"},
            headers=CORS_HEADERS
        )

    # 3️⃣ File Size Validation
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse(
            status_code=413,
            content={"detail": "File too large"},
            headers=CORS_HEADERS
        )

    # If not CSV, accept but don’t process
    if not filename.endswith(".csv"):
        return JSONResponse(
            content={
                "email": "23f2003450@ds.study.iitm.ac.in",
                "filename": filename,
                "message": "File accepted but not processed"
            },
            headers=CORS_HEADERS
        )

    # 4️⃣ Process CSV
    decoded = contents.decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(decoded))

    rows = 0
    total_value = 0.0
    category_counter = Counter()
    columns = csv_reader.fieldnames

    for row in csv_reader:
        rows += 1
        try:
            total_value += float(row["value"])
        except:
            pass

        category = row.get("category")
        if category:
            category_counter[category] += 1

    return JSONResponse(
        content={
            "email": "23f2003450@ds.study.iitm.ac.in",
            "filename": filename,
            "rows": rows,
            "columns": columns,
            "totalValue": round(total_value, 2),
            "categoryCounts": dict(category_counter)
        },
        headers=CORS_HEADERS
    )