<script>
    import {priceChangeTable, priceToday} from './store.js';
    function colorSymbolRound(percent){
        if (percent>0){
            return "<span style=\"color:green;\"><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"</span>"
        }
        else if (percent==0){
            return "<span>"+ naiveRound(percent)+"</span>"
        }
        else{
            return "<span style=\"color:red;\"><i class=\"bi bi-caret-down\"></i>"+ naiveRound(percent)+"</span>"
        }
    }

    function percentText(percent){
        if (percent>0){
            return "<span style=\"color:green;\"><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
        }
        else if (percent==0){
            return "<span>"+ naiveRound(percent)+"%</span>"
        }
        else{
            return "<span style=\"color:red;\"><i class=\"bi bi-caret-down\"></i>"+ naiveRound(percent)+"%</span>"
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
            <td>${naiveRound(priceChangeRow.currentPrice)}</td>
            <td>{@html colorSymbolRound(priceChangeRow.currentPriceChangeFromToday)}</td>
            <td>{@html percentText(priceChangeRow.currentPriceChangePercentageFromToday)}</td>
        </tr>
        {/each}
        {#if $priceToday}
        <tr>
            <td><strong>Price Today: {$priceToday.date}</strong></td>
            <td>${naiveRound($priceToday.price)}</td>
            <td>{@html colorSymbolRound($priceToday.currentPriceChangeFromToday)}</td>
            <td>{@html percentText($priceToday.currentPriceChangePercentageFromToday)}</td>
        </tr>
        {/if}
    </tbody>
</table>
{/if}        