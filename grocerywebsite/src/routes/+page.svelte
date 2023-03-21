<script>
    import Header from './Header.svelte';
    import Table from './Table.svelte';
    import Graph from './Graph.svelte';
    import {page_store_item} from './store.js';
    import SevenDayPriceChange from './7DayPriceChange.svelte';
    import ThirtyDayPriceChange from './30DayPriceChange.svelte';
	import PriceChangeTable from './PriceChangeTable.svelte';
</script>
<svelte:window/>

    <div class="app">
        <Header />
    </div>
    <div class="container">
    {#if $page_store_item}
        <div class="table-div"><Table/></div>
        <div class="graph-div">
            <Graph/>
        </div>
        <div class="pricechange-div">
            <PriceChangeTable/>
        </div>
    {/if}
        <div class="top-price-change-div"><SevenDayPriceChange/></div>
        <div class="top-price-change-div"><ThirtyDayPriceChange/></div>
</div>
<style>
    .table-div{
        border-radius: 10px;
    }
    .graph-div{
        margin-top: 50px;
        margin-bottom: 50px;
    }
    .top-price-change-div{
        border-radius: 10px;
    }
    .pricechange-div{
        margin-top:50px;
    }
</style>