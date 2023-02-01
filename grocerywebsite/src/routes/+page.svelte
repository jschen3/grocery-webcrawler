<script>
    import Header from './Header.svelte';
    import Table from './Table.svelte';
    import Graph from './Graph.svelte';
    import {page_store_item} from './store.js';
    import { onDestroy} from 'svelte';
    //let store_item;

    // const subscription=page_store_item.subscribe(value=>{
    //     if (value!=null && value!=undefined){
    //         store_item = value;
    //         console.log("store_item:"+store_item);
    //     }else{
    //         store_item = null;
    //     }       
    // });
    //onDestroy(subscription);
</script>
<svelte:window/>

    <div class="app">
        <Header />
    </div>
    <div class="container">
    {#if $page_store_item}
    <!-- rest calls caused by these sections dont occur.
        https://linguinecode.com/post/3-methods-to-run-code-after-dom-update-in-svelte
    --> 
        <div><Table/></div>
        <div>
            <Graph/>
            </div>
        {/if}
</div>