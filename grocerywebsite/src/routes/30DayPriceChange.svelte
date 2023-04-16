<script>
    // @ts-nocheck
    import { onMount } from 'svelte';
    import {priceChangeData30Days, greatest_price_change_options_30, display_30_days, display_7_days, page_store_item, store_id} from './store.js';
    import {colorPercentText, addDollarSymbol} from '../util/textformat.js'
    onMount(()=>{
        let storeValue;
        store_id.subscribe(value =>{
            storeValue=value;
        });   
        greatest_price_change_options_30.set({
            "storeId":storeValue,  //set this from a another st
            "thirty_day_or_7_day": true,
            "offset": 0,
            "limit": 50,
        });
    });

    function itemNameClicked(upc){
        let storeValue;
        store_id.subscribe(value =>{
            storeValue=value;
        });
        page_store_item.set({"upc":upc, "storeId":storeValue, "store_item_days":7});
        display_7_days.set(false);
        display_30_days.set(false);
    }
    
    </script>
    {#key $display_30_days}
    {#if $display_30_days==true}
    <div class="row">
        <div class="col-sm"><h1 class="text-white">Greatest Price Changes in the Last 30 Days</h1></div>
        <div class="float-end"><h3 class="text-white">StoreId: {$store_id}</h3></div>
    </div>
    <table class="table table-hover table-light table-striped table-bordered">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Category</th>
                <th scope="col">Current Price</th>
                <th scope="col">Price 30 Days Ago</th>
                <th scope="col">Percent Price Change 30 Days</th>
            </tr>
            </thead>
            <tbody>
            {#if $priceChangeData30Days}    
            {#key $priceChangeData30Days}
                {#each $priceChangeData30Days as priceChange, i}
                    <tr>
                        <th scope="row">{i+1}</th>
                        <td><a on:click={itemNameClicked(priceChange.upc)} class="text-black">{priceChange.name}</a></td>
                        <td>{priceChange.category}</td>
                        <td>{addDollarSymbol(priceChange.currentPrice)}</td>
                        <td>{addDollarSymbol(priceChange.price30DaysAgo)}</td>       
                        <td>{@html colorPercentText(priceChange.percentPriceChange30Days)}</td>
                    </tr>
                {/each}    
            {/key}
            {/if}
            </tbody>
    </table>
    {/if}
    {/key}
    
    
    <style>
    h1{
        margin-top:25px;
    }
    .table{
        margin-top:25px;
    }
    </style>
    