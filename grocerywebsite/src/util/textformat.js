export function colorPercentText(percent){
    if (percent>0){
        return "<span style=\"color:green;\"><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
    }
    else if (percent==0){
        return "<span><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
    }
    else{
        return "<span style=\"color:red;\"><i class=\"bi bi-caret-down\"></i>"+ naiveRound(percent)+"%</span>"
    }
}
export function percentText(percent){
    if (percent>0){
        return "<span><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
    }
    else if (percent==0){
        return "<span><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"%</span>"
    }
    else{
        return "<span><i class=\"bi bi-caret-down\"></i>"+ naiveRound(percent)+"%</span>"
    }
}

export function naiveRound(num, decimalPlaces = 2) {
    var p = Math.pow(10, decimalPlaces);
    return (Math.round(num * p) / p).toFixed(2);

}

export function addDollarSymbol(num){
    return "$"+num.toFixed(2);
}

export function colorSymbolRound(percent){
    if (percent>0){
        return "<span style=\"color:green;\"><i class=\"bi bi-caret-up\"></i>+"+ naiveRound(percent)+"</span>"
    }
    else if (percent==0){
        return "<span>"+ naiveRound(percent)+"</span>"
    }
    else{
        return "<span style=\"color:red;\"><i class=\"bi bi-caret-down\"></i>"+ naiveRound(percent)+"</span>"
    }
}