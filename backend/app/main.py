from pathlib import Path
import ast
import os
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DevMind AI", version="0.1.0",
              description="MVP: Python code analysis and weakness recommendations")

# Set ALLOWED_ORIGINS in the cloud host, e.g. https://your-site.netlify.app
# Local development origins are included by default.
_default_origins = "http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500"
_allowed_origins = os.getenv("ALLOWED_ORIGINS", _default_origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in _allowed_origins.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

MAX_FILE_BYTES = 200_000
ALLOWED_SUFFIXES = {".py"}


def analyze_python(source: str) -> dict[str, Any]:
    """Small deterministic starter analyzer; it does not execute submitted code."""
    findings: list[dict[str, Any]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {
            "ok": False,
            "summary": "تعذر تحليل الملف بسبب خطأ نحوي.",
            "findings": [{
                "severity": "high",
                "title": "Syntax error",
                "line": exc.lineno or 1,
                "evidence": exc.msg,
                "recommendation": "راجع السطر المشار إليه وأصلح الصياغة ثم أعد الفحص.",
            }],
        }

    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append({
                "severity": "medium",
                "title": "استثناء عام جدًا",
                "line": node.lineno,
                "evidence": "except: يلتقط كل الاستثناءات، بما فيها حالات يصعب تشخيصها.",
                "recommendation": "التقط أنواع الاستثناءات المتوقعة وسجّل الخطأ مع سياق مناسب.",
            })
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                findings.append({
                    "severity": "high",
                    "title": "استخدام eval",
                    "line": node.lineno,
                    "evidence": "eval ينفّذ تعبيرًا كنص برمجي وقد يخلق خطرًا أمنيًا عند التعامل مع مدخلات غير موثوقة.",
                    "recommendation": "تجنب eval؛ استخدم parsing أو تحويلًا صريحًا يناسب نوع البيانات.",
                })
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.end_lineno and node.end_lineno - node.lineno + 1 > 50:
                findings.append({
                    "severity": "low",
                    "title": "دالة طويلة نسبيًا",
                    "line": node.lineno,
                    "evidence": f"الدالة {node.name} تمتد على {node.end_lineno - node.lineno + 1} سطرًا.",
                    "recommendation": "راجع إمكانية تقسيم الدالة إلى وظائف صغيرة ذات مسؤوليات واضحة، إذا كان ذلك يحسن القراءة والاختبار.",
                })

    for index, line in enumerate(lines, start=1):
        if line.rstrip() != line:
            findings.append({
                "severity": "low",
                "title": "مسافات زائدة في نهاية السطر",
                "line": index,
                "evidence": "يوجد فراغ أو tab في نهاية السطر.",
                "recommendation": "شغّل Ruff formatter أو أزل المسافات الزائدة.",
            })

    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (severity_order.get(f["severity"], 3), f["line"]))
    return {
        "ok": True,
        "summary": f"اكتمل الفحص. تم العثور على {len(findings)} ملاحظة.",
        "findings": findings,
        "note": "هذا فحص أولي وليس بديلًا عن مراجعة أمنية أو اختبارات كاملة.",
    }


@app.get("/health")
def health():
    return {"status": "ok", "app": "DevMind AI"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    if Path(filename).suffix.lower() not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=415, detail="النسخة الأولى تدعم ملفات Python (.py) فقط.")
    content = await file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف أكبر من الحد المسموح (200 KB).")
    try:
        source = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بترميز UTF-8.")
    result = analyze_python(source)
    result["filename"] = filename
    return result
