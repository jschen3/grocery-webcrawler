<script>
// @ts-nocheck

	import { onMount } from 'svelte';


    import {priceChangeData, greatest_price_change_options} from './store.js';

    onMount(()=>greatest_price_change_options.set({
		"thirty_day_or_7_day": true,
		"offset": 0,
		"limit": 30,
        "visible":true
	}));

</script>
{#key $greatest_price_change_options!= undefined && $greatest_price_change_options.visible==true}
<table class="table table-hover table-light table-striped table-bordered">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">UPC</th>
            <th scope="col">Category</th>
            <th scope="col">Current Price</th>
            <th scope="col">Price 7 Days Ago</th>
            <th scope="col">Price 30 Days Ago</th>
            <th scope="col">Percent Price Change 7 Days Ago</th>
            <th scope="col">Percent Price Change 30 Days Ago</th>
            <th scope="col">Graph</th>
        </tr>
        </thead>
        <tbody>
        {#if $priceChangeData}    
        {#key $priceChangeData}
            {#each $priceChangeData as priceChange, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td>{priceChange.name}</td>
                    <td>{priceChange.upc}</td>
                    <td>{priceChange.category}</td>
                    <td>{priceChange.currentPrice}</td>
                    <td>{priceChange.price7DaysAgo}</td>
                    <td>{priceChange.price30DaysAgo}</td>
                    <td>{priceChange.percentPriceChange7DaysAgo}</td>
                    <td>{priceChange.percentPriceChange30Days}</td>
                    <td>Graph</td>
                </tr>
            {/each}    
        {/key}
        {/if}
        </tbody>
    
</table>
{/key}


<style>
.table{
    margin-top:50px;
}
</style>
