# تدقيق التكرار — 20 نوفمبر 2026

الحالة: مراجعة مصدر HTML بعد الإصلاح؛ لا تمثل شجرة وصول أو اختبار NVDA. نطاقها 14 صفحة عامة في المستودعين؛ لا تشمل نصوص الوسائط أو الحالات الديناميكية بعد تشغيل JavaScript.

## القاعدة
تُحذف المعلومة المعادة إذا لم تضف سياقًا أو وظيفة، مع إبقاء أسماء الروابط وعناوين مسارات التنقل، والبيانات اللازمة في بطاقة المنتج، والمقارنات التعليمية، والحقوق النظامية. تُقيّم التسميات المسموعة بعد تشغيل المتصفح قبل ادعاء «صفر تكرار».

| الصفحة | دليل المصدر | نتيجة مراجعة المصدر |
|---|---|---|
| الرئيسية | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/index.html) | أُفرغت alt للقطات الثماني لأن العناوين والأوصاف والروابط المجاورة تعرّف النماذج؛ اختُصر نص توفر الخدمات. |
| 404 | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/404.html) | لا تكرار معلوماتي مثبت يستدعي تغيير المصدر؛ فحص المسار الحي معلّق. |
| مكتبة الأدلة | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/guides/index.html) | العنوان في مسار التنقل ثم h1 لتحديد الموقع؛ الوصف والخطوات يضيفان متطلبات وإجراءً، لا حشو مثبتًا. |
| دليل Hermex | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/guides/hermex-hermes-windows/index.html) | العنوان المتكرر في مسار التنقل وh1 سياقي؛ المتطلبات والأمان والمحتوى والمراجع تؤدي وظائف مختلفة. |
| العيادة | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/clinic/index.html) | التنبيه ونموذج الموعد وخصوصية المدخلات مختلفة؛ لا عبارة زائدة مؤكدة من المصدر. |
| لمسة | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/cosmetics-store/index.html) | أسماء المنتجات والوصف والسعر وأزرار السلة متمايزة؛ صور المنتجات الزخرفية ذات alt فارغ وتليها بيانات نصية. |
| وصف مِداد | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/product-copy/index.html) | تكرار المواصفات مقصود لمقارنة قبل التحرير وبعده والبطاقة المختصرة؛ لم نحذف المقارنة التعليمية. |
| بيت الكرم | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/restaurant/index.html) | اسم الطبق ووصفه وسعره نص مستقل بجانب الصور ذات alt فارغ؛ تعليمات التبويبات فريدة. |
| القهوة | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/salla-coffee/index.html) | حُصر العنوان الكامل للمنتج في البطاقة، والتنبيه عن الرسائل في فقرة التواصل، والدعوة بالبريد في قسم طلب الخدمة. أبقيت بنود السياسات النظامية. |
| صفاء | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/serum-landing/index.html) | حُذفت صورة 8054400.jpg المكررة في المعرض، وقسم افتتاحي يكرر مزايا البطاقات، وأسئلة تعيد معلومات الحجم والقطارة. |
| إعلان مِداد | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/short-ad/index.html) | تفريغ الكلام ووصف المشاهد مقصودان لإتاحة الفيديو؛ روابط النسخ والترجمة موارد مستقلة. |
| دورة VoiceOver | [المصدر](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/voiceover-course/index.html) | المدة في ملخص الدورة والمنهج التفصيلي تؤدي وظيفتين؛ تكرار عنوان الدرس في المعاينة والمنهج يحدد موضعه. |
| تحويل الجذر | [المصدر](https://github.com/hayismohammed/hayismohammed.github.io/blob/rashed/final-audit-2026-11-20/index.html) | اختُصر الرابط الاحتياطي إلى «افتح المعرض»، وبقي عنوان الصفحة الكامل مرة واحدة. |
| 404 الجذر | [المصدر](https://github.com/hayismohammed/hayismohammed.github.io/blob/rashed/final-audit-2026-11-20/404.html) | رسالة الخطأ وروابط العودة مختلفة؛ لا تكرار معلوماتي مثبت. |

## تغييرات محددة
- [الجذر، السطر 48](https://github.com/hayismohammed/hayismohammed.github.io/blob/rashed/final-audit-2026-11-20/index.html#L48): رابط مختصر واسم الصفحة الكامل مرة واحدة.
- [القهوة، السطور 369–370 و412 و476–503](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/salla-coffee/index.html#L369): عنوان المنتج الكامل في البطاقة؛ فقرة واحدة «النموذج لا يرسل رسائل»؛ رابط خدمة واحد بالبريد في قسم الطلب. وصف المجموعة والزر لا يعيدان التنبيه.
- [المعرض، السطور 120–194](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/index.html#L120): ثماني لقطات alt="" لأن النصوص المحيطة تحمل أسماء النماذج ونوعها ووظيفتها. يلزم التأكد بصريًا من عدم وجود معلومة فريدة في الصور.
- [صفاء، السطور 401–520](https://github.com/hayismohammed/portfolio/blob/rashed/final-audit-2026-11-20/samples/serum-landing/index.html#L401): بقيت نسخة واحدة من 8054400.jpg، وصور المعرض الباقية مختلفة. حُذف السؤالان اللذان يعيدان الحجم والقطارة.

## لم يُفحص بعد
شجرة الوصول بعد JavaScript، نطق NVDA الفعلي، ترتيب التركيز، محتوى الفيديو والصوت، النصوص التي تنشئها السكربتات، وفحص بصري لتمييز معلومات الصور. يعيد راشد معالجة ما يثبته تعليق الفحص الذي يبدأ «يا راشد» على طلب الدمج نفسه.
