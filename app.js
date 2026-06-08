const BASE_URL = "http://127.0.0.1:8000/products/nearby?lat=21.1458&lng=79.0882";

let cart = [];

function loadProducts() {
  fetch(BASE_URL)
    .then(res => res.json())
    .then(displayProducts);
}

// ✅ FILTER
function filterCategory(category) {
  fetch(BASE_URL)
    .then(res => res.json())
    .then(data => {
      const filtered = data.filter(item => item.category === category);
      displayProducts(filtered);
    });
}

// ✅ DISPLAY PRODUCTS
function displayProducts(data) {
  const container = document.getElementById("products");
  container.innerHTML = "";

  data.forEach(item => {
    const isVeg = item.category === "veg";

    container.innerHTML += `
      <div class="card">
        <h3>${item.name}</h3>

        <span class="badge ${isVeg ? "veg" : "nonveg"}">
          ${isVeg ? "VEG" : "NON VEG"}
        </span>

        <p>₹${item.price}</p>
        <p>${item.vendor_name}</p>
        <p>${item.distance.toFixed(2)} km</p>

        <button class="add" onclick="addToCart('${item.name}')">
          Add to Cart
        </button>
      </div>
    `;
  });
}

// ✅ CART
function addToCart(name) {
  cart.push(name);
  document.getElementById("cart-count").innerText = cart.length;
}

// ✅ LOAD ON PAGE START
loadProducts();