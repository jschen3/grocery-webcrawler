<script>
  import { scaleLinear } from "d3-scale";
  import { extent, bisector } from "d3-array";
  import { line, area } from "d3-shape";
  import { format } from "d3-format";
  import { timeFormat } from "d3-time-format";
  import TooltipTop from "./TooltipTop.svelte";
  import TooltipRight from "./TooltipRight.svelte";
  import TooltipPoint from "./TooltipPoint.svelte";
  import TooltipLines from "./TooltipLines.svelte";
  import Axes from "./Axes.svelte";
  import ChartArea from "./ChartArea.svelte";
  import ChartLine from "./ChartLine.svelte";
  import { timeParse } from "d3-time-format";

export let pricingValue;
	let pricingData = pricingValue
if (pricingData==undefined){
  pricingData = [{
    "name": "",
    "upc": "",
    "date": "2023-01-26",
    "price": 0.0,
    "basePrice": 0.0,
    "pricePer": 0.0
    }];
}

pricingData.forEach((d) => {
    d.date = timeParse("%Y-%m-%d")(d.date);
    d.date = new Date(d.date);
  });
console.log("pricingData:" +pricingData);

    const padding = { top: 30, right: 10, bottom: 20, left: 20 };
    let width = 500
    let height = 250;

    var formatTime = timeFormat("%b %d");
    var formatDollars = format("$.2f");

    let m = { x: 0, y: 0 };

    var bisect = bisector((d) => d.date).right;

    function handleMousemove(event) {
      m.x = event.offsetX;
      m.y = event.offsetY;
      let i = bisect(pricingData, xScale.invert(m.x));
      if (i < pricingData.length) {
        point = pricingData[i];
      }
    }

    $: minX = pricingData[0].date;
    $: maxX = pricingData[pricingData.length - 1].date;
    $: extentY = extent(pricingData, (d) => d.price);

    $: xScale = scaleLinear()
      .domain([minX, maxX])
      .range([padding.left, width - padding.right]);
    $: yScale = scaleLinear()
      .domain([0, extentY[1]])
      .range([height - padding.bottom, padding.top]);

    $: xTicks = xScale.ticks(5);
    $: yTicks = yScale.ticks(4);

    $: pathLine = line()
      .x((d) => xScale(d.date))
      .y((d) => yScale(d.price))(pricingData);
    $: pathArea = area()
      .x((d) => xScale(d.date))
      .y1((d) => yScale(d.price))
      .y0(yScale(0))(pricingData);

    // $: pathLine2 = line()
    //   .x((d) => xScale(d.date))
    //   .y((d) => yScale(d.basePrice))(pricingData);
    // $: pathArea2 = area()
    //   .x((d) => xScale(d.date))
    //   .y1((d) => yScale(d.basePrice))
    //   .y0(yScale(0))(pricingData);

    $: point = pricingData[0];
    $: last = pricingData[pricingData.length - 1];



    // coords for horizontal tooltip line
    let hline = {};
    $: hline.y1 = yScale(point.price);
    $: hline.y2 = yScale(point.price);
    $: hline.x1 = padding.left;
    $: hline.x2 = width - padding.right;

    // coords for vertical tooltip line
    let vline = {};
    $: vline.y1 = 0;
    $: vline.y2 = height - padding.bottom;
    $: vline.x1 = xScale(point.date);
    $: vline.x2 = xScale(point.date);
  </script>
  {#key pricingValue}
  <div class="chart" bind:clientHeight={height} bind:clientWidth={width}>
    <TooltipTop value={formatTime(point.date)} left={xScale(point.date)} />
    
    <TooltipRight
      value={formatDollars(last.price)}
      top={yScale(last.price)}
      type="last"
    />
    <TooltipRight
      value={formatDollars(point.price)}
      top={yScale(point.price)}

      type="point"
    />
    <svg on:mousemove={handleMousemove}>
      <TooltipLines {hline} {vline} />
      <Axes
        {xTicks}
        {yTicks}
        {xScale}
        {yScale}
        {width}
        {height}
        {padding}
        {formatTime}
      />
  
      <!-- data -->
      <ChartArea  {pathArea} /> 
   
      <ChartLine {pathLine} /> 
      
      <!-- tooltip point marker -->
      <TooltipPoint x={xScale(point.date)} y={yScale(point.price)} />  
    </svg>
  </div>
  {/key}
  <style>
    .chart {
      width: 100%;
      margin-left: auto;
      margin-right: auto;
    }
  
    svg {
      position: relative;
      width: 100%;
      height: 250px;
      overflow: visible;
    }
  </style>