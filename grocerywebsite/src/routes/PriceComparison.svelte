<script>
    import { addDollarSymbol } from '../util/textformat.js';
    import {priceComparison} from './store.js';
</script>
 {#if $priceComparison!=undefined && $priceComparison.prices.length>0}
    <div class="price-comparison-div">
        <h2 class="text-white">Price Comparison:</h2>
            <table class="table table-hover table-light table-striped table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Store Location</th>
                        <th scope="col">Price at store</th>
                        <th scope="col">Updated Date</th>
                    </tr>
                </thead>
                <tbody>
                    {#each $priceComparison.prices as {storeId, storeLocation, price, date}}
                    <tr>
                        <td>{storeLocation}</td>
                        <td>{addDollarSymbol(price)}</td>
                        <td>{date}</td>
                    </tr>
                    {/each}
                </tbody>
            </table>
    </div>
{/if}
<style>
</style>