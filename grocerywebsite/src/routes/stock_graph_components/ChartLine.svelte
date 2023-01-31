<script>
    export let pathLine;
    //console.log(pathLine);
    //export let pathLine2;
  </script>
  
  <path class="path-line" d={pathLine}  /> 
  <!--<path class="path-line2" d={pathLine2}  />-->
  <style>
    .path-line {
      fill: none;
      stroke: rgb(100, 0, 3);
      stroke-linejoin: round;
      stroke-linecap: round;
      stroke-width: 2;
    }
    .path-line2 {
      fill: none;
      stroke: rgb(100, 0, 40);
      stroke-linejoin: round;
      stroke-linecap: round;
      stroke-width: 2;
    }
  </style>