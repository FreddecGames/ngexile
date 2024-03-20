export const formatDate = function(value) {

    value = new Date(value)
    return value.toLocaleString()
}

export const formatTime = function(value) {

    if (value == Infinity) return 'Infinity'

    if (value < 1) return Math.ceil(value * 1000) + ' ms'

    if (value > 31536000e3) return formatNumber(value / 31536000) + 'yr'

    if (value > 31536000) return Math.floor(value / 31536000) + 'yr ' + formatTime(value % 31536000)

    if (value > 86400) return Math.floor(value / 86400) + 'd ' + formatTime(value % 86400)

    let h = Math.floor(value / 3600)
    if (h < 10) { h = '0' + h }

    let m = Math.floor(value / 60) % 60
    if (m < 10) { m = '0' + m }

    let s = Math.floor(value % 60)
    if (s < 10) { s = '0' + s }

    let val = h + ':' + m + ':' + s                
    return val
}

export const formatNumber = function(value, fixed) {

    let sign = ''
    if (value < 0) sign = '-'

    let absValue = Math.abs(value)

    let ret = '', symbol = null

    if (absValue >= 1e33) {
        
        let start = 33
        for (let i = 0; i < 26; ++i) {
            for (let j = 0; j < 26; ++j) {
                
                let limit = Math.pow(10, start)

                if (absValue < limit) {
                    ret = (Math.floor(10 * absValue / (limit / 1e3)) / 10); symbol = String.fromCharCode(97 + i) + String.fromCharCode(97 + j);
                    break
                }
                else start += 3
            }

            if (ret != '') break
        }
    }
    
    else if (absValue >= 1e30) { ret = (Math.floor(10 * absValue / 1e30) / 10); symbol = 'Q'; }
    else if (absValue >= 1e27) { ret = (Math.floor(10 * absValue / 1e27) / 10); symbol = 'R'; }
    else if (absValue >= 1e24) { ret = (Math.floor(10 * absValue / 1e24) / 10); symbol = 'Y'; }
    else if (absValue >= 1e21) { ret = (Math.floor(10 * absValue / 1e21) / 10); symbol = 'Z'; }
    else if (absValue >= 1e18) { ret = (Math.floor(10 * absValue / 1e18) / 10); symbol = 'E'; }
    else if (absValue >= 1e15) { ret = (Math.floor(10 * absValue / 1e15) / 10); symbol = 'P'; }
    else if (absValue >= 1e12) { ret = (Math.floor(10 * absValue / 1e12) / 10); symbol = 'T'; }
    else if (absValue >= 1e9) { ret = (Math.floor(10 * absValue / 1e9) / 10); symbol = 'G'; }
    else if (absValue >= 1e6) { ret = (Math.floor(10 * absValue / 1e6) / 10); symbol = 'M'; }
    else if (absValue >= 1e3) { ret = (Math.floor(10 * absValue / 1e3) / 10); symbol = 'k'; }
    
    else ret = (Math.floor(100 * absValue) / 100)

    if (fixed >= 0) ret = ret.toFixed(fixed)

    return sign + ret + (symbol ? symbol : '')
}

import { defineStore } from 'pinia'

export const useGameStore = defineStore({

    id: 'app-store',

    state: () => { return {
        
    }},

    getters: {
        
    },
    
    actions: {
        
    },
})
