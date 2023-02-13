<script>
// @ts-nocheck

	import { onMount } from 'svelte';
    import {priceChangeData7Days, greatest_price_change_options_7, display_7_days,display_30_days, page_store_item} from './store.js';
    onMount(()=>greatest_price_change_options_7.set({
		"thirty_day_or_7_day": false,
		"offset": 0,
		"limit": 50,
	}));

    function percentText(percent){
        if (percent>0){
            return "<i class=\"bi bi-caret-up\"></i>"+" +"+naiveRound(percent)
        }
        else{
            return "<i class=\"bi bi-caret-down\"></i>"+" "+naiveRound(percent)
        }
    }

    function naiveRound(num, decimalPlaces = 2) {
        var p = Math.pow(10, decimalPlaces);
        return (Math.round(num * p) / p).toFixed(2);

    }

    function addDollarSign(num){
        return "$"+num.toFixed(2);
    }

    function itemNameClicked(storeId, upc){
        storeId=2948;
        page_store_item.set({"upc":upc, "storeId":storeId});
        display_7_days.set(false);
        display_30_days.set(false);
    }


</script>
{#key $display_7_days}
{#if $display_7_days==true}
<h1 class="text-white">Greatest Price Changes in the Last 7 Days</h1>
<table class="table table-hover table-light table-striped table-bordered">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Category</th>
            <th scope="col">Current Price</th>
            <th scope="col">Price 7 Days Ago</th>
            <!--<th scope="col">Price 30 Days Ago</th>-->
            <th scope="col">Percent Price Change 7 Days</th>
            <!--
            <th scope="col">Percent Price Change 30 Days Ago</th> -->
        </tr>
        </thead>
        <tbody>
        {#if $priceChangeData7Days}    
        {#key $priceChangeData7Days}
            {#each $priceChangeData7Days as priceChange, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td><a on:click={itemNameClicked(priceChange.storeId, priceChange.upc)} class="text-black">{priceChange.name}</a></td>
                    <td>{priceChange.category}</td>
                    <td>{addDollarSign(priceChange.currentPrice)}</td>
                    <td>{addDollarSign(priceChange.price7DaysAgo)}</td>
                    <!--
                    <td>{priceChange.price30DaysAgo}</td>
                    -->
                    <td>{@html percentText(priceChange.percentPriceChange7DaysAgo)}</td>
                    <!--        
                    <td>{priceChange.percentPriceChange30Days}</td>
                    -->
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
