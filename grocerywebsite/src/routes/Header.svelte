<script>
    import Stock_Market_Icon from "$lib/images/stock_market_icon.png";    
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
	<nav class="header-nav navbar navbar-expand-lg navbar-dark bg-secondary">
        <div class="container-fluid">
            <a class="navbar-brand navbar btn-secondary" href="#">
                <img src={Stock_Market_Icon} class="stock-icon" alt="stock icon"/></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav me-auto mb-2 mb-lg-0">
                    <select id="Area" class="nav-item header-area bg-dark text-white">
                        <option>Bay Area</option>
                        <!-- <option>San Francisco</option>
                        <option>Denver</option>
                        <option>Texas</option>
                        <option>Northwest(washington, oregon)</option>    -->
                    </select>
                    <select id="Store" class="nav-item header-store bg-dark text-white">
                        <option>2948 645 San Antonio Rd</option>
                    </select>
                    <SelectBar/>
                    {#if $display_7_days==true}
                        <a class="nav-item nav-link active" on:click={seven_day_click}>7 Day Price Changes</a>
                        <a class="nav-item nav-link" on:click={thirty_day_click}>30 Day Price Changes</a>
                    {:else if $display_30_days==true}          
                        <a class="nav-item nav-link" on:click={seven_day_click}>7 Day Price Changes</a>
                        <a class="nav-item nav-link active" on:click={thirty_day_click}>30 Day Price Changes</a>
                    {:else}
                        <a class="nav-item nav-link" on:click={seven_day_click}>7 Day Price Changes</a>
                        <a class="nav-item nav-link" on:click={thirty_day_click}>30 Day Price Changes</a>
                    {/if}                            
                </div>    
            </div>
        </div>
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
    /* .navbar{
        height: 60px;
    }
    .nav-link{
        margin-left: 10px;
    } */
</style>
