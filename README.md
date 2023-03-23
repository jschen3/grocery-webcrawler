# Grocery Webcrawler
## https://grocerymarketwatch.com
## 3 Pieces
### Piece 1:
Web crawler: In order to get prices from safeway.com. You do the following steps. 
1. Selenium get an api key.
2. Paginate and grab every item on the deals page for a particular store. Collect the price of each item. Collect prices everyday and store it into RDS. 
Currently only supports local bay area stores. 


### Piece 2:
For each distinct item we calculate the price changes for 7 days, 30 days and all records. 

### Piece 3:
Svelte UI where you can search and receive a graph of the price changes of an item for 30 days.

## Built With
* Python
* Svelte
* AWS RDS

## Getting started
- Piece 1 is called by the file webcrawl.py
- Piece 2 is called by the file pricechange.py

## Website 
### grocerywebsite
1. npm install
2. npm run dev

## More Detailed FAQ
https://docs.google.com/document/d/1lk6KaXkdY_-acrKYbjEW9h_ECPEg7JN7C1RDlYvtrX4/edit?usp=sharing
