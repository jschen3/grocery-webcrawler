<script>
	import axios from 'axios';
    import {page_store_item, display_7_days, display_30_days} from '../store.js'
    
    import SelectOption from './select_options.svelte';	
        
        
    /* FILTERING countres DATA BASED ON INPUT */	
    let filterOptions = [];
    // $: console.log(filteredCountries)	
    
    const get_filter_options = async() => {
        let storageArr = []
        if (inputValueText && inputValueText.length>3){
            let storeItems;
            //console.log("store items starting async method")
            const response = await axios.get("https://server.grocerymarketwatch.com/items/2948?q="+inputValueText);
            const data = await response.data;
            //console.log(data);
            storeItems = data;
            storeItems.forEach(storeItem => {
                storageArr = [...storageArr, {"name":storeItem.name, "upc":storeItem.upc, "storeId":storeItem.storeId}];
                //console.log("storage area is:"+storageArr);
            });
        }
        filterOptions = storageArr;
    }	
    
    
    /* HANDLING THE INPUT */
    let searchInput; // use with bind:this to focus element
    let inputValueText = "";
    let inputValueObject = null;
        
    $: if (!inputValueText) {
        filterOptions = [];
        hiLiteIndex = null;
    }
    
    const clearInput = () => {
        inputValueText = "";	
        searchInput.focus();
        filterOptions = [];
    }
        
    const setInputVal = (inputVal) => {
        inputValueText = inputVal.name;
        inputValueObject = inputVal;
        console.log("inputValue object: "+inputValueObject);
        filterOptions = [];
        hiLiteIndex = null;
        document.querySelector('#searchbar-input').focus();
    }	
    
    const submitValue = () => {
        if (inputValueObject) {
            console.log(`${inputValueObject.name} is submitted!`);
            console.log(`${inputValueObject.upc} upc is:`);
            console.log(`${inputValueObject.storeId} storeId:`);
            page_store_item.set({"upc":inputValueObject.upc, "storeId":inputValueObject.storeId});
            display_7_days.set(false);
            display_30_days.set(false);
            console.log("display 7 days:"+$display_7_days);
            // let prev_greatest_price_change_options = $greatest_price_change_options
            // if (prev_greatest_price_change_options!=null && prev_greatest_price_change_options!=undefined){
            //     prev_greatest_price_change_options.visible=false;
            // }    
            // greatest_price_change_options.set(prev_greatest_price_change_options)
            // set these variables in a svelte store and pull data from svelte store 
            setTimeout(clearInput, 8000);
            filterOptions = [];
        } else {
            alert("You didn't type anything.");
        }
    }
    
    
    const removeBold = (str) => {
        //replace < and > all characters between
        return str.replace(/<(.)*?>/g, "");
        // return str.replace(/<(strong)>/g, "").replace(/<\/(strong)>/g, "");
    }	
        
    
    /* NAVIGATING OVER THE LIST OF COUNTRIES W HIGHLIGHTING */	
    let hiLiteIndex = null;
    //$: console.log(hiLiteIndex);	
    $: hiLitedCountry = filterOptions[hiLiteIndex]; 	
        
    const navigateList = (e) => {
        if (e.key === "ArrowDown" && hiLiteIndex <= filterOptions.length-1) {
            hiLiteIndex === null ? hiLiteIndex = 0 : hiLiteIndex += 1
        } else if (e.key === "ArrowUp" && hiLiteIndex !== null) {
            hiLiteIndex === 0 ? hiLiteIndex = filterOptions.length-1 : hiLiteIndex -= 1
        } else if (e.key === "Enter") {
            setInputVal(filterOptions[hiLiteIndex]);
        } else {
            return;
        }
    } 
    </script>
    
    
    <svelte:window on:keydown={navigateList} />
    
    <form class="form-inline my-2 my-lg-0 d-flex" autocomplete="off" on:submit|preventDefault={submitValue}>
        <div class="autocomplete">
            <input class="form-control mr-sm-2 bg-dark text-white navbar" id="searchbar-input"
                            type="text" 
                            placeholder="Search Store Items..."
                            bind:this={searchInput}
                            bind:value={inputValueText} 
                            on:input={get_filter_options}>
            {#if filterOptions.length > 0}
                <ul id="autocomplete-items-list">
                    {#each filterOptions as filterOption, i}
                        <SelectOption itemLabel={filterOption.name} highlighted={i === hiLiteIndex} on:click={() => setInputVal(filterOption)} />
                    {/each}
                </ul>
            {/if}
        </div>
        <button class="btn btn-outline-dark my-sm-0 svelte-bar-submit-button" type="submit">Search</button>
        
    </form>
        
        
    <style>
    #searchbar-input{
        position: relative;
    }    
    #autocomplete-items-list {
        position:absolute;
        margin: 0;
        padding: 0;
        top: 100%;
        width: 297px;
        border: 1px solid #ddd;
        background-color: #ddd;
    }	
    div.autocomplete {
      /*the container must be positioned relative:*/
      position: relative;
      display: inline-block;
      width: 350px;
    }
    input {
      border: 1px solid transparent;
      font-size: 16px;
        margin: 0;
    }
    input[type=text] {
      width: 100%;
    }
    .svelte-bar-submit-button{
        margin-left: 10px;
        height: 40px;
    }
    ::placeholder{
        color:white;
    }

    </style>	