import {writable, derived} from 'svelte/store';
import axios from 'axios';
export const page_store_item = writable(null);

export const greatest_price_change_options_7=writable(null);

export const greatest_price_change_options_30=writable(null);

export const display_7_days = writable(true);

export const display_30_days = writable(false);

const server_url = "https://server.grocerymarketwatch.com"
export const itemData = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const storeId = $page_store_item.storeId;
        const upc = $page_store_item.upc;
        const response = await axios.get(server_url+"/items/"+storeId+"/"+upc);
        const data = await response.data;
        console.log(data);
        set(data);
    }
        
});

export const graphData = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const storeId = $page_store_item.storeId;
        const upc = $page_store_item.upc;
        const response = await axios.get(server_url+"/items/"+storeId+"/"+upc+"/json/prices");
        const data= await response.data;
        console.log(data);
        set(data);
    }    
});

export const priceChangeData7Days = derived(greatest_price_change_options_7, async($greatest_price_change_options, set)=>{
    let thirty_day_or_7_day;
    let offset;
    let limit;
    if ($greatest_price_change_options!=null){
        thirty_day_or_7_day = $greatest_price_change_options.thirty_day_or_7_day;
        offset = $greatest_price_change_options.offset;
        limit = $greatest_price_change_options.limit;
        const response = await axios.get(server_url+"/greatest_price_changes?limit="+limit+"&offset="+offset+"&thirtyOr7Days="+thirty_day_or_7_day);
        const data = await response.data;
        console.log(data);
        set(data);
    }
    
});

export const priceChangeData30Days = derived(greatest_price_change_options_30, async($greatest_price_change_options, set)=>{
    let thirty_day_or_7_day;
    let offset;
    let limit;
    if ($greatest_price_change_options!=null){
        thirty_day_or_7_day = $greatest_price_change_options.thirty_day_or_7_day;
        offset = $greatest_price_change_options.offset;
        limit = $greatest_price_change_options.limit;
        const response = await axios.get(server_url+"/greatest_price_changes?limit="+limit+"&offset="+offset+"&thirtyOr7Days="+thirty_day_or_7_day);
        const data = await response.data;
        console.log(data);
        set(data);
    }
    
});