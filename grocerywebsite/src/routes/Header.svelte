<script>
    import Heart from "svelte-bootstrap-icons/lib/Heart.svelte"
	import SelectBar from "./header_components/select_bar.svelte";
</script>

<header>
	<nav class="header-nav navbar navbar-expand-lg bg-secondary">
        <a class="navbar-brand navbar btn-secondary">Grocery Market Watch</a>
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

		<!--
			https://svelte.dev/repl/d9360e33b13f4bf2b78c99cff6145b9a?version=3.47.0
		-->
        <!--
        https://svelte.dev/repl/5734f123973d4682978427024ca90850?version=3.29.0

        -->
		<a class="grocery-prices nav-link"><Heart/> Favorites</a>
	</nav>
</header>

<style>
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
