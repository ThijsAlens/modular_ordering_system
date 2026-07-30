
async function findOrder_searchButton() {
    const searchValue = document.getElementById("find-order_search-value").value;
    const messageEl = document.getElementById("find-order_error-message");

    messageEl.textContent = ""; // Clear previous error message

    if (!searchValue) {
        messageEl.innerText = "Please enter a value to search.";
        return; 
    }

    try {
        const order = await getOrderById(searchValue);
        renderOrderDetails(order);
    } catch (error) {
        messageEl.innerText = error.message || "Network error: Could not connect to the server.";
    }
}

function renderOrderDetails(order) {
    const orderDetailsEl = document.getElementById("current-order-details");
    
    let htmlContent = `
        <div style="margin-bottom: 2rem;">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; border-bottom: 2px solid var(--pico-muted-border-color); padding-bottom: 0.5rem; margin-bottom: 1rem;">
                <div style="text-align: left;">
                    <small><strong>Order ID</strong></small><br>
                    ${order.order_id}
                </div>
                <div style="text-align: center;">
                    <small><strong>Table Reference</strong></small><br>
                    ${order.table_reference}
                </div>
                <div style="text-align: right;">
                    <small><strong>Status</strong></small><br>
                    <kbd>${order.status}</kbd>
                </div>
            </div>
        </div>
    `;
    
    // 1. Group all items together by product_id
    const aggregatedItems = {};

    // Ensure tickets exist before looping
    const tickets = order.tickets || [];

    tickets.forEach(ticket => {
        const items = ticket.items || [];
        
        items.forEach(item => {
            const product = item.product;
            if (!product) return; // Safety check

            const pId = product.product_id;
            
            // If we have already seen this product, just add 1 to the amount
            if (aggregatedItems[pId]) {
                aggregatedItems[pId].amount += 1;
            } else {
                // If this is the first time seeing it, create a new entry
                aggregatedItems[pId] = {
                    name: product.name,
                    price: product.price,
                    amount: 1
                };
            }
        });
    });

    // 2. Build the Table HTML
    let grandTotal = 0;
    
    htmlContent += `
        <figure>
            <table role="grid">
                <thead>
                    <tr>
                        <th scope="col">Product</th>
                        <th scope="col" style="text-align: center;">Amount</th>
                        <th scope="col" style="text-align: right;">Unit Price</th>
                        <th scope="col" style="text-align: right;">Total Price</th>
                    </tr>
                </thead>
                <tbody>
    `;

    const productIds = Object.keys(aggregatedItems);

    if (productIds.length === 0) {
        htmlContent += `<tr><td colspan="4" style="text-align: center;">No items found for this order.</td></tr>`;
    } else {
        // Loop through our grouped items and create a table row for each
        productIds.forEach(pId => {
            const groupedItem = aggregatedItems[pId];
            
            // Calculate the total for this specific product (Amount * Unit Price)
            const lineTotal = groupedItem.amount * groupedItem.price;
            
            // Add it to the total order bill
            grandTotal += lineTotal;

            htmlContent += `
                <tr>
                    <td>${groupedItem.name}</td>
                    <td style="text-align: center;">${groupedItem.amount}</td>
                    <td style="text-align: right;">€${groupedItem.price.toFixed(2)}</td>
                    <td style="text-align: right;">€${lineTotal.toFixed(2)}</td>
                </tr>
            `;
        });
    }

    // 3. Add the Grand Total footer and close the table
    htmlContent += `
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" style="text-align: right;"><strong>Grand Total:</strong></td>
                        <td style="text-align: right; color: var(--pico-primary);"><strong>€${grandTotal.toFixed(2)}</strong></td>
                    </tr>
                </tfoot>
            </table>
        </figure>
    `;

    // 4. Add a button to finalize the order
    htmlContent += `
        <div style="text-align: center; margin-top: 1rem;">
            <button onclick="finalizeOrder(${order.order_id})" class="primary">Finalize Order</button>
        </div>
    `;

    // Inject everything into the DOM at once
    orderDetailsEl.innerHTML = htmlContent;
}

async function finalizeOrder(orderId) {
    try {
        await changeOrderStatusById(orderId, "payed");
        alert(`Order ${orderId} has been finalized successfully.`);
        document.getElementById("current-order-details").innerHTML = "";
    } catch (error) {
        alert(`Error finalizing order: ${error.message}`);
    }
}