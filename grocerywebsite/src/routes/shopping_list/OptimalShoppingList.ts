import type { PriceAtStore } from "./PriceAtStore"

export interface GroupedStoreAndItems{
    index: number
    storeId: string
    shoppingItems: Array<PriceAtStore>
    totalPrice:number
    missingItems: Array<string>
}