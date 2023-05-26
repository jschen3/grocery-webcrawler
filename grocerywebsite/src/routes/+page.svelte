<script>
    import Header from './Header.svelte';
    import Table from './Table.svelte';
    import Graph from './Graph.svelte';
    import {page_store_item, display_30_days, display_7_days} from './store.js';
    import SevenDayPriceChange from './7DayPriceChange.svelte';
    import ThirtyDayPriceChange from './30DayPriceChange.svelte';
	import PriceChangeTable from './PriceChangeTable.svelte';
    import { page } from '$app/stores';
    function hasURLPatterns(){
        if ($page.url.searchParams.has("storeId") && $page.url.searchParams.has("upc")){
            let urlParams = $page.url.searchParams
            page_store_item.set({"upc":urlParams.get("upc"), "storeId":urlParams.get("storeId"), "store_item_days":7});
            display_7_days.set(false);
            display_30_days.set(false);
            return true;
        }
        return false;
        
    }
    
</script>
<svelte:window/>

    <div class="app">
        <Header />
    </div>
    <div class="container">
    {#if $page_store_item || hasURLPatterns()}
        {#key page_store_item}
        <div class="table-div"><Table/></div>
        <div class="graph-div">
            <Graph/>
        </div>
        <div class="pricechange-div">
            <PriceChangeTable/>
        </div>
        {/key}
    {/if}
    {#key display_7_days}
        <div class="top-price-change-div"><SevenDayPriceChange/></div>
    {/key}
    {#key display_30_days}    
        <div class="top-price-change-div"><ThirtyDayPriceChange/></div>
    {/key}    
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