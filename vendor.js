const BASE = "http://127.0.0.1:8000";

// ✅ LOAD ORDERS
function loadOrders() {
  fetch(BASE + "/vendor/orders")
    .then(res => res.json())
    .then(data => displayOrders(data));
}

// ✅ DISPLAY
function displayOrders(data) {
  const container = document.getElementById("orders");
  container.innerHTML = "";

  data.forEach(order => {
    container.innerHTML += `
      <div class="card">
        <h3>Order #${order.id}</h3>
        <p>Status: ${order.status}</p>

        <button class="accept" onclick="updateStatus(${order.id}, 'ACCEPTED')">Accept</button>
        <button class="reject" onclick="updateStatus(${order.id}, 'REJECTED')">Reject</button>
        <button class="prepare" onclick="updateStatus(${order.id}, 'PREPARING')">Preparing</button>
        <button class="ready" onclick="markReady(${order.id})">Ready</button>
      </div>
    `;
  });
}

// ✅ UPDATE STATUS (ACCEPT / PREPARE)
function updateStatus(orderId, status) {
  fetch(`${BASE}/vendor/order/${orderId}/status?status=${status}`, {
    method: "POST"
  })
  .then(() => {
    alert("Updated ✅");
    loadOrders();
  });
}

// ✅ MARK READY (IMPORTANT)
function markReady(orderId) {
  fetch(`${BASE}/vendor/order/${orderId}/ready`, {
    method: "POST"
  })
  .then(() => {
    alert("Marked READY ✅ (Delivery triggered)");
    loadOrders();
  });
}

// AUTO LOAD
loadOrders();