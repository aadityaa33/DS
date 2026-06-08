const API = "http://127.0.0.1:8000/products/nearby?lat=21.1458&lng=79.0882";

let cart = [];

// ✅ LOAD PRODUCTS
fetch(API)
  .then(res => res.json())
  .then(data => showProducts(data));

// ✅ DISPLAY PRODUCTS
function showProducts(data) {
  const container = document.getElementById("products");
  container.innerHTML = "";

  data.forEach(p => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <img src="https://source.unsplash.com/400x300/?food" />

      <div class="card-content">
        <h3>${p.name}</h3>
        <p class="price">₹${p.price}</p>
        <p>${p.vendor_name}</p>

        <button>Add to Cart</button>
      </div>
    `;

    // ✅ SAFE button handling (no JSON stringify issue)
    card.querySelector("button").addEventListener("click", () => addToCart(p));

    container.appendChild(card);
  });
}

// ✅ ADD TO CART
function addToCart(item) {

  // ✅ enforce single vendor rule (important)
  if (cart.length > 0 && cart[0].vendor_id !== item.vendor_id) {
    alert("You can only order from one vendor at a time ❌");
    return;
  }

  cart.push(item);
  updateCart();
}

// ✅ UPDATE CART
function updateCart() {
  document.getElementById("cart-count").innerText = cart.length;

  let total = 0;
  let itemsHTML = "";

  cart.forEach(i => {
    total += i.price;
    itemsHTML += `<p>${i.name} - ₹${i.price}</p>`;
  });

  const cartItems = document.getElementById("cart-items");
  if (cartItems) cartItems.innerHTML = itemsHTML;

  const totalEl = document.getElementById("total");
  if (totalEl) totalEl.innerText = total;
}

// ✅ TOGGLE CART
function toggleCart() {
  document.getElementById("cart-panel").classList.toggle("open");
}

// ✅ CHECKOUT
function checkout() {
  if (cart.length === 0) {
    alert("Cart is empty ❌");
    return;
  }

  fetch("http://127.0.0.1:8000/order", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      vendor_id: cart[0].vendor_id,
      items: cart
    })
  })
  .then(res => res.json())
  .then(data => {
    alert("Order placed ✅ ID: " + data.order_id);

    cart = [];
    updateCart();
  })
  .catch(err => {
    console.error(err);
    alert("Checkout failed ❌");
  });
}