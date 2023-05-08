//---
function formatNumber(value, fixed=0) {
    //---
    let sign = ''
    if (value < 0) sign = '-'
    //---
    let absValue = Math.abs(value)
    //---
    let ret = '', symbol = null
    //---
    if (absValue >= 1e9) { ret = (Math.round(100 * absValue / 1e9) / 100); symbol = 'G'; }
    else if (absValue >= 1e6) { ret = (Math.round(100 * absValue / 1e6) / 100); symbol = 'M'; }
    else if (absValue >= 1e3) { ret = (Math.round(100 * absValue / 1e3) / 100); symbol = 'k'; }
    else ret = (Math.round(100 * absValue) / 100)
    //---
    if (fixed) ret = ret.toFixed(fixed)
    //---
    document.write(sign + ret + (symbol ? ' <small class="text-muted">' + symbol + '</small>' : ''))
}
//---
function formatPlanet(g, s, p, rel) {
    //---
    switch(rel) {
        //---
        case 2: var col = 'text-self'; break;
        case 1: var col = 'text-ally'; break;
        case 0:	var col = 'text-friend'; break;
        case -1: var col = 'text-enemy'; break;
        case -2: var col = 'text-enemy'; break;
        default: var col = 'text-normal'; break;
    }
    //---
	document.write('<a href="/ng0/map-sector/?g=' + g + '&s=' + s + '" class="' + col + '"><span>' + g + '.' + s + '.' + p + '</span></a>')
}