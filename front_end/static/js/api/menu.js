
/**
 * 
 * @param {Destination} destination 
 * @returns {Promise<Object>} The menu dictionary for the specified destination.
 */
async function getMenuByDestination(destination) {
    const response = await fetch(`${BACKEND_URL}/get_menu_by_destination?destination=${destination}`);

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch menu for the specified destination.");
    }

    return await response.json();
}