<script>
	import axios from 'axios';
    import {page_store_item} from '../store.js'
    
    import SelectOption from './select_options.svelte';	
        
        
    /* FILTERING countres DATA BASED ON INPUT */	
    let filterOptions = [];
    // $: console.log(filteredCountries)	
    
    const get_filter_options = async() => {
        let storageArr = []
        if (inputValueText && inputValueText.length>3){
            let storeItems;
            //console.log("store items starting async method")
            const response = await axios.get("http://localhost:8000/items/2948?q="+inputValueText);
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
            page_store_item.set({"upc":inputValueObject.upc, "storeId":inputValueObject.storeId})
            // set these variables in a svelte store and pull data from svelte store 
            setTimeout(clearInput, 5000);
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
    
    <form class="form-inline my-2 my-lg-0" autocomplete="off" on:submit|preventDefault={submitValue}>
      <div class="autocomplete">
        <input class="form-control mr-sm-2 bg-dark text-white navbar" id="searchbar-input"
                         type="text" 
                         placeholder="Search Store Items..."
                         bind:this={searchInput}
                         bind:value={inputValueText} 
                         on:input={get_filter_options}>
      </div>
        
      <button class="btn btn-outline-dark my-2 my-sm-0 svelte-bar-submit-button" type="submit">Search</button>
        
        <!-- FILTERED LIST OF COUNTRIES -->
        <!-- need to mess with and change toa await promise and mess with promises. -->
        {#if filterOptions.length > 0}
            <ul id="autocomplete-items-list navbar-nav mr-auto">
                {#each filterOptions as filterOption, i}
                    <SelectOption itemLabel={filterOption.name} highlighted={i === hiLiteIndex} on:click={() => setInputVal(filterOption)} />
                {/each}
            </ul>
        {/if}
    </form>
        
        
    <style>
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
    }
    ::placeholder{
        color:white;
    }

    </style>	