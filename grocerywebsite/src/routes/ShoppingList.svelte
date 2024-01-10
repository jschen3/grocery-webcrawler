<script>
import {display_shopping_list, page_store_item} from './store'
import {addDollarSymbol} from '../util/textformat.js';
import { changeURLParams } from '../util/url.js';
import axios from 'axios';
import shoppingListOutput from './shopping_list/shoppingliststore.js'
$shoppingListOutput={
    "shoppingListItems": [
        {
            "index": 0,
            "updatedDate": "2023-12-28",
            "itemName": "Signature SELECT Tape Invisible Matte Finish 0.75 Inch x 300 Inch - 3 Count",
            "upc": "0002113006008",
            "cheapestPrice": 1.25,
            "cheapestPriceLocation": "570 N Shorline Blvd, Mountain View, CA, 94040",
            "highestPrice": 4.99,
            "highestPriceLocation": "6150 Bollinger Rd, San Jose, CA, 95129"
        },
        {
            "index": 1,
            "updatedDate": "2024-01-02",
            "itemName": "De Wafelbakkers Buttermilk Pancakes Pack - 18 Count",
            "upc": "0067984410457",
            "cheapestPrice": 4.99,
            "cheapestPriceLocation": "570 N Shorline Blvd, Mountain View, CA, 94040",
            "highestPrice": 4.99,
            "highestPriceLocation": "570 N Shorline Blvd, Mountain View, CA, 94040"
        },
        {
            "index": 2,
            "updatedDate": "2024-01-03",
            "itemName": "waterfront BISTRO Shrimp Raw Extra Jumbo Shell & Tail On Frozen 16-20 Count - 2 Lb",
            "upc": "0002113012531",
            "cheapestPrice": 11.98,
            "cheapestPriceLocation": "6150 Bollinger Rd, San Jose, CA, 95129",
            "highestPrice": 25.98,
            "highestPriceLocation": "2811 Middlefield Rd, Palo Alto, CA, 94306"
        }
    ],
    "optimalStore": {
        "storeId": "705",
        "storeLocation": "570 N Shorline Blvd, Mountain View, CA, 94040",
        "shoppingItems": [
            {
                "index": 0,
                "upc": "0002113006008",
                "name": "Signature SELECT Tape Invisible Matte Finish 0.75 Inch x 300 Inch - 3 Count",
                "storeId": "705",
                "storeLocation": "570 N Shorline Blvd, Mountain View, CA, 94040",
                "price": 1.25,
                "updatedDate": "2023-12-28"
            },
            {
                "index": 1,
                "upc": "0067984410457",
                "name": "De Wafelbakkers Buttermilk Pancakes Pack - 18 Count",
                "storeId": "705",
                "storeLocation": "570 N Shorline Blvd, Mountain View, CA, 94040",
                "price": 4.99,
                "updatedDate": "2024-01-02"
            },
            {
                "index": 2,
                "upc": "0002113012531",
                "name": "waterfront BISTRO Shrimp Raw Extra Jumbo Shell & Tail On Frozen 16-20 Count - 2 Lb",
                "storeId": "705",
                "storeLocation": "570 N Shorline Blvd, Mountain View, CA, 94040",
                "price": 11.98,
                "updatedDate": "2024-01-03"
            }
        ],
        "totalPrice": 18.22,
        "missingItems": [],
        "maximumPrice": 35.96,
        "maximumSavings": 17.740000000000002
    }
}
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
        shoppingListOutput.set(JSON.stringify(response));
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