async function loadPage() {
    const tableRef = document.getElementById("table_reference").value;
    const containerEl = document.getElementById("orders-container");

    try {
        const orders = await getOrdersByTableReference(tableRef);

        containerEl.innerHTML = ""; // Clear the "Loading orders..." text

        // Just in case, handle the case where the table has no active orders
        if (!orders || orders.length === 0) {
            containerEl.innerHTML = `<p style="color: gray;"><em>No active orders found for table ${tableRef}.</em></p>`;
            return;
        }

        // Loop through each order and create a button for it
        orders.forEach(order => {
            const timeString = new Date(order.time_at_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

            const wrapperDiv = document.createElement("div");
            wrapperDiv.className = "grid";
            wrapperDiv.style.marginBottom = "20px";

            const buttonEl = document.createElement("a");
            buttonEl.href = `/order_edit?order_id=${order.order_id}`;
            buttonEl.setAttribute("role", "button");
            
            buttonEl.innerText = `Order ${order.order_id} (Created at ${timeString})`;

            wrapperDiv.appendChild(buttonEl);
            containerEl.appendChild(wrapperDiv);
        });

    } catch (error) {
        containerEl.innerHTML = `<p style="color: red;">Error loading orders: ${error.message}</p>`;
    }
}

window.onload = loadPage;