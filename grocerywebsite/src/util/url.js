export function changeURLParams(storeId, upc){
    const url = new URL(window.location.toString());
    if (storeId) {
        url.searchParams.set("storeId", storeId);
    } else {
        url.searchParams.delete("storeId");
    }
    
    if (upc){
        url.searchParams.set("upc", upc);
    }else{
        url.searchParams.delete("upc");
    }
    history.replaceState(history.state, '', url);
};