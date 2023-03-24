<script>
    import {priceChangeTable, priceToday} from './store.js';
    import {colorPercentText, addDollarSymbol, colorSymbolRound} from '../util/textformat.js'
    
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
            <td>{addDollarSymbol(priceChangeRow.currentPrice)}</td>
            <td>{@html colorSymbolRound(priceChangeRow.currentPriceChangeFromToday)}</td>
            <td>{@html colorPercentText(priceChangeRow.currentPriceChangePercentageFromToday)}</td>
        </tr>
        {/each}
        {#if $priceToday}
        <tr>
            <td><strong>Price Today: {$priceToday.date}</strong></td>
            <td>{addDollarSymbol($priceToday.price)}</td>
            <td>{@html colorSymbolRound($priceToday.currentPriceChangeFromToday)}</td>
            <td>{@html colorPercentText($priceToday.currentPriceChangePercentageFromToday)}</td>
        </tr>
        {/if}
    </tbody>
</table>
{/if}        