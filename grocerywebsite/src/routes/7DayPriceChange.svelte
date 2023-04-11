<script>
// @ts-nocheck

	import { onMount } from 'svelte';
    import {priceChangeData7Days, greatest_price_change_options_7, display_7_days, display_30_days, page_store_item, storeId} from './store.js';
    import {colorPercentText, addDollarSymbol} from '../util/textformat.js'
    onMount(()=>{
        let storeValue;
        storeId.subscribe(value =>{
            storeValue=value;
        });
        greatest_price_change_options_7.set({
        "storeId":storeValue,
		"thirty_day_or_7_day": false,
		"offset": 0,
		"limit": 50,
	    });
    });    


    function itemNameClicked(upc){
        let storeValue;
        storeId.subscribe(value =>{
            storeValue=value;
        })
        page_store_item.set({"upc":upc, "storeId":storeValue, "store_item_days":7});
        display_7_days.set(false);
        display_30_days.set(false);
    }


</script>
{#key $display_7_days}
{#if $display_7_days==true}
<!-- Something here related to the store id using columns.... -->
<div class="row">
    <div class="col-sm"><h1 class="text-white">Greatest Price Changes in the Last 7 Days</h1></div>
    <div class="float-end"><h3 class="text-white">StoreId: {$storeId}</h3></div>
</div>

<table class="table table-hover table-light table-striped table-bordered">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Category</th>
            <th scope="col">Current Price</th>
            <th scope="col">Price 7 Days Ago</th>
            <th scope="col">Percent Price Change 7 Days</th>
        </tr>
        </thead>
        <tbody>
        {#if $priceChangeData7Days}    
        {#key $priceChangeData7Days}
            {#each $priceChangeData7Days as priceChange, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td><a on:click={itemNameClicked(priceChange.upc)} class="text-black">{priceChange.name}</a></td>
                    <td>{priceChange.category}</td>
                    <td>{addDollarSymbol(priceChange.currentPrice)}</td>
                    <td>{addDollarSymbol(priceChange.price7DaysAgo)}</td>
                    <td>{@html colorPercentText(priceChange.percentPriceChange7DaysAgo)}</td>
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
:global(.icon-flipped) {
    transform: scaleX(-1);
    -moz-transform: scaleX(-1);
    -webkit-transform: scaleX(-1);
    -ms-transform: scaleX(-1);
}
</style>
