<script>
// @ts-nocheck

	import { onMount } from 'svelte';
    import {priceChangeData7Days, greatest_price_change_options_7, display_7_days} from './store.js';
    onMount(()=>greatest_price_change_options_7.set({
		"thirty_day_or_7_day": false,
		"offset": 0,
		"limit": 30,
	}));

</script>
{#key $display_7_days}
{#if $display_7_days==true}
<h1 class="text-white">Greatest Price Changes 7 Days</h1>
<table class="table table-hover table-light table-striped table-bordered">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Category</th>
            <th scope="col">Current Price</th>
            <th scope="col">Price 7 Days Ago</th>
            <!--<th scope="col">Price 30 Days Ago</th>-->
            <th scope="col">Percent Price Change 7 Days Ago</th>
            <!--
            <th scope="col">Percent Price Change 30 Days Ago</th> -->
            <th scope="col">Graph</th>
        </tr>
        </thead>
        <tbody>
        {#if $priceChangeData7Days}    
        {#key $priceChangeData7Days}
            {#each $priceChangeData7Days as priceChange, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td>{priceChange.name}</td>
                    <td>{priceChange.category}</td>
                    <td>{priceChange.currentPrice}</td>
                    <td>{priceChange.price7DaysAgo}</td>
                    <!--
                    <td>{priceChange.price30DaysAgo}</td>
                    -->
                    <td>{priceChange.percentPriceChange7DaysAgo}</td>
                    <!--        
                    <td>{priceChange.percentPriceChange30Days}</td>
                    -->
                    <td>Graph</td>
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
