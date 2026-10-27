# DevMind AI — تطوير محلي ونشر تجريبي عام

المشروع الآن يتكوّن من واجهة ثابتة (Netlify) وواجهة API بـ FastAPI (Render). محلل Python الحالي حقيقي لكنه أولي وقائم على قواعد ثابتة؛ لا توجد بعد نماذج LLM أو RAG أو إنشاء Pull Requests حقيقية.

## تشغيل محلي على macOS

افتح Terminal في مجلد المشروع. شغّل الواجهة في نافذة أولى:

```bash
python3 -m http.server 5500 --directory frontend
```

في نافذة ثانية:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

افتح http://127.0.0.1:5500. إعداد الواجهة المحلي موجود في `frontend/config.js`.

## النشر العام

### 1. انشر الـ Backend على Render

1. ادفع مجلد المشروع إلى مستودع GitHub.
2. في Render اختر New > Blueprint ثم اختر المستودع الذي يحتوي على `render.yaml`.
3. أضف قيمة `ALLOWED_ORIGINS` بعد إنشاء موقع Netlify، مثل `https://your-site-name.netlify.app` (بدون شرطة مائلة في النهاية).
4. بعد النشر، اختبر `https://YOUR-API.onrender.com/health`.

### 2. اربط الواجهة بعنوان API السحابي

عدّل `frontend/config.js` ليحتوي على رابط API الحقيقي:

```js
window.DEVMIND_CONFIG = {
  API_BASE_URL: 'https://YOUR-API.onrender.com'
};
```

لا تضع مفاتيح سرية في هذا الملف؛ فهو يُرسل إلى كل زائر.

### 3. انشر الواجهة على Netlify

استورد مستودع GitHub في Netlify. إعداد `netlify.toml` يحدد `frontend` كمجلد النشر. بعد أي تعديل ورفعه إلى GitHub، ستعيد Netlify بناء الموقع تلقائيًا إذا كان الربط بالمستودع مفعّلًا.

## ما يعمل فعلًا الآن

- `GET /health` لفحص الخدمة.
- `POST /analyze` لاستقبال ملف `.py` بحد أقصى 200 KB وتحليل قواعد أولية مثل `eval` و`except:` العاري والدوال الطويلة والمسافات النهائية.
- الواجهة تستدعي API وتعرض نتائج التحليل الفعلية.
- إعداد عنوان API منفصل في `frontend/config.js`.

## ما زال تجريبيًا أو غير مكتمل

- أرقام لوحة التحكم وبعض بطاقات الإصلاح/الاختبارات في التصميم بيانات توضيحية، وليست إحصائيات حيّة. لا تعتمد عليها كقياسات فعلية.
- إنشاء GitHub Pull Request وCI غير مفعّل.
- لا يوجد RAG أو LLM مدمج حتى الآن.

## قبل مشاركة الرابط مع الجمهور

- لا ترفع ملفات سرية أو مشاريع خاصة إلى النسخة العامة.
- أضف تحديد معدل الطلبات (rate limiting) ومراقبة الاستخدام قبل توسيع الجمهور.
- ضع حدًا لحجم الطلبات وأضف تحققًا من نوع الملفات. لا تشغّل كود المستخدمين على الخادم.
- تذكّر أن خدمة الاستضافة المجانية قد تدخل في وضع السكون أو تفرض حدود استخدام.
