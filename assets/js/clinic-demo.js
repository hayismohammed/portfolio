"use strict";
(() => {
  const form = document.getElementById("appointment-form");
  const date = document.getElementById("dt");
  const period = document.getElementById("period");
  const help = document.getElementById("period-help");
  const status = document.getElementById("appointment-status");
  const now = new Date();
  const today = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, "0"),
    String(now.getDate()).padStart(2, "0"),
  ].join("-");
  date.min = today;
  const normalize = (value) =>
    value
      .replace(/[٠-٩]/g, (c) => String(c.charCodeAt(0) - 1632))
      .replace(/[۰-۹]/g, (c) => String(c.charCodeAt(0) - 1776));
  const weekdayPeriods = [
    ["morning", "صباحًا — 9 إلى 12"],
    ["afternoon", "ظهرًا — 12 إلى 4"],
    ["evening", "مساءً — 4 إلى 9"],
  ];
  function selectedDay() {
    if (!date.value || date.value < today) return null;
    const day = new Date(date.value + "T12:00:00").getDay();
    return Number.isNaN(day) ? null : day;
  }
  function availablePeriods() {
    const day = selectedDay();
    if (day === null || day === 5) return [];
    return day === 6 ? [["evening", "مساءً — 4 إلى 10"]] : weekdayPeriods;
  }
  function updatePeriods() {
    const previous = period.value;
    const options = availablePeriods();
    period.replaceChildren();
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "اختر الفترة";
    period.append(placeholder);
    for (const [value, label] of options) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      period.append(option);
    }
    period.disabled = options.length === 0;
    if (options.some(([value]) => value === previous)) period.value = previous;
    const day = selectedDay();
    help.textContent =
      day === 5
        ? "العيادة مغلقة يوم الجمعة. اختر تاريخًا آخر."
        : day === null
          ? "اختر تاريخ اليوم أو يومًا لاحقًا لعرض الفترات المتاحة."
          : day === 6
            ? "يوم السبت: فترة مسائية واحدة من 4 مساءً إلى 10 مساءً."
            : "الفترات تغطي الدوام من 9 صباحًا إلى 9 مساءً: صباحية، وظهرية، ومسائية.";
    status.textContent = "";
    for (const [input, error] of [
      [date, "date-error"],
      [period, "period-error"],
    ]) {
      input.removeAttribute("aria-invalid");
      document.getElementById(error).textContent = "";
    }
  }
  date.addEventListener("change", updatePeriods);
  form.addEventListener("reset", () => setTimeout(updatePeriods, 0));
  updatePeriods();
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const day = selectedDay();
    const checks = [
      [
        "nm",
        "name-error",
        (v) => v.trim().length >= 3,
        "اكتب اسمًا من ثلاثة أحرف على الأقل.",
      ],
      [
        "ph",
        "phone-error",
        (v) => /^05\d{8}$/.test(normalize(v.trim())),
        "اكتب رقمًا من 10 أرقام يبدأ بـ 05.",
      ],
      [
        "dt",
        "date-error",
        () => day !== null && day !== 5,
        day === 5
          ? "العيادة مغلقة يوم الجمعة. اختر يومًا آخر."
          : "اختر تاريخ اليوم أو تاريخًا لاحقًا.",
      ],
      [
        "period",
        "period-error",
        (v) => availablePeriods().some(([value]) => value === v),
        "اختر إحدى الفترات المتاحة لليوم المحدد.",
      ],
    ];
    let first = null;
    for (const [id, error, valid, message] of checks) {
      const input = document.getElementById(id);
      const ok = valid(input.value);
      input.setAttribute("aria-invalid", String(!ok));
      document.getElementById(error).textContent = ok ? "" : message;
      if (!ok && !first) first = input;
    }
    if (first) {
      status.textContent = "";
      first.focus();
      return;
    }
    const service = document.getElementById("sv").value;
    const spokenDate = new Intl.DateTimeFormat("ar-SA-u-ca-gregory", {
      dateStyle: "full",
    }).format(new Date(date.value + "T12:00:00"));
    status.textContent = `تمت معاينة اختيارك: ${service}، بتاريخ ${spokenDate}، ${period.selectedOptions[0].textContent}. لم يُرسل شيء؛ هذه معاينة وليست تأكيد حجز.`;
  });
})();
