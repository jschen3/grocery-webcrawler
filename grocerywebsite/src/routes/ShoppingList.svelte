<script>
import {display_shopping_list} from './store'
import {getFromLocalStorage} from './shopping_list/LocalStorage'
import {IShoppingListItem} from './shopping_list/IShoppingListItem'
// import { addDollarSymbol } from '../util/textformat.js';



  
//let shoppingItems = getFromLocalStorage<IShoppingListItem>('shoppinglist', [])
let shoppingItems=[{
    "index":0,
	"itemName":"beef",
	"itemCategory":"meat",
	"upc":123457,
	"cheapestPrice":8.99,
	"cheapestPriceLocation":"500 arapahoe",
	"highestPrice":11.99,
	"highestPriceLocation":"500 camino",
	"optimalPrice":8.99,
	"optimalPriceLocation":"500 arapahoe",
},
{
    "index":1,
	"itemName":"beef2",
	"itemCategory":"meat",
	"upc":123457,
	"cheapestPrice":8.99,
	"cheapestPriceLocation":"500 arapahoe",
	"highestPrice":11.99,
	"highestPriceLocation":"500 camino",
	"optimalPrice":8.99,
	"optimalPriceLocation":"500 arapahoe"
}]

function deleteItem(index, shoppingItems){

}


</script>
{#key $display_shopping_list}
    {#if $display_shopping_list==true}
        <h1 class="text-white">Shopping List</h1>
        <table class="table table-hover table-light table-striped table-bordered">
            <thead>
                <tr>
                    <th scope="col">X</th>
                    <th scope="col">Item Name</th>
                    <th scope="col">Category</th>
                    <th scope="col">Cheapest Price</th>
                    <th scope="col">Cheapest Price Location</th>
                    <th scope="col">Highest Price</th>
                    <th scope="col">Highest Price Location</th>
                    <th scope="col">Optimal Store Price</th>
                    <th scope="col">Optimal Location</th>

                </tr>
            </thead>
            <tbody>
                <!-- {#if $shoppingItems && $shoppingItems.length>0}
                    {#each $shoppingItems as item}
                        <tr>
                            <td>
                                item.itemName
                            </td>
                            <td>
                                item.itemCategory
                            </td>
                            <td>
                                addDollarSymbol(item.cheapestPrice)
                            </td>
                            <td>
                                item.cheapestPriceLocation
                            </td>
                            <td>
                                addDollarSymbol(item.highestPrice)
                            </td>
                            <td>
                                item.highestPriceLocation
                            </td>
                            <td>
                                addDollarSymbol(item.optimalPrice)
                            </td>
                            <td>
                                item.optimalPriceLocation
                            </td>
                            <td></td>  item clicked delete item action
                        </tr>
                    {/each}
                {/if} -->
            </tbody>
        </table>
    {/if}
{/key}
<style>

</style>