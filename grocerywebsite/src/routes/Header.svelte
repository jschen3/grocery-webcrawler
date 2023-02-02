<script>
    import Stock_Market_Icon from "$lib/images/stock_market_icon.png";
    import Heart from "svelte-bootstrap-icons/lib/Heart.svelte"
	import SelectBar from "./header_components/select_bar.svelte";
</script>

<header>
	<nav class="header-nav navbar navbar-expand-lg bg-secondary">
        <a class="navbar-brand navbar btn-secondary" href="#">
            <img src={Stock_Market_Icon} class="stock-icon" alt="stock icon"/>
            Grocery Market Watch</a>
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
		<a class="grocery-prices nav-link" href="#"><Heart/> Favorites</a>
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
