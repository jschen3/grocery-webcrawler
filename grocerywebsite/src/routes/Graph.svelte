<script>
// @ts-nocheck

    import Chart from './stock_graph_components/Chart.svelte';
    import {graphData} from './store.js';

   
    

</script>
    <!--
        https://toltman.medium.com/creating-tooltips-in-svelte-2faf317402f2
        https://layercake.graphics/example/MultiLine/
    -->
 {#if $graphData}
 <Chart pricingValue={$graphData}/>

{/if}



<style></style>
