<script>
    export let itemLabel;
    export let highlighted;

    
    //console.log(itemLabel)
  </script>
  
  <style>
  li.autocomplete-items {
    list-style: none;
    border-bottom: 1px solid #d4d4d4;
    z-index: 99;
    top:100%;
    /*position the autocomplete items to be the same width as the container:*/
    left: 0;
    right: 0;
    padding: 10px;
    padding-top: 10px;
    cursor: pointer;
    background-color: #fff;
  }
  
  li.autocomplete-items:hover {
    /*when hovering an item:*/
    background-color: #81921f;
      color: white;
  }
  
  li.autocomplete-items:active {
    /*when navigating through the items using the arrow keys:*/
    background-color: DodgerBlue !important;
    color: #ffffff;
  }	
      
  .autocomplete-active {
    /*when navigating through the items using the arrow keys:*/
    background-color: DodgerBlue !important;
    color: #ffffff;
  }
  .search-bar{
    padding-top:20px;
  }
  </style>
  {#if itemLabel !=undefined}
    <li class="nav-item autocomplete-items search-bar" class:autocomplete-active={highlighted} on:click>{itemLabel}</li>
  {/if}