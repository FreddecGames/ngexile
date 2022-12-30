--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: ng0; Type: SCHEMA; Schema: -; Owner: freddec
--

CREATE SCHEMA ng0;


ALTER SCHEMA ng0 OWNER TO freddec;

--
-- Name: fleet_generate_rogue(bigint, integer); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.fleet_generate_rogue(planetid bigint, size integer) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   fleet_id int4;

BEGIN

   INSERT INTO ng0.fleets(profile_id, name, planet_id, stance) VALUES(2, 'Fossoyeurs', planetid, true) RETURNING id INTO fleet_id;

   IF size = 0 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, ship_id, count) VALUES(fleet_id, 'fighter1', 2);

   ELSEIF size = 1 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, ship_id, count) VALUES(fleet_id, 'fighter1', 2);

   ELSEIF size = 2 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, ship_id, count) VALUES(fleet_id, 'fighter1', 2);

   ELSEIF size = 3 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, ship_id, count) VALUES(fleet_id, 'fighter1', 2);

   ELSEIF size = 4 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, ship_id, count) VALUES(fleet_id, 'fighter1', 2);

   END IF;

END;$$;


ALTER FUNCTION ng0.fleet_generate_rogue(planetid bigint, size integer) OWNER TO freddec;

--
-- Name: galaxy_generate(); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.galaxy_generate() RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   galaxy_id int4;

   sector int4;

   number int4;

   sector_value int4;

   planet_type int4;

   planet_img int4;

   planet_id int4;

BEGIN

   SELECT INTO galaxy_id COALESCE(MAX(id), 0) + 1 FROM ng0.galaxies;

   INSERT INTO ng0.galaxies(id) VALUES(galaxy_id);

   FOR sector IN 1..100 LOOP

      sector_value := 0;

      IF sector IN (12, 13, 14, 15, 16, 17, 18, 19, 22, 29, 32, 39, 42, 49, 52, 59, 62, 69, 72, 79, 82, 83, 84, 85, 86, 87, 88, 89) THEN sector_value := 1;

      ELSEIF sector IN (23, 24, 25, 26, 27, 28, 33, 38, 43, 48, 53, 58, 63, 68, 73, 74, 75, 76, 77, 78) THEN sector_value := 2;

      ELSEIF sector IN (34, 35, 36, 37, 44, 47, 54, 57, 64, 65, 66, 67) THEN sector_value := 3;

      ELSEIF sector IN (45, 46, 55, 56) THEN sector_value := 4;

      END IF;

      FOR number IN 1..25 LOOP

         planet_type := int2(2 * random());

         IF planet_type < 1 THEN

            INSERT INTO ng0.planets(galaxy, sector, number, type) VALUES(galaxy_id, sector, number, 'empty') RETURNING id INTO planet_id;

         ELSE

            planet_img := int2(12 * random());

            IF sector_value > 0 THEN INSERT INTO ng0.planets(galaxy, sector, number, type, img) VALUES(galaxy_id, sector, number, 'planet', planet_img) RETURNING id INTO planet_id;

            ELSE INSERT INTO ng0.planets(galaxy, sector, number, type, img, is_protected) VALUES(galaxy_id, sector, number, 'planet', planet_img, true) RETURNING id INTO planet_id;

            END IF;

         END IF;

         IF sector_value > 0 THEN PERFORM ng0.fleet_generate_rogue(planet_id, sector_value); END IF;

      END LOOP;

   END LOOP;

END;$$;


ALTER FUNCTION ng0.galaxy_generate() OWNER TO freddec;

