export interface IShoppingListItem{
    index: number
    itemName:string
    itemCategory:string
    upc:string
    cheapestPrice:number
    cheapestPriceLocation:string
    highestPrice:number
    highestPriceLocation:string
    optimalPrice:number
    optimalPriceLocation:string
}