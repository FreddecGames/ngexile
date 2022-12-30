CREATE VIEW s03.vw_alliances_reports AS
 SELECT r.ownerallianceid,
    r.ownerid,
    r.type,
    r.datetime,
    r.battleid,
    r.fleetid,
    r.fleet_name,
    r.planetid,
    r.planet_name,
    r.planet_relation,
    r.planet_ownername,
    nav_planet.galaxy,
    nav_planet.sector,
    nav_planet.planet,
    r.researchid,
    r.read_date,
    r.ore,
    r.hydrocarbon,
    r.credits,
    r.subtype,
    r.scientists,
    r.soldiers,
    r.workers,
    users.username,
    alliances.tag AS alliance_tag,
    alliances.name AS alliance_name,
    r.invasionid,
    r.spyid,
    spy.key AS spy_key,
    r.commanderid,
    c.name,
    r.description,
    u_owner.username AS login,
    r.invited_username,
    r.buildingid
   FROM ((((((s03.alliances_reports r
     LEFT JOIN s03.nav_planet ON ((nav_planet.id = r.planetid)))
     JOIN s03.users u_owner ON ((u_owner.id = r.ownerid)))
     LEFT JOIN s03.users ON ((users.id = r.userid)))
     LEFT JOIN s03.alliances ON ((alliances.id = r.allianceid)))
     LEFT JOIN s03.spy ON ((spy.id = r.spyid)))
     LEFT JOIN s03.commanders c ON ((c.id = r.commanderid)))
  WHERE ((r.datetime <= now()) AND (r.datetime > (now() - '14 days'::interval)));
