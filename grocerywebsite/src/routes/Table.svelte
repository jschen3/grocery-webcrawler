<script>
    
    import {itemData cart_list} from './store.js';
    import Safeway_Icon from "$lib/images/safeway-icon.png";
    import Buy_Icon from "$lib/images/buy-icon.png";
    import Add_To_Cart_Icon from "$lib/images/add-to-cart.png"
    import {percentText, addDollarSymbol, capitalize} from '../util/textformat.js'
	import axios from 'axios';
    
  function addToCart(upc){
    cart_clone=JSON.parse(JSON.stringify($cart_list));
    cart_clone.push(upc)
    cart_list.set(cart_clone)
    //rest call to api 
    // save result as localstorage shopping list
    axios({
        method:'post',
        url: 'http://localhost:8000/shoppinglist',
        data: $cart_list
    }).then((response)=>{
        console.log(response);
        // local storage
    }, (error)=>{
        console.log(error);
    });
  }
</script>
{#if $itemData!= undefined}
    <div class="row">
        <div class="col-md"><h2 class="text-white item-name-header "><strong>Item Name: </strong>{$itemData.name}</h2></div>
    </div>
    <div class="row store-info">
        <div class="col-sm text-white"><strong>Store Name: </strong><img src={Safeway_Icon} alt="safeway icon"/>{capitalize($itemData.storeType)} </div>
        <div class="col-sm text-white"><strong>Location:</strong> {$itemData.storeLocation} </div>
    </div>
    <div class="row store-info">
        <div class="col-sm text-white"><strong>Current Date:</strong> {$itemData.date} </div>
        <div class="col-sm text-white"><strong>Last Updated Date: </strong>{$itemData.lastUpdatedDate} </div>
    </div>
   <div class="row">
        <p class="text-white go-to-safeway-link"><strong>Go to item: </strong><a href="https://www.safeway.com/shop/search-results.html?q={$itemData.name}">https://www.safeway.com/shop/search-results.html?q={$itemData.name}</a></p>
    </div>
    <div class="row">
        <p class="text-white" on:click={addToCart($itemData.upc)}><strong>Add to shopping list: </strong><img class="cart-image" src={Add_To_Cart_Icon} alt="add to cart icon"/></p>
    </div>
    <div class="table-div bg-secondary">
        <div class="row">
            <div class="col-sm"><h2>Prices</h2></div>
            <div class="col-sm"><h2>Price Changes</h2></div>
            <div class="col-sm"><h2>Similar Items</h2></div>
        </div>
        <div class="row">
            <div class="col-sm">
                <p><strong>Current Price:</strong><img src={Buy_Icon} alt="buy"/>{addDollarSymbol($itemData.price)}</p>
                <p><strong>Price Per:</strong><img src={Buy_Icon} alt="buy"/>{addDollarSymbol($itemData.pricePer)}</p>
                <p><strong>Base Price:</strong><img src={Buy_Icon} alt="buy"/>{addDollarSymbol($itemData.basePrice)}</p>
            </div>
            <div class="col-sm">
                <p><strong>Price 7 Days Ago: </strong><img src={Buy_Icon} alt="buy"/>{addDollarSymbol($itemData.price7DaysAgo)}</p>
                <p><strong>Price Change Last 7 Days: </strong>{addDollarSymbol($itemData.priceChangeLast7Days)}</p>
                <p><strong>Percent Price Change Last 7 Days: </strong>{@html percentText($itemData.percentPriceChange7Days)}</p>
                <p><strong>Price 30 Days Ago: </strong><img src={Buy_Icon} alt="buy"/>{addDollarSymbol($itemData.price30DaysAgo)}</p>
                <p><strong>Price Change Last 30 Days: </strong>{addDollarSymbol($itemData.priceChangeLast30days)}</p>
                <p><strong>Percent Price Change Last 30 Days: </strong>{@html percentText($itemData.percentPriceChange30days)}</p>
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
        text-overflow:clip;
        white-space: nowrap;
        overflow:hidden;
    }
    .cart-image{
        height:50px;
        width: 50px;
    }
</style>