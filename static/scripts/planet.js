function planet_str(id,name,g,s,p,rel)
{
	if(rel == 2)
		var s = '<a href="/game/planet/?planet='+id+'" class="self" title="'+inspectplanet+name+'">'+name+'</a> <a href="/game/map/?g='+g+'&s='+s+'" class="self" title="'+locateplanet+name+'">('+g+'.'+s+'.'+p+')</a>';
	else
	{
		switch(rel){
			case 1: var col = 'ally'; break;
			case 0:	var col = 'friend'; break;
			case -1: var col = 'enemy'; break;
			case -2: var col = 'enemy'; break;
			case -3: var col = 'neutral'; break;
		}

		var s = '<a href="/game/map/?g='+g+'&s='+s+'" class="'+col+'" title="'+locateplanet+name+'">'+name+' ('+g+'.'+s+'.'+p+')</a>';
	}

	return s;
}
function putplanet(id,name,g,s,p,rel){ document.write(planet_str(id,name,g,s,p,rel)); }