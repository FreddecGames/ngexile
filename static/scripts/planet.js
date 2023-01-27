function planet_str(id,name,g,s,p,rel)
{
	if(rel == 2)
		var s = '<a href="/s03/planet/?planet='+id+'" class="self" data-bs-toggle="tooltip" data-bs-title="Voir planète">'+name+'</a> <a href="/s03/map/?g='+g+'&s='+s+'" class="ms-2 self" data-bs-toggle="tooltip" data-bs-title="Carte spatiale">'+g+'.'+s+'.'+p+'</a>';
	else
	{
		switch(rel){
			case 1: var col = 'ally'; break;
			case 0:	var col = 'friend'; break;
			case -1: var col = 'enemy'; break;
			case -2: var col = 'enemy'; break;
			case -3: var col = 'neutral'; break;
		}

		var s = '<a href="/s03/map/?g='+g+'&s='+s+'" class="'+col+'" data-bs-toggle="tooltip" data-bs-title="Carte spatiale">'+(name ? '<span class="me-2">' + name + '</span>': '')+'<span>'+g+'.'+s+'.'+p+'</span></a>';
	}

	return s;
}
function putplanet(id,name,g,s,p,rel){ document.write(planet_str(id,name,g,s,p,rel)); }