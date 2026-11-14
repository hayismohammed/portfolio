# فحص الأداء والفهرسة والحضور المهني — 14 نوفمبر 2026

> نطاق التكليف: أداء Lighthouse ومؤشرات Core Web Vitals؛ جاهزية الفهرسة في Google؛ الملف الشخصي ومستودعات GitHub. **لا** يتضمن اختبار VoiceOver/ NVDA على جهاز فعلي — يحتفظ به مالك الموقع.

## المرجع ومصدر النسخة

- [سجل المستجدات المعتمد](https://docs.google.com/spreadsheets/d/1L1G5s0S1d9G8j8bRSMdyz8CXGVc9DeVNKSzb9PWtrP0/edit) — أحدث سجل معتمد سابق متاح بتاريخ 2026-11-12 01:59 بتوقيت الرياض.
- آخر `main` قبل بدء هذه الجولة: [b982f4c](https://github.com/hayismohammed/portfolio/commit/b982f4c37b9ea15eb2d97ed6668aa079413d70e3).
- لم تمس هذه الجولة الفيديو أو الصوت أو المنتجات أو أسعارها أو المستودع الجذري.

## 1. نتائج Lighthouse المخبرية

[Lighthouse 13.6 — أول تشغيل موثق](https://github.com/hayismohammed/portfolio/actions/runs/43557771024):

| المسار | محاكاة | الأداء | الوصول الآلي | أفضل الممارسات | SEO | LCP مخبري | TBT | CLS |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| الصفحة الرئيسية | سطح مكتب | 100 | 100 | 100 | 100 | 0.24 ثانية | 0 مللي ثانية | 0 |
| الصفحة الرئيسية | جوال | 76 | 100 | 100 | 100 | 2.00 ثانية | 1108 مللي ثانية | 0 |
| القهوة النموذجية | جوال | 88 | 100 | 96 | 100 | 0.81 ثانية | 472 مللي ثانية | 0 |
| دورة VoiceOver | جوال | 100 | 100 | 100 | 100 | 0.85 ثانية | 0 | 0 |
| مكتبة الأدلة | جوال | 100 | 100 | 100 | 0.78 ثانية | 0 | 0 |

[Lighthouse 13.6 — إعادة قياس مع التشخيص](https://github.com/hayismohammed/portfolio/actions/runs/43557998383):

- الرئيسية، جوال، إعادة أولى: أداء **80**، LCP **1.16 ثانية**، TBT **236 مللي ثانية**، CLS **0.311**.
- الرئيسية، جوال، إعادة ثانية: أداء **100**، LCP **0.95 ثانية**، TBT **0**، CLS **0**.
- القهوة، جوال: أداء **100**، LCP **0.81 ثانية**، TBT **45 مللي ثانية**، CLS **0**. أفضل الممارسات بقيت **96** بسبب فشل تحميل `/favicon.ico` من الجذر (HTTP 503 عند الفحص).
- الاختلاف الكبير بين تشغيلات متتابعة دون تغيير المحتوى يشير إلى حساسية النتائج لبيئة الاختبار؛ حذّر Lighthouse أيضًا من بطء المعالج في أول تشغيل للجوال. **هذه ليست قياسات تفاعل حقيقي أو إثباتًا للنتائج الميدانية.**

### معالجة مستندة إلى التشخيص

- **تجربة القائمة بالجوال:** كان شريط التنقل يظهر مبدئيًا قبل تشغيل JavaScript المؤجل ثم يُخفى عند تهيئة الزر. أضيف أسلوب إخفاء مؤقت فقط بوجود JavaScript حتى تكتمل التهيئة، مع إبقاء التنقل ظاهرًا في الوضع الخالي من JavaScript. الهدف منع إزاحة المحتوى عند بدء التحميل؛ لا نزعم تحسنًا محددًا دون إعادة القياس على الإصدار المنشور.
- **القهوة:** أُضيف رابط `favicon.svg` موجود داخل المعرض لتجنب طلب `/favicon.ico` من الجذر وما نتج عنه من خطأ متصفح في فحص Lighthouse.
- **الصور:** كشف Lighthouse إمكانية خفض أحجام صور معاينات الأعمال البعيدة عن منطقة العرض، مع أنها موسومة `loading=lazy`. لم نغيّر ملفات لقطات الأعمال الأصلية من دون ضرورة بصرية أو قياس مستقر.

**الفرق المهم:** مؤشرات Core Web Vitals الحقيقية هي LCP وINP وCLS عند الشريحة المئوية 75 خلال فترة مراقبة. Lighthouse يقيس LCP وCLS في المختبر ويستخدم TBT للتشخيص، ولا يعطي INP حقيقيًا. بيانات CrUX / Search Console الخاصة بالمستخدمين لم تتوفر عبر الموصلات الحالية. [المرجع الرسمي لمؤشرات الأداء](https://developers.google.com/search/docs/appearance/core-web-vitals).

## 2. جاهزية الفهرسة

- [خريطة الموقع](https://hayismohammed.github.io/portfolio/sitemap.xml) تشمل 11 مسارًا؛ ملفات الصفحات بها 11 عنوانًا مختلفًا، وصفوص Meta مختلفة، وCanonical مطابق للمسارات العامة.
- [ملف robots.txt في جذر النطاق](https://hayismohammed.github.io/robots.txt) يحيل إلى خريطتي جذر الموقع والمعرض، ولا يضع حظرًا على المعرض.
- لا توجد علامة `noindex` في الصفحات الإحدى عشرة؛ مصدر الصفحة الرئيسية يحتوي على `google-site-verification`.
- عُدّل `lastmod` للصفحة الرئيسية والقهوة إلى 2026-11-14 فقط؛ وهو يوم تغيرهما الفعلي، دون تحديث مصطنع لبقية الصفحات.
- أُضيف اختبار `tests/check_search_readiness.py` إلى GitHub Actions لتأكيد هذه الشروط وصحة JSON-LD المتاح.

**غير مؤكد:** عدد الروابط المفهرسة لدى Google، آخر زحف، مشاكل الفهرسة المستبعدة أو النقرات والظهور؛ كلها تحتاج صلاحية مستخدم موقع في [Google Search Console](https://search.google.com/search-console). لا يعتبر فحص `site:` العام أو درجة SEO = 100 بديلًا عن أداة فحص عنوان URL. [مرجع Google الرسمي](https://developers.google.com/search/docs/monitor-debug/search-console-start).

## 3. GitHub: نتائج مؤكدة ومتطلبات ضبط الحساب

عند الفحص كانت بيانات [المستودع](https://api.github.com/repos/hayismohammed/portfolio) تتضمن وصفًا عربيًا صحيحًا ولكن `homepage=null` و`topics=[]`. كذلك أعاد اتصال GitHub الحساب الشخصي `name=null`. لا توفر الإجراءات المتصلة حاليًا كتابة حقول **Public profile** أو إعدادات **About** للمستودعات؛ لا يجوز اعتبارها معدّلة.

### نصوص جاهزة لتحديث الحقول من صفحة GitHub نفسها

- **Public profile / Name:** `هايس العنزي | Hayis Alanazi`
- **Public profile / Bio:** `أصمم صفحات هبوط عربية وأكتب محتوى المنتجات، وأقدم دورات وأدلة تقنية تراعي سهولة الوصول.`
- **Public profile / Website:** `https://hayismohammed.github.io/portfolio/`
- **portfolio / About / Website:** `https://hayismohammed.github.io/portfolio/`
- **portfolio / Topics:** `portfolio`, `arabic`, `rtl`, `accessibility`, `web-design`, `landing-page`, `github-pages`
- **hayismohammed.github.io / About / Website:** `https://hayismohammed.github.io/`

[الإعدادات الشخصية](https://github.com/settings/profile) · [مستودع المعرض](https://github.com/hayismohammed/portfolio) · [المستودع الجذري](https://github.com/hayismohammed/hayismohammed.github.io) · [كيفية تعديل الملف الشخصي — GitHub](https://docs.github.com/en/account-and-profile/tutorials/personalize-your-profile).

**الخصوصية:** لا تُضف رقم الهاتف، ولا تغيّر عنوان الدخول أو البريد الخاص بالحساب. المستخدم فوّض تعديل البيانات المهنية العامة، لا إعدادات الأمان أو الصلاحيات.

## دليل اختبار فعلي قبل الدمج

- [نجاح Chrome على الجوال والكمبيوتر ووضع JavaScript المعطل](https://github.com/hayismohammed/portfolio/actions/runs/43558409834): تم اختبار زر القائمة، وEscape، واستعادة قائمة الكمبيوتر بعد الاستجابة لتغيير المقاس، وإتاحة روابط القائمة مع تعطيل JavaScript. فشل التشغيل الأول لأن الاختبار فحص حالة مقاس الكمبيوتر قبل وصول حدث تغيير العرض، ثم صُحّح الاختبار وأُعيد بنجاح.
- [نجاح فحص SEO بعد تصحيح كاشف noindex](https://github.com/hayismohammed/portfolio/actions/runs/43558030851).
- [نجاح فحص جميع صفحات المستودع بعد تغييرات القائمة والأيقونة](https://github.com/hayismohammed/portfolio/actions/runs/43558188300).
- حُذفت إجراءات Lighthouse وChrome المؤقتة من فرع التسليم بعد أخذ الأدلة، منعًا لتشغيل فحوص ثقيلة مع كل تحديث.
- **لم تكتمل** مراجعة Google Search Console الخاصة بالمالك أو كتابة حقول GitHub الشخصية/metadata؛ الموصل المتاح لا يسمح بهذه الأفعال. تبقى هذه الحدود صريحة حتى تتصل الأداة المناسبة أو تُحدّث الحقول من إعدادات الموقع.

## التحقق بعد الدمج

لا تُسجَّل هنا نتيجة نشر أو اختبار حي للنسخة المدمجة قبل التحقق الفعلي منها.
