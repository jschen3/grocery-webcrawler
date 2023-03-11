<script>
    import {priceChangeTable} from './store.js';

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
</script>
{#if $priceChangeTable!=undefined}
<table class="table table-hover table-light table-striped table-bordered">
    <thead>
        <tr>
            <th scope="col">Date Range</th>
            <th scope="col">Price</th>
            <th scope="col">Price Difference From Today</th>
            <th scope="col">Percent Price Difference From Today</th>
        </tr>
    </thead>
    <tbody>
        {#each $priceChangeTable as priceChangeRow}
        <tr>
            <td>{priceChangeRow.startDateEndDateStr}</td>
            <td>${priceChangeRow.currentPrice}</td>
            <td>{@html percentText(priceChangeRow.currentPriceChangeFromToday)}</td>
            <td>{@html percentText(priceChangeRow.currentPriceChangePercentageFromToday)}</td>
        </tr>
        {/each}
    </tbody>
</table>
{/if}        