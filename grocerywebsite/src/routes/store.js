import {writable, derived} from 'svelte/store';
import axios from 'axios';
export const page_store_item = writable(null);

export const itemData = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const storeId = $page_store_item.storeId
        const upc = $page_store_item.upc;
        const response = await axios.get("http://localhost:8000/items/"+storeId+"/"+upc);
        const data = await response.data;
        console.log(data);
        set(data);
    }
        
});

export const graphData = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const storeId = $page_store_item.storeId
        const upc = $page_store_item.upc;
        const response = await axios.get("http://localhost:8000/items/"+storeId+"/"+upc+"/json/prices?days=30");
        const data= await response.data
        console.log(data);
        set(data);
    }    
});