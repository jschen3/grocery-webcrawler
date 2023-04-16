import {writable, derived} from 'svelte/store';
import axios from 'axios';
export const page_store_item = writable(null);

export const greatest_price_change_options_7=writable(null);

export const greatest_price_change_options_30=writable(null);

export const display_7_days = writable(true);

export const display_30_days = writable(false);

export const store_item_days = writable(7);

export const store_id = writable(2948);

const server_url = "https://grocerymarketwatch.com:5000"
export const itemData = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const store_id = $page_store_item.storeId;
        const upc = $page_store_item.upc;
        const response = await axios.get(server_url+"/items/"+store_id+"/"+upc);
        const data = await response.data;
        //console.log(data);
        set(data);
    }
        
});

export const priceToday = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const store_id = $page_store_item.storeId;
        const upc = $page_store_item.upc;
        const response = await axios.get(server_url+"/items/"+store_id+"/"+upc);
        const data = await response.data;
        set({"date":data.date, "price":data.price, "currentPriceChangeFromToday": 0.00, "currentPriceChangePercentageFromToday":0.00})
    }
});

export const graphData = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const store_id = $page_store_item.storeId;
        const upc = $page_store_item.upc;
        const store_item_days = $page_store_item.store_item_days
        const response = await axios.get(server_url+"/items/"+store_id+"/"+upc+"/json/prices?days="+store_item_days);
        const data= await response.data;
        //console.log(data);
        set(data);
    }    
});

export const priceChangeTable = derived(page_store_item, async($page_store_item, set)=>{
    if ($page_store_item!=null && $page_store_item!=undefined){
        const store_item_days = $page_store_item.store_item_days;
        const storeId = $page_store_item.storeId;
        const upc = $page_store_item.upc;
        const response = await axios.get(server_url+"/pricechangetable/"+storeId+"/"+upc+"?days="+store_item_days);
        const data = await response.data;
        //console.log(data)
        set(data);
    }
})

export const priceChangeData7Days = derived(greatest_price_change_options_7, async($greatest_price_change_options, set)=>{
    let thirty_day_or_7_day;
    let offset;
    let limit;
    let store;
    if ($greatest_price_change_options!=null){
        thirty_day_or_7_day = $greatest_price_change_options.thirty_day_or_7_day;
        store = $greatest_price_change_options.storeId;
        offset = $greatest_price_change_options.offset;
        limit = $greatest_price_change_options.limit;
        const response = await axios.get(server_url+"/greatest_price_changes?storeId="+store+"&limit="+limit+"&offset="+offset+"&thirtyOr7Days="+thirty_day_or_7_day);
        const data = await response.data;
        //console.log(data);
        set(data);
    }
    
});

export const priceChangeData30Days = derived(greatest_price_change_options_30, async($greatest_price_change_options, set)=>{
    let thirty_day_or_7_day;
    let offset;
    let limit;
    let store;
    if ($greatest_price_change_options!=null){
        thirty_day_or_7_day = $greatest_price_change_options.thirty_day_or_7_day;
        store = $greatest_price_change_options.storeId;
        offset = $greatest_price_change_options.offset;
        limit = $greatest_price_change_options.limit;
        const response = await axios.get(server_url+"/greatest_price_changes?storeId="+store+"&limit="+limit+"&offset="+offset+"&thirtyOr7Days="+thirty_day_or_7_day);
        const data = await response.data;
        //console.log(data);
        set(data);
    }
    
});

export const storeInfo = derived(store_id, async($store_id, set)=>{
    if ($store_id!=null && $store_id!=undefined){
        const response = await axios.get(server_url+"/storeinfo/"+$store_id);
        const data = await response.data;
        set(data);
    }    
});
