"use strict";
(() => {
  const date = document.getElementById("dt"),
    period = document.getElementById("period");
  const now = new Date(),
    today = [
      now.getFullYear(),
      String(now.getMonth() + 1).padStart(2, "0"),
      String(now.getDate()).padStart(2, "0"),
    ].join("-");
  date.min = today;
  const normalize = (v) =>
    v
      .replace(/[٠-٩]/g, (c) => String(c.charCodeAt(0) - 1632))
      .replace(/[۰-۹]/g, (c) => String(c.charCodeAt(0) - 1776));
  document
    .getElementById("appointment-form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      const day = date.value
        ? new Date(date.value + "T12:00:00").getDay()
        : null;
      const checks = [
        [
          "nm",
          "name-error",
          (v) => v.trim().length >= 3,
          "اكتب اسمًا تجريبيًا من ثلاثة أحرف على الأقل.",
        ],
        [
          "ph",
          "phone-error",
          (v) => /^05\d{8}$/.test(normalize(v.trim())),
          "اكتب رقمًا تجريبيًا من 10 أرقام يبدأ بـ 05.",
        ],
        [
          "dt",
          "date-error",
          (v) => !!v && v >= today && day !== 5,
          day === 5
            ? "العيادة مغلقة يوم الجمعة. اختر يومًا آخر."
            : "اختر تاريخ اليوم أو تاريخًا لاحقًا.",
        ],
        [
          "period",
          "period-error",
          (v) => !!v && !(day === 6 && v === "morning"),
          "اختر فترة متاحة؛ يوم السبت الفترة المسائية فقط.",
        ],
      ];
      let first = null;
      for (const [id, err, valid, message] of checks) {
        const input = document.getElementById(id),
          ok = valid(input.value);
        input.setAttribute("aria-invalid", String(!ok));
        document.getElementById(err).textContent = ok ? "" : message;
        if (!ok && !first) first = input;
      }
      const status = document.getElementById("appointment-status");
      if (first) {
        status.textContent = "";
        first.focus();
        return;
      }
      const service = document.getElementById("sv").value;
      status.textContent = `اختيارك التجريبي: ${service}، بتاريخ ${date.value}، ${period.selectedOptions[0].textContent}. تم التحقق محليًا؛ لم يُرسل شيء ولم يُحجز موعد.`;
    });
})();
