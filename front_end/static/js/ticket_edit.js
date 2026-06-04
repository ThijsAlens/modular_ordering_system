const ticketQuantities = {};
let loadedMenu = null;

async function loadPage() {
    const orderId = document.getElementById("hidden-order-id").value;
    const tableRefEl = document.getElementById("display-table-reference");
    const tbodyEl = document.getElementById("tickets-table-body");
    const destination = document.getElementById("hidden-destination").value;

    const ticketIdRaw = document.getElementById("hidden-ticket-id").value;
    const ticketId = (ticketIdRaw && ticketIdRaw !== "None") ? parseInt(ticketIdRaw) : null;

    try {
        const order = await getOrderById(orderId);
        tableRefEl.innerText = order.table_reference;
        
        loadedMenu = await getMenuByDestination(destination);

        let existingTicket = null;
        if (ticketId !== null) {
            existingTicket = await getTicketByIds(orderId, ticketId);
        }

        renderMenu(loadedMenu, tbodyEl, existingTicket);
    } catch (error) {
        tbodyEl.innerHTML = `<tr><td colspan="2">An error occurred while loading... ${error.message}</td></tr>`;
    }
}

function renderMenu(menu, tbodyEl, existingTicket) {
    tbodyEl.innerHTML = ""; 
    
    if (!menu.products || menu.products.length === 0) {
        tbodyEl.innerHTML = `<tr><td colspan="2" style="text-align: center;">No items found for this destination.</td></tr>`;
        return;
    }

    menu.products.forEach(product => {
        let startQty = 0;
        let startComment = "";

        if (existingTicket && existingTicket.items) {
            const foundItem = existingTicket.items.find(i => i.product.product_id == product.product_id);
            if (foundItem) {
                const matchingItems = existingTicket.items.filter(i => i.product.product_id == product.product_id);
                startQty = matchingItems.length;
                startComment = foundItem.comment || "";
            }
        }
        ticketQuantities[product.product_id] = startQty;

        const row = document.createElement("tr");
        row.innerHTML = `
            <td style="vertical-align: middle;">
                <strong>${product.name}</strong>
                <input type="text" id="comment-${product.product_id}" value="${startComment}" placeholder="Notes..." style="margin-top: 0.5rem; margin-bottom: 0; padding: 0.25rem 0.5rem; font-size: 0.8rem; height: auto;">
            </td>
            <td style="vertical-align: middle;">
                <div style="display: flex; align-items: center; justify-content: flex-end; gap: 10px;">
                    <button class="secondary outline" style="width: 40px; margin-bottom: 0; padding: 0;" onclick="changeAmount('${product.product_id}', -1)">-</button>
                    <span id="qty-${product.product_id}" style="min-width: 20px; text-align: center; font-weight: bold;">${startQty}</span>
                    <button class="outline" style="width: 40px; margin-bottom: 0; padding: 0;" onclick="changeAmount('${product.product_id}', 1)">+</button>
                </div>
            </td>
        `;
        tbodyEl.appendChild(row);
    });
    
    const globalCommentStart = existingTicket ? (existingTicket.comment || "") : "";
    const commentRow = document.createElement("tr");
    commentRow.innerHTML = `
        <td colspan="2">
            <input type="text" id="ticket-comment" value="${globalCommentStart}" placeholder="Other notes for this ticket..." style="width: 100%; margin-top: 0.5rem; margin-bottom: 0; padding: 0.25rem 0.5rem; font-size: 0.8rem; height: auto;">
        </td>
    `;
    tbodyEl.appendChild(commentRow);
}

function changeAmount(productId, change) {
    let newAmount = ticketQuantities[productId] + change;
    if (newAmount < 0) newAmount = 0; 
    
    ticketQuantities[productId] = newAmount;
    document.getElementById(`qty-${productId}`).innerText = newAmount;
}

async function saveTicket_saveButton() {
    const btnEl = document.getElementById("save-ticket_save-button");
    
    try {
        btnEl.disabled = true;
        btnEl.innerText = "Saving...";

        const orderId = document.getElementById("hidden-order-id").value;
        const destination = document.getElementById("hidden-destination").value;
        const username = document.getElementById("hidden-username").value;
        const ticketComment = document.getElementById("ticket-comment").value.trim();

        const ticketIdRaw = document.getElementById("hidden-ticket-id").value;
        const ticketId = (ticketIdRaw && ticketIdRaw !== "None") ? parseInt(ticketIdRaw) : null;

        const selectedItems = [];

        for (const [productId, qty] of Object.entries(ticketQuantities)) {
            if (qty > 0) {
                const noteInput = document.getElementById(`comment-${productId}`);
                const itemComment = noteInput ? noteInput.value.trim() : "";
                
                const productData = loadedMenu.products.find(p => p.product_id === parseInt(productId));

                for (let i = 0; i < qty; i++) {
                    selectedItems.push({ 
                        product: productData, 
                        comment: itemComment
                    });
                }
            }
        }

        if (selectedItems.length === 0) {
            alert("Please add at least one item to the ticket!");
            btnEl.disabled = false;
            btnEl.innerText = "Save ticket";
            return;
        }

        if (ticketId !== null) { 
            await updateTicketByIds(orderId, ticketId, selectedItems, ticketComment, username);
        } else {
            await createNewTicket(orderId, destination, selectedItems, ticketComment, username); 
        }

        window.location.href = `/order_edit?order_id=${orderId}`;

    } catch (error) {
        alert("Error saving ticket: " + error.message);
        btnEl.disabled = false;
        btnEl.innerText = "Save ticket";
    }
}

window.onload = loadPage;