"use strict";
(() => {
  const products = new Map([
    ["ethiopia", { name: "إثيوبيا المغسول", price: 72 }],
    ["colombia", { name: "كولومبيا المعالجة العسلية", price: 68 }],
    ["house", { name: "خلطة الدار", price: 59 }],
  ]);
  const basket = new Map();
  const list = document.getElementById("coffee-cart-items");
  const status = document.getElementById("coffee-cart-status");
  const clear = document.getElementById("coffee-clear-cart");
  const cart = document.getElementById("cart");
  const maxQuantity = 99;
  const summary = () => [...basket].reduce(
    (sum, [id, qty]) => ({ count: sum.count + qty, total: sum.total + products.get(id).price * qty }),
    { count: 0, total: 0 },
  );
  function render(focusId = null, action = null) {
    list.replaceChildren();
    for (const [id, qty] of basket) {
      const product = products.get(id);
      const row = document.createElement("li");
      const heading = document.createElement("h3");
      heading.textContent = product.name;
      const price = document.createElement("p");
      price.textContent = `${product.price} ر.س للوحدة · المجموع ${product.price * qty} ر.س`;
      const controls = document.createElement("div");
      controls.className = "cart-controls";
      const amount = document.createElement("span");
      amount.textContent = `الكمية: ${qty}`;
      for (const [key, label, text] of [
        ["minus", "تقليل كمية", "−"],
        ["plus", "زيادة كمية", "+"],
        ["remove", "حذف", "حذف"],
      ]) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.coffeeId = id;
        button.dataset.coffeeAction = key;
        button.textContent = text;
        button.setAttribute("aria-label", `${label} ${product.name}`);
        button.disabled = (key === "minus" && qty === 1) || (key === "plus" && qty === maxQuantity);
        controls.append(button);
        if (key === "minus") controls.append(amount);
      }
      row.append(heading, price, controls);
      list.append(row);
    }
    const { count, total } = summary();
    document.getElementById("coffee-cart-count").textContent = String(count);
    document.getElementById("coffee-summary-count").textContent = String(count);
    document.getElementById("coffee-cart-total").textContent = String(total);
    document.getElementById("coffee-cart-empty").hidden = count > 0;
    clear.disabled = count === 0;
    if (focusId) {
      const same = [...list.querySelectorAll("button")].find(
        b => b.dataset.coffeeId === focusId && b.dataset.coffeeAction === action && !b.disabled,
      );
      (same || list.querySelector("button:not(:disabled)") || cart).focus();
    }
  }
  function announce(message) {
    const { count, total } = summary();
    status.textContent = `${message} عدد الوحدات ${count}، والإجمالي ${total} ريال.`;
  }
  document.querySelectorAll("[data-coffee-add]").forEach(button => {
    const id = button.dataset.coffeeAdd;
    if (!products.has(id)) return;
    button.disabled = false;
    button.addEventListener("click", () => {
      if ((basket.get(id) || 0) >= maxQuantity) {
        status.textContent = `الحد الأقصى لكل منتج ${maxQuantity} وحدة.`;
        return;
      }
      basket.set(id, (basket.get(id) || 0) + 1);
      render();
      announce(`أُضيف ${products.get(id).name}.`);
    });
  });
  list.addEventListener("click", event => {
    const button = event.target.closest("button[data-coffee-action]");
    if (!button || button.disabled) return;
    const id = button.dataset.coffeeId;
    const action = button.dataset.coffeeAction;
    if (!products.has(id) || !basket.has(id)) return;
    if (action === "remove") basket.delete(id);
    else basket.set(id, Math.max(1, Math.min(maxQuantity, basket.get(id) + (action === "plus" ? 1 : -1))));
    render(id, action);
    announce(`${action === "remove" ? "حُذف" : "عُدّل"} ${products.get(id).name}.`);
  });
  clear.addEventListener("click", () => {
    basket.clear();
    render();
    cart.focus();
    status.textContent = "أُفرغت السلة.";
  });
  render();
})();
