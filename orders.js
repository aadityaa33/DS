fetch("http://127.0.0.1:8000/orders")
  .then(res => res.json())
  .then(showOrders);

function showOrders(data) {
  const container = document.getElementById("orders");
  container.innerHTML = ""; // clear before adding

  data.forEach(o => {
    container.innerHTML += `
      <div class="card">
        <h3>Order #${o.id}</h3>
        <p>Status: ${o.status}</p>
        <button onclick="viewOrder(${o.id})">View</button>
      </div>
    `;
  });
}

// ✅ SINGLE function (no override issue)
function viewOrder(id) {
  // choose ONE page only
  window.location.href = `order-tracking.html?id=${id}`;
}