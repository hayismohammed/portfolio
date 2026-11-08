"use strict";
(() => {
  const menu = {
      "الأطباق الرئيسية": [
        [
          "كبسة لحم",
          "أرز متبّل مع قطع لحم وتزيين بالخضرة، بتقديم مستوحى من المائدة السعودية.",
          65,
          "kabsa",
        ],
        [
          "مندي دجاج",
          "دجاج مع أرز طويل الحبة وتوابل دافئة، في طبق للمشاركة على المائدة.",
          45,
          "mandi",
        ],
        [
          "مرقوق",
          "رقائق عجين مع خضار ولحم في مرق غني، بطابع منزلي.",
          38,
          "marqooq",
        ],
      ],
      المقبلات: [
        [
          "سمبوسة",
          "ست حبات مقرمشة بتقديم بسيط، لبداية خفيفة مع الوجبة.",
          18,
          "samosa",
        ],
        [
          "سلطة",
          "تشكيلة خضار بألوان متنوعة، لترافق الأطباق الرئيسية.",
          12,
          "salad",
        ],
      ],
      الحلى: [
        ["كليجا", "أقراص حلوى سعودية متبّلة، تُقدَّم مع القهوة.", 15, "kleija"],
        [
          "لقيمات",
          "كرات عجين ذهبية مع لمسة دبس، بتقديم للمشاركة.",
          16,
          "luqaimat",
        ],
      ],
      المشروبات: [
        [
          "قهوة سعودية",
          "قهوة بلمسة هيل، تُقدَّم مع التمر لإكمال الجلسة.",
          20,
          "coffee",
        ],
        [
          "شاي بالنعناع",
          "إبريق شاي بنكهة النعناع، يناسب جلسة ما بعد الطعام.",
          12,
          "tea",
        ],
      ],
    },
    keys = Object.keys(menu),
    tabs = document.getElementById("menu-tabs"),
    panel = document.getElementById("menu-panel");
  function show(index) {
    [...tabs.children].forEach((button, i) => {
      button.setAttribute("aria-selected", String(i === index));
      button.tabIndex = i === index ? 0 : -1;
    });
    panel.setAttribute("aria-labelledby", "menu-tab-" + index);
    panel.replaceChildren();
    for (const [name, desc, price, image] of menu[keys[index]]) {
      const article = document.createElement("article");
      article.className = "menu-item";
      const img = document.createElement("img");
      img.src = "../../assets/media/demo/" + image + ".svg";
      img.alt = "";
      img.width = 640;
      img.height = 480;
      const content = document.createElement("div"),
        h = document.createElement("h3"),
        p = document.createElement("p"),
        amount = document.createElement("p");
      h.textContent = name;
      p.textContent = desc;
      amount.className = "price";
      amount.textContent = price + " ر.س";
      content.append(h, p);
      article.append(img, content, amount);
      panel.append(article);
    }
  }
  keys.forEach((name, i) => {
    const button = document.createElement("button");
    button.type = "button";
    button.id = "menu-tab-" + i;
    button.setAttribute("role", "tab");
    button.setAttribute("aria-controls", "menu-panel");
    button.textContent = name;
    button.addEventListener("click", () => show(i));
    button.addEventListener("keydown", (event) => {
      let n = null;
      if (event.key === "ArrowLeft") n = (i + 1) % keys.length;
      if (event.key === "ArrowRight") n = (i - 1 + keys.length) % keys.length;
      if (event.key === "Home") n = 0;
      if (event.key === "End") n = keys.length - 1;
      if (n === null) return;
      event.preventDefault();
      show(n);
      tabs.children[n].focus();
    });
    tabs.append(button);
  });
  show(0);
  document.getElementById("menu-fallback").hidden = true;
  tabs.hidden = false;
  panel.hidden = false;
})();
