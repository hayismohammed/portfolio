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
  const storageKey = "hayis-portfolio-lamsa-cart-v1";
  const maxQuantity = 99;
  const storageNote = document.getElementById("cart-storage-note");
  let storageAvailable = true;
  let restored = false;
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved !== null) {
      const entries = JSON.parse(saved);
      if (!Array.isArray(entries) || entries.length > products.length)
        throw new Error("Invalid cart");
      for (const entry of entries) {
        if (
          entry &&
          products.some((p) => p.id === entry.id) &&
          Number.isSafeInteger(entry.quantity) &&
          entry.quantity >= 1 &&
          entry.quantity <= maxQuantity
        ) {
          basket.set(entry.id, entry.quantity);
        }
      }
      restored = basket.size > 0;
    }
  } catch {
    storageAvailable = false;
  }
  function describeStorage() {
    storageNote.textContent = storageAvailable
      ? "تُحفظ المنتجات والكميات محليًا في هذا المتصفح، دون إرسالها إلى خادم. قد يمحو المتصفح بياناتها عند مسح بيانات المواقع أو إنهاء التصفح الخاص."
      : "تعذر حفظ السلة أو قراءة نسختها السابقة. يمكنك متابعة التجربة، لكن قد لا تبقى التغييرات بعد تحديث الصفحة.";
  }
  function saveBasket() {
    try {
      if (basket.size) {
        localStorage.setItem(
          storageKey,
          JSON.stringify(
            [...basket].map(([id, quantity]) => ({ id, quantity })),
          ),
        );
      } else {
        localStorage.removeItem(storageKey);
      }
      storageAvailable = true;
    } catch {
      storageAvailable = false;
    }
    describeStorage();
  }
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
        if (key === "plus" && qty === maxQuantity) button.disabled = true;
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
    document.getElementById("clear-cart").disabled = count === 0;
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
      if ((basket.get(id) || 0) === maxQuantity) {
        tell(`الحد الأقصى في التجربة ${maxQuantity} وحدة من ${item.name}.`);
        return;
      }
      basket.set(id, (basket.get(id) || 0) + 1);
      saveBasket();
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
        Math.min(
          maxQuantity,
          Math.max(1, basket.get(id) + (action === "plus" ? 1 : -1)),
        ),
      );
    saveBasket();
    renderCart(id, action);
    tell(
      `${action === "remove" ? "حُذف" : "عُدّل"} ${item.name}. عدد الوحدات ${totalQuantity()}، والإجمالي ${document.getElementById("cart-total").textContent} ريال.`,
    );
  });
  document.getElementById("clear-cart").addEventListener("click", () => {
    basket.clear();
    saveBasket();
    renderCart();
    document.getElementById("cart").focus();
    tell(
      storageAvailable
        ? "أُفرغت السلة التجريبية وحُذفت نسختها المحفوظة من هذا المتصفح."
        : "أُفرغت السلة في الصفحة، لكن تعذر حذف نسختها المحفوظة من المتصفح.",
    );
  });
  const search = document.getElementById("product-search");
  const sort = document.getElementById("product-sort");
  const grid = document.getElementById("product-grid");
  const cards = [...grid.children].map((card, index) => ({
    card,
    index,
    product: products.find(
      (p) => p.id === card.querySelector("[data-add]").dataset.add,
    ),
  }));
  const normalize = (value) =>
    value
      .toLocaleLowerCase("ar")
      .replace(/[\u064b-\u065f\u0670\u0640]/g, "")
      .replace(/[أإآٱ]/g, "ا")
      .replace(/ى/g, "ي")
      .replace(/ة/g, "ه");
  let filter = "all";
  function showProducts() {
    const query = normalize(search.value.trim());
    const ordered = [...cards].sort((a, b) => {
      if (sort.value === "price-asc")
        return a.product.price - b.product.price || a.index - b.index;
      if (sort.value === "price-desc")
        return b.product.price - a.product.price || a.index - b.index;
      return a.index - b.index;
    });
    let count = 0;
    for (const { card, product } of ordered) {
      card.hidden =
        (filter !== "all" && product.category !== filter) ||
        !normalize(`${product.name} ${product.desc}`).includes(query);
      if (!card.hidden) count++;
      grid.append(card);
    }
    document.getElementById("no-products").hidden = count !== 0;
    document.getElementById("product-results").textContent =
      `عدد المنتجات المطابقة: ${count} من ${products.length}.`;
  }
  const filters = [...document.querySelectorAll("[data-filter]")];
  function selectFilter(value) {
    filter = value;
    filters.forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.filter === filter),
      ),
    );
  }
  filters.forEach((button) =>
    button.addEventListener("click", () => {
      selectFilter(button.dataset.filter);
      showProducts();
    }),
  );
  search.addEventListener("input", showProducts);
  sort.addEventListener("change", showProducts);
  document.getElementById("reset-products").addEventListener("click", () => {
    search.value = "";
    sort.value = "default";
    selectFilter("all");
    showProducts();
    search.focus();
  });
  document.getElementById("store-tools").hidden = false;
  describeStorage();
  showProducts();
  renderCart();
  if (restored)
    tell(
      `استُعيدت السلة المحفوظة: ${totalQuantity()} وحدة، والإجمالي ${document.getElementById("cart-total").textContent} ريال.`,
    );
})();
