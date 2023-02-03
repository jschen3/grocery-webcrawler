<script>
    // @ts-nocheck
    
    import { onMount } from 'svelte';
        import {priceChangeData30Days, greatest_price_change_options_30, display_30_days} from './store.js';
    onMount(()=>greatest_price_change_options_30.set({
        "thirty_day_or_7_day": true,
        "offset": 0,
        "limit": 30,
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
    
    </script>
    {#key $display_30_days}
    {#if $display_30_days==true}
    <h1 class="text-white">Greatest Price Changes 30 Days</h1>
    <table class="table table-hover table-light table-striped table-bordered">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Category</th>
                <th scope="col">Current Price</th>
                <th scope="col">Price 30 Days Ago</th>
                <!--<th scope="col">Price 30 Days Ago</th>-->
                <th scope="col">Percent Price Change 30 Days</th>
                <!--
                <th scope="col">Percent Price Change 30 Days Ago</th> -->
            </tr>
            </thead>
            <tbody>
            {#if $priceChangeData30Days}    
            {#key $priceChangeData30Days}
                {#each $priceChangeData30Days as priceChange, i}
                    <tr>
                        <th scope="row">{i+1}</th>
                        <td>{priceChange.name}</td>
                        <td>{priceChange.category}</td>
                        <td>{addDollarSign(priceChange.currentPrice)}</td>
                        <td>{addDollarSign(priceChange.price30DaysAgo)}</td>       
                        <td>{@html percentText(priceChange.percentPriceChange30Days)}</td>
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
    