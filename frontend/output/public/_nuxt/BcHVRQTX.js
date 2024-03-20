import{L as a,v as l,B as o,x as s,y as e,M as n,t as c}from"./Cah09oso.js";const d=a("/img/interface/credits.gif"),r=a("/img/interface/ore.gif"),_=a("/img/interface/hydrocarbon.gif"),h=a("/img/interface/workers.gif"),m=a("/img/interface/scientists.gif"),p=a("/img/interface/soldiers.gif"),f=a("/img/interface/prestige.gif"),g=a("/img/interface/stance_attack.gif"),u=a("/img/interface/stance_defend.gif"),v={class:"scroll-content",style:{height:"calc(100% - 52px)"}},b={class:"page-content"},w={class:"row g-3"},y={class:"col-12"},k={class:"card"},V=s("div",{class:"card-header","data-bs-toggle":"collapse","data-bs-target":"#motd_content"},[s("span",{class:"fs-6"}," Annonce de l'alliance - {% if alliance.defcon == 5 %}DEFCON 5: Préparation normale en temps de paix {% elif alliance.defcon == 4 %}DEFCON 4: Préparation normale, mais renseignement accru et mesures de sécurité renforcées {% elif alliance.defcon == 3 %}DEFCON 3: Accroissement de la préparation des forces au-dessus de la préparation normale {% elif alliance.defcon == 2 %}DEFCON 2: Accroissement supplémentaire dans la préparation des forces {% elif alliance.defcon == 1 %}DEFCON 1: Préparation maximale des forces (état de guerre) {% endif %} ")],-1),x={id:"motd_content",class:"collapse show"},N={class:"card-body"},S={class:"col-12"},A={class:"card"},C={class:"card-header","data-bs-toggle":"collapse","data-bs-target":"#stats_content"},M={class:"fs-6"},T={id:"stats_content",class:"collapse show"},E={class:"card-body"},D={class:"row gx-3"},F={class:"col-5"},q={class:"row g-1 flex-column"},B={class:"col-12"},O=s("span",{class:"text-normal me-2"},"Nation",-1),P=s("span",{class:"me-2"}," {% if orientation == 1 %}Marchand {% elif orientation == 2 %}Militaire {% elif orientation == 3 %}Scientifique {% endif %} ",-1),j={class:"text-info me-2"},H={class:"col-12"},L=s("span",{class:"text-normal me-2"},"Grade",-1),R={href:"/s03/alliance-view/?tag={{ alliance.tag }}",class:"ms-2","data-bs-toggle":"tooltip","data-bs-title":"Voir alliance"},G=s("span",{class:"text-normal"},"Indépendant",-1),I={class:"col-12"},U=s("span",{class:"text-normal me-2"},"Trésorerie",-1),z=s("img",{src:d,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Crédits",width:"16px",height:"16px"},null,-1),J={class:"{% if stat_credits <= 0 %}text-danger{% endif %}"},K={class:"col-12"},Q=s("span",{class:"text-normal me-2"},"Score de développement",-1),W={class:"ms-2 {% if stat_score_delta > 0 %}text-success{% else %}text-danger{% endif %}"},X={href:"/s03/ranking-players/",class:"small ms-2","data-bs-toggle":"tooltip","data-bs-title":"Voir classement"},Y={class:"col-4"},Z={class:"row g-1 flex-column"},$={class:"col-12"},ss=s("span",{class:"text-normal me-2"},"Nombre de colonies",-1),ts={class:"text-normal"},es={class:"col-12"},os=s("span",{class:"text-normal me-2"},"Minerai par heure",-1),as=s("img",{src:r,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Minerai",width:"16px",height:"16px"},null,-1),is={class:"col-12"},ls=s("span",{class:"text-normal me-2"},"Hydrocarbure par heure",-1),ns=s("img",{src:_,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Hydrocarbure",width:"16px",height:"16px"},null,-1),cs={class:"col-12"},ds=s("span",{class:"text-normal me-2"},"Score de prestige",-1),rs={href:"/s03/ranking-players/?col=4",class:"small ms-2","data-bs-toggle":"tooltip","data-bs-title":"Voir classement"},_s={class:"col-3"},hs={class:"row g-1 flex-column"},ms={class:"col-12"},ps=s("span",{class:"text-normal me-2"},"Travailleurs",-1),fs=s("img",{src:h,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Travailleur",width:"16px",height:"16px"},null,-1),gs=s("span",{class:"text-normal me-2"},"Scientifiques",-1),us=s("img",{src:m,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Scientifique",width:"16px",height:"16px"},null,-1),vs=s("span",{class:"text-normal me-2"},"Soldats",-1),bs=s("img",{src:p,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Soldat",width:"16px",height:"16px"},null,-1),ws=s("span",{class:"text-normal me-2"},"Points de prestige",-1),ys=s("img",{src:f,class:"res","data-bs-toggle":"tooltip","data-bs-title":"Prestige",width:"16px",height:"16px"},null,-1),ks={class:"col-12"},Vs={class:"card"},xs=s("div",{class:"card-header"},[s("span",{class:"fs-6"},"Mouvements en cours")],-1),Ns={class:"card-body"},Ss={class:"row gx-3"},As={class:"col"},Cs=s("img",{src:g,class:"stance","data-bs-toggle":"tooltip","data-bs-title":"Mode attaque",width:"10",height:"10"},null,-1),Ms=s("img",{src:u,class:"stance","data-bs-toggle":"tooltip","data-bs-title":"Mode riposte",width:"10",height:"10"},null,-1),Ts={href:"/s03/fleet-view/?id={{ fleet.id }}",class:"text-info","data-bs-toggle":"tooltip","data-bs-title":"Voir flotte"},Es={href:"/s03/mail-new/?to={{ fleet.name }}",class:"text-success","data-bs-toggle":"tooltip","data-bs-title":"Contacter propriétaire"},Ds={href:"/s03/mail-new/?to={{ fleet.name }}",class:"text-friend","data-bs-toggle":"tooltip","data-bs-title":"Contacter propriétaire"},Fs={href:"/s03/profile-view/?name={{ fleet.owner_name }}",class:"text-danger","data-bs-toggle":"tooltip","data-bs-title":"Voir profil"},qs={class:"ms-2"},Bs={class:"col-auto"},Os=s("span",{class:"text-normal"},"???",-1),Ps=s("i",{class:"fa-fw fas fa-long-arrow-alt-right mx-2 text-normal"},null,-1),js={class:"col-auto text-end",style:{width:"75px"}},Hs={class:"text-yellow"},Ls=s("div",{class:"card-body text-center"},[s("span",{class:"text-normal"},"Aucun mouvement en cours")],-1),Rs={class:"col-12"},Gs={class:"card"},Is=s("div",{class:"card-header"},[s("span",{class:"fs-6"},"Recherche en cours")],-1),Us={class:"card-body"},zs={class:"row gx-3"},Js={class:"col"},Ks={href:"/s03/tech-list/#{{ research.researchid }}","data-bs-toggle":"tooltip","data-bs-title":"Voir laboratoire"},Qs={class:"col-auto"},Ws={class:"text-yellow"},Xs=s("a",{href:"/s03/tech-list/","data-bs-toggle":"tooltip","data-bs-title":"Voir laboratoire"},"Aucune recherche en cours",-1),Ys={class:"col-6"},Zs={class:"card"},$s=s("div",{class:"card-header"},[s("span",{class:"fs-6"},"Bâtiments en construction")],-1),st={class:"card-body"},tt={class:"row gx-3"},et={class:"col-auto",style:{width:"55px"}},ot={class:"text-normal"},at={class:"col"},it={href:"/s03/planet-buildings/?planet={{ item.planetid }}","data-bs-toggle":"tooltip","data-bs-title":"Voir bâtiments"},lt={class:"col-auto"},nt={class:"row g-1 flex-column"},ct={class:"col-12"},dt={class:"row gx-3 justify-content-end"},rt={class:"col text-end"},_t={class:"{% if building.destroying %}text-danger{% endif %}"},ht={class:"col-auto text-end",style:{width:"75px"}},mt={class:"text-yellow"},pt=s("div",{class:"col-12 text-end"},[s("span",{class:"text-normal"},"Aucun bâtiment en cours")],-1),ft={class:"col-6"},gt={class:"card"},ut=s("div",{class:"card-header"},[s("span",{class:"fs-6"},"Vaisseaux en construction")],-1),vt={class:"card-body"},bt={class:"row gx-3"},wt={class:"col-auto",style:{width:"55px"}},yt={class:"text-normal"},kt={class:"col"},Vt={href:"/s03/planet-ships/?planet={{ item.planetid }}","data-bs-toggle":"tooltip","data-bs-title":"Voir vaisseaux"},xt={class:"col-auto"},Nt={class:"row gx-3 justify-content-end"},St={class:"col"},At=s("div",{class:"col-auto"},[s("span",{class:"text-danger"},"En attente de ressources")],-1),Ct={class:"row gx-3 justify-content-end"},Mt={class:"col"},Tt={class:"{% if item.recycle %}text-danger{% endif %}"},Et={class:"col-auto text-end",style:{width:"65px"}},Dt={class:"text-yellow"},Ft=s("span",{class:"text-normal"},"Aucun vaisseau en cours",-1),Pt={__name:"view",setup(qt){function i(t){t>0?document.write("<small>"+formatnumber(t)+"</small>"):document.write("???")}return(t,Bt)=>(c(),l(n,null,[o(' {% include "s03/empire-tabs.html" %} '),s("div",v,[s("div",b,[s("div",w,[o(" {% if alliance %} "),s("div",y,[s("div",k,[V,s("div",x,[s("div",N,e(t.alliance.announce|t.safe|t.bbcode),1)])])]),o(" {% endif %} "),s("div",S,[s("div",A,[s("div",C,[s("span",M,"Statistiques de votre empire - "+e(t.date),1)]),s("div",T,[s("div",E,[s("div",D,[s("div",F,[s("div",q,[s("div",B,[O,P,s("span",j,e(t.nation),1)]),s("div",H,[L,o(" {% if alliance %}"+e(t.alliance_rank_label),1),s("a",R,"["+e(t.alliance.tag)+"] "+e(t.alliance.name),1),o(" {% else %}"),G,o(" {% endif %} ")]),s("div",I,[U,z,s("span",J,e(t.stat_credits|t.intcomma),1)]),s("div",K,[Q,o(" "+e(t.stat_score|t.intcomma)+" ",1),s("small",W,"{% if stat_score_delta > 0 %}+{% endif %}"+e(t.stat_score_delta|t.intcomma),1),s("a",X,e(t.stat_rank)+" /"+e(t.stat_players),1)])])]),s("div",Y,[s("div",Z,[s("div",$,[ss,o(" "+e(t.stat_colonies|t.intcomma)+" ",1),s("small",ts,"/"+e(t.stat_maxcolonies|t.intcomma),1)]),s("div",es,[os,as,o(" "+e(t.stat_prod_ore|t.intcomma),1)]),s("div",is,[ls,ns,o(" "+e(t.stat_prod_hydrocarbon|t.intcomma),1)]),s("div",cs,[ds,o(" "+e(t.stat_score_battle|t.intcomma)+" ",1),s("a",rs,e(t.stat_rank_battle)+" /"+e(t.stat_players),1)])])]),s("div",_s,[s("div",hs,[s("div",ms,[ps,fs,o(" "+e(t.stat_workers|t.intcomma),1)]),s("div",null,[gs,us,o(" "+e(t.stat_scientists|t.intcomma),1)]),s("div",null,[vs,bs,o(" "+e(t.stat_soldiers|t.intcomma),1)]),s("div",null,[ws,ys,o(" "+e(t.stat_victory_marks|t.intcomma),1)])])])])])])])]),s("div",ks,[s("div",Vs,[xs,o(" {% for fleet in fleets %} "),s("div",Ns,[s("div",Ss,[s("div",As,[o(" {% if fleet.owner_relation == 2 %} {% if fleet.attackonsight %} "),Cs,o(" {% else %} "),Ms,o(" {% endif %} "),s("a",Ts,e(t.fleet.name),1),o(" {% elif fleet.owner_relation == 1 %} "),s("a",Es,e(t.fleet.owner_name),1),o(" {% elif fleet.owner_relation == 0 %} "),s("a",Ds,e(t.fleet.owner_name),1),o(" {% else %} "),s("a",Fs,e(t.fleet.owner_name),1),o(" {% endif %} "),s("span",qs,e(i(t.fleet.signature)),1)]),s("div",Bs,[o(" {% if fleet.f_planetid %}"+e(t.putplanet(t.fleet.f_planetid,t.fleet.f_planetname,t.fleet.f_g,t.fleet.f_s,t.fleet.f_p,t.fleet.f_relation))+" {% else %}",1),Os,o("{% endif %} "),Ps,o(" "+e(t.putplanet(t.fleet.t_planetid,t.fleet.t_planetname,t.fleet.t_g,t.fleet.t_s,t.fleet.t_p,t.fleet.t_relation)),1)]),s("div",js,[s("span",Hs,e(t.putcountdown1(t.fleet.time,"Terminé","/s03/empire-view/")),1)])])]),o(" {% empty %} "),Ls,o(" {% endfor %} ")])]),s("div",Rs,[s("div",Gs,[Is,s("div",Us,[o(" {% if research %} "),s("div",zs,[s("div",Js,[s("a",Ks,e(t.research.label),1)]),s("div",Qs,[s("span",Ws,e(t.putcountdown1(t.research.time,"Terminé","/s03/tech-list/")),1)])]),o(" {% else %} "),Xs,o(" {% endif %} ")])])]),s("div",Ys,[s("div",Zs,[$s,o(" {% for item in constructionyards %} "),s("div",st,[s("div",tt,[s("div",et,[s("small",ot,e(t.item.galaxy)+"."+e(t.item.sector)+"."+e(t.item.planet),1)]),s("div",at,[s("a",it,e(t.item.planetname),1)]),s("div",lt,[s("div",nt,[o(" {% for building in item.buildings %} "),s("div",ct,[s("div",dt,[s("div",rt,[s("span",_t,e(t.building.building),1)]),s("div",ht,[s("span",mt,e(t.putcountdown1(t.building.time,"Terminé","/s03/planet-buildings/?planet=item.planetid#building.buildingid")),1)])])]),o(" {% empty %} "),pt,o(" {% endfor %} ")])])])]),o(" {% endfor %} ")])]),o(" {% if shipyards|length > 0 %} "),s("div",ft,[s("div",gt,[ut,o(" {% for item in shipyards %} "),s("div",vt,[s("div",bt,[s("div",wt,[s("small",yt,e(t.item.galaxy)+"."+e(t.item.sector)+"."+e(t.item.planet),1)]),s("div",kt,[s("a",Vt,e(t.item.planetname),1)]),s("div",xt,[o(" {% if item.waiting_resources %} "),s("div",Nt,[s("div",St,e(t.item.waiting_label),1),At]),o(" {% elif item.shipid %} "),s("div",Ct,[s("div",Mt,[s("span",Tt,e(t.item.shiplabel),1)]),s("div",Et,[s("span",Dt,e(t.putcountdown1(t.item.time,"Terminé","/s03/planet-ships/?planet=item.planetid#item.shipid")),1)])]),o(" {% else %} "),Ft,o(" {% endif %} ")])])]),o(" {% endfor %} ")])]),o(" {% endif %} ")])])])],64))}};export{Pt as default};
