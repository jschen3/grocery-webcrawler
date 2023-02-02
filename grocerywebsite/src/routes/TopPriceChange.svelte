<script>
    import {priceChangeData} from './store.js';

const priceChanges=[{
    "upc": "0002113012323",
    "id": "2948_0002113012323_2023-02-01 12:45:16.871068",
    "price30DaysAgo": 21.98,
    "date30DaysAgo": "2023-01-03T00:00:00",
    "priceChange7DaysAgo": -7,
    "percentPriceChange7DaysAgo": -70.14028056112224,
    "price7DaysAgo": 16.98,
    "earliestPrice": 9.98,
    "absPercentPriceChange7Days": 70.14028056112224,
    "name": "waterfront BISTRO Shrimp Raw Medium Ez Peel Shell & Tail On Frozen 31-40 Count - 2 Lb",
    "priceChange30Days": -12,
    "storeId": "2948",
    "percentPriceChange30Days": -120.24048096192384,
    "currentPrice": 15.98,
    "date7DaysAgo": "2023-01-25T00:00:00",
    "currentDate": "2023-02-01T12:45:16.871068",
    "earliestDate": "2023-01-01T00:00:00",
    "absPercentPriceChange30Days": 120.24048096192384
    },
    {
    "upc": "0002113012323",
    "id": "2948_0002113012323_2023-02-01 12:25:41.386314",
    "price30DaysAgo": 21.98,
    "date30DaysAgo": "2023-01-03T00:00:00",
    "priceChange7DaysAgo": -7,
    "percentPriceChange7DaysAgo": -70.14028056112224,
    "price7DaysAgo": 16.98,
    "earliestPrice": 9.98,
    "absPercentPriceChange7Days": 70.14028056112224,
    "name": "waterfront BISTRO Shrimp Raw Medium Ez Peel Shell & Tail On Frozen 31-40 Count - 2 Lb",
    "priceChange30Days": -12,
    "storeId": "2948",
    "percentPriceChange30Days": -120.24048096192384,
    "currentPrice": 15.98,
    "date7DaysAgo": "2023-01-25T00:00:00",
    "currentDate": "2023-02-01T12:25:41.386314",
    "earliestDate": "2023-01-01T00:00:00",
    "absPercentPriceChange30Days": 120.24048096192384
    },
    {
    "upc": "0002113012323",
    "id": "2948_0002113012323_2023-02-01 12:50:11.904679",
    "price30DaysAgo": 21.98,
    "date30DaysAgo": "2023-01-03T00:00:00",
    "priceChange7DaysAgo": -7,
    "percentPriceChange7DaysAgo": -70.14028056112224,
    "price7DaysAgo": 16.98,
    "earliestPrice": 9.98,
    "absPercentPriceChange7Days": 70.14028056112224,
    "name": "waterfront BISTRO Shrimp Raw Medium Ez Peel Shell & Tail On Frozen 31-40 Count - 2 Lb",
    "priceChange30Days": -12,
    "storeId": "2948",
    "percentPriceChange30Days": -120.24048096192384,
    "currentPrice": 15.98,
    "date7DaysAgo": "2023-01-25T00:00:00",
    "currentDate": "2023-02-01T12:50:11.904679",
    "earliestDate": "2023-01-01T00:00:00",
    "absPercentPriceChange30Days": 120.24048096192384
    },
    {
    "upc": "0020220000000",
    "id": "2948_0020220000000_2023-02-01 12:54:39.397363",
    "price30DaysAgo": 24.98,
    "date30DaysAgo": "2023-01-03T00:00:00",
    "priceChange7DaysAgo": -12.5,
    "percentPriceChange7DaysAgo": -100.16025641025641,
    "price7DaysAgo": 24.98,
    "earliestPrice": 12.48,
    "absPercentPriceChange7Days": 100.16025641025641,
    "name": "Meat Service Counter USDA Choice Beef Top Sirloin Roast Boneless - 2.5 Lb",
    "priceChange30Days": -12.5,
    "storeId": "2948",
    "percentPriceChange30Days": -100.16025641025641,
    "currentPrice": 24.98,
    "date7DaysAgo": "2023-01-25T00:00:00",
    "currentDate": "2023-02-01T12:54:39.397363",
    "earliestDate": "2023-01-01T00:00:00",
    "absPercentPriceChange30Days": 100.16025641025641
}]

</script>

<table class="table table-hover table-light table-striped table-bordered">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">UPC</th>
            <th scope="col">Category</th>
            <th scope="col">Current Price</th>
            <th scope="col">Price 7 Days Ago</th>
            <th scope="col">Price 30 Days Ago</th>
            <th scope="col">Percent Price Change 7 Days Ago</th>
            <th scope="col">Percent Price Change 30 Days Ago</th>
            <th scope="col">Graph</th>
        </tr>
        </thead>
        <tbody>
        {#if $priceChangeData}    
        {#key $priceChangeData}
            {#each $priceChangeData as priceChange, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td>{priceChange.name}</td>
                    <td>{priceChange.upc}</td>
                    <td>{priceChange.category}</td>
                    <td>{priceChange.currentPrice}</td>
                    <td>{priceChange.price7DaysAgo}</td>
                    <td>{priceChange.price30DaysAgo}</td>
                    <td>{priceChange.percentPriceChange7DaysAgo}</td>
                    <td>{priceChange.percentPriceChange30Days}</td>
                    <td>Graph</td>
                </tr>
            {/each}    
        {/key}
        {/if}
        </tbody>
    
</table>



<style>
.table{
    margin-top:50px;
}
</style>
