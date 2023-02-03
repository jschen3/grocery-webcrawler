<script>
    import Stock_Market_Icon from "$lib/images/stock_market_icon.png";
	import { dispatch_dev } from "svelte/internal";
    
	import SelectBar from "./header_components/select_bar.svelte";
	import { display_7_days, page_store_item, display_30_days } from "./store";

    function seven_day_click(){
        page_store_item.set(null);
        display_7_days.set(true);
        display_30_days.set(false);
    }

    function thirty_day_click(){
        page_store_item.set(null);
        display_7_days.set(false);
        display_30_days.set(true);
    }

</script>

<header>
	<nav class="header-nav navbar navbar-expand-lg bg-secondary">
        <a class="navbar-brand navbar btn-secondary" href="#">
            <img src={Stock_Market_Icon} class="stock-icon" alt="stock icon"/>
            Grocery Market Watch</a>
        <ul class="navbar-nav">
            <select id="Area" class="header-area bg-dark text-white">
                <option>Bay Area</option>
                <!-- <option>San Francisco</option>
                <option>Denver</option>
                <option>Texas</option>
                <option>Northwest(washington, oregon)</option> -->   
            </select>
            <select id="Store" class="header-store bg-dark text-white">
                <option>2948 645 San Antonio Rd</option>
            </select>
            <SelectBar/>
                <li class="nav-item">
                    <a class="nav-link text-white" on:click={seven_day_click}>7 Day Price Changes</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-white" on:click={thirty_day_click}>30 Day Price Changes</a>
                </li>
        </ul>    
	</nav>
</header>

<style>
    .stock-icon{
        margin-right:10px;
    }
    .header-nav{
        display: flex;
        flex-direction: row;
    }
    .header-area{
        border-radius: 5px;
        height: 40px;
        margin-right:15px;
    }
    .header-store{
        border-radius: 5px;
        height: 40px;
        margin-right:15px;
    }
    .navbar{
        height: 60px;
    }
</style>
