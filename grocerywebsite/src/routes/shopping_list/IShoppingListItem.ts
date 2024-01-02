export interface IShoppingListItem{
    index: number
    itemName:string
    upc:string
    cheapestPrice:number
    cheapestPriceLocation:string
    highestPrice:number
    highestPriceLocation:string
    updatedDate:Date
}