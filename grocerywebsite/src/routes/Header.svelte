<script>
  import Stock_Market_Icon from "$lib/images/stock_market_icon.png";    
	import SelectBar from "./header_components/select_bar.svelte";
	import { display_7_days, page_store_item, display_30_days ,greatest_price_change_options_30, greatest_price_change_options_7, storeId} from "./store";

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

    function locationClicked(storeIdValue){
      if (storeIdValue!=null && storeIdValue!=undefined){
        // clone and copy variabls...
        let clone30 = JSON.parse(JSON.stringify($greatest_price_change_options_30));
        let clone7 = JSON.parse(JSON.stringify($greatest_price_change_options_7));
        storeId.set(storeIdValue)
        greatest_price_change_options_30.set({
          "storeId":storeIdValue,
          "thirty_day_or_7_day": true,
          "offset": 0,
          "limit": 50,
        });
        greatest_price_change_options_7.set({
          "storeId":storeIdValue,
          "thirty_day_or_7_day": false,
          "offset": 0,
          "limit": 50,
        });
        console.log(clone30);
        console.log(clone7);
      }
    }
</script>

<header>
<nav class="navbar navbar-expand-lg navbar-dark bg-secondary">
  <div class="container-fluid">
    <a class="navbar-brand" on:click={seven_day_click}><img src={Stock_Market_Icon} class="stock-icon" alt="stock icon"/>Grocery Market Watch</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">  
        <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Location
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" on:click|once={locationClicked(2948)}>645 San Antonio, Mountain View, Ca</a>
              <a class="dropdown-item" on:click|once={locationClicked(705)}>570 N Shorline Blvd, Mountain View Ca</a>
              <a class="dropdown-item" on:click|once={locationClicked(2887)}>150 El Camino Real, Sunnyvale, Ca</a>
              <a class="dropdown-item" on:click|once={locationClicked(1465)}>5146 Stevens Creek Blvd, San Jose, Ca</a>
              <a class="dropdown-item" on:click|once={locationClicked(1682)}>2811 Middlefield Rd, Palo Alto, Ca</a>
              <a class="dropdown-item" on:click|once={locationClicked(767)}>6150 Bollinger Rd, San Jose, Ca</a>
            </div>
          </li>
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
      </ul>
      <SelectBar/>
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
    } */
    /*
    .nav-link{
        margin-left: 10px;
    } */
</style>
