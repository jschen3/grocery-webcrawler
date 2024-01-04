<script>
	import { json } from '@sveltejs/kit';
import {display_shopping_list, page_store_item} from './store'
import {shoppingListOutput} from './shopping_list/shoppingliststore';
import {addDollarSymbol} from '../util/textformat.js';
import { changeURLParams } from '../util/url.js';

const shoppingList = $shoppingListOutput.shoppingListItems;
const optimalStore = $shoppingListOutput.optimalStore;
const optimalStoreShoppingList = optimalStore.shoppingItems;

function itemNameClicked(upc, storeValue){
    page_store_item.set({"upc":upc, "storeId":storeValue, "store_item_days":-1});
    display_shopping_list.set(false);
    changeURLParams(storeValue, upc);
}   
</script>
{#key $display_shopping_list}
    {#if $display_shopping_list==true}
        <h1 class="text-white">Optimal Store Location: {optimalStore.storeLocation}</h1>
        <h2 class="text-white">Optimal Store Shopping List</h2>
        <table class="table table-hover table-light table-striped table-bordered">
            <thead>
                <tr>
                    <th scope="col">Item Name</th>
                    <th scope="col">Price</th>
                    <th scope="col">Remove Item</th>
                </tr>
            </thead>
            <tbody>
                {#if optimalStoreShoppingList && optimalStoreShoppingList.length>0}
                        {#each optimalStoreShoppingList as item}
                            <tr>
                                <td><a on:click={()=>itemNameClicked(item.upc, optimalStore.storeId)} class="text-black">{item.name}</a></td>
                                <td>{addDollarSymbol(item.price)}</td>
                                <td><a>delete item</a></td>
                            </tr>
                        {/each}
                    <tr>
                        <td><strong>Total Price:</strong></td>
                        <td>{addDollarSymbol(optimalStore.totalPrice)}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><strong>Maximum Price:</strong></td>
                        <td>{addDollarSymbol(optimalStore.maximumPrice)}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><strong>Savings:</strong></td>
                        <td>{addDollarSymbol(optimalStore.maximumSavings)}</td>
                        <td></td>
                    </tr>
                {/if}    
            </tbody>
        </table>
        <h1 class="text-white">Shopping List Additional Options</h1>
        <table class="table table-hover table-light table-striped table-bordered">
            <thead>
                <tr>
                    <th scope="col">Item Name</th>
                    <th scope="col">Cheapest Price</th>
                    <th scope="col">Cheapest Price Location</th>
                    <th scope="col">Highest Price</th>
                    <th scope="col">Highest Price Location</th>
                    <th scope="col">Remove Item</th>
                </tr>
            </thead>
            <tbody>
                 {#if shoppingList && shoppingList.length>0}
                    {#each shoppingList as item}
                        <tr>
                            <td>
                                <a class="text-black" on:click={()=>itemNameClicked(item.upc, optimalStore.storeId)}>{item.itemName}</a>
                            </td>
                            <td>
                                {addDollarSymbol(item.cheapestPrice)}
                            </td>
                            <td>
                                {item.cheapestPriceLocation}
                            </td>
                            <td>
                                {addDollarSymbol(item.highestPrice)}
                            </td>
                            <td>
                                {item.highestPriceLocation}
                            </td>
                            <td><a>delete item</a></td>  
                        </tr>
                    {/each}
                {/if} 
            </tbody>
        </table>
    {/if}
{/key}
<style>

</style>