<script>
import {display_shopping_list, page_store_item} from './store'
import {addDollarSymbol} from '../util/textformat.js';
import { changeURLParams } from '../util/url.js';
import axios from 'axios';
import {shoppingListOutput} from './shopping_list/shoppingliststore.js'

const shoppingList = $shoppingListOutput.shoppingListItems; 
const optimalStore = $shoppingListOutput.optimalStore;
const optimalStoreShoppingList = optimalStore.shoppingItems;

function itemNameClicked(upc, storeValue){
    page_store_item.set({"upc":upc, "storeId":storeValue, "store_item_days":-1});
    display_shopping_list.set(false);
    changeURLParams(storeValue, upc);
}   
function deleteItem(index, staticShoppingList){
    let upcsWithRemovedIndex = []
    for (let i=0; i<staticShoppingList.length;i++){
        if (staticShoppingList[i].index==index){
            continue
        }    
        else{
            upcsWithRemovedIndex.push(staticShoppingList[i].upc)
        }
    }        
    axios({
        method:'post',
        url: 'http://localhost:8000/shoppinglist',
        data: upcsWithRemovedIndex
    }).then((response)=>{
        console.log(response);
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem("shoppingList", JSON.stringify(response.data))
        }    
        }, (error)=>{
        console.log(error);
    });

}
</script>
{#key $display_shopping_list}
    {#if $display_shopping_list==true}
    {#key $shoppingListOutput}
        <h1 class="text-white">Optimal Store Location: {optimalStore.storeLocation}</h1>
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
                                <td><a on:click={()=>deleteItem(item.index, optimalStoreShoppingList)}>delete item</a></td>
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
        <h1 class="text-white">Additional Options</h1>
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
                            <td><a on:click={()=>deleteItem(item.index, shoppingList)}>delete item</a></td>  
                        </tr>
                    {/each}
                {/if} 
            </tbody>
        </table>
        {/key}
    {/if}
{/key}
<style>

</style>