import {writable} from 'svelte/store'
export const shoppingListOutput = writable({
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
});