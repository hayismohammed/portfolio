"use strict";
(() => {
  const products = [
    {
      id: "cleanser",
      name: "غسول وجه لطيف",
      category: "skin",
      price: 45,
      desc: "عبوة بمضخة لتوزيع الكمية بسهولة، ضمن مجموعة العناية اليومية.",
    },
    {
      id: "moisturizer",
      name: "مرطب بشرة يومي",
      category: "skin",
      price: 69,
      desc: "عبوة بغطاء لولبي وتصميم بسيط، لتكتمل بها مجموعة العناية.",
    },
    {
      id: "sunscreen",
      name: "واقي شمس",
      category: "skin",
      price: 79,
      desc: "عبوة صغيرة بلون رملي، بتصميم يناسب حقيبة العناية اليومية.",
    },
    {
      id: "hair-oil",
      name: "زيت شعر",
      category: "hair",
      price: 55,
      desc: "عبوة كهرمانية بقطّارة تساعد على توزيع كمية صغيرة في كل مرة.",
    },
    {
      id: "conditioner",
      name: "بلسم للشعر",
      category: "hair",
      price: 49,
      desc: "عبوة بمضخة بلون هادئ، من قسم العناية بالشعر.",
    },
    {
      id: "rose",
      name: "عطر ورد",
      category: "perfume",
      price: 189,
      desc: "عبوة وردية بسيطة بغطاء داكن، تضيف لونًا هادئًا إلى ركن العطور.",
    },
    {
      id: "oud",
      name: "عطر عود",
      category: "perfume",
      price: 240,
      desc: "تصوّر لعطر بطابع خشبي، بعبوة داكنة وتفاصيل هادئة.",
    },
    {
      id: "lip",
      name: "مقشر شفاه",
      category: "skin",
      price: 29,
      desc: "عبوة دائرية صغيرة تكمل تشكيلة العناية اليومية.",
    },
  ];
  const basket = new Map();
  const money = (value) => String(value);
  const status = document.getElementById("store-status");
  const list = document.getElementById("cart-items");
  const totalQuantity = () => [...basket.values()].reduce((a, b) => a + b, 0);
  const tell = (message) => {
    status.textContent = message;
  };
  function renderCart(focusId = null, action = null) {
    const ids = [...basket.keys()];
    list.replaceChildren();
    for (const id of ids) {
      const item = products.find((p) => p.id === id),
        qty = basket.get(id);
      const li = document.createElement("li");
      li.className = "cart-row";
      const h = document.createElement("h3");
      h.textContent = item.name;
      const detail = document.createElement("p");
      detail.textContent = `${item.price} ر.س للوحدة · المجموع ${money(item.price * qty)} ر.س`;
      const controls = document.createElement("div");
      controls.className = "cart-controls";
      for (const [key, label, visible] of [
        ["minus", "تقليل كمية", "−"],
        ["plus", "زيادة كمية", "+"],
        ["remove", "حذف", "حذف"],
      ]) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.id = id;
        button.dataset.action = key;
        button.textContent = visible;
        button.setAttribute("aria-label", `${label} ${item.name}`);
        if (key === "minus" && qty === 1) {
          button.disabled = true;
          button.title = "استخدمي زر الحذف لإزالة المنتج";
        }
        controls.append(button);
        if (key === "minus") {
          const amount = document.createElement("span");
          amount.textContent = `الكمية: ${qty}`;
          controls.append(amount);
        }
      }
      li.append(h, detail, controls);
      list.append(li);
    }
    const count = totalQuantity();
    for (const id of ["cart-count", "summary-count"])
      document.getElementById(id).textContent = String(count);
    document.getElementById("cart-total").textContent = money(
      products.reduce((sum, p) => sum + p.price * (basket.get(p.id) || 0), 0),
    );
    document.getElementById("empty-cart").hidden = count > 0;
    if (focusId) {
      const row = [...list.querySelectorAll("button")].find(
        (b) =>
          b.dataset.id === focusId &&
          b.dataset.action === action &&
          !b.disabled,
      );
      (
        row ||
        list.querySelector("button:not(:disabled)") ||
        document.getElementById("cart")
      ).focus();
    }
  }
  document.querySelectorAll("[data-add]").forEach((button) =>
    button.addEventListener("click", () => {
      const id = button.dataset.add,
        item = products.find((p) => p.id === id);
      basket.set(id, (basket.get(id) || 0) + 1);
      renderCart();
      tell(
        `أُضيف ${item.name}. عدد الوحدات ${totalQuantity()}، والإجمالي ${document.getElementById("cart-total").textContent} ريال. سلة تجريبية.`,
      );
    }),
  );
  list.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const id = button.dataset.id,
      action = button.dataset.action,
      item = products.find((p) => p.id === id);
    if (action === "remove") basket.delete(id);
    else
      basket.set(
        id,
        Math.max(1, basket.get(id) + (action === "plus" ? 1 : -1)),
      );
    renderCart(id, action);
    tell(
      `${action === "remove" ? "حُذف" : "عُدّل"} ${item.name}. عدد الوحدات ${totalQuantity()}، والإجمالي ${document.getElementById("cart-total").textContent} ريال.`,
    );
  });
  document.querySelectorAll("[data-filter]").forEach((button) =>
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      document
        .querySelectorAll("[data-filter]")
        .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
      let count = 0;
      document.querySelectorAll("[data-category]").forEach((card) => {
        card.hidden = filter !== "all" && card.dataset.category !== filter;
        if (!card.hidden) count++;
      });
      tell(`تم عرض ${button.textContent}: ${count} منتجات.`);
    }),
  );
  renderCart();
})();
