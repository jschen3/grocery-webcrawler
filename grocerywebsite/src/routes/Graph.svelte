<script>

    import Chart from './stock_graph_components/Chart.svelte';
    import {graphData, page_store_item} from './store.js';
    
    let days_select = 7
    function store_item_days_on_change(){
       let clone = JSON.parse(JSON.stringify($page_store_item));
       console.log(clone);
       page_store_item.set({"upc":clone.upc, "storeId":clone.storeId, "store_item_days":days_select});
    }

</script>
    <!--
        https://toltman.medium.com/creating-tooltips-in-svelte-2faf317402f2
        https://layercake.graphics/example/MultiLine/
    -->
{#key $graphData}
<div class="days-select-div">
    <select bind:value={days_select} on:change={store_item_days_on_change} class="days-select">
        <option value={7}>7 Days</option>
        <option value={14}>14 Days</option>
        <option value={30}>30 Days</option>
        <option value={-1}>All Days</option>
    </select>   
</div>         
    <Chart pricingValue={$graphData}/>
{/key}

<style>
    .days-select-div{
        margin-bottom: 20px;
    }
    .days-select{
        width:200px;
    }
</style>
