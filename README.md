# Grocery Webcrawler
## 3 Pieces
### Piece 1:
Web crawler that makes a selenium to a safeway website and acquires an api key. From the api key a series of web calls are triggered that downloads the prices and all items in a particular safeway store. Prices are stored in aws rds.

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
