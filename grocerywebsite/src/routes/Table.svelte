<script>
    
    import {itemData} from './store.js';
    import Safeway_Icon from "$lib/images/safeway-icon.png";
    import Buy_Icon from "$lib/images/buy-icon.png";

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

    function capitalize(input){
        return input.charAt(0).toUpperCase() + input.slice(1)
    }    
</script>
{#if $itemData!= undefined}
    <h2 class="text-white item-name-header"><strong>Item Name: </strong> {$itemData.name}</h2>
    <div class="row store-info">
        <div class="col-sm text-white"><strong>Store Name: </strong><img src={Safeway_Icon} alt="safeway icon"/>{capitalize($itemData.storeType)} </div>
        <div class="col-sm text-white"><strong>Location:</strong> {$itemData.storeLocation} </div>
    </div>
    <div class="row store-info">
        <div class="col-sm text-white"><strong>Current Date:</strong> {$itemData.date} </div>
        <div class="col-sm text-white"><strong>Last Updated Date: </strong>{$itemData.lastUpdatedDate} </div>
    </div>
    <p class="text-white go-to-safeway-link"><strong>Go to item: </strong><a href="https://www.safeway.com/shop/search-results.html?q={$itemData.name}">https://www.safeway.com/shop/search-results.html?q={$itemData.name}</a></p>
    <div class="table-div bg-secondary">
        <div class="row">
            <div class="col-sm"><h2>Prices</h2></div>
            <div class="col-sm"><h2>Price Changes</h2></div>
            <div class="col-sm"><h2>Similar Items</h2></div>
        </div>
        <div class="row">
            <div class="col-sm">
                <p><strong>Current Price:</strong><img src={Buy_Icon} alt="buy"/>${$itemData.price}</p>
                <p><strong>Price Per:</strong><img src={Buy_Icon} alt="buy"/>${$itemData.pricePer}</p>
                <p><strong>Base Price:</strong><img src={Buy_Icon} alt="buy"/>${$itemData.basePrice}</p>
            </div>
            <div class="col-sm">
                <p><strong>Price 7 Days Ago: </strong><img src={Buy_Icon} alt="buy"/>${$itemData.price7DaysAgo}</p>
                <p><strong>Price Change Last 7 Days: </strong>{addDollarSign($itemData.priceChangeLast7Days)}</p>
                <p><strong>Percent Price Change Last 7 Days: </strong>{@html percentText($itemData.percentPriceChange7Days)}</p>
                <p><strong>Price 30 Days Ago: </strong><img src={Buy_Icon} alt="buy"/>${$itemData.price30DaysAgo}</p>
                <p><strong>Price Change Last 30 Days: </strong>{addDollarSign($itemData.priceChangeLast30days)}</p>
                <p><strong>Percent Price Change Last 30 Days: </strong>{@html percentText($itemData.percentPriceChange30days)}</p>
                <!-- <p><strong>Price Change All Records: </strong>{$itemData.priceChangeForAllRecords}</p>
                <p><strong>Percent Price Change All Records: </strong>{$itemData.percentPriceChangeForAllRecords}</p> -->
            </div>
            <div class="col-sm">   
                <td>
                    <p><strong>Category: </strong>{$itemData.category}</p>
                    <p>Same Store Similar Items</p>
                    <ul>
                        {#each $itemData.itemsInCategory as { upc, name }}
                        <li>{name}</li>
                        {/each}
                    </ul>
                </td>
            </div>
        </div>
    </div>

{/if}
<style>
    .table-div{
        border-radius: 5px;
        padding-inline: 10px;
    }
    .go-to-safeway-link{
        padding-top:10px
    }
    .store-info{
        padding-top:10px
    }
    .item-name-header{
        padding-top: 5px;
    }
</style>