--
-- Name: planet_colonize(bigint, bigint); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.planet_colonize(planetid bigint, profileid bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   profile record;

BEGIN

   SELECT INTO profile * FROM ng0.profiles WHERE id = profileid LIMIT 1;

   UPDATE ng0.planets SET profile_id = profileid, name = profile.name, lastproduction_date = now(), is_production_frozen = false WHERE id = planetid;

   INSERT INTO ng0.planet_buildings(planet_id, building_id) VALUES(planetid, 'colony');

END;$$;


ALTER FUNCTION ng0.planet_colonize(planetid bigint, profileid bigint) OWNER TO freddec;

--
-- Name: profile_create(bigint, character varying); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.profile_create(userid bigint, nickname character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   profile_id int4;

   planet_id int4;

BEGIN

   INSERT INTO ng0.profiles(name, user_id) VALUES(nickname, userid) RETURNING id INTO profile_id;

   SELECT INTO planet_id id FROM ng0.planets WHERE is_protected = true AND profile_id IS NULL ORDER BY RANDOM() LIMIT 1;

   PERFORM ng0.planet_colonize(planet_id, profile_id);

   PERFORM ng0.fleet_generate_rogue(planet_id, 0);

END;$$;


ALTER FUNCTION ng0.profile_create(userid bigint, nickname character varying) OWNER TO freddec;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alliance_chat_lines; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.alliance_chat_lines (
    id bigint NOT NULL,
    alliance_id bigint NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    profile_name character varying NOT NULL,
    message character varying NOT NULL
);


ALTER TABLE ng0.alliance_chat_lines OWNER TO freddec;

--
-- Name: alliance_chat_lines_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.alliance_chat_lines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.alliance_chat_lines_id_seq OWNER TO freddec;

--
-- Name: alliance_chat_lines_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.alliance_chat_lines_id_seq OWNED BY ng0.alliance_chat_lines.id;


--
-- Name: alliance_invitations; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.alliance_invitations (
    alliance_id bigint NOT NULL,
    profile_id bigint NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    reply_status character varying,
    reply_date timestamp without time zone
);


ALTER TABLE ng0.alliance_invitations OWNER TO freddec;

--
-- Name: alliance_ranks; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.alliance_ranks (
    id bigint NOT NULL,
    alliance_id bigint NOT NULL,
    name character varying NOT NULL,
    is_leader boolean NOT NULL,
    is_default boolean NOT NULL
);


ALTER TABLE ng0.alliance_ranks OWNER TO freddec;

--
-- Name: alliance_ranks_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.alliance_ranks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.alliance_ranks_id_seq OWNER TO freddec;

--
-- Name: alliance_ranks_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.alliance_ranks_id_seq OWNED BY ng0.alliance_ranks.id;


--
-- Name: alliances; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.alliances (
    id bigint NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    tag character varying NOT NULL,
    name character varying NOT NULL,
    member_max integer DEFAULT 30 NOT NULL,
    score integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.alliances OWNER TO freddec;

--
-- Name: alliances_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.alliances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.alliances_id_seq OWNER TO freddec;

--
-- Name: alliances_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.alliances_id_seq OWNED BY ng0.alliances.id;


--
-- Name: battle_fleet_ship_kills; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_fleet_ship_kills (
    battle_fleet_ship_id bigint NOT NULL,
    ship_id character varying NOT NULL,
    count integer NOT NULL
);


ALTER TABLE ng0.battle_fleet_ship_kills OWNER TO freddec;

--
-- Name: battle_fleet_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_fleet_ships (
    id bigint NOT NULL,
    battle_fleet_id bigint NOT NULL,
    ship_id character varying NOT NULL,
    before_count integer NOT NULL,
    after_count integer NOT NULL
);


ALTER TABLE ng0.battle_fleet_ships OWNER TO freddec;

--
-- Name: battle_fleet_ships_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.battle_fleet_ships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.battle_fleet_ships_id_seq OWNER TO freddec;

--
-- Name: battle_fleet_ships_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.battle_fleet_ships_id_seq OWNED BY ng0.battle_fleet_ships.id;


--
-- Name: battle_fleets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_fleets (
    id bigint NOT NULL,
    battle_id bigint NOT NULL,
    alliance_tag character varying,
    profile_name character varying NOT NULL,
    fleet_name character varying NOT NULL,
    stance boolean NOT NULL
);


ALTER TABLE ng0.battle_fleets OWNER TO freddec;

--
-- Name: battle_fleets_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.battle_fleets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.battle_fleets_id_seq OWNER TO freddec;

--
-- Name: battle_fleets_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.battle_fleets_id_seq OWNED BY ng0.battle_fleets.id;


--
-- Name: battle_relations; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_relations (
    battle_id bigint NOT NULL,
    profile1_id bigint NOT NULL,
    profile2_id bigint NOT NULL,
    relation integer NOT NULL
);


ALTER TABLE ng0.battle_relations OWNER TO freddec;

--
-- Name: battles; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battles (
    id bigint NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    planet_id bigint NOT NULL,
    round_count integer NOT NULL
);


ALTER TABLE ng0.battles OWNER TO freddec;

--
-- Name: battles_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.battles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.battles_id_seq OWNER TO freddec;

--
-- Name: battles_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.battles_id_seq OWNED BY ng0.battles.id;


--
-- Name: building_building_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.building_building_reqs (
    building_id character varying NOT NULL,
    req_id character varying NOT NULL,
    req_level integer NOT NULL
);


ALTER TABLE ng0.building_building_reqs OWNER TO freddec;

--
-- Name: buildings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.buildings (
    id character varying NOT NULL,
    cost_ore_base integer DEFAULT 0 NOT NULL,
    cost_hydro_base integer DEFAULT 0 NOT NULL,
    cost_energy_base integer DEFAULT 0 NOT NULL,
    cost_ore_coeff real DEFAULT 1.0 NOT NULL,
    cost_hydro_coeff real DEFAULT 1.0 NOT NULL,
    cost_energy_coeff real DEFAULT 1.0 NOT NULL,
    prod_ore_base integer DEFAULT 0 NOT NULL,
    prod_hydro_base integer DEFAULT 0 NOT NULL,
    prod_energy_base integer DEFAULT 0 NOT NULL,
    prod_credit_base integer DEFAULT 0 NOT NULL,
    prod_ore_coeff real DEFAULT 1.0 NOT NULL,
    prod_hydro_coeff real DEFAULT 1.0 NOT NULL,
    prod_energy_coeff real DEFAULT 1.0 NOT NULL,
    prod_credit_coeff real DEFAULT 1.0 NOT NULL,
    storage_ore_base integer DEFAULT 0 NOT NULL,
    storage_hydro_base integer DEFAULT 0 NOT NULL,
    storage_energy_base integer DEFAULT 0 NOT NULL,
    storage_ore_coeff real DEFAULT 1.0 NOT NULL,
    storage_hydro_coeff real DEFAULT 1.0 NOT NULL,
    storage_energy_coeff real DEFAULT 1.0 NOT NULL,
    level_max integer DEFAULT 65 NOT NULL
);


ALTER TABLE ng0.buildings OWNER TO freddec;

--
-- Name: fleet_actions; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.fleet_actions (
    id bigint NOT NULL,
    fleet_id bigint NOT NULL,
    action character varying NOT NULL,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    planet_id bigint,
    ore_count integer,
    hydro_count integer,
    next_id bigint
);


ALTER TABLE ng0.fleet_actions OWNER TO freddec;

--
-- Name: fleet_actions_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.fleet_actions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.fleet_actions_id_seq OWNER TO freddec;

--
-- Name: fleet_actions_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.fleet_actions_id_seq OWNED BY ng0.fleet_actions.id;


--
-- Name: fleet_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.fleet_ships (
    fleet_id bigint NOT NULL,
    ship_id character varying NOT NULL,
    count integer NOT NULL
);


ALTER TABLE ng0.fleet_ships OWNER TO freddec;

--
-- Name: fleets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.fleets (
    id bigint NOT NULL,
    profile_id bigint NOT NULL,
    name character varying NOT NULL,
    planet_id bigint,
    stance boolean DEFAULT false NOT NULL,
    is_engaged boolean DEFAULT false NOT NULL,
    cargo integer DEFAULT 0 NOT NULL,
    ore_count integer DEFAULT 0 NOT NULL,
    hydro_count integer DEFAULT 0 NOT NULL,
    ship_count integer DEFAULT 0 NOT NULL,
    speed integer DEFAULT 0 NOT NULL,
    signature_total integer DEFAULT 0 NOT NULL,
    signature_military integer DEFAULT 0 NOT NULL,
    recycling_output integer DEFAULT 0 NOT NULL,
    score bigint DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.fleets OWNER TO freddec;

--
-- Name: fleets_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.fleets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.fleets_id_seq OWNER TO freddec;

--
-- Name: fleets_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.fleets_id_seq OWNED BY ng0.fleets.id;


--
-- Name: galaxies; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.galaxies (
    id bigint NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE ng0.galaxies OWNER TO freddec;

--
-- Name: mail_addressees; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.mail_addressees (
    profile_id bigint NOT NULL,
    addressee_id bigint NOT NULL
);


ALTER TABLE ng0.mail_addressees OWNER TO freddec;

--
-- Name: mail_blacklists; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.mail_blacklists (
    profile_id bigint NOT NULL,
    blacklist_id bigint NOT NULL
);


ALTER TABLE ng0.mail_blacklists OWNER TO freddec;

--
-- Name: mails; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.mails (
    id bigint NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    reading_date timestamp without time zone,
    profile_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    subject character varying NOT NULL,
    content text NOT NULL,
    is_deleted boolean DEFAULT false NOT NULL
);


ALTER TABLE ng0.mails OWNER TO freddec;

--
-- Name: mails_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.mails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.mails_id_seq OWNER TO freddec;

--
-- Name: mails_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.mails_id_seq OWNED BY ng0.mails.id;


--
-- Name: planet_buildings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_buildings (
    planet_id bigint NOT NULL,
    building_id character varying NOT NULL,
    level integer DEFAULT 1 NOT NULL,
    id integer NOT NULL
);


ALTER TABLE ng0.planet_buildings OWNER TO freddec;

--
-- Name: planet_buildings_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.planet_buildings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.planet_buildings_id_seq OWNER TO freddec;

--
-- Name: planet_buildings_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.planet_buildings_id_seq OWNED BY ng0.planet_buildings.id;


--
-- Name: planet_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_ships (
    planet_id bigint NOT NULL,
    ship_id character varying NOT NULL,
    count integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.planet_ships OWNER TO freddec;

--
-- Name: planets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planets (
    id bigint NOT NULL,
    galaxy integer DEFAULT 0 NOT NULL,
    sector integer DEFAULT 0 NOT NULL,
    number integer DEFAULT 0 NOT NULL,
    profile_id bigint,
    name character varying,
    score bigint DEFAULT 0 NOT NULL,
    ore_count integer DEFAULT 0 NOT NULL,
    ore_storage integer DEFAULT 0 NOT NULL,
    ore_prod integer DEFAULT 0 NOT NULL,
    hydro_count integer DEFAULT 0 NOT NULL,
    hydro_storage integer DEFAULT 0 NOT NULL,
    hydro_prod integer DEFAULT 0 NOT NULL,
    energy_count integer DEFAULT 0 NOT NULL,
    energy_prod integer DEFAULT 0 NOT NULL,
    energy_storage integer DEFAULT 0 NOT NULL,
    credit_prod integer DEFAULT 0 NOT NULL,
    lastproduction_date timestamp without time zone DEFAULT now(),
    is_production_frozen boolean DEFAULT false NOT NULL,
    radar_strength integer DEFAULT 0 NOT NULL,
    radar_jamming integer DEFAULT 0 NOT NULL,
    orbit_ore integer DEFAULT 0 NOT NULL,
    orbit_hydro integer DEFAULT 0 NOT NULL,
    battle_date timestamp without time zone,
    type character varying NOT NULL,
    img character varying,
    is_protected boolean DEFAULT false NOT NULL
);


ALTER TABLE ng0.planets OWNER TO freddec;

--
-- Name: planets_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.planets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.planets_id_seq OWNER TO freddec;

--
-- Name: planets_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.planets_id_seq OWNED BY ng0.planets.id;


--
-- Name: processes; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.processes (
    procedure character varying NOT NULL,
    frequency interval DEFAULT '00:00:01'::interval NOT NULL,
    lastrun_date timestamp without time zone DEFAULT now() NOT NULL,
    lastrun_result character varying
);


ALTER TABLE ng0.processes OWNER TO freddec;

--
-- Name: profile_reports; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_reports (
    id bigint NOT NULL,
    profile_id bigint NOT NULL,
    type integer NOT NULL,
    subtype integer NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    reading_date timestamp without time zone,
    data character varying
);


ALTER TABLE ng0.profile_reports OWNER TO freddec;

--
-- Name: profile_reports_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.profile_reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.profile_reports_id_seq OWNER TO freddec;

--
-- Name: profile_reports_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.profile_reports_id_seq OWNED BY ng0.profile_reports.id;


--
-- Name: profile_ship_kills; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_ship_kills (
    profile_id bigint NOT NULL,
    ship_id character varying NOT NULL,
    count integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.profile_ship_kills OWNER TO freddec;

--
-- Name: profile_techs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_techs (
    profile_id bigint NOT NULL,
    tech_id character varying NOT NULL,
    level integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.profile_techs OWNER TO freddec;

--
-- Name: profiles; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profiles (
    id bigint NOT NULL,
    name character varying,
    credit_count integer DEFAULT 0 NOT NULL,
    prestige_count integer DEFAULT 0 NOT NULL,
    score integer DEFAULT 0 NOT NULL,
    curplanet_id bigint,
    alliance_id bigint,
    alliance_rank_id bigint,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    user_id bigint
);


ALTER TABLE ng0.profiles OWNER TO freddec;

--
-- Name: profiles_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.profiles_id_seq OWNER TO freddec;

--
-- Name: profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.profiles_id_seq OWNED BY ng0.profiles.id;


--
-- Name: ship_building_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.ship_building_reqs (
    ship_id character varying NOT NULL,
    req_id character varying NOT NULL,
    req_level integer NOT NULL
);


ALTER TABLE ng0.ship_building_reqs OWNER TO freddec;

--
-- Name: ship_tech_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.ship_tech_reqs (
    ship_id character varying NOT NULL,
    req_id character varying NOT NULL,
    req_level integer NOT NULL
);


ALTER TABLE ng0.ship_tech_reqs OWNER TO freddec;

--
-- Name: ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.ships (
    id character varying NOT NULL,
    cost_ore integer DEFAULT 0 NOT NULL,
    cost_hydro integer DEFAULT 0 NOT NULL,
    cost_energy integer DEFAULT 0 NOT NULL,
    tech integer DEFAULT 0 NOT NULL,
    hull integer DEFAULT 0 NOT NULL,
    speed integer DEFAULT 0 NOT NULL,
    shield integer DEFAULT 0 NOT NULL,
    turret integer DEFAULT 0 NOT NULL,
    handling integer DEFAULT 0 NOT NULL,
    tracking integer DEFAULT 0 NOT NULL,
    signature integer DEFAULT 0 NOT NULL,
    recycling_output integer DEFAULT 0 NOT NULL,
    damage_em integer DEFAULT 0 NOT NULL,
    damage_explosive integer DEFAULT 0 NOT NULL,
    damage_kinetic integer DEFAULT 0 NOT NULL,
    damage_thermal integer DEFAULT 0 NOT NULL,
    resist_em integer DEFAULT 0 NOT NULL,
    resist_explosive integer DEFAULT 0 NOT NULL,
    resist_kinetic integer DEFAULT 0 NOT NULL,
    resist_thermal integer DEFAULT 0 NOT NULL,
    reward_prestige integer DEFAULT 0 NOT NULL,
    reward_credit integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.ships OWNER TO freddec;

--
-- Name: techs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.techs (
    id character varying NOT NULL,
    cost_credit integer DEFAULT 0 NOT NULL,
    cost_prestige integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.techs OWNER TO freddec;

--
-- Name: alliance_chat_lines id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_chat_lines ALTER COLUMN id SET DEFAULT nextval('ng0.alliance_chat_lines_id_seq'::regclass);


--
-- Name: alliance_ranks id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_ranks ALTER COLUMN id SET DEFAULT nextval('ng0.alliance_ranks_id_seq'::regclass);


--
-- Name: alliances id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliances ALTER COLUMN id SET DEFAULT nextval('ng0.alliances_id_seq'::regclass);


--
-- Name: battle_fleet_ships id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships ALTER COLUMN id SET DEFAULT nextval('ng0.battle_fleet_ships_id_seq'::regclass);


--
-- Name: battle_fleets id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets ALTER COLUMN id SET DEFAULT nextval('ng0.battle_fleets_id_seq'::regclass);


--
-- Name: battles id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battles ALTER COLUMN id SET DEFAULT nextval('ng0.battles_id_seq'::regclass);


--
-- Name: fleet_actions id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions ALTER COLUMN id SET DEFAULT nextval('ng0.fleet_actions_id_seq'::regclass);


--
-- Name: fleets id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets ALTER COLUMN id SET DEFAULT nextval('ng0.fleets_id_seq'::regclass);


--
-- Name: mails id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mails ALTER COLUMN id SET DEFAULT nextval('ng0.mails_id_seq'::regclass);


--
-- Name: planet_buildings id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings ALTER COLUMN id SET DEFAULT nextval('ng0.planet_buildings_id_seq'::regclass);


--
-- Name: planets id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets ALTER COLUMN id SET DEFAULT nextval('ng0.planets_id_seq'::regclass);


--
-- Name: profile_reports id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_reports ALTER COLUMN id SET DEFAULT nextval('ng0.profile_reports_id_seq'::regclass);


--
-- Name: profiles id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles ALTER COLUMN id SET DEFAULT nextval('ng0.profiles_id_seq'::regclass);


--
-- Data for Name: alliance_chat_lines; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.alliance_chat_lines (id, alliance_id, creation_date, profile_name, message) FROM stdin;
\.


--
-- Data for Name: alliance_invitations; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.alliance_invitations (alliance_id, profile_id, creation_date, reply_status, reply_date) FROM stdin;
\.


--
-- Data for Name: alliance_ranks; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.alliance_ranks (id, alliance_id, name, is_leader, is_default) FROM stdin;
\.


--
-- Data for Name: alliances; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.alliances (id, creation_date, tag, name, member_max, score) FROM stdin;
1	2022-12-28 14:03:10.805654	FO	Fossoyeurs	30	0
2	2022-12-28 14:03:37.681861	GM	Guilde Marchande	30	0
\.


--
-- Data for Name: battle_fleet_ship_kills; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_fleet_ship_kills (battle_fleet_ship_id, ship_id, count) FROM stdin;
\.


--
-- Data for Name: battle_fleet_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_fleet_ships (id, battle_fleet_id, ship_id, before_count, after_count) FROM stdin;
\.


--
-- Data for Name: battle_fleets; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_fleets (id, battle_id, alliance_tag, profile_name, fleet_name, stance) FROM stdin;
\.


--
-- Data for Name: battle_relations; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_relations (battle_id, profile1_id, profile2_id, relation) FROM stdin;
\.


--
-- Data for Name: battles; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battles (id, creation_date, planet_id, round_count) FROM stdin;
\.


--
-- Data for Name: building_building_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.building_building_reqs (building_id, req_id, req_level) FROM stdin;
\.


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.buildings (id, cost_ore_base, cost_hydro_base, cost_energy_base, cost_ore_coeff, cost_hydro_coeff, cost_energy_coeff, prod_ore_base, prod_hydro_base, prod_energy_base, prod_credit_base, prod_ore_coeff, prod_hydro_coeff, prod_energy_coeff, prod_credit_coeff, storage_ore_base, storage_hydro_base, storage_energy_base, storage_ore_coeff, storage_hydro_coeff, storage_energy_coeff, level_max) FROM stdin;
colony	0	0	0	1	1	1	0	0	0	0	1	1	1	1	50	50	40	1	1	1	65
mine	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
pumpjack	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
powerplant	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
oresilo	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
hydrosilo	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
accumulator	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
spaceport	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
shipyardfighter	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
shipyardcorvette	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
shipyardfrigate	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
shipyardcruiser	0	0	0	1	1	1	0	0	0	0	1	1	1	1	0	0	0	1	1	1	65
\.


--
-- Data for Name: fleet_actions; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.fleet_actions (id, fleet_id, action, start_date, end_date, planet_id, ore_count, hydro_count, next_id) FROM stdin;
\.


--
-- Data for Name: fleet_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.fleet_ships (fleet_id, ship_id, count) FROM stdin;
\.


--
-- Data for Name: fleets; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.fleets (id, profile_id, name, planet_id, stance, is_engaged, cargo, ore_count, hydro_count, ship_count, speed, signature_total, signature_military, recycling_output, score) FROM stdin;
\.


--
-- Data for Name: galaxies; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.galaxies (id, creation_date) FROM stdin;
\.


--
-- Data for Name: mail_addressees; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.mail_addressees (profile_id, addressee_id) FROM stdin;
\.


--
-- Data for Name: mail_blacklists; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.mail_blacklists (profile_id, blacklist_id) FROM stdin;
\.


--
-- Data for Name: mails; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.mails (id, creation_date, reading_date, profile_id, sender_id, subject, content, is_deleted) FROM stdin;
\.


--
-- Data for Name: planet_buildings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_buildings (planet_id, building_id, level, id) FROM stdin;
\.


--
-- Data for Name: planet_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_ships (planet_id, ship_id, count) FROM stdin;
\.


--
-- Data for Name: planets; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planets (id, galaxy, sector, number, profile_id, name, score, ore_count, ore_storage, ore_prod, hydro_count, hydro_storage, hydro_prod, energy_count, energy_prod, energy_storage, credit_prod, lastproduction_date, is_production_frozen, radar_strength, radar_jamming, orbit_ore, orbit_hydro, battle_date, type, img, is_protected) FROM stdin;
\.


--
-- Data for Name: processes; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.processes (procedure, frequency, lastrun_date, lastrun_result) FROM stdin;
\.


--
-- Data for Name: profile_reports; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_reports (id, profile_id, type, subtype, creation_date, reading_date, data) FROM stdin;
\.


--
-- Data for Name: profile_ship_kills; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_ship_kills (profile_id, ship_id, count) FROM stdin;
\.


--
-- Data for Name: profile_techs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_techs (profile_id, tech_id, level) FROM stdin;
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profiles (id, name, credit_count, prestige_count, score, curplanet_id, alliance_id, alliance_rank_id, creation_date, user_id) FROM stdin;
1	Admin	0	0	0	\N	\N	\N	2022-12-28 14:01:35.093789	\N
2	Fossoyeurs	0	0	0	\N	1	\N	2022-12-28 14:04:44.714459	\N
3	Guilde Marchande	0	0	0	\N	2	\N	2022-12-28 14:05:26.940876	\N
\.


--
-- Data for Name: ship_building_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.ship_building_reqs (ship_id, req_id, req_level) FROM stdin;
\.


--
-- Data for Name: ship_tech_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.ship_tech_reqs (ship_id, req_id, req_level) FROM stdin;
\.


--
-- Data for Name: ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.ships (id, cost_ore, cost_hydro, cost_energy, tech, hull, speed, shield, turret, handling, tracking, signature, recycling_output, damage_em, damage_explosive, damage_kinetic, damage_thermal, resist_em, resist_explosive, resist_kinetic, resist_thermal, reward_prestige, reward_credit) FROM stdin;
fighter1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
\.


--
-- Data for Name: techs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.techs (id, cost_credit, cost_prestige) FROM stdin;
\.


--
-- Name: alliance_chat_lines_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.alliance_chat_lines_id_seq', 1, false);


--
-- Name: alliance_ranks_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.alliance_ranks_id_seq', 1, false);


--
-- Name: alliances_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.alliances_id_seq', 2, true);


--
-- Name: battle_fleet_ships_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.battle_fleet_ships_id_seq', 1, false);


--
-- Name: battle_fleets_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.battle_fleets_id_seq', 1, false);


--
-- Name: battles_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.battles_id_seq', 1, false);


--
-- Name: fleet_actions_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.fleet_actions_id_seq', 1, false);


--
-- Name: fleets_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.fleets_id_seq', 1, true);


--
-- Name: mails_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.mails_id_seq', 1, false);


--
-- Name: planet_buildings_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.planet_buildings_id_seq', 1, false);


--
-- Name: planets_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.planets_id_seq', 280, true);


--
-- Name: profile_reports_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.profile_reports_id_seq', 1, false);


--
-- Name: profiles_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.profiles_id_seq', 3, true);


--
-- Name: alliance_chat_lines alliance_chat_lines_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_chat_lines
    ADD CONSTRAINT alliance_chat_lines_pkey PRIMARY KEY (id);


--
-- Name: alliance_invitations alliance_invitations_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_invitations
    ADD CONSTRAINT alliance_invitations_pkey PRIMARY KEY (alliance_id, profile_id);


--
-- Name: alliance_ranks alliance_ranks_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_ranks
    ADD CONSTRAINT alliance_ranks_pkey PRIMARY KEY (id);


--
-- Name: alliances alliances_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliances
    ADD CONSTRAINT alliances_pkey PRIMARY KEY (id);


--
-- Name: battle_fleet_ship_kills battle_fleet_ship_kills_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ship_kills
    ADD CONSTRAINT battle_fleet_ship_kills_pkey PRIMARY KEY (battle_fleet_ship_id, ship_id);


--
-- Name: battle_fleet_ships battle_fleet_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battle_fleet_ships_pkey PRIMARY KEY (id);


--
-- Name: battle_fleets battle_fleets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets
    ADD CONSTRAINT battle_fleets_pkey PRIMARY KEY (id);


--
-- Name: battle_relations battle_relations_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_relations
    ADD CONSTRAINT battle_relations_pkey PRIMARY KEY (battle_id, profile1_id, profile2_id);


--
-- Name: battles battles_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battles
    ADD CONSTRAINT battles_pkey PRIMARY KEY (id);


--
-- Name: building_building_reqs building_building_reqs_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.building_building_reqs
    ADD CONSTRAINT building_building_reqs_pkey PRIMARY KEY (building_id, req_id);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);


--
-- Name: fleet_actions fleet_actions_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_pkey PRIMARY KEY (id);


--
-- Name: fleet_ships fleet_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_ships
    ADD CONSTRAINT fleet_ships_pkey PRIMARY KEY (fleet_id, ship_id);


--
-- Name: fleets fleets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_pkey PRIMARY KEY (id);


--
-- Name: galaxies galaxies_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.galaxies
    ADD CONSTRAINT galaxies_pkey PRIMARY KEY (id);


--
-- Name: mail_addressees mail_addressees_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mail_addressees
    ADD CONSTRAINT mail_addressees_pkey PRIMARY KEY (profile_id, addressee_id);


--
-- Name: mail_blacklists mail_blacklists_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mail_blacklists
    ADD CONSTRAINT mail_blacklists_pkey PRIMARY KEY (profile_id, blacklist_id);


--
-- Name: mails mails_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mails
    ADD CONSTRAINT mails_pkey PRIMARY KEY (id);


--
-- Name: planet_buildings planet_buildings_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings
    ADD CONSTRAINT planet_buildings_pkey PRIMARY KEY (id);


--
-- Name: planet_ships planet_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ships
    ADD CONSTRAINT planet_ships_pkey PRIMARY KEY (planet_id, ship_id);


--
-- Name: planets planets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_pkey PRIMARY KEY (id);


--
-- Name: processes processes_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.processes
    ADD CONSTRAINT processes_pkey PRIMARY KEY (procedure);


--
-- Name: profile_reports profile_reports_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_reports
    ADD CONSTRAINT profile_reports_pkey PRIMARY KEY (id);


--
-- Name: profile_ship_kills profile_ship_kills_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_ship_kills
    ADD CONSTRAINT profile_ship_kills_pkey PRIMARY KEY (profile_id, ship_id);


--
-- Name: profile_techs profile_techs_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_techs
    ADD CONSTRAINT profile_techs_pkey PRIMARY KEY (profile_id, tech_id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: ship_building_reqs ship_building_reqs_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ship_building_reqs
    ADD CONSTRAINT ship_building_reqs_pkey PRIMARY KEY (ship_id, req_id);


--
-- Name: ship_tech_reqs ship_tech_reqs_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ship_tech_reqs
    ADD CONSTRAINT ship_tech_reqs_pkey PRIMARY KEY (ship_id, req_id);


--
-- Name: ships ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ships
    ADD CONSTRAINT ships_pkey PRIMARY KEY (id);


--
-- Name: techs techs_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.techs
    ADD CONSTRAINT techs_pkey PRIMARY KEY (id);


--
-- Name: alliance_chat_lines alliance_chat_lines_alliance_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_chat_lines
    ADD CONSTRAINT alliance_chat_lines_alliance_id_fkey FOREIGN KEY (alliance_id) REFERENCES ng0.alliances(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: alliance_invitations alliance_invitations_alliance_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_invitations
    ADD CONSTRAINT alliance_invitations_alliance_id_fkey FOREIGN KEY (alliance_id) REFERENCES ng0.alliances(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: alliance_invitations alliance_invitations_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_invitations
    ADD CONSTRAINT alliance_invitations_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: alliance_ranks alliance_ranks_alliance_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.alliance_ranks
    ADD CONSTRAINT alliance_ranks_alliance_id_fkey FOREIGN KEY (alliance_id) REFERENCES ng0.alliances(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleet_ship_kills battle_fleet_ship_kills_battle_fleet_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ship_kills
    ADD CONSTRAINT battle_fleet_ship_kills_battle_fleet_ship_id_fkey FOREIGN KEY (battle_fleet_ship_id) REFERENCES ng0.battle_fleet_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleet_ship_kills battle_fleet_ship_kills_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ship_kills
    ADD CONSTRAINT battle_fleet_ship_kills_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleet_ships battle_fleet_ships_battle_fleet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battle_fleet_ships_battle_fleet_id_fkey FOREIGN KEY (battle_fleet_id) REFERENCES ng0.battle_fleets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleet_ships battle_fleet_ships_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battle_fleet_ships_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleets battle_fleets_battle_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets
    ADD CONSTRAINT battle_fleets_battle_id_fkey FOREIGN KEY (battle_id) REFERENCES ng0.battles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_relations battle_relations_battle_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_relations
    ADD CONSTRAINT battle_relations_battle_id_fkey FOREIGN KEY (battle_id) REFERENCES ng0.battles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_relations battle_relations_profile1_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_relations
    ADD CONSTRAINT battle_relations_profile1_id_fkey FOREIGN KEY (profile1_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_relations battle_relations_profile2_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_relations
    ADD CONSTRAINT battle_relations_profile2_id_fkey FOREIGN KEY (profile2_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battles battles_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battles
    ADD CONSTRAINT battles_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: building_building_reqs building_building_reqs_building_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.building_building_reqs
    ADD CONSTRAINT building_building_reqs_building_id_fkey FOREIGN KEY (building_id) REFERENCES ng0.buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: building_building_reqs building_building_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.building_building_reqs
    ADD CONSTRAINT building_building_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleet_actions fleet_actions_fleet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_fleet_id_fkey FOREIGN KEY (fleet_id) REFERENCES ng0.fleets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleet_actions fleet_actions_next_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_next_id_fkey FOREIGN KEY (next_id) REFERENCES ng0.fleet_actions(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: fleet_actions fleet_actions_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleet_ships fleet_ships_fleet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_ships
    ADD CONSTRAINT fleet_ships_fleet_id_fkey FOREIGN KEY (fleet_id) REFERENCES ng0.fleets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleet_ships fleet_ships_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_ships
    ADD CONSTRAINT fleet_ships_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleets fleets_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleets fleets_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: mail_addressees mail_addressees_addressee_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mail_addressees
    ADD CONSTRAINT mail_addressees_addressee_id_fkey FOREIGN KEY (addressee_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: mail_addressees mail_addressees_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mail_addressees
    ADD CONSTRAINT mail_addressees_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: mail_blacklists mail_blacklists_blacklist_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mail_blacklists
    ADD CONSTRAINT mail_blacklists_blacklist_id_fkey FOREIGN KEY (blacklist_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: mail_blacklists mail_blacklists_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mail_blacklists
    ADD CONSTRAINT mail_blacklists_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: mails mails_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mails
    ADD CONSTRAINT mails_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: mails mails_sender_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.mails
    ADD CONSTRAINT mails_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_buildings planet_buildings_building_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings
    ADD CONSTRAINT planet_buildings_building_id_fkey FOREIGN KEY (building_id) REFERENCES ng0.buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_buildings planet_buildings_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings
    ADD CONSTRAINT planet_buildings_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_ships planet_ships_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ships
    ADD CONSTRAINT planet_ships_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_ships planet_ships_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ships
    ADD CONSTRAINT planet_ships_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planets planets_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_reports profile_reports_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_reports
    ADD CONSTRAINT profile_reports_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_ship_kills profile_ship_kills_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_ship_kills
    ADD CONSTRAINT profile_ship_kills_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_ship_kills profile_ship_kills_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_ship_kills
    ADD CONSTRAINT profile_ship_kills_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_techs profile_techs_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_techs
    ADD CONSTRAINT profile_techs_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_techs profile_techs_tech_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_techs
    ADD CONSTRAINT profile_techs_tech_id_fkey FOREIGN KEY (tech_id) REFERENCES ng0.techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profiles profiles_alliance_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT profiles_alliance_id_fkey FOREIGN KEY (alliance_id) REFERENCES ng0.alliances(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: profiles profiles_alliance_rank_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT profiles_alliance_rank_id_fkey FOREIGN KEY (alliance_rank_id) REFERENCES ng0.alliance_ranks(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: profiles profiles_curplanet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT profiles_curplanet_id_fkey FOREIGN KEY (curplanet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ship_building_reqs ship_building_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ship_building_reqs
    ADD CONSTRAINT ship_building_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ship_building_reqs ship_building_reqs_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ship_building_reqs
    ADD CONSTRAINT ship_building_reqs_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ship_tech_reqs ship_tech_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ship_tech_reqs
    ADD CONSTRAINT ship_tech_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ship_tech_reqs ship_tech_reqs_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.ship_tech_reqs
    ADD CONSTRAINT ship_tech_reqs_ship_id_fkey FOREIGN KEY (ship_id) REFERENCES ng0.ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--
