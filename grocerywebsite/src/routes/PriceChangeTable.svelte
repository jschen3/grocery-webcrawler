<script>
    import {priceChangeTable, priceToday} from './store.js';
    function color_symbol_round(percent){
        if (percent>0){
            return "<span style=\"color:green;\"><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"</span>"
        }
        else if (percent==0){
            return "<span><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"</span>"
        }
        else{
            return "<span style=\"color:red;\"><i class=\"bi bi-caret-down\"></i>-"+" "+naiveRound(percent)+"</span>"
        }
    }

    function percentText(percent){
        if (percent>0){
            return "<span style=\"color:green;\"><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
        }
        else if (percent==0){
            return "<span><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
        }
        else{
            return "<span style=\"color:red;\"><i class=\"bi bi-caret-down\"></i>-"+" "+naiveRound(percent)+"%</span>"
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
            <td>{@html color_symbol_round(priceChangeRow.currentPriceChangeFromToday)}</td>
            <td>{@html percentText(priceChangeRow.currentPriceChangePercentageFromToday)}</td>
        </tr>
        {/each}
        <tr>
            <td><strong>Price Today: {$priceToday.date}</strong></td>
            <td>{$priceToday.price}</td>
            <td>{@html color_symbol_round($priceToday.currentPriceChangeFromToday)}</td>
            <td>{@html percentText($priceToday.currentPriceChangePercentageFromToday)}</td>
        </tr>
    </tbody>
</table>
{/if}        