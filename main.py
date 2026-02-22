from fastapi import FastAPI, File, UploadFile, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
from collections import Counter

app = FastAPI()

# ✅ CORS (CRITICAL FOR EXAM)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_TOKEN = "1f55ttd6zehw8pf3"
MAX_FILE_SIZE = 58 * 1024  # 58KB
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt"}


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_2757: str = Header(None)
):

    # ✅ 1️⃣ Authentication
    if x_upload_token_2757 != VALID_TOKEN:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    filename = file.filename

    # ✅ 2️⃣ File Type Validation
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid file type"}
        )

    # ✅ 3️⃣ File Size Validation
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse(
            status_code=413,
            content={"detail": "File too large"}
        )

    # ✅ Accept non-CSV files
    if not filename.endswith(".csv"):
        return {
            "message": "File accepted",
            "filename": filename
        }

    # ✅ 4️⃣ CSV Processing
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

    return {
        "email": "23f2005050@ds.study.iitm.ac.in",
        "filename": filename,
        "rows": rows,
        "columns": columns,
        "totalValue": round(total_value, 2),
        "categoryCounts": dict(category_counter)
    }