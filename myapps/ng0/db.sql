--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 15.3

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
-- Name: fleet_generate_rogue(integer, integer); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.fleet_generate_rogue(_planet_id integer, _strength integer) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   fleet_id integer;

BEGIN

   INSERT INTO ng0.fleets(profile_id, name, planet_id, stance) VALUES(1, 'Rogue', _planet_id, true) RETURNING id INTO fleet_id;

   IF _strength = 0 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 20 + int4(random() * 20));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 10 + int4(random() * 10));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 10 + int4(random() * 10));

   ELSEIF _strength = 1 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 20 + int4(random() * 20));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 80 + int4(random() * 50));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 50 + int4(random() * 50));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 20 + int4(random() * 20));

   ELSEIF _strength = 2 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 100 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 100 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 60 + int4(random() * 50));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 100 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 30 + int4(random() * 30));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 30 + int4(random() * 30));

   ELSEIF _strength = 3 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 100 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 100 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 200 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 50 + int4(random() * 50));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 402, 150 + int4(random() * 100));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 501, 200 + int4(random() * 100));

   ELSEIF _strength = 4 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 200 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 200 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 200 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 200 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 200 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 200 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 402, 200 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 404, 500 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 501, 300 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 504, 500 + int4(random() * 300));

   ELSEIF _strength = 5 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 200 + int4(random() * 2000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 200 + int4(random() * 2000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 200 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 200 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 200 + int4(random() * 600));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 200 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 402, 200 + int4(random() * 800));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 404, 500 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 501, 300 + int4(random() * 800));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 504, 500 + int4(random() * 700));

   ELSEIF _strength = 6 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 200 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 200 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 200 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 200 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 200 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 200 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 402, 200 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 404, 500 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 501, 300 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 504, 500 + int4(random() * 300));

   ELSEIF _strength = 7 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 1200 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 1200 + int4(random() * 1000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 300 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 300 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 300 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 300 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 402, 400 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 404, 700 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 501, 500 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 504, 1000 + int4(random() * 300));

   ELSEIF _strength = 8 THEN

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 201, 5200 + int4(random() * 2000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 202, 5200 + int4(random() * 2000));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 301, 800 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 302, 800 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 304, 1200 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 401, 1000 + int4(random() * 300));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 402, 600 + int4(random() * 200));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 404, 1000 + int4(random() * 500));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 501, 1200 + int4(random() * 800));

      INSERT INTO ng0.fleet_ships(fleet_id, db_ship_id, count) VALUES(fleet_id, 504, 2000 + int4(random() * 1000));

   END IF;

END;$$;


ALTER FUNCTION ng0.fleet_generate_rogue(_planet_id integer, _strength integer) OWNER TO freddec;

--
-- Name: galaxy_generate(integer, character varying, boolean); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.galaxy_generate(_galaxy_id integer, _name character varying, _allow_new_players boolean) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   sector integer;

   number integer;

   planet_id integer;

   planet_type integer;

BEGIN

   INSERT INTO ng0.galaxies(id, allow_new_players, name) VALUES(_galaxy_id, _allow_new_players, _name);

   FOR sector IN 1..100 LOOP

      FOR number IN 1..25 LOOP

         planet_type := int2(100 * random());

         IF planet_type < 40 THEN planet_type := 0;

         ELSEIF planet_type <= 80 THEN planet_type := 2;

         ELSEIF planet_type <= 90 THEN planet_type := 3;

         ELSE planet_type := 1;

         END IF;

         IF planet_type = 0 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number) VALUES(_galaxy_id, sector, number) RETURNING id INTO planet_id;

            IF sector % 10 <> 0 AND sector % 10 <> 1 AND sector > 10 AND sector <= 90 THEN

               PERFORM ng0.fleet_generate_rogue(planet_id, int2(8 * random()));

            END IF;

         ELSEIF planet_type = 1 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number, floor_count, space_count) VALUES(_galaxy_id, sector, number, 80, 10) RETURNING id INTO planet_id;

            IF sector % 10 <> 0 AND sector % 10 <> 1 AND sector > 10 AND sector <= 90 THEN

               PERFORM ng0.fleet_generate_rogue(planet_id, int2(8 * random()));

            END IF;

         ELSEIF planet_type = 2 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number, spawn_ore) VALUES(_galaxy_id, sector, number, 22000 + 5000 * random());

         ELSEIF planet_type = 3 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number, spawn_hydro) VALUES(_galaxy_id, sector, number, 22000 + 5000 * random());

         END IF;

      END LOOP;

   END LOOP;

END;$$;


ALTER FUNCTION ng0.galaxy_generate(_galaxy_id integer, _name character varying, _allow_new_players boolean) OWNER TO freddec;

--
-- Name: profile_connect(integer, character varying, character varying, character varying); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.profile_connect(_user_id integer, _ip_address character varying, _forwarded character varying, _user_agent character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$BEGIN

   PERFORM 1 FROM ng0.profiles WHERE id = _user_id;

   IF NOT FOUND THEN

      INSERT INTO ng0.profiles(id) VALUES(_user_id);

   END IF;

   INSERT INTO ng0.profile_connections(profile_id, ip_address, forwarded, user_agent) VALUES(_user_id, _ip_address, _forwarded, _user_agent);

   UPDATE ng0.profiles SET last_connection_date = now();

END;$$;


ALTER FUNCTION ng0.profile_connect(_user_id integer, _ip_address character varying, _forwarded character varying, _user_agent character varying) OWNER TO freddec;

--
-- Name: trigger_profileconnections_beforeinsert(); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.trigger_profileconnections_beforeinsert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN

   PERFORM 1 FROM ng0.profile_connections WHERE profile_id = NEW.profile_id AND ip_address = NEW.ip_address AND forwarded = NEW.forwarded AND user_agent = NEW.user_agent;

   IF FOUND THEN RETURN NULL;
   END IF;

   RETURN NEW;

END;$$;


ALTER FUNCTION ng0.trigger_profileconnections_beforeinsert() OWNER TO freddec;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: battle_fleet_ship_kills; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_fleet_ship_kills (
    battle_fleet_ship_id integer NOT NULL,
    db_ship_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT battle_fleet_ship_kills_count_check CHECK ((count > 0))
);


ALTER TABLE ng0.battle_fleet_ship_kills OWNER TO freddec;

--
-- Name: battle_fleet_ships_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.battle_fleet_ships_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.battle_fleet_ships_id_seq OWNER TO freddec;

--
-- Name: battle_fleet_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_fleet_ships (
    id integer DEFAULT nextval('ng0.battle_fleet_ships_id_seq'::regclass) NOT NULL,
    battle_fleet_id integer NOT NULL,
    db_ship_id integer NOT NULL,
    initial_count integer NOT NULL,
    remaining_count integer NOT NULL,
    CONSTRAINT battle_fleet_ships_check CHECK (((initial_count > 0) AND (remaining_count > 0) AND (initial_count >= remaining_count)))
);


ALTER TABLE ng0.battle_fleet_ships OWNER TO freddec;

--
-- Name: battle_fleets_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.battle_fleets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.battle_fleets_id_seq OWNER TO freddec;

--
-- Name: battle_fleets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battle_fleets (
    id integer DEFAULT nextval('ng0.battle_fleets_id_seq'::regclass) NOT NULL,
    battle_id integer NOT NULL,
    profile_id integer,
    profile_name character varying(16) NOT NULL,
    fleet_id integer,
    fleet_name character varying(16) NOT NULL,
    fleet_stance boolean NOT NULL,
    winner boolean NOT NULL,
    mod_shield integer NOT NULL,
    mod_handling integer NOT NULL,
    mod_tracking integer NOT NULL,
    mod_damage integer NOT NULL,
    CONSTRAINT battle_fleets_check CHECK (((mod_shield >= 0) AND (mod_handling >= 0) AND (mod_tracking >= 0) AND (mod_damage >= 0)))
);


ALTER TABLE ng0.battle_fleets OWNER TO freddec;

--
-- Name: battles_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.battles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.battles_id_seq OWNER TO freddec;

--
-- Name: battles; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.battles (
    id integer DEFAULT nextval('ng0.battles_id_seq'::regclass) NOT NULL,
    creation_date timestamp with time zone DEFAULT now() NOT NULL,
    planet_id integer NOT NULL,
    round_count integer NOT NULL,
    key character varying(8) NOT NULL,
    CONSTRAINT battles_round_count_check CHECK ((round_count > 0))
);


ALTER TABLE ng0.battles OWNER TO freddec;

--
-- Name: db_building_building_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_building_building_reqs (
    db_building_id integer NOT NULL,
    req_id integer NOT NULL
);


ALTER TABLE ng0.db_building_building_reqs OWNER TO freddec;

--
-- Name: db_building_tech_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_building_tech_reqs (
    db_building_id integer NOT NULL,
    req_id integer NOT NULL,
    level integer NOT NULL,
    CONSTRAINT db_building_tech_reqs_level_check CHECK ((level > 0))
);


ALTER TABLE ng0.db_building_tech_reqs OWNER TO freddec;

--
-- Name: db_buildings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_buildings (
    id integer NOT NULL,
    category integer NOT NULL,
    name character varying(32) NOT NULL,
    floor smallint DEFAULT 0 NOT NULL,
    space smallint DEFAULT 0 NOT NULL,
    cost_ore integer DEFAULT 0 NOT NULL,
    cost_hydro integer DEFAULT 0 NOT NULL,
    cost_worker integer DEFAULT 0 NOT NULL,
    cost_credit integer DEFAULT 0 NOT NULL,
    cost_prestige integer DEFAULT 0 NOT NULL,
    prod_energy integer DEFAULT 0 NOT NULL,
    prod_ore integer DEFAULT 0 NOT NULL,
    prod_hydro integer DEFAULT 0 NOT NULL,
    prod_credit integer DEFAULT 0 NOT NULL,
    prod_prestige integer DEFAULT 0 NOT NULL,
    storage_ore integer DEFAULT 0 NOT NULL,
    storage_hydro integer DEFAULT 0 NOT NULL,
    storage_energy integer DEFAULT 0 NOT NULL,
    storage_worker integer DEFAULT 0 NOT NULL,
    storage_scientist integer DEFAULT 0 NOT NULL,
    storage_soldier integer DEFAULT 0 NOT NULL,
    buildable boolean DEFAULT true NOT NULL,
    build_max integer DEFAULT 1 NOT NULL,
    build_time integer DEFAULT 0 NOT NULL,
    destroyable boolean DEFAULT true NOT NULL,
    mod_prod_ore real DEFAULT 0 NOT NULL,
    mod_prod_hydro real DEFAULT 0 NOT NULL,
    mod_prod_energy real DEFAULT 0 NOT NULL,
    mod_prod_worker real DEFAULT 0 NOT NULL,
    mod_speed_building real DEFAULT 0 NOT NULL,
    mod_speed_ship real DEFAULT 0 NOT NULL,
    strength_radar smallint DEFAULT 0 NOT NULL,
    strength_jammer smallint DEFAULT 0 NOT NULL,
    training_scientist integer DEFAULT 0 NOT NULL,
    training_soldiers integer DEFAULT 0 NOT NULL,
    expiration integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.db_buildings OWNER TO freddec;

--
-- Name: db_ship_building_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_ship_building_reqs (
    db_ship_id integer NOT NULL,
    req_id integer NOT NULL
);


ALTER TABLE ng0.db_ship_building_reqs OWNER TO freddec;

--
-- Name: db_ship_tech_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_ship_tech_reqs (
    db_ship_id integer NOT NULL,
    req_id integer NOT NULL,
    level integer NOT NULL,
    CONSTRAINT db_ship_tech_reqs_level_check CHECK ((level > 0))
);


ALTER TABLE ng0.db_ship_tech_reqs OWNER TO freddec;

--
-- Name: db_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_ships (
    id integer NOT NULL,
    category integer NOT NULL,
    name character varying(32) NOT NULL,
    cost_ore integer DEFAULT 0 NOT NULL,
    cost_hydro integer DEFAULT 0 NOT NULL,
    cost_energy integer DEFAULT 0 NOT NULL,
    cost_worker integer DEFAULT 0 NOT NULL,
    cost_credit integer DEFAULT 0 NOT NULL,
    cost_prestige integer DEFAULT 0 NOT NULL,
    build_time integer DEFAULT 0 NOT NULL,
    cargo integer DEFAULT 0 NOT NULL,
    hull integer DEFAULT 0 NOT NULL,
    shield integer DEFAULT 0 NOT NULL,
    tracking integer DEFAULT 0 NOT NULL,
    turret integer DEFAULT 0 NOT NULL,
    signature integer DEFAULT 0 NOT NULL,
    speed integer DEFAULT 0 NOT NULL,
    handling integer DEFAULT 0 NOT NULL,
    recycling_capacity integer DEFAULT 0 NOT NULL,
    warping_capacity integer DEFAULT 0 NOT NULL,
    db_building_id integer,
    buildable boolean DEFAULT true NOT NULL,
    dmg_em integer DEFAULT 0 NOT NULL,
    dmg_explosive integer DEFAULT 0 NOT NULL,
    dmg_kinetic integer DEFAULT 0 NOT NULL,
    dmg_thermal integer DEFAULT 0 NOT NULL,
    resist_em integer DEFAULT 0 NOT NULL,
    resist_explosive integer DEFAULT 0 NOT NULL,
    resist_kinetic integer DEFAULT 0 NOT NULL,
    resist_thermal integer DEFAULT 0 NOT NULL,
    class integer DEFAULT 0 NOT NULL,
    reward_prestige integer DEFAULT 0 NOT NULL,
    reward_credit integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.db_ships OWNER TO freddec;

--
-- Name: db_tech_tech_reqs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_tech_tech_reqs (
    db_tech_id integer NOT NULL,
    req_id integer NOT NULL,
    level integer NOT NULL,
    CONSTRAINT db_tech_tech_reqs_level_check CHECK ((level > 0))
);


ALTER TABLE ng0.db_tech_tech_reqs OWNER TO freddec;

--
-- Name: db_techs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.db_techs (
    id integer NOT NULL,
    category integer NOT NULL,
    name character varying(32) NOT NULL,
    rank integer DEFAULT 1 NOT NULL,
    level_count integer DEFAULT 0 NOT NULL,
    level_default integer DEFAULT 0 NOT NULL,
    cost_credit integer DEFAULT 0 NOT NULL,
    mod_prod_ore real DEFAULT 0 NOT NULL,
    mod_prod_hydro real DEFAULT 0 NOT NULL,
    mod_prod_energy real DEFAULT 0 NOT NULL,
    mod_prod_worker real DEFAULT 0 NOT NULL,
    mod_speed_building real DEFAULT 0 NOT NULL,
    mod_speed_ship real DEFAULT 0 NOT NULL,
    mod_fleet_damage real DEFAULT 0 NOT NULL,
    mod_fleet_speed real DEFAULT 0 NOT NULL,
    mod_fleet_shield real DEFAULT 0 NOT NULL,
    mod_fleet_handling real DEFAULT 0 NOT NULL,
    mod_fleet_tracking real DEFAULT 0 NOT NULL,
    mod_fleet_recycling real DEFAULT 0 NOT NULL,
    mod_tech_cost real DEFAULT 0 NOT NULL,
    mod_tech_time real DEFAULT 0 NOT NULL,
    mod_planet_count real DEFAULT 0 NOT NULL,
    expiration interval
);


ALTER TABLE ng0.db_techs OWNER TO freddec;

--
-- Name: fleet_actions_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.fleet_actions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.fleet_actions_id_seq OWNER TO freddec;

--
-- Name: fleet_actions; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.fleet_actions (
    id integer DEFAULT nextval('ng0.fleet_actions_id_seq'::regclass) NOT NULL,
    fleet_id integer NOT NULL,
    action character varying(16) NOT NULL,
    "time" integer NOT NULL,
    origin_planet_id integer,
    dest_planet_id integer,
    ore_count integer DEFAULT 0 NOT NULL,
    hydro_count integer DEFAULT 0 NOT NULL,
    scientist_count integer DEFAULT 0 NOT NULL,
    soldier_count integer DEFAULT 0 NOT NULL,
    worker_count integer DEFAULT 0 NOT NULL,
    CONSTRAINT fleet_actions_check CHECK (((ore_count >= 0) AND (hydro_count >= 0) AND (scientist_count >= 0) AND (soldier_count >= 0) AND (worker_count >= 0)))
);


ALTER TABLE ng0.fleet_actions OWNER TO freddec;

--
-- Name: fleet_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.fleet_ships (
    fleet_id integer NOT NULL,
    db_ship_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT fleet_ships_count_check CHECK ((count >= 0))
);


ALTER TABLE ng0.fleet_ships OWNER TO freddec;

--
-- Name: fleets_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.fleets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.fleets_id_seq OWNER TO freddec;

--
-- Name: fleets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.fleets (
    id integer DEFAULT nextval('ng0.fleets_id_seq'::regclass) NOT NULL,
    profile_id integer NOT NULL,
    name character varying(16) NOT NULL,
    planet_id integer,
    stance boolean DEFAULT false NOT NULL,
    engaged boolean DEFAULT false NOT NULL,
    ore_count integer DEFAULT 0 NOT NULL,
    hydro_count integer DEFAULT 0 NOT NULL,
    worker_count integer DEFAULT 0 NOT NULL,
    scientist_count integer DEFAULT 0 NOT NULL,
    soldier_count integer DEFAULT 0 NOT NULL,
    cur_action_id integer,
    CONSTRAINT fleets_check CHECK (((ore_count >= 0) AND (hydro_count >= 0) AND (scientist_count >= 0) AND (soldier_count >= 0) AND (worker_count >= 0)))
);


ALTER TABLE ng0.fleets OWNER TO freddec;

--
-- Name: galaxies; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.galaxies (
    id integer NOT NULL,
    allow_new_players boolean DEFAULT true NOT NULL,
    creation_date timestamp with time zone DEFAULT now() NOT NULL,
    name character varying(16) NOT NULL
);


ALTER TABLE ng0.galaxies OWNER TO freddec;

--
-- Name: planet_building_pendings_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.planet_building_pendings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.planet_building_pendings_id_seq OWNER TO freddec;

--
-- Name: planet_building_pendings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_building_pendings (
    id integer DEFAULT nextval('ng0.planet_building_pendings_id_seq'::regclass) NOT NULL,
    planet_id integer NOT NULL,
    db_building_id integer NOT NULL,
    starting_date timestamp with time zone,
    ending_time timestamp with time zone,
    loop boolean DEFAULT false NOT NULL,
    count integer DEFAULT 1 NOT NULL,
    CONSTRAINT planet_building_pendings_count_check CHECK ((count <> 0))
);


ALTER TABLE ng0.planet_building_pendings OWNER TO freddec;

--
-- Name: planet_buildings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_buildings (
    planet_id integer NOT NULL,
    db_building_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT planet_buildings_count_check CHECK ((count >= 0))
);


ALTER TABLE ng0.planet_buildings OWNER TO freddec;

--
-- Name: planet_ship_pendings_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.planet_ship_pendings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.planet_ship_pendings_id_seq OWNER TO freddec;

--
-- Name: planet_ship_pendings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_ship_pendings (
    id integer DEFAULT nextval('ng0.planet_ship_pendings_id_seq'::regclass) NOT NULL,
    planet_id integer NOT NULL,
    db_ship_id integer NOT NULL,
    starting_date timestamp with time zone,
    ending_date timestamp with time zone,
    count integer DEFAULT 1 NOT NULL,
    loop boolean DEFAULT false NOT NULL,
    CONSTRAINT planet_ship_pendings_count_check CHECK ((count <> 0))
);


ALTER TABLE ng0.planet_ship_pendings OWNER TO freddec;

--
-- Name: planet_ships; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_ships (
    planet_id integer NOT NULL,
    db_ship_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT planet_ships_count_check CHECK ((count >= 0))
);


ALTER TABLE ng0.planet_ships OWNER TO freddec;

--
-- Name: planet_training_pendings_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.planet_training_pendings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.planet_training_pendings_id_seq OWNER TO freddec;

--
-- Name: planet_training_pendings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planet_training_pendings (
    id integer DEFAULT nextval('ng0.planet_training_pendings_id_seq'::regclass) NOT NULL,
    planet_id integer NOT NULL,
    starting_date timestamp with time zone,
    ending_date timestamp with time zone,
    scientist_count integer DEFAULT 0 NOT NULL,
    soldier_count integer DEFAULT 0 NOT NULL,
    loop boolean DEFAULT false NOT NULL,
    CONSTRAINT planet_training_pendings_check CHECK (((scientist_count > 0) OR (soldier_count > 0)))
);


ALTER TABLE ng0.planet_training_pendings OWNER TO freddec;

--
-- Name: planets_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.planets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.planets_id_seq OWNER TO freddec;

--
-- Name: planets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planets (
    id integer DEFAULT nextval('ng0.planets_id_seq'::regclass) NOT NULL,
    profile_id integer,
    name character varying(16),
    galaxy_id integer NOT NULL,
    sector integer NOT NULL,
    number integer NOT NULL,
    floor_count integer DEFAULT 0 NOT NULL,
    space_count integer DEFAULT 0 NOT NULL,
    ore_count integer DEFAULT 0 NOT NULL,
    hydro_count integer DEFAULT 0 NOT NULL,
    energy_count integer DEFAULT 0 NOT NULL,
    worker_count integer DEFAULT 0 NOT NULL,
    scientist_count integer DEFAULT 0 NOT NULL,
    soldier_count integer DEFAULT 0 NOT NULL,
    prod_last_date timestamp with time zone,
    spawn_ore integer DEFAULT 0 NOT NULL,
    spawn_hydro integer DEFAULT 0 NOT NULL,
    orbit_ore bigint DEFAULT 0 NOT NULL,
    orbit_hydro bigint DEFAULT 0 NOT NULL,
    next_battle_date timestamp with time zone,
    recruit_worker boolean DEFAULT true NOT NULL,
    CONSTRAINT planets_check CHECK (((ore_count >= 0) AND (hydro_count >= 0) AND (energy_count >= 0) AND (scientist_count >= 0) AND (soldier_count >= 0) AND (worker_count >= 0)))
);


ALTER TABLE ng0.planets OWNER TO freddec;

--
-- Name: profile_connections; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_connections (
    id integer NOT NULL,
    profile_id integer NOT NULL,
    ip_address character varying,
    forwarded character varying,
    user_agent character varying
);


ALTER TABLE ng0.profile_connections OWNER TO freddec;

--
-- Name: profile_connections_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.profile_connections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.profile_connections_id_seq OWNER TO freddec;

--
-- Name: profile_connections_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.profile_connections_id_seq OWNED BY ng0.profile_connections.id;


--
-- Name: profile_reports_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.profile_reports_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.profile_reports_id_seq OWNER TO freddec;

--
-- Name: profile_reports; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_reports (
    id integer DEFAULT nextval('ng0.profile_reports_id_seq'::regclass) NOT NULL,
    profile_id integer NOT NULL,
    type integer NOT NULL,
    creation_date timestamp with time zone DEFAULT now() NOT NULL,
    reading_date timestamp with time zone,
    data character varying NOT NULL
);


ALTER TABLE ng0.profile_reports OWNER TO freddec;

--
-- Name: profile_ship_kills; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_ship_kills (
    profile_id integer NOT NULL,
    db_ship_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT profile_ship_kills_count_check CHECK ((count > 0))
);


ALTER TABLE ng0.profile_ship_kills OWNER TO freddec;

--
-- Name: profile_tech_pendings_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.profile_tech_pendings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.profile_tech_pendings_id_seq OWNER TO freddec;

--
-- Name: profile_tech_pendings; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_tech_pendings (
    id integer DEFAULT nextval('ng0.profile_tech_pendings_id_seq'::regclass) NOT NULL,
    profile_id integer NOT NULL,
    db_tech_id integer NOT NULL,
    starting_date timestamp with time zone,
    ending_date timestamp with time zone,
    loop boolean DEFAULT false NOT NULL
);


ALTER TABLE ng0.profile_tech_pendings OWNER TO freddec;

--
-- Name: profile_techs; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profile_techs (
    profile_id integer NOT NULL,
    db_tech_id integer NOT NULL,
    level integer NOT NULL,
    CONSTRAINT profile_techs_level_check CHECK ((level >= 0))
);


ALTER TABLE ng0.profile_techs OWNER TO freddec;

--
-- Name: profiles; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profiles (
    id integer NOT NULL,
    status integer DEFAULT '-3'::integer NOT NULL,
    username character varying(16),
    credit_count integer DEFAULT 3500 NOT NULL,
    avatar_url character varying(255),
    cur_planet_id integer,
    deletion_date timestamp with time zone,
    last_connection_date timestamp with time zone DEFAULT now() NOT NULL,
    reset_count integer DEFAULT 0 NOT NULL,
    starting_date timestamp with time zone,
    prestige_count integer DEFAULT 0 NOT NULL,
    CONSTRAINT profiles_check CHECK (((credit_count >= 0) AND (prestige_count >= 0)))
);


ALTER TABLE ng0.profiles OWNER TO freddec;

--
-- Name: server_processes; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.server_processes (
    process character varying(64) NOT NULL,
    lastrun_date timestamp with time zone DEFAULT now() NOT NULL,
    frequency interval NOT NULL,
    lastrun_result character varying
);


ALTER TABLE ng0.server_processes OWNER TO freddec;

--
-- Name: vw_galaxies; Type: VIEW; Schema: ng0; Owner: freddec
--

CREATE VIEW ng0.vw_galaxies AS
 SELECT galaxies.id,
    galaxies.creation_date,
    galaxies.name,
    galaxies.allow_new_players,
    ( SELECT count(planets.id) AS count
           FROM ng0.planets
          WHERE ((planets.galaxy_id = galaxies.id) AND (((planets.sector % 10) = 0) OR ((planets.sector % 10) = 1) OR (planets.sector <= 10) OR (planets.sector > 90)))) AS planet_count_for_new
   FROM ng0.galaxies;


ALTER TABLE ng0.vw_galaxies OWNER TO freddec;

--
-- Name: vw_profiles; Type: VIEW; Schema: ng0; Owner: freddec
--

CREATE VIEW ng0.vw_profiles AS
 SELECT profiles.id,
    profiles.status,
    profiles.username,
    profiles.credit_count,
    profiles.prestige_count,
    profiles.last_connection_date,
    profiles.reset_count,
    profiles.starting_date
   FROM ng0.profiles;


ALTER TABLE ng0.vw_profiles OWNER TO freddec;

--
-- Name: profile_connections id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_connections ALTER COLUMN id SET DEFAULT nextval('ng0.profile_connections_id_seq'::regclass);


--
-- Data for Name: battle_fleet_ship_kills; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_fleet_ship_kills (battle_fleet_ship_id, db_ship_id, count) FROM stdin;
\.


--
-- Data for Name: battle_fleet_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_fleet_ships (id, battle_fleet_id, db_ship_id, initial_count, remaining_count) FROM stdin;
\.


--
-- Data for Name: battle_fleets; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battle_fleets (id, battle_id, profile_id, profile_name, fleet_id, fleet_name, fleet_stance, winner, mod_shield, mod_handling, mod_tracking, mod_damage) FROM stdin;
\.


--
-- Data for Name: battles; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.battles (id, creation_date, planet_id, round_count, key) FROM stdin;
\.


--
-- Data for Name: db_building_building_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_building_building_reqs (db_building_id, req_id) FROM stdin;
201	102
201	101
202	201
203	201
205	201
301	202
301	201
302	301
303	302
303	301
303	203
321	301
320	301
221	201
220	201
222	201
207	201
218	207
208	201
308	301
206	201
204	201
309	301
391	301
209	201
390	201
390	202
102	101
115	101
116	101
117	101
105	101
106	101
118	101
217	202
317	302
401	301
400	301
402	301
230	201
404	403
403	207
231	201
\.


--
-- Data for Name: db_building_tech_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_building_tech_reqs (db_building_id, req_id, level) FROM stdin;
317	402	3
317	404	3
217	402	2
317	403	3
118	401	2
391	405	1
390	405	1
403	402	3
403	403	3
403	404	3
\.


--
-- Data for Name: db_buildings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_buildings (id, category, name, floor, space, cost_ore, cost_hydro, cost_worker, cost_credit, cost_prestige, prod_energy, prod_ore, prod_hydro, prod_credit, prod_prestige, storage_ore, storage_hydro, storage_energy, storage_worker, storage_scientist, storage_soldier, buildable, build_max, build_time, destroyable, mod_prod_ore, mod_prod_hydro, mod_prod_energy, mod_prod_worker, mod_speed_building, mod_speed_ship, strength_radar, strength_jammer, training_scientist, training_soldiers, expiration) FROM stdin;
120	31	ore_hangar1	1	0	1000	500	5000	10	0	0	0	0	0	0	50000	0	0	0	0	0	f	200	9000	t	0	0	0	0	0	0	0	0	0	0	0
390	10	cave	-4	0	400000	300000	45000	0	0	0	0	0	0	0	0	0	0	0	0	0	t	5	345600	f	0	0	0	0	0	0	0	0	0	0	0
391	10	moon	0	-10	700000	150000	55000	0	0	0	0	0	0	0	0	0	0	0	0	0	t	1	432000	f	0	0	0	0	0	0	0	0	0	0	0
601	0	space_jammer	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	f	1	3600	t	0	0	0	0	0	0	0	10	0	0	28800
600	0	space_radar	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	f	1	3600	t	0	0	0	0	0	0	1	0	0	0	28800
121	32	hydro_hangar1	1	0	1000	500	5000	10	0	0	0	0	0	0	0	50000	0	0	0	0	f	200	9900	t	0	0	0	0	0	0	0	0	0	0	0
117	23	solar_power_plant	1	0	200	300	1000	20	0	-200	0	0	0	0	0	0	0	0	0	0	t	200	1200	t	0	0	0	0	0	0	0	0	0	0	0
101	10	colony1	2	0	20000	10000	2500	0	0	300	100	50	2500	10	100000	100000	30000	20000	1000	1000	t	1	44800	f	0	0	0	0	0	0	0	0	50	50	0
403	23	star_belt	0	2	2000000	1600000	50000	10000	200000	50000	0	0	0	0	0	0	0	0	0	0	t	1	512000	t	0	0	0	0	0	0	0	0	0	0	0
320	31	ore_hangar3	3	0	80000	55000	15000	100	0	-500	0	0	0	0	1000000	0	0	0	0	0	t	200	56000	t	0	0	0	0	0	0	0	0	0	0	0
102	11	construction_plant1	1	0	2000	1250	5000	50	0	-50	0	0	0	0	0	0	0	0	0	0	t	1	43200	t	0	0	0	0	0.05	0	0	0	0	0	0
218	23	solar_power_satellite	0	1	4000	7000	2500	125	0	600	0	0	0	0	0	0	0	0	0	0	t	200	32000	t	0	0	0	0	0	0	0	0	0	0	0
309	80	jammer	0	1	90000	65000	25000	100	0	-1000	0	0	0	0	0	0	0	0	0	0	t	200	100000	t	0	0	0	0	0	0	0	2	0	0	0
222	33	energy_storage	1	0	30000	20000	15000	20	0	-100	0	0	0	0	0	0	100000	0	0	0	t	200	30800	t	0	0	0	0	0	0	0	0	0	0	0
220	31	ore_hangar2	2	0	25000	14000	10000	20	0	-100	0	0	0	0	200000	0	0	0	0	0	t	200	28000	t	0	0	0	0	0	0	0	0	0	0	0
308	30	military_base	3	0	110000	90000	30000	250	0	-600	0	0	0	0	0	0	0	0	0	10000	t	200	172800	t	0	0	0	0	0	0	0	0	0	100	0
207	23	rectenna	2	0	16000	5000	6000	25	0	-50	0	0	0	0	0	0	0	0	0	0	t	1	42000	t	0	0	0	0	0	0	0	0	0	0	0
302	11	construction_plant3	1	0	100000	80000	35000	150	0	-800	0	0	0	0	0	0	0	0	0	0	t	1	172800	t	0	0	0	0	0	0	0	0	0	0	0
116	20	hydro_mine	2	0	1000	500	2000	20	0	-25	0	400	0	0	0	0	0	0	0	0	t	200	7200	t	0	0.01	0	0	0	0	0	0	0	0	0
115	20	ore_mine	2	0	500	1000	2000	20	0	-25	400	0	0	0	0	0	0	0	0	0	t	200	7200	t	0.01	0	0	0	0	0	0	0	0	0	0
317	23	tokamat	4	0	140000	90000	40000	600	0	10000	0	0	0	100	0	0	0	0	0	0	t	1	172800	t	0	0	0	0	0	0	0	0	0	0	0
401	31	ore_hangar4	2	0	500000	400000	25000	200	10000	-1000	0	0	0	0	2000000	0	0	0	0	0	t	200	128000	t	0	0	0	0	0	0	0	0	0	0	0
402	32	hydro_hangar4	2	0	500000	400000	25000	200	10000	-1000	0	0	0	0	0	2000000	0	0	0	0	t	200	128000	t	0	0	0	0	0	0	0	0	0	0	0
221	32	hydro_hangar2	2	0	25000	14000	10000	20	0	-100	0	0	0	0	0	200000	0	0	0	0	t	200	30800	t	0	0	0	0	0	0	0	0	0	0	0
321	32	hydro_hangar3	3	0	80000	55000	15000	100	0	-500	0	0	0	0	0	1000000	0	0	0	0	t	200	61600	t	0	0	0	0	0	0	0	0	0	0	0
303	40	heavy_factory	12	0	180000	160000	32000	1000	0	-600	0	0	0	0	0	0	0	0	0	0	t	1	172800	t	0	0	0	0	0	0.02	0	0	0	0	0
203	40	light_factory	6	0	32000	25000	17500	300	0	-250	0	0	0	0	0	0	0	0	0	0	t	1	50400	t	0	0	0	0	0	0.02	0	0	0	0	0
231	20	credit_mine	4	0	30000	25000	10000	0	0	-3000	0	0	8000	0	0	0	0	0	0	0	t	200	54000	t	0	0	0	0	0	0	0	0	0	0	0
206	30	research_center	2	0	28000	21000	15000	50	0	-150	0	0	0	0	0	0	0	0	5000	0	t	1	108000	t	0	0	0	0	0	0	0	0	100	0	0
400	10	wonder	2	0	600000	150000	28000	0	1000	-200	0	0	1000	100	0	0	0	0	0	0	t	1	320000	t	0	0	0	0	0	0	0	0	0	0	0
208	30	military_barracks	1	0	22000	10000	6000	100	0	-200	0	0	0	0	0	0	0	0	0	2000	t	200	108000	t	0	0	0	0	0	0	0	0	0	100	0
230	30	housing	4	0	30000	18000	10000	0	0	-500	0	0	1000	0	0	0	0	0	0	0	t	10	28000	t	0	0	0	0.1	0	0	0	0	0	0	0
106	30	laboratory	1	0	2500	2000	4000	50	0	-100	0	0	0	0	0	0	0	0	1000	0	t	200	9600	t	0	0	0	0	0	0	0	0	150	0	0
201	10	colony2	2	0	35000	35000	6000	0	0	-100	0	0	1500	0	0	0	70000	10000	0	0	t	1	64800	t	0.02	0.02	0.02	0.1	0	0	0	0	0	0	0
301	10	colony3	3	1	200000	200000	30000	0	0	-500	0	0	2500	0	0	0	0	10000	0	0	t	1	259200	t	0.02	0.02	0.02	0.1	0	0	0	0	0	0	0
202	11	construction_plant2	1	0	22500	15000	15000	100	0	-250	0	0	0	0	0	0	0	0	0	0	t	1	64800	t	0	0	0	0	0.05	0	0	0	0	0	0
205	80	shipyard	2	6	40000	30000	22000	1500	0	-150	0	0	0	0	0	0	0	0	0	0	t	1	108000	t	0	0	0	0	0	0.05	0	0	0	0	0
105	80	spaceport	4	0	2500	2000	5000	200	0	-50	0	0	0	0	0	0	0	0	0	0	t	1	36000	t	0	0	0	0	0	0	0	0	0	0	0
204	30	workshop	1	0	8000	4000	5000	0	0	-150	0	0	200	0	0	0	0	3000	0	0	t	200	21600	t	0	0	0	0	0	0	0	0	0	0	0
209	80	radar	0	2	15000	8500	7000	200	0	-300	0	0	0	0	0	0	0	0	0	0	t	200	39600	t	0	0	0	0	0	0	2	0	0	0	0
217	23	nuclear_power_plant	2	0	28000	14000	7500	150	0	-2000	0	0	0	0	0	0	0	0	0	0	t	200	43200	t	0	0	0	0	0	0	0	0	0	0	0
118	23	geothermal_power_plant	1	0	1500	1250	1000	50	0	300	0	0	0	0	0	0	0	0	0	0	t	200	3600	t	0	0	0	0	0	0	0	0	0	0	0
404	23	star_belt_panel	0	0	400000	300000	25000	1000	10000	10000	0	0	0	0	0	0	0	0	0	0	t	5	128000	t	0	0	0	0	0	0	0	0	0	0	0
\.


--
-- Data for Name: db_ship_building_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_ship_building_reqs (db_ship_id, req_id) FROM stdin;
102	205
103	205
201	105
202	105
301	105
301	203
302	203
304	203
402	205
402	303
404	205
404	203
501	205
501	303
504	205
504	303
101	105
950	205
100	105
106	205
150	105
110	105
140	205
141	205
104	205
302	105
304	105
505	205
505	303
203	105
\.


--
-- Data for Name: db_ship_tech_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_ship_tech_reqs (db_ship_id, req_id, level) FROM stdin;
101	902	1
201	501	1
202	501	2
501	505	2
102	902	2
103	902	5
106	105	1
402	506	1
504	505	3
304	504	3
301	504	1
404	503	1
302	502	1
150	902	3
110	902	3
106	902	5
501	907	1
104	902	5
402	906	2
404	906	3
301	905	1
302	905	2
304	905	3
201	904	1
104	105	1
140	903	2
141	903	3
504	907	2
202	904	2
100	901	1
505	505	3
505	907	3
203	904	3
203	501	3
305	504	3
305	905	3
\.


--
-- Data for Name: db_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_ships (id, category, name, cost_ore, cost_hydro, cost_energy, cost_worker, cost_credit, cost_prestige, build_time, cargo, hull, shield, tracking, turret, signature, speed, handling, recycling_capacity, warping_capacity, db_building_id, buildable, dmg_em, dmg_explosive, dmg_kinetic, dmg_thermal, resist_em, resist_explosive, resist_kinetic, resist_thermal, class, reward_prestige, reward_credit) FROM stdin;
102	10	cargo_V	21000	18000	1000	350	40	0	7200	100000	9000	4000	0	0	78	1100	100	0	0	\N	t	0	0	0	0	0	0	0	0	1	0	0
110	10	recycler	10000	7000	500	100	5	0	5760	5000	6000	5000	0	0	34	1000	100	3000	0	\N	t	0	0	0	0	0	0	0	0	1	0	0
101	10	cargo_I	8000	8000	500	200	20	0	3600	30000	3000	1000	0	0	32	1200	200	0	0	\N	t	0	0	0	0	0	0	0	0	1	0	0
103	10	cargo_X	48000	27000	2000	600	75	0	10800	225000	25000	20000	0	0	150	1000	50	0	0	\N	t	0	0	0	0	0	0	0	0	1	0	0
106	10	jumper	45000	35000	8000	16	10	0	20400	0	5000	3000	0	0	40	800	10	0	2000	\N	t	0	0	0	0	0	0	0	0	1	0	0
140	15	sector_probe	30000	20000	2500	0	50	0	19000	0	1	0	0	0	100	22500	1	0	0	600	t	0	0	0	0	0	0	0	0	1	0	0
601	60	redempteur	2000000	1800000	500000	6000	8000	100000	280000	10000	1000000	3200000	900	28	7600	450	350	0	0	\N	f	1500	0	0	0	40	75	30	91	5	1000	0
950	50	imperial_cruiser	900000	800000	5000	25000	200	0	240000	25000	15000	25000	720	7	3400	750	470	0	0	\N	f	250	0	250	0	35	60	25	90	1	10	0
952	20	mower	1100	900	100	3	8	0	500	5	300	50	2300	2	8	1650	1500	0	0	\N	f	10	0	0	10	-30	50	0	5	1	1	0
953	80	fortress	10000000	20000000	0	30000	20000	0	500000	10000000	63568	53392	100	400	20000	150	600	20000	32500	\N	f	0	0	0	0	0	0	0	0	1	1000	0
954	40	escorter	10000	5000	1000	100	26	0	2880	50	200	250	400	4	26	550	330	0	0	\N	f	0	50	30	70	30	40	25	50	3	7	0
955	30	rogue_ctm	4500	2600	750	32	10	0	2240	50	3000	0	2300	16	15	1200	900	0	0	\N	f	0	0	0	10	0	0	0	25	2	3	0
100	10	probe	500	500	50	0	1	0	180	0	1	0	0	0	1	25000	1	0	0	\N	t	0	0	0	0	0	0	0	0	1	0	0
104	10	cargo_Z	120000	80000	10000	1000	175	0	36000	1000000	75000	60000	0	0	300	1000	25	0	300	\N	t	0	0	0	0	0	0	0	0	1	0	0
141	15	jammer_probe	100000	70000	5000	0	200	0	19000	0	1	0	0	0	340	20000	1	0	0	601	t	0	0	0	0	0	0	0	0	1	0	0
501	50	cruiser	20000	14000	3000	250	50	0	4400	200	10000	20000	720	4	68	800	400	0	50	\N	t	0	0	400	0	30	65	45	85	4	10	0
504	50	battle_cruiser	35000	25000	5000	500	90	0	7900	300	10000	25000	720	6	120	800	400	0	100	\N	t	0	0	750	0	35	70	50	85	4	10	0
302	30	heavy_corvette	2000	2500	500	8	6	0	800	25	1500	0	1100	1	9	1200	960	0	0	\N	t	0	225	0	0	10	35	20	35	2	2	0
304	30	multi_gun_corvette	2500	2500	750	10	7	0	950	25	1500	0	2300	5	10	1200	970	0	0	\N	t	0	0	0	15	11	36	21	36	2	2	0
150	10	colonizer_I	25000	11600	10000	2500	100	0	54400	0	10000	2000	0	0	72	450	1	0	0	101	t	0	0	0	0	0	0	0	0	1	0	0
404	40	missile_frigate	13000	12000	2000	120	35	0	4000	50	6000	2500	2000	8	50	950	685	0	16	\N	t	0	50	0	0	60	45	30	65	3	5	0
402	40	ion_frigate	9000	7000	1500	80	20	0	2500	75	3500	2500	450	1	32	900	680	0	16	\N	t	4000	0	0	0	60	45	30	65	3	5	0
202	20	interceptor	1000	1500	75	2	3	0	550	0	275	0	2400	1	5	1500	1500	0	0	\N	t	0	0	0	30	0	90	0	-25	1	1	0
201	20	fighter	800	1200	50	2	2	0	420	15	350	0	2200	1	4	1450	1400	0	0	\N	t	0	0	0	20	0	85	0	-30	1	1	0
301	30	light_corvette	1500	2000	100	4	4	0	600	50	1600	0	1500	3	7	1200	965	0	0	\N	t	0	0	0	15	5	30	15	30	2	2	0
959	60	annihilator	2000000	1500000	20000	30000	1000	0	300000	30000	500000000	500000000	1500	200	1	400	200	0	0	\N	f	5000	5000	5000	5000	20	95	95	95	5	1000000	0
951	60	obliterator	200000	200000	20000	30000	1000	0	300000	30000	200000	200000	650	20	800	600	450	0	0	\N	f	500	500	500	500	20	50	50	50	5	100	0
203	20	predator	1000	1500	75	2	2	5	590	0	275	0	2450	1	5	1550	1505	0	0	\N	t	0	0	0	35	1	91	1	-24	1	1	0
505	50	elite_cruiser	35000	25000	5000	500	80	100	8400	300	10000	25000	725	6	120	900	405	0	100	\N	t	0	0	800	0	36	71	51	90	4	10	0
305	30	elite_corvette	3000	3000	600	8	9	10	1300	50	1800	0	1700	4	12	1350	965	0	0	\N	f	0	0	0	20	10	35	20	35	2	5	0
401	40	assault_frigate	9000	5000	1000	50	16	0	2080	50	7500	2500	1000	3	28	900	680	0	16	\N	t	0	0	130	0	55	45	25	60	3	5	0
\.


--
-- Data for Name: db_tech_tech_reqs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_tech_tech_reqs (db_tech_id, req_id, level) FROM stdin;
202	201	3
203	201	2
204	201	5
204	203	5
205	201	3
206	201	5
206	205	5
403	401	5
404	401	3
502	501	2
505	504	3
501	901	1
405	401	4
902	901	1
503	501	3
504	501	3
503	502	1
506	501	5
505	501	4
403	402	3
506	403	1
105	404	3
402	401	2
510	102	5
102	101	3
907	901	5
907	102	4
906	901	4
906	102	3
905	901	3
905	102	1
904	901	2
903	902	5
903	901	5
\.


--
-- Data for Name: db_techs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.db_techs (id, category, name, rank, level_count, level_default, cost_credit, mod_prod_ore, mod_prod_hydro, mod_prod_energy, mod_prod_worker, mod_speed_building, mod_speed_ship, mod_fleet_damage, mod_fleet_speed, mod_fleet_shield, mod_fleet_handling, mod_fleet_tracking, mod_fleet_recycling, mod_tech_cost, mod_tech_time, mod_planet_count, expiration) FROM stdin;
501	50	weaponry	3	5	1	150	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
203	20	mining	2	5	0	90	0.01	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
206	20	improved_refining	7	5	0	2000	0	0.01	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
402	40	nuclear_physics	2	3	0	300	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
502	50	rockets	2	1	0	40	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
503	50	missiles	4	1	0	110	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
504	50	laser_turrets	2	3	0	60	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
505	50	railgun	5	3	0	210	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
506	50	ion_cannon	6	1	0	290	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
510	50	enhanced_shield	6	5	0	500	0	0	0	0	0	0	0	0	0.05	0	0	0	0	0	0	\N
902	90	utility_ship_construction	1	5	0	40	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
401	40	science	3	5	2	40	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
204	20	improved_mining	7	5	0	2000	0.01	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
101	10	propulsion	1	5	0	40	0	0	0	0	0	0	0	0.01	0	0	0	0	0	0	0	\N
102	10	energy_conservation	3	5	0	220	0	0	0.02	0	0	0	0	0	0	0	0	0	0	0	0	\N
907	90	cruiser_construction	6	3	0	600	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
403	40	plasma_physics	4	3	0	1600	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
404	40	quantum_physics	6	3	0	700	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
901	90	mechanic	3	5	1	50	0	0	0	0	0	0.01	0	0	0	0	0	0	0	0	0	\N
405	40	planetology	8	1	0	6000	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
205	20	refining	2	5	0	90	0	0.01	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
202	20	mass_production	3	5	0	600	0	0	0	0	0.04	0.05	0	0	0	0	0	0	0	0	0	\N
906	90	frigate_construction	4	3	0	350	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
903	90	tactical_ship_construction	8	3	0	800	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
905	90	corvette_construction	2	3	0	120	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
201	20	industry	3	5	0	40	0	0	0	0	0.01	0	0	0	0	0	0	0	0	0	0	\N
105	10	jumpdrive	7	1	0	4000	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
904	90	light_ship_construction	1	3	1	40	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	\N
301	30	planet_control	7	5	0	2000	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	\N
\.


--
-- Data for Name: fleet_actions; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.fleet_actions (id, fleet_id, action, "time", origin_planet_id, dest_planet_id, ore_count, hydro_count, scientist_count, soldier_count, worker_count) FROM stdin;
\.


--
-- Data for Name: fleet_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.fleet_ships (fleet_id, db_ship_id, count) FROM stdin;
9	201	33
9	202	103
9	301	52
9	302	29
10	201	28
10	202	12
10	302	12
11	201	153
11	202	182
11	304	234
11	401	93
11	402	232
11	501	223
12	201	281
12	202	219
12	301	352
12	302	341
12	304	475
12	401	478
12	402	263
12	404	733
12	501	559
12	504	651
13	201	109
13	202	125
13	301	63
13	302	164
13	304	33
13	401	55
14	201	1547
14	202	1611
14	301	618
14	302	238
14	304	351
14	401	421
14	402	459
14	404	1162
14	501	1099
14	504	1068
15	201	349
15	202	272
15	301	276
15	302	533
15	304	799
15	401	301
15	402	491
15	404	1165
15	501	964
15	504	1122
16	201	7125
16	202	5702
16	301	842
16	302	857
16	304	1392
16	401	1025
16	402	601
16	404	1006
16	501	1966
16	504	2911
17	201	31
17	202	81
17	301	54
17	302	26
18	201	1376
18	202	1597
18	301	351
18	302	462
18	304	357
18	401	360
18	402	555
18	404	906
18	501	723
18	504	1298
19	201	1221
19	202	2023
19	301	260
19	302	618
19	304	509
19	401	277
19	402	984
19	404	1288
19	501	347
19	504	918
20	201	39
20	202	104
20	301	56
20	302	22
21	201	7144
21	202	5437
21	301	972
21	302	867
21	304	1394
21	401	1203
21	402	795
21	404	1277
21	501	1946
21	504	2070
22	201	1608
22	202	1698
22	301	529
22	302	592
22	304	676
22	401	691
22	402	274
22	404	1480
22	501	733
22	504	886
23	201	102
23	202	140
23	304	277
23	401	66
23	402	248
23	501	220
24	201	1686
24	202	809
24	301	643
24	302	550
24	304	273
24	401	582
24	402	474
24	404	1179
24	501	913
24	504	1129
25	201	28
25	202	108
25	301	67
25	302	27
26	201	124
26	202	198
26	301	84
26	302	184
26	304	43
26	401	45
27	201	7025
27	202	5919
27	301	987
27	302	877
27	304	1489
27	401	1059
27	402	785
27	404	1411
27	501	1728
27	504	2312
28	201	1746
28	202	1959
28	301	351
28	302	376
28	304	500
28	401	596
28	402	519
28	404	783
28	501	723
28	504	1195
29	201	1874
29	202	267
29	301	546
29	302	568
29	304	358
29	401	404
29	402	994
29	404	633
29	501	759
29	504	1126
30	201	864
30	202	930
30	301	369
30	302	204
30	304	310
30	401	489
30	402	372
30	404	581
30	501	547
30	504	591
31	201	6542
31	202	6159
31	301	945
31	302	982
31	304	1267
31	401	1163
31	402	651
31	404	1081
31	501	1824
31	504	2328
32	201	906
32	202	416
32	301	321
32	302	384
32	304	237
32	401	219
32	402	337
32	404	978
32	501	447
32	504	604
33	201	216
33	202	219
33	301	360
33	302	309
33	304	492
33	401	422
33	402	276
33	404	571
33	501	360
33	504	629
34	201	546
34	202	1104
34	301	243
34	302	202
34	304	443
34	401	237
34	402	270
34	404	521
34	501	428
34	504	586
35	201	6984
35	202	6729
35	301	985
35	302	974
35	304	1215
35	401	1223
35	402	615
35	404	1402
35	501	1537
35	504	2906
36	201	539
36	202	557
36	301	209
36	302	226
36	304	438
36	401	227
36	402	314
36	404	505
36	501	427
36	504	764
37	201	1337
37	202	1975
37	301	390
37	302	325
37	304	360
37	401	348
37	402	541
37	404	879
37	501	603
37	504	1141
38	201	934
38	202	218
38	301	370
38	302	511
38	304	212
38	401	249
38	402	641
38	404	1029
38	501	656
38	504	565
39	201	123
39	202	151
39	304	287
39	401	82
39	402	182
39	501	280
40	201	39
40	202	14
40	302	17
41	201	35
41	202	10
41	302	11
42	201	34
42	202	81
42	301	87
42	302	25
43	201	31
43	202	19
43	302	12
44	201	1608
44	202	1515
44	301	451
44	302	344
44	304	546
44	401	396
44	402	494
44	404	836
44	501	797
44	504	1289
45	201	711
45	202	627
45	301	235
45	302	206
45	304	276
45	401	426
45	402	212
45	404	623
45	501	515
45	504	569
46	201	966
46	202	441
46	301	397
46	302	396
46	304	264
46	401	334
46	402	328
46	404	607
46	501	548
46	504	799
47	201	5905
47	202	5640
47	301	896
47	302	832
47	304	1323
47	401	1200
47	402	635
47	404	1277
47	501	1985
47	504	2720
48	201	172
48	202	199
48	304	252
48	401	69
48	402	212
48	501	286
49	201	542
49	202	290
49	301	326
49	302	301
49	304	488
49	401	307
49	402	241
49	404	851
49	501	318
49	504	655
50	201	103
50	202	110
50	304	254
50	401	74
50	402	194
50	501	241
51	201	105
51	202	144
51	304	284
51	401	80
51	402	207
51	501	209
52	201	550
52	202	1080
52	301	373
52	302	304
52	304	202
52	401	462
52	402	361
52	404	805
52	501	560
52	504	723
53	201	180
53	202	160
53	301	60
53	302	156
53	304	49
53	401	56
54	201	555
54	202	933
54	301	307
54	302	309
54	304	396
54	401	416
54	402	350
54	404	940
54	501	599
54	504	773
55	201	1201
55	202	982
55	301	358
55	302	364
55	304	634
55	401	200
55	402	530
55	404	881
55	501	524
55	504	602
56	201	189
56	202	110
56	304	218
56	401	90
56	402	178
56	501	295
57	201	170
57	202	150
57	304	243
57	401	69
57	402	194
57	501	293
58	201	1571
58	202	1533
58	301	373
58	302	336
58	304	404
58	401	519
58	402	466
58	404	1167
58	501	524
58	504	1217
59	201	630
59	202	397
59	301	241
59	302	200
59	304	222
59	401	497
59	402	397
59	404	579
59	501	435
59	504	791
60	201	1884
60	202	1729
60	301	476
60	302	388
60	304	597
60	401	490
60	402	442
60	404	878
60	501	558
60	504	1180
61	201	196
61	202	198
61	301	68
61	302	186
61	304	39
61	401	57
62	201	123
62	202	133
62	301	95
62	302	146
62	304	32
62	401	47
63	201	1026
63	202	437
63	301	245
63	302	334
63	304	462
63	401	495
63	402	205
63	404	537
63	501	422
63	504	748
64	201	1907
64	202	1276
64	301	435
64	302	443
64	304	302
64	401	467
64	402	564
64	404	1184
64	501	744
64	504	1165
65	201	136
65	202	123
65	304	265
65	401	96
65	402	184
65	501	247
66	201	1675
66	202	1602
66	301	349
66	302	375
66	304	357
66	401	468
66	402	482
66	404	1061
66	501	543
66	504	1188
67	201	124
67	202	117
67	301	69
67	302	109
67	304	55
67	401	43
68	201	27
68	202	129
68	301	57
68	302	27
69	201	631
69	202	446
69	301	284
69	302	364
69	304	440
69	401	439
69	402	258
69	404	714
69	501	508
69	504	785
70	201	187
70	202	149
70	304	260
70	401	91
70	402	178
70	501	248
71	201	1636
71	202	2024
71	301	465
71	302	334
71	304	451
71	401	331
71	402	489
71	404	876
71	501	538
71	504	1128
72	201	861
72	202	1088
72	301	381
72	302	214
72	304	372
72	401	282
72	402	393
72	404	685
72	501	499
72	504	509
73	201	1125
73	202	833
73	301	247
73	302	340
73	304	268
73	401	254
73	402	289
73	404	593
73	501	398
73	504	677
74	201	318
74	202	333
74	301	242
74	302	223
74	304	220
74	401	316
74	402	274
74	404	817
74	501	326
74	504	709
75	201	38
75	202	113
75	301	70
75	302	36
76	201	33
76	202	121
76	301	99
76	302	36
77	201	115
77	202	179
77	304	223
77	401	69
77	402	171
77	501	299
78	201	842
78	202	582
78	301	236
78	302	236
78	304	302
78	401	462
78	402	351
78	404	536
78	501	373
78	504	699
79	201	22
79	202	81
79	301	71
79	302	29
80	201	1079
80	202	1135
80	301	296
80	302	335
80	304	399
80	401	471
80	402	346
80	404	873
80	501	410
80	504	629
81	201	2005
81	202	363
81	301	682
81	302	312
81	304	712
81	401	643
81	402	313
81	404	1406
81	501	501
81	504	1173
82	201	6185
82	202	6382
82	301	825
82	302	924
82	304	1381
82	401	1279
82	402	797
82	404	1455
82	501	1765
82	504	2763
83	201	1692
83	202	2017
83	301	486
83	302	357
83	304	356
83	401	505
83	402	448
83	404	1007
83	501	620
83	504	1290
84	201	2143
84	202	2122
84	301	383
84	302	331
84	304	388
84	401	515
84	402	475
84	404	1078
84	501	695
84	504	1156
85	201	621
85	202	1387
85	301	544
85	302	626
85	304	298
85	401	296
85	402	706
85	404	1188
85	501	389
85	504	699
86	201	26
86	202	96
86	301	56
86	302	37
87	201	1739
87	202	2041
87	301	467
87	302	377
87	304	492
87	401	405
87	402	538
87	404	1082
87	501	569
87	504	1117
88	201	619
88	202	410
88	301	394
88	302	257
88	304	383
88	401	414
88	402	387
88	404	831
88	501	445
88	504	674
89	201	930
89	202	368
89	301	327
89	302	255
89	304	481
89	401	454
89	402	303
89	404	998
89	501	594
89	504	714
90	201	964
90	202	691
90	301	272
90	302	356
90	304	210
90	401	441
90	402	321
90	404	864
90	501	334
90	504	721
91	201	111
91	202	116
91	304	289
91	401	77
91	402	236
91	501	253
92	201	2150
92	202	1250
92	301	452
92	302	320
92	304	389
92	401	375
92	402	514
92	404	1049
92	501	579
92	504	1004
93	201	830
93	202	865
93	301	567
93	302	246
93	304	619
93	401	504
93	402	420
93	404	734
93	501	384
93	504	521
94	201	1190
94	202	536
94	301	385
94	302	259
94	304	470
94	401	237
94	402	309
94	404	747
94	501	483
94	504	694
95	201	5711
95	202	5799
95	301	810
95	302	920
95	304	1428
95	401	1061
95	402	648
95	404	1288
95	501	1357
95	504	2745
96	201	141
96	202	108
96	301	110
96	302	128
96	304	40
96	401	40
97	201	38
97	202	12
97	302	15
98	201	1921
98	202	1370
98	301	686
98	302	399
98	304	638
98	401	668
98	402	863
98	404	616
98	501	1070
98	504	559
99	201	159
99	202	179
99	301	76
99	302	119
99	304	53
99	401	44
100	201	25
100	202	87
100	301	81
100	302	38
101	201	1843
101	202	2038
101	301	450
101	302	312
101	304	589
101	401	442
101	402	521
101	404	1143
101	501	676
101	504	1088
102	201	544
102	202	267
102	301	362
102	302	228
102	304	425
102	401	414
102	402	375
102	404	741
102	501	365
102	504	730
103	201	679
103	202	594
103	301	393
103	302	217
103	304	348
103	401	247
103	402	295
103	404	673
103	501	526
103	504	509
104	201	1199
104	202	1070
104	301	283
104	302	251
104	304	495
104	401	201
104	402	278
104	404	818
104	501	569
104	504	566
105	201	5627
105	202	5697
105	301	961
105	302	942
105	304	1259
105	401	1240
105	402	732
105	404	1200
105	501	1451
105	504	2496
106	201	163
106	202	121
106	304	227
106	401	86
106	402	220
106	501	221
107	201	21
107	202	114
107	301	77
107	302	29
108	201	374
108	202	759
108	301	295
108	302	233
108	304	283
108	401	357
108	402	290
108	404	975
108	501	435
108	504	704
109	201	31
109	202	15
109	302	17
110	201	1159
110	202	1382
110	301	237
110	302	341
110	304	572
110	401	421
110	402	410
110	404	972
110	501	386
110	504	1142
111	201	39
111	202	98
111	301	87
111	302	31
112	201	23
112	202	15
112	302	10
113	201	193
113	202	154
113	301	69
113	302	189
113	304	46
113	401	57
114	201	177
114	202	114
114	301	90
114	302	116
114	304	59
114	401	57
115	201	911
115	202	743
115	301	368
115	302	343
115	304	423
115	401	225
115	402	358
115	404	996
115	501	433
115	504	587
116	201	676
116	202	504
116	301	250
116	302	362
116	304	346
116	401	442
116	402	377
116	404	531
116	501	389
116	504	696
117	201	1154
117	202	1139
117	301	347
117	302	271
117	304	687
117	401	304
117	402	236
117	404	1489
117	501	850
117	504	761
118	201	1416
118	202	1254
118	301	266
118	302	395
118	304	384
118	401	513
118	402	653
118	404	1075
118	501	596
118	504	1168
119	201	902
119	202	1126
119	301	367
119	302	331
119	304	472
119	401	365
119	402	384
119	404	860
119	501	354
119	504	744
120	201	416
120	202	1429
120	301	358
120	302	428
120	304	752
120	401	457
120	402	619
120	404	823
120	501	737
120	504	1016
121	201	519
121	202	1049
121	301	352
121	302	283
121	304	465
121	401	419
121	402	201
121	404	964
121	501	452
121	504	554
122	201	904
122	202	821
122	301	266
122	302	208
122	304	424
122	401	321
122	402	234
122	404	895
122	501	361
122	504	600
123	201	659
123	202	500
123	301	366
123	302	243
123	304	462
123	401	200
123	402	326
123	404	824
123	501	519
123	504	543
124	201	1097
124	202	1314
124	301	394
124	302	614
124	304	431
124	401	494
124	402	505
124	404	1061
124	501	476
124	504	1159
125	201	179
125	202	115
125	304	224
125	401	65
125	402	151
125	501	251
126	201	909
126	202	1171
126	301	279
126	302	390
126	304	337
126	401	408
126	402	287
126	404	678
126	501	595
126	504	605
127	201	149
127	202	162
127	304	284
127	401	78
127	402	187
127	501	223
128	201	1066
128	202	1105
128	301	223
128	302	332
128	304	434
128	401	360
128	402	378
128	404	536
128	501	360
128	504	559
129	201	195
129	202	147
129	301	81
129	302	182
129	304	34
129	401	32
130	201	1881
130	202	1582
130	301	495
130	302	436
130	304	317
130	401	326
130	402	525
130	404	772
130	501	522
130	504	1216
131	201	7053
131	202	6340
131	301	872
131	302	946
131	304	1438
131	401	1246
131	402	660
131	404	1042
131	501	1349
131	504	2920
132	201	1248
132	202	1274
132	301	383
132	302	487
132	304	368
132	401	571
132	402	458
132	404	780
132	501	641
132	504	1064
133	201	318
133	202	563
133	301	212
133	302	300
133	304	330
133	401	308
133	402	391
133	404	859
133	501	515
133	504	538
134	201	112
134	202	170
134	301	83
134	302	189
134	304	52
134	401	54
135	201	959
135	202	965
135	301	209
135	302	206
135	304	347
135	401	270
135	402	215
135	404	823
135	501	473
135	504	736
136	201	718
136	202	744
136	301	374
136	302	247
136	304	496
136	401	461
136	402	241
136	404	742
136	501	529
136	504	687
137	201	504
137	202	419
137	301	257
137	302	251
137	304	314
137	401	477
137	402	216
137	404	600
137	501	344
137	504	549
138	201	813
138	202	1077
138	301	279
138	302	215
138	304	429
138	401	222
138	402	326
138	404	818
138	501	410
138	504	539
139	201	811
139	202	2169
139	301	620
139	302	344
139	304	594
139	401	584
139	402	976
139	404	1300
139	501	890
139	504	844
140	201	1563
140	202	1437
140	301	568
140	302	312
140	304	247
140	401	508
140	402	563
140	404	767
140	501	652
140	504	1044
141	201	170
141	202	142
141	301	70
141	302	159
141	304	32
141	401	56
142	201	6648
142	202	5699
142	301	996
142	302	967
142	304	1484
142	401	1003
142	402	762
142	404	1470
142	501	1374
142	504	2178
143	201	1537
143	202	1712
143	301	495
143	302	627
143	304	374
143	401	413
143	402	720
143	404	918
143	501	372
143	504	904
144	201	29
144	202	11
144	302	19
145	201	6294
145	202	5680
145	301	940
145	302	889
145	304	1446
145	401	1298
145	402	679
145	404	1124
145	501	1656
145	504	2922
146	201	592
146	202	816
146	301	315
146	302	356
146	304	327
146	401	446
146	402	350
146	404	829
146	501	460
146	504	618
147	201	34
147	202	12
147	302	17
148	201	36
148	202	111
148	301	68
148	302	27
149	201	195
149	202	166
149	304	247
149	401	78
149	402	164
149	501	247
150	201	2079
150	202	1445
150	301	693
150	302	663
150	304	367
150	401	363
150	402	820
150	404	632
150	501	979
150	504	691
151	201	1318
151	202	1433
151	301	483
151	302	481
151	304	384
151	401	324
151	402	999
151	404	1248
151	501	311
151	504	550
152	201	1159
152	202	352
152	301	239
152	302	335
152	304	296
152	401	230
152	402	378
152	404	742
152	501	405
152	504	633
153	201	1125
153	202	377
153	301	411
153	302	257
153	304	541
153	401	476
153	402	762
153	404	1466
153	501	897
153	504	933
154	201	6186
154	202	5796
154	301	840
154	302	837
154	304	1491
154	401	1023
154	402	734
154	404	1224
154	501	1498
154	504	2849
155	201	2139
155	202	1853
155	301	372
155	302	411
155	304	544
155	401	562
155	402	593
155	404	795
155	501	780
155	504	1125
156	201	333
156	202	338
156	301	380
156	302	251
156	304	309
156	401	267
156	402	204
156	404	823
156	501	393
156	504	745
157	201	555
157	202	465
157	301	308
157	302	269
157	304	246
157	401	349
157	402	221
157	404	552
157	501	360
157	504	548
158	201	7137
158	202	6928
158	301	921
158	302	907
158	304	1492
158	401	1187
158	402	721
158	404	1392
158	501	1621
158	504	2808
159	201	906
159	202	471
159	301	265
159	302	210
159	304	353
159	401	238
159	402	368
159	404	797
159	501	472
159	504	634
160	201	131
160	202	158
160	301	76
160	302	107
160	304	36
160	401	32
161	201	131
161	202	171
161	304	269
161	401	96
161	402	221
161	501	218
162	201	36
162	202	129
162	301	84
162	302	32
163	201	616
163	202	1325
163	301	475
163	302	698
163	304	782
163	401	699
163	402	433
163	404	1088
163	501	621
163	504	983
164	201	461
164	202	572
164	301	290
164	302	275
164	304	257
164	401	332
164	402	208
164	404	907
164	501	482
164	504	654
165	201	519
165	202	1178
165	301	303
165	302	245
165	304	259
165	401	481
165	402	292
165	404	762
165	501	417
165	504	679
166	201	164
166	202	164
166	304	293
166	401	94
166	402	219
166	501	241
167	201	6021
167	202	6111
167	301	998
167	302	971
167	304	1319
167	401	1292
167	402	699
167	404	1029
167	501	1682
167	504	2459
168	201	36
168	202	14
168	302	12
169	201	164
169	202	177
169	301	61
169	302	176
169	304	42
169	401	52
170	201	34
170	202	13
170	302	13
171	201	119
171	202	150
171	304	285
171	401	84
171	402	181
171	501	281
172	201	185
172	202	118
172	301	89
172	302	116
172	304	47
172	401	52
173	201	479
173	202	1087
173	301	334
173	302	208
173	304	310
173	401	431
173	402	263
173	404	714
173	501	404
173	504	640
174	201	196
174	202	197
174	301	86
174	302	112
174	304	60
174	401	47
175	201	130
175	202	195
175	304	240
175	401	88
175	402	183
175	501	235
176	201	35
176	202	18
176	302	12
177	201	24
177	202	116
177	301	76
177	302	36
178	201	124
178	202	110
178	301	73
178	302	122
178	304	58
178	401	35
179	201	1426
179	202	1747
179	301	462
179	302	438
179	304	308
179	401	442
179	402	544
179	404	850
179	501	506
179	504	1187
180	201	38
180	202	119
180	301	83
180	302	34
181	201	178
181	202	156
181	301	60
181	302	133
181	304	52
181	401	40
182	201	129
182	202	160
182	304	227
182	401	74
182	402	153
182	501	224
183	201	103
183	202	155
183	304	201
183	401	59
183	402	244
183	501	216
184	201	38
184	202	129
184	301	80
184	302	21
185	201	739
185	202	1063
185	301	350
185	302	230
185	304	335
185	401	441
185	402	364
185	404	660
185	501	439
185	504	717
186	201	7119
186	202	5536
186	301	974
186	302	889
186	304	1456
186	401	1058
186	402	697
186	404	1176
186	501	1435
186	504	2642
187	201	197
187	202	127
187	304	251
187	401	72
187	402	210
187	501	241
188	201	1740
188	202	1804
188	301	516
188	302	294
188	304	451
188	401	428
188	402	245
188	404	566
188	501	379
188	504	1025
189	201	115
189	202	103
189	304	282
189	401	62
189	402	233
189	501	266
190	201	249
190	202	570
190	301	259
190	302	355
190	304	408
190	401	253
190	402	201
190	404	649
190	501	581
190	504	781
191	201	1744
191	202	2175
191	301	372
191	302	474
191	304	580
191	401	352
191	402	503
191	404	1168
191	501	536
191	504	1205
192	201	251
192	202	279
192	301	388
192	302	611
192	304	429
192	401	641
192	402	272
192	404	580
192	501	1047
192	504	916
193	201	150
193	202	185
193	304	206
193	401	93
193	402	231
193	501	231
194	201	219
194	202	710
194	301	208
194	302	383
194	304	429
194	401	348
194	402	209
194	404	642
194	501	497
194	504	658
195	201	1657
195	202	1507
195	301	321
195	302	433
195	304	453
195	401	439
195	402	524
195	404	1149
195	501	798
195	504	1176
196	201	6296
196	202	5620
196	301	945
196	302	982
196	304	1475
196	401	1017
196	402	728
196	404	1040
196	501	1971
196	504	2836
197	201	1749
197	202	1377
197	301	421
197	302	349
197	304	425
197	401	590
197	402	585
197	404	856
197	501	619
197	504	1192
198	201	489
198	202	1174
198	301	398
198	302	349
198	304	283
198	401	257
198	402	279
198	404	919
198	501	318
198	504	554
199	201	1833
199	202	1794
199	301	311
199	302	409
199	304	465
199	401	550
199	402	474
199	404	999
199	501	594
199	504	1111
200	201	781
200	202	528
200	301	343
200	302	209
200	304	328
200	401	204
200	402	325
200	404	524
200	501	434
200	504	500
201	201	1622
201	202	1260
201	301	334
201	302	351
201	304	703
201	401	581
201	402	582
201	404	1357
201	501	658
201	504	795
202	201	119
202	202	109
202	304	295
202	401	88
202	402	235
202	501	251
203	201	25
203	202	97
203	301	71
203	302	39
204	201	1154
204	202	913
204	301	213
204	302	386
204	304	334
204	401	283
204	402	239
204	404	633
204	501	376
204	504	534
205	201	170
205	202	141
205	301	93
205	302	198
205	304	49
205	401	49
206	201	1637
206	202	1534
206	301	488
206	302	307
206	304	348
206	401	441
206	402	509
206	404	771
206	501	716
206	504	1020
207	201	153
207	202	169
207	301	99
207	302	125
207	304	59
207	401	51
208	201	309
208	202	582
208	301	349
208	302	380
208	304	784
208	401	382
208	402	954
208	404	971
208	501	772
208	504	705
209	201	2060
209	202	813
209	301	622
209	302	499
209	304	288
209	401	341
209	402	822
209	404	682
209	501	445
209	504	562
210	201	1996
210	202	1895
210	301	346
210	302	420
210	304	520
210	401	544
210	402	538
210	404	969
210	501	607
210	504	1145
211	201	1192
211	202	1107
211	301	349
211	302	362
211	304	202
211	401	205
211	402	283
211	404	867
211	501	303
211	504	500
212	201	171
212	202	143
212	304	236
212	401	61
212	402	237
212	501	200
213	201	1590
213	202	1339
213	301	367
213	302	300
213	304	408
213	401	463
213	402	444
213	404	849
213	501	708
213	504	1256
214	201	25
214	202	100
214	301	98
214	302	23
215	201	1150
215	202	862
215	301	283
215	302	387
215	304	434
215	401	371
215	402	211
215	404	537
215	501	336
215	504	509
216	201	39
216	202	88
216	301	73
216	302	36
217	201	759
217	202	484
217	301	293
217	302	335
217	304	311
217	401	474
217	402	376
217	404	618
217	501	520
217	504	798
218	201	406
218	202	467
218	301	282
218	302	378
218	304	446
218	401	392
218	402	260
218	404	544
218	501	567
218	504	751
219	201	34
219	202	117
219	301	60
219	302	32
220	201	114
220	202	173
220	304	265
220	401	70
220	402	187
220	501	250
221	201	1701
221	202	1406
221	301	497
221	302	338
221	304	381
221	401	485
221	402	408
221	404	901
221	501	747
221	504	1220
222	201	188
222	202	166
222	301	67
222	302	180
222	304	41
222	401	58
223	201	1646
223	202	1739
223	301	308
223	302	427
223	304	359
223	401	356
223	402	482
223	404	1094
223	501	547
223	504	1147
224	201	1220
224	202	1967
224	301	482
224	302	493
224	304	543
224	401	560
224	402	505
224	404	1073
224	501	750
224	504	1247
225	201	794
225	202	254
225	301	514
225	302	286
225	304	708
225	401	291
225	402	831
225	404	1447
225	501	663
225	504	663
226	201	1943
226	202	1702
226	301	563
226	302	400
226	304	475
226	401	224
226	402	572
226	404	917
226	501	805
226	504	579
227	201	2188
227	202	1442
227	301	364
227	302	404
227	304	476
227	401	522
227	402	519
227	404	852
227	501	796
227	504	1201
228	201	30
228	202	15
228	302	13
229	201	151
229	202	130
229	301	89
229	302	103
229	304	32
229	401	32
230	201	951
230	202	1095
230	301	393
230	302	212
230	304	331
230	401	236
230	402	365
230	404	817
230	501	534
230	504	658
231	201	1057
231	202	498
231	301	334
231	302	369
231	304	443
231	401	341
231	402	249
231	404	728
231	501	421
231	504	792
232	201	841
232	202	1011
232	301	357
232	302	223
232	304	231
232	401	482
232	402	320
232	404	767
232	501	553
232	504	574
233	201	1635
233	202	861
233	301	225
233	302	676
233	304	529
233	401	514
233	402	646
233	404	721
233	501	532
233	504	915
234	201	985
234	202	350
234	301	342
234	302	241
234	304	298
234	401	237
234	402	317
234	404	826
234	501	496
234	504	679
235	201	102
235	202	153
235	301	80
235	302	142
235	304	59
235	401	53
236	201	492
236	202	1134
236	301	214
236	302	266
236	304	455
236	401	318
236	402	285
236	404	883
236	501	502
236	504	728
237	201	36
237	202	93
237	301	91
237	302	22
238	201	28
238	202	116
238	301	64
238	302	21
239	201	30
239	202	14
239	302	19
240	201	145
240	202	192
240	304	234
240	401	60
240	402	169
240	501	265
241	201	140
241	202	143
241	301	105
241	302	120
241	304	53
241	401	60
242	201	297
242	202	429
242	301	248
242	302	360
242	304	357
242	401	460
242	402	267
242	404	619
242	501	515
242	504	676
243	201	1174
243	202	841
243	301	256
243	302	321
243	304	250
243	401	412
243	402	340
243	404	598
243	501	464
243	504	685
244	201	1689
244	202	1543
244	301	402
244	302	477
244	304	390
244	401	516
244	402	523
244	404	882
244	501	641
244	504	1104
245	201	1178
245	202	900
245	301	224
245	302	296
245	304	344
245	401	321
245	402	346
245	404	681
245	501	302
245	504	776
246	201	2060
246	202	1767
246	301	315
246	302	479
246	304	540
246	401	544
246	402	498
246	404	1047
246	501	718
246	504	1299
247	201	1542
247	202	1936
247	301	261
247	302	693
247	304	726
247	401	229
247	402	654
247	404	1001
247	501	756
247	504	530
248	201	37
248	202	120
248	301	71
248	302	30
249	201	27
249	202	118
249	301	78
249	302	20
250	201	1748
250	202	2121
250	301	403
250	302	325
250	304	453
250	401	302
250	402	457
250	404	1064
250	501	791
250	504	1183
251	201	24
251	202	98
251	301	54
251	302	21
252	201	31
252	202	89
252	301	55
252	302	37
253	201	633
253	202	366
253	301	372
253	302	307
253	304	221
253	401	488
253	402	226
253	404	970
253	501	382
253	504	652
254	201	105
254	202	190
254	301	88
254	302	102
254	304	58
254	401	58
255	201	972
255	202	837
255	301	269
255	302	393
255	304	293
255	401	217
255	402	308
255	404	672
255	501	558
255	504	722
256	201	141
256	202	112
256	304	214
256	401	91
256	402	177
256	501	262
257	201	621
257	202	784
257	301	267
257	302	230
257	304	436
257	401	203
257	402	326
257	404	953
257	501	368
257	504	755
258	201	25
258	202	12
258	302	16
259	201	22
259	202	101
259	301	66
259	302	34
260	201	1727
260	202	1490
260	301	376
260	302	414
260	304	399
260	401	344
260	402	582
260	404	979
260	501	795
260	504	1040
261	201	1837
261	202	2200
261	301	456
261	302	368
261	304	421
261	401	493
261	402	518
261	404	928
261	501	764
261	504	1237
262	201	362
262	202	261
262	301	372
262	302	279
262	304	306
262	401	296
262	402	375
262	404	692
262	501	468
262	504	678
263	201	833
263	202	958
263	301	369
263	302	281
263	304	373
263	401	213
263	402	244
263	404	624
263	501	531
263	504	613
264	201	251
264	202	419
264	301	541
264	302	589
264	304	532
264	401	435
264	402	817
264	404	804
264	501	1015
264	504	993
265	201	122
265	202	135
265	304	250
265	401	94
265	402	175
265	501	248
266	201	895
266	202	893
266	301	210
266	302	305
266	304	592
266	401	205
266	402	225
266	404	1051
266	501	646
266	504	1109
267	201	792
267	202	988
267	301	240
267	302	253
267	304	459
267	401	434
267	402	359
267	404	806
267	501	363
267	504	533
268	201	106
268	202	164
268	304	280
268	401	61
268	402	151
268	501	225
269	201	1752
269	202	1575
269	301	359
269	302	316
269	304	414
269	401	470
269	402	510
269	404	887
269	501	638
269	504	1221
270	201	35
270	202	122
270	301	76
270	302	38
271	201	1735
271	202	2080
271	301	415
271	302	451
271	304	295
271	401	297
271	402	732
271	404	714
271	501	524
271	504	1121
272	201	23
272	202	10
272	302	11
273	201	183
273	202	196
273	301	70
273	302	128
273	304	50
273	401	49
274	201	677
274	202	1062
274	301	250
274	302	317
274	304	226
274	401	313
274	402	215
274	404	933
274	501	419
274	504	555
275	201	38
275	202	89
275	301	80
275	302	22
276	201	192
276	202	152
276	301	101
276	302	138
276	304	52
276	401	48
277	201	454
277	202	960
277	301	234
277	302	310
277	304	480
277	401	286
277	402	362
277	404	507
277	501	549
277	504	539
278	201	210
278	202	1092
278	301	354
278	302	360
278	304	685
278	401	541
278	402	823
278	404	1342
278	501	413
278	504	615
279	201	1431
279	202	606
279	301	680
279	302	605
279	304	240
279	401	522
279	402	820
279	404	1147
279	501	406
279	504	1051
280	201	423
280	202	255
280	301	266
280	302	544
280	304	647
280	401	318
280	402	873
280	404	1357
280	501	528
280	504	899
281	201	6494
281	202	6855
281	301	922
281	302	831
281	304	1312
281	401	1267
281	402	610
281	404	1495
281	501	1203
281	504	2284
282	201	165
282	202	145
282	301	71
282	302	124
282	304	44
282	401	47
283	201	877
283	202	885
283	301	299
283	302	383
283	304	295
283	401	316
283	402	266
283	404	795
283	501	555
283	504	688
284	201	36
284	202	115
284	301	64
284	302	34
285	201	450
285	202	627
285	301	228
285	302	358
285	304	312
285	401	326
285	402	310
285	404	951
285	501	541
285	504	500
286	201	1042
286	202	385
286	301	439
286	302	622
286	304	268
286	401	467
286	402	389
286	404	1086
286	501	645
286	504	507
287	201	163
287	202	166
287	301	81
287	302	137
287	304	41
287	401	37
288	201	250
288	202	432
288	301	476
288	302	596
288	304	286
288	401	472
288	402	577
288	404	1149
288	501	361
288	504	975
289	201	148
289	202	164
289	304	270
289	401	70
289	402	233
289	501	292
290	201	184
290	202	160
290	301	97
290	302	175
290	304	34
290	401	54
291	201	1475
291	202	1870
291	301	436
291	302	428
291	304	414
291	401	507
291	402	511
291	404	869
291	501	560
291	504	1179
292	201	1874
292	202	2186
292	301	498
292	302	478
292	304	386
292	401	301
292	402	426
292	404	990
292	501	662
292	504	1212
293	201	32
293	202	12
293	302	14
294	201	21
294	202	102
294	301	75
294	302	34
295	201	986
295	202	430
295	301	337
295	302	273
295	304	456
295	401	354
295	402	288
295	404	621
295	501	475
295	504	761
296	201	130
296	202	187
296	301	82
296	302	170
296	304	33
296	401	41
297	201	359
297	202	448
297	301	249
297	302	358
297	304	480
297	401	258
297	402	344
297	404	788
297	501	504
297	504	578
298	201	7121
298	202	5721
298	301	851
298	302	890
298	304	1416
298	401	1027
298	402	637
298	404	1121
298	501	1562
298	504	2754
299	201	28
299	202	116
299	301	81
299	302	25
300	201	35
300	202	18
300	302	16
301	201	231
301	202	241
301	301	386
301	302	328
301	304	318
301	401	341
301	402	225
301	404	743
301	501	468
301	504	621
302	201	1846
302	202	1638
302	301	434
302	302	357
302	304	580
302	401	366
302	402	405
302	404	1094
302	501	747
302	504	1231
303	201	254
303	202	261
303	301	251
303	302	286
303	304	499
303	401	336
303	402	334
303	404	570
303	501	528
303	504	788
304	201	161
304	202	179
304	304	282
304	401	81
304	402	169
304	501	251
305	201	161
305	202	177
305	301	100
305	302	171
305	304	46
305	401	58
306	201	5272
306	202	6198
306	301	881
306	302	983
306	304	1295
306	401	1226
306	402	638
306	404	1160
306	501	1698
306	504	2046
307	201	31
307	202	97
307	301	87
307	302	33
308	201	1060
308	202	1726
308	301	605
308	302	335
308	304	647
308	401	678
308	402	350
308	404	758
308	501	678
308	504	1157
309	201	129
309	202	143
309	301	72
309	302	114
309	304	35
309	401	37
310	201	1123
310	202	508
310	301	277
310	302	369
310	304	395
310	401	409
310	402	214
310	404	736
310	501	506
310	504	505
311	201	38
311	202	120
311	301	89
311	302	38
312	201	29
312	202	84
312	301	71
312	302	30
313	201	131
313	202	159
313	301	88
313	302	145
313	304	36
313	401	57
314	201	128
314	202	149
314	304	268
314	401	57
314	402	208
314	501	270
315	201	6313
315	202	5328
315	301	801
315	302	988
315	304	1247
315	401	1179
315	402	780
315	404	1311
315	501	1619
315	504	2128
316	201	20
316	202	103
316	301	79
316	302	22
317	201	1477
317	202	1398
317	301	305
317	302	318
317	304	587
317	401	583
317	402	573
317	404	906
317	501	709
317	504	1151
318	201	707
318	202	1105
318	301	643
318	302	309
318	304	301
318	401	330
318	402	571
318	404	880
318	501	513
318	504	829
319	201	299
319	202	712
319	301	252
319	302	307
319	304	495
319	401	277
319	402	360
319	404	538
319	501	402
319	504	757
320	201	178
320	202	158
320	304	284
320	401	61
320	402	166
320	501	259
321	201	6172
321	202	5843
321	301	887
321	302	923
321	304	1486
321	401	1015
321	402	662
321	404	1302
321	501	1485
321	504	2946
322	201	244
322	202	660
322	301	322
322	302	375
322	304	290
322	401	285
322	402	329
322	404	997
322	501	399
322	504	735
323	201	127
323	202	133
323	301	89
323	302	176
323	304	40
323	401	39
324	201	869
324	202	704
324	301	340
324	302	372
324	304	406
324	401	341
324	402	371
324	404	585
324	501	490
324	504	545
325	201	190
325	202	169
325	304	262
325	401	58
325	402	158
325	501	231
326	201	687
326	202	777
326	301	251
326	302	336
326	304	391
326	401	408
326	402	351
326	404	605
326	501	473
326	504	732
327	201	1023
327	202	512
327	301	317
327	302	283
327	304	493
327	401	442
327	402	352
327	404	727
327	501	592
327	504	549
328	201	349
328	202	1201
328	301	392
328	302	239
328	304	668
328	401	408
328	402	909
328	404	803
328	501	648
328	504	573
329	201	2198
329	202	1997
329	301	223
329	302	521
329	304	450
329	401	339
329	402	255
329	404	797
329	501	827
329	504	975
330	201	136
330	202	188
330	304	279
330	401	83
330	402	195
330	501	255
331	201	190
331	202	140
331	304	288
331	401	79
331	402	197
331	501	289
332	201	1453
332	202	1668
332	301	359
332	302	592
332	304	476
332	401	210
332	402	636
332	404	1333
332	501	969
332	504	620
333	201	199
333	202	171
333	301	65
333	302	115
333	304	56
333	401	42
334	201	235
334	202	1107
334	301	337
334	302	272
334	304	250
334	401	388
334	402	365
334	404	776
334	501	514
334	504	572
335	201	1130
335	202	742
335	301	231
335	302	262
335	304	282
335	401	276
335	402	210
335	404	519
335	501	514
335	504	716
336	201	1882
336	202	1368
336	301	466
336	302	370
336	304	430
336	401	454
336	402	520
336	404	966
336	501	679
336	504	1054
337	201	6488
337	202	6129
337	301	832
337	302	908
337	304	1308
337	401	1195
337	402	726
337	404	1280
337	501	1641
337	504	2248
338	201	5342
338	202	5509
338	301	892
338	302	904
338	304	1438
338	401	1173
338	402	685
338	404	1160
338	501	1507
338	504	2829
339	201	591
339	202	433
339	301	286
339	302	304
339	304	273
339	401	436
339	402	390
339	404	870
339	501	321
339	504	746
340	201	153
340	202	179
340	301	72
340	302	129
340	304	46
340	401	60
341	201	164
341	202	102
341	304	249
341	401	75
341	402	172
341	501	205
342	201	117
342	202	187
342	304	287
342	401	60
342	402	233
342	501	255
343	201	21
343	202	123
343	301	54
343	302	38
344	201	710
344	202	385
344	301	388
344	302	386
344	304	456
344	401	413
344	402	206
344	404	988
344	501	353
344	504	758
345	201	2013
345	202	1833
345	301	448
345	302	346
345	304	464
345	401	495
345	402	548
345	404	734
345	501	657
345	504	1114
346	201	232
346	202	296
346	301	222
346	302	256
346	304	213
346	401	286
346	402	262
346	404	784
346	501	343
346	504	696
347	201	192
347	202	173
347	301	106
347	302	142
347	304	54
347	401	55
348	201	548
348	202	375
348	301	303
348	302	273
348	304	398
348	401	291
348	402	243
348	404	806
348	501	569
348	504	736
349	201	23
349	202	109
349	301	95
349	302	28
350	201	146
350	202	117
350	304	272
350	401	70
350	402	196
350	501	236
351	201	971
351	202	430
351	301	200
351	302	308
351	304	443
351	401	439
351	402	209
351	404	797
351	501	436
351	504	565
352	201	104
352	202	168
352	301	83
352	302	140
352	304	42
352	401	31
353	201	284
353	202	844
353	301	306
353	302	340
353	304	235
353	401	229
353	402	212
353	404	635
353	501	507
353	504	646
354	201	36
354	202	15
354	302	19
355	201	185
355	202	169
355	304	205
355	401	72
355	402	170
355	501	269
356	201	32
356	202	19
356	302	20
357	201	25
357	202	91
357	301	61
357	302	23
358	201	1669
358	202	2200
358	301	228
358	302	658
358	304	449
358	401	339
358	402	364
358	404	1066
358	501	868
358	504	1115
359	201	156
359	202	139
359	301	95
359	302	176
359	304	41
359	401	57
360	201	1817
360	202	1784
360	301	348
360	302	439
360	304	503
360	401	340
360	402	427
360	404	843
360	501	688
360	504	1141
361	201	168
361	202	181
361	304	270
361	401	69
361	402	158
361	501	284
362	201	914
362	202	350
362	301	316
362	302	318
362	304	393
362	401	201
362	402	380
362	404	793
362	501	391
362	504	656
363	201	184
363	202	146
363	304	247
363	401	100
363	402	189
363	501	247
364	201	1849
364	202	845
364	301	549
364	302	645
364	304	307
364	401	565
364	402	976
364	404	622
364	501	666
364	504	832
365	201	2059
365	202	1948
365	301	300
365	302	440
365	304	363
365	401	360
365	402	587
365	404	1071
365	501	662
365	504	1023
366	201	6315
366	202	5779
366	301	953
366	302	931
366	304	1316
366	401	1090
366	402	602
366	404	1284
366	501	1846
366	504	2956
367	201	1644
367	202	1741
367	301	599
367	302	462
367	304	502
367	401	617
367	402	598
367	404	603
367	501	941
367	504	543
368	201	125
368	202	174
368	301	79
368	302	160
368	304	46
368	401	47
369	201	1878
369	202	1570
369	301	404
369	302	619
369	304	480
369	401	631
369	402	865
369	404	683
369	501	514
369	504	816
370	201	1571
370	202	1920
370	301	417
370	302	411
370	304	502
370	401	671
370	402	565
370	404	1480
370	501	452
370	504	893
371	201	130
371	202	142
371	301	85
371	302	192
371	304	41
371	401	41
372	201	1963
372	202	1900
372	301	496
372	302	385
372	304	404
372	401	432
372	402	437
372	404	1110
372	501	509
372	504	1272
373	201	970
373	202	2045
373	301	309
373	302	207
373	304	553
373	401	262
373	402	847
373	404	732
373	501	481
373	504	852
374	201	121
374	202	125
374	301	91
374	302	121
374	304	35
374	401	60
375	201	35
375	202	128
375	301	80
375	302	28
376	201	134
376	202	198
376	304	224
376	401	84
376	402	225
376	501	282
377	201	468
377	202	1823
377	301	345
377	302	460
377	304	485
377	401	659
377	402	508
377	404	1130
377	501	618
377	504	954
378	201	7031
378	202	6580
378	301	902
378	302	974
378	304	1403
378	401	1196
378	402	787
378	404	1004
378	501	1298
378	504	2513
379	201	161
379	202	147
379	301	87
379	302	106
379	304	46
379	401	52
380	201	1503
380	202	1828
380	301	625
380	302	471
380	304	359
380	401	632
380	402	858
380	404	694
380	501	849
380	504	752
381	201	31
381	202	17
381	302	19
382	201	1642
382	202	1840
382	301	481
382	302	374
382	304	577
382	401	394
382	402	401
382	404	795
382	501	589
382	504	1014
383	201	34
383	202	105
383	301	100
383	302	24
384	201	157
384	202	153
384	304	246
384	401	96
384	402	195
384	501	226
385	201	109
385	202	101
385	301	72
385	302	150
385	304	39
385	401	39
386	201	101
386	202	146
386	304	229
386	401	94
386	402	224
386	501	268
387	201	135
387	202	199
387	301	76
387	302	184
387	304	42
387	401	54
388	201	137
388	202	168
388	304	233
388	401	66
388	402	213
388	501	294
389	201	23
389	202	82
389	301	68
389	302	24
390	201	36
390	202	130
390	301	99
390	302	24
391	201	1835
391	202	2180
391	301	346
391	302	410
391	304	584
391	401	537
391	402	468
391	404	749
391	501	662
391	504	1173
392	201	549
392	202	416
392	301	328
392	302	362
392	304	240
392	401	459
392	402	226
392	404	794
392	501	564
392	504	747
393	201	1365
393	202	2000
393	301	334
393	302	303
393	304	425
393	401	406
393	402	533
393	404	1083
393	501	585
393	504	1141
394	201	171
394	202	103
394	301	89
394	302	175
394	304	48
394	401	50
395	201	189
395	202	169
395	304	259
395	401	75
395	402	232
395	501	255
396	201	117
396	202	180
396	304	265
396	401	92
396	402	152
396	501	216
397	201	821
397	202	441
397	301	337
397	302	269
397	304	292
397	401	276
397	402	200
397	404	511
397	501	422
397	504	554
398	201	191
398	202	124
398	301	93
398	302	163
398	304	31
398	401	36
399	201	1160
399	202	489
399	301	202
399	302	257
399	304	359
399	401	336
399	402	256
399	404	990
399	501	521
399	504	778
400	201	308
400	202	361
400	301	244
400	302	333
400	304	234
400	401	356
400	402	326
400	404	968
400	501	491
400	504	675
401	201	29
401	202	114
401	301	98
401	302	24
402	201	27
402	202	16
402	302	14
403	201	1698
403	202	1628
403	301	411
403	302	459
403	304	521
403	401	517
403	402	530
403	404	716
403	501	656
403	504	1123
404	201	676
404	202	515
404	301	299
404	302	361
404	304	488
404	401	488
404	402	305
404	404	743
404	501	492
404	504	701
405	201	6883
405	202	5283
405	301	810
405	302	895
405	304	1238
405	401	1197
405	402	608
405	404	1485
405	501	1358
405	504	2370
406	201	21
406	202	119
406	301	67
406	302	27
407	201	971
407	202	844
407	301	384
407	302	257
407	304	327
407	401	446
407	402	296
407	404	749
407	501	573
407	504	551
408	201	37
408	202	88
408	301	56
408	302	40
409	201	117
409	202	186
409	301	83
409	302	193
409	304	41
409	401	41
410	201	111
410	202	163
410	301	93
410	302	172
410	304	52
410	401	52
411	201	6957
411	202	6675
411	301	965
411	302	980
411	304	1301
411	401	1147
411	402	780
411	404	1182
411	501	1746
411	504	2012
412	201	5876
412	202	5213
412	301	919
412	302	907
412	304	1427
412	401	1290
412	402	659
412	404	1427
412	501	1898
412	504	2192
413	201	1559
413	202	1216
413	301	442
413	302	338
413	304	359
413	401	600
413	402	531
413	404	702
413	501	713
413	504	1217
414	201	21
414	202	92
414	301	60
414	302	26
415	201	22
415	202	126
415	301	72
415	302	29
416	201	6975
416	202	5991
416	301	818
416	302	910
416	304	1489
416	401	1006
416	402	767
416	404	1277
416	501	1429
416	504	2558
417	201	40
417	202	10
417	302	15
418	201	155
418	202	188
418	301	67
418	302	131
418	304	49
418	401	48
419	201	198
419	202	112
419	301	108
419	302	133
419	304	49
419	401	45
420	201	202
420	202	1023
420	301	310
420	302	272
420	304	439
420	401	431
420	402	245
420	404	958
420	501	343
420	504	628
421	201	537
421	202	771
421	301	304
421	302	261
421	304	440
421	401	381
421	402	251
421	404	856
421	501	476
421	504	775
422	201	1282
422	202	1544
422	301	456
422	302	315
422	304	344
422	401	517
422	402	538
422	404	782
422	501	746
422	504	1218
423	201	146
423	202	103
423	301	81
423	302	126
423	304	32
423	401	38
424	201	111
424	202	168
424	304	263
424	401	55
424	402	235
424	501	227
425	201	32
425	202	88
425	301	76
425	302	33
426	201	154
426	202	117
426	304	236
426	401	77
426	402	166
426	501	256
427	201	288
427	202	814
427	301	366
427	302	255
427	304	304
427	401	361
427	402	245
427	404	813
427	501	546
427	504	677
428	201	1621
428	202	1297
428	301	446
428	302	495
428	304	387
428	401	367
428	402	591
428	404	821
428	501	600
428	504	1244
429	201	1206
429	202	1566
429	301	352
429	302	464
429	304	437
429	401	430
429	402	555
429	404	1051
429	501	613
429	504	1018
430	201	889
430	202	238
430	301	287
430	302	288
430	304	434
430	401	382
430	402	384
430	404	543
430	501	574
430	504	512
431	201	27
431	202	130
431	301	81
431	302	21
432	201	138
432	202	136
432	301	69
432	302	144
432	304	53
432	401	33
433	201	21
433	202	115
433	301	71
433	302	20
434	201	1415
434	202	2080
434	301	500
434	302	364
434	304	673
434	401	428
434	402	331
434	404	1036
434	501	370
434	504	1135
435	201	1200
435	202	745
435	301	517
435	302	629
435	304	464
435	401	236
435	402	516
435	404	541
435	501	777
435	504	785
436	201	2103
436	202	1922
436	301	456
436	302	479
436	304	455
436	401	381
436	402	425
436	404	1068
436	501	517
436	504	1129
437	201	169
437	202	148
437	304	262
437	401	55
437	402	170
437	501	231
438	201	2175
438	202	1522
438	301	415
438	302	461
438	304	359
438	401	392
438	402	466
438	404	820
438	501	756
438	504	1006
439	201	25
439	202	101
439	301	66
439	302	33
440	201	189
440	202	183
440	301	96
440	302	161
440	304	41
440	401	32
441	201	105
441	202	114
441	301	83
441	302	157
441	304	32
441	401	59
442	201	6933
442	202	6669
442	301	851
442	302	965
442	304	1314
442	401	1098
442	402	788
442	404	1032
442	501	1971
442	504	2408
443	201	506
443	202	619
443	301	274
443	302	269
443	304	419
443	401	356
443	402	310
443	404	775
443	501	376
443	504	633
444	201	5984
444	202	6941
444	301	872
444	302	858
444	304	1277
444	401	1214
444	402	690
444	404	1231
444	501	1268
444	504	2455
445	201	24
445	202	127
445	301	68
445	302	25
446	201	193
446	202	105
446	304	204
446	401	54
446	402	181
446	501	287
447	201	37
447	202	86
447	301	79
447	302	40
448	201	761
448	202	818
448	301	391
448	302	327
448	304	405
448	401	397
448	402	279
448	404	532
448	501	365
448	504	641
449	201	30
449	202	18
449	302	18
450	201	1838
450	202	1980
450	301	482
450	302	342
450	304	372
450	401	393
450	402	426
450	404	1075
450	501	567
450	504	1014
451	201	1091
451	202	885
451	301	247
451	302	300
451	304	353
451	401	464
451	402	319
451	404	977
451	501	583
451	504	797
452	201	29
452	202	16
452	302	14
453	201	1890
453	202	563
453	301	522
453	302	217
453	304	284
453	401	659
453	402	304
453	404	989
453	501	957
453	504	582
454	201	134
454	202	153
454	304	214
454	401	81
454	402	242
454	501	244
455	201	1956
455	202	2029
455	301	399
455	302	490
455	304	556
455	401	430
455	402	408
455	404	934
455	501	567
455	504	1206
456	201	149
456	202	176
456	301	105
456	302	173
456	304	46
456	401	51
457	201	351
457	202	510
457	301	281
457	302	365
457	304	404
457	401	287
457	402	336
457	404	619
457	501	410
457	504	639
458	201	622
458	202	206
458	301	255
458	302	213
458	304	329
458	401	489
458	402	357
458	404	915
458	501	327
458	504	527
459	201	1465
459	202	1819
459	301	326
459	302	492
459	304	549
459	401	411
459	402	510
459	404	726
459	501	621
459	504	1010
460	201	1898
460	202	2016
460	301	623
460	302	247
460	304	482
460	401	271
460	402	373
460	404	1081
460	501	835
460	504	1100
461	201	817
461	202	264
461	301	307
461	302	280
461	304	407
461	401	461
461	402	387
461	404	922
461	501	337
461	504	550
462	201	1874
462	202	2061
462	301	414
462	302	492
462	304	573
462	401	352
462	402	595
462	404	916
462	501	666
462	504	1052
463	201	503
463	202	2073
463	301	401
463	302	354
463	304	268
463	401	579
463	402	798
463	404	678
463	501	570
463	504	638
464	201	875
464	202	507
464	301	340
464	302	391
464	304	314
464	401	482
464	402	397
464	404	623
464	501	526
464	504	537
465	201	21
465	202	98
465	301	80
465	302	32
466	201	26
466	202	109
466	301	59
466	302	33
467	201	271
467	202	1001
467	301	330
467	302	321
467	304	388
467	401	480
467	402	230
467	404	917
467	501	531
467	504	511
468	201	179
468	202	149
468	304	228
468	401	97
468	402	152
468	501	209
469	201	570
469	202	234
469	301	254
469	302	312
469	304	275
469	401	457
469	402	203
469	404	914
469	501	463
469	504	559
470	201	145
470	202	140
470	304	252
470	401	71
470	402	167
470	501	297
471	201	180
471	202	162
471	301	94
471	302	175
471	304	58
471	401	48
472	201	728
472	202	830
472	301	228
472	302	332
472	304	494
472	401	346
472	402	361
472	404	824
472	501	345
472	504	751
473	201	23
473	202	15
473	302	12
474	201	1928
474	202	1619
474	301	376
474	302	446
474	304	345
474	401	572
474	402	571
474	404	781
474	501	653
474	504	1010
475	201	21
475	202	113
475	301	73
475	302	35
476	201	141
476	202	170
476	301	82
476	302	162
476	304	56
476	401	40
477	201	1076
477	202	334
477	301	259
477	302	303
477	304	442
477	401	240
477	402	251
477	404	678
477	501	577
477	504	652
478	201	202
478	202	2062
478	301	333
478	302	514
478	304	635
478	401	580
478	402	511
478	404	854
478	501	351
478	504	718
479	201	1849
479	202	1887
479	301	344
479	302	482
479	304	344
479	401	454
479	402	509
479	404	901
479	501	544
479	504	1057
480	201	1986
480	202	1641
480	301	435
480	302	382
480	304	363
480	401	412
480	402	581
480	404	737
480	501	738
480	504	1191
481	201	1830
481	202	1953
481	301	457
481	302	312
481	304	362
481	401	509
481	402	435
481	404	901
481	501	592
481	504	1202
482	201	1223
482	202	982
482	301	258
482	302	580
482	304	512
482	401	514
482	402	307
482	404	902
482	501	420
482	504	946
483	201	637
483	202	736
483	301	284
483	302	277
483	304	218
483	401	306
483	402	363
483	404	852
483	501	407
483	504	564
484	201	378
484	202	676
484	301	265
484	302	201
484	304	438
484	401	479
484	402	266
484	404	521
484	501	420
484	504	800
485	201	21
485	202	127
485	301	65
485	302	31
486	201	108
486	202	124
486	301	105
486	302	158
486	304	54
486	401	54
487	201	1207
487	202	1604
487	301	450
487	302	432
487	304	489
487	401	323
487	402	586
487	404	850
487	501	553
487	504	1199
488	201	112
488	202	134
488	301	108
488	302	150
488	304	42
488	401	60
489	201	20
489	202	122
489	301	67
489	302	24
490	201	175
490	202	157
490	304	297
490	401	73
490	402	164
490	501	262
491	201	265
491	202	768
491	301	202
491	302	384
491	304	239
491	401	241
491	402	355
491	404	505
491	501	408
491	504	737
492	201	2149
492	202	2012
492	301	379
492	302	302
492	304	303
492	401	462
492	402	536
492	404	816
492	501	710
492	504	1021
493	201	346
493	202	1284
493	301	354
493	302	469
493	304	312
493	401	223
493	402	662
493	404	1417
493	501	995
493	504	871
494	201	933
494	202	769
494	301	205
494	302	346
494	304	348
494	401	482
494	402	309
494	404	901
494	501	404
494	504	730
495	201	26
495	202	112
495	301	79
495	302	32
496	201	103
496	202	121
496	301	82
496	302	135
496	304	43
496	401	36
497	201	1693
497	202	392
497	301	420
497	302	532
497	304	588
497	401	641
497	402	940
497	404	1311
497	501	417
497	504	523
498	201	172
498	202	164
498	301	109
498	302	181
498	304	57
498	401	33
499	201	31
499	202	107
499	301	66
499	302	22
500	201	2081
500	202	1800
500	301	236
500	302	496
500	304	517
500	401	241
500	402	534
500	404	1188
500	501	846
500	504	517
501	201	1518
501	202	1974
501	301	652
501	302	414
501	304	708
501	401	447
501	402	283
501	404	1126
501	501	937
501	504	867
502	201	1782
502	202	1437
502	301	369
502	302	388
502	304	336
502	401	599
502	402	550
502	404	842
502	501	769
502	504	1234
503	201	115
503	202	194
503	304	201
503	401	85
503	402	183
503	501	242
504	201	111
504	202	189
504	301	72
504	302	122
504	304	41
504	401	50
505	201	1009
505	202	1094
505	301	205
505	302	385
505	304	469
505	401	381
505	402	398
505	404	655
505	501	519
505	504	768
506	201	40
506	202	87
506	301	64
506	302	35
507	201	1078
507	202	1004
507	301	298
507	302	343
507	304	332
507	401	322
507	402	268
507	404	920
507	501	361
507	504	628
508	201	1080
508	202	250
508	301	367
508	302	270
508	304	433
508	401	399
508	402	206
508	404	506
508	501	435
508	504	698
509	201	32
509	202	13
509	302	14
510	201	359
510	202	463
510	301	245
510	302	385
510	304	244
510	401	204
510	402	329
510	404	889
510	501	378
510	504	569
511	201	487
511	202	400
511	301	311
511	302	321
511	304	316
511	401	286
511	402	330
511	404	659
511	501	536
511	504	761
512	201	157
512	202	112
512	301	82
512	302	149
512	304	41
512	401	40
513	201	1579
513	202	2067
513	301	318
513	302	455
513	304	458
513	401	456
513	402	511
513	404	908
513	501	645
513	504	1252
514	201	37
514	202	14
514	302	15
515	201	124
515	202	105
515	301	103
515	302	153
515	304	56
515	401	49
516	201	1422
516	202	2003
516	301	311
516	302	453
516	304	573
516	401	541
516	402	515
516	404	751
516	501	640
516	504	1122
517	201	470
517	202	372
517	301	633
517	302	206
517	304	393
517	401	505
517	402	893
517	404	722
517	501	430
517	504	1187
518	201	183
518	202	157
518	301	61
518	302	131
518	304	33
518	401	56
519	201	687
519	202	1192
519	301	350
519	302	205
519	304	227
519	401	385
519	402	316
519	404	674
519	501	344
519	504	738
520	201	173
520	202	173
520	304	221
520	401	65
520	402	196
520	501	201
521	201	28
521	202	90
521	301	64
521	302	28
522	201	34
522	202	124
522	301	61
522	302	37
523	201	629
523	202	1021
523	301	312
523	302	282
523	304	372
523	401	227
523	402	385
523	404	858
523	501	382
523	504	604
524	201	21
524	202	110
524	301	80
524	302	37
525	201	1345
525	202	1440
525	301	475
525	302	387
525	304	306
525	401	420
525	402	544
525	404	768
525	501	501
525	504	1055
526	201	1688
526	202	1362
526	301	342
526	302	336
526	304	532
526	401	410
526	402	517
526	404	766
526	501	718
526	504	1123
527	201	22
527	202	107
527	301	73
527	302	34
528	201	6385
528	202	6614
528	301	909
528	302	836
528	304	1307
528	401	1006
528	402	716
528	404	1068
528	501	1932
528	504	2014
529	201	268
529	202	1088
529	301	393
529	302	389
529	304	275
529	401	212
529	402	382
529	404	524
529	501	374
529	504	610
530	201	1170
530	202	713
530	301	262
530	302	332
530	304	495
530	401	258
530	402	258
530	404	541
530	501	394
530	504	601
531	201	430
531	202	309
531	301	353
531	302	381
531	304	293
531	401	380
531	402	328
531	404	927
531	501	356
531	504	543
532	201	5964
532	202	6452
532	301	874
532	302	851
532	304	1461
532	401	1005
532	402	604
532	404	1089
532	501	1553
532	504	2927
533	201	980
533	202	458
533	301	318
533	302	239
533	304	287
533	401	269
533	402	397
533	404	952
533	501	510
533	504	500
534	201	1215
534	202	1649
534	301	276
534	302	531
534	304	259
534	401	386
534	402	671
534	404	958
534	501	554
534	504	1106
535	201	214
535	202	736
535	301	545
535	302	584
535	304	293
535	401	571
535	402	295
535	404	870
535	501	898
535	504	528
536	201	39
536	202	123
536	301	84
536	302	30
537	201	164
537	202	193
537	304	252
537	401	69
537	402	201
537	501	243
538	201	1902
538	202	1705
538	301	360
538	302	446
538	304	491
538	401	413
538	402	532
538	404	904
538	501	786
538	504	1064
539	201	450
539	202	786
539	301	225
539	302	254
539	304	224
539	401	435
539	402	214
539	404	994
539	501	575
539	504	696
540	201	31
540	202	125
540	301	66
540	302	33
541	201	599
541	202	366
541	301	341
541	302	369
541	304	328
541	401	321
541	402	312
541	404	509
541	501	341
541	504	677
542	201	192
542	202	147
542	304	260
542	401	87
542	402	173
542	501	205
543	201	38
543	202	12
543	302	13
544	201	166
544	202	104
544	304	215
544	401	88
544	402	185
544	501	286
545	201	1554
545	202	1376
545	301	353
545	302	437
545	304	429
545	401	510
545	402	408
545	404	1125
545	501	767
545	504	1089
546	201	5241
546	202	5232
546	301	982
546	302	931
546	304	1483
546	401	1234
546	402	651
546	404	1073
546	501	1652
546	504	2226
547	201	1026
547	202	481
547	301	388
547	302	203
547	304	462
547	401	490
547	402	203
547	404	994
547	501	517
547	504	614
548	201	31
548	202	119
548	301	65
548	302	39
549	201	38
549	202	109
549	301	60
549	302	35
550	201	252
550	202	844
550	301	315
550	302	217
550	304	428
550	401	410
550	402	353
550	404	858
550	501	493
550	504	594
551	201	121
551	202	139
551	304	266
551	401	58
551	402	173
551	501	245
552	201	276
552	202	600
552	301	208
552	302	382
552	304	436
552	401	364
552	402	342
552	404	890
552	501	381
552	504	792
553	201	774
553	202	804
553	301	236
553	302	317
553	304	415
553	401	485
553	402	357
553	404	688
553	501	448
553	504	722
554	201	1021
554	202	604
554	301	318
554	302	351
554	304	472
554	401	418
554	402	380
554	404	648
554	501	435
554	504	677
555	201	1846
555	202	391
555	301	326
555	302	463
555	304	731
555	401	561
555	402	330
555	404	565
555	501	946
555	504	996
556	201	5572
556	202	6359
556	301	858
556	302	985
556	304	1353
556	401	1256
556	402	612
556	404	1430
556	501	1550
556	504	2913
557	201	1381
557	202	1610
557	301	432
557	302	495
557	304	429
557	401	316
557	402	433
557	404	906
557	501	624
557	504	1149
558	201	1108
558	202	759
558	301	250
558	302	291
558	304	350
558	401	312
558	402	284
558	404	836
558	501	595
558	504	570
559	201	150
559	202	123
559	301	78
559	302	143
559	304	60
559	401	54
560	201	522
560	202	1168
560	301	342
560	302	309
560	304	454
560	401	326
560	402	259
560	404	581
560	501	464
560	504	768
561	201	5824
561	202	5616
561	301	997
561	302	904
561	304	1447
561	401	1070
561	402	793
561	404	1406
561	501	1488
561	504	2523
562	201	25
562	202	125
562	301	56
562	302	37
563	201	185
563	202	132
563	301	90
563	302	184
563	304	39
563	401	54
564	201	6676
564	202	5855
564	301	950
564	302	976
564	304	1362
564	401	1158
564	402	763
564	404	1027
564	501	1330
564	504	2992
565	201	179
565	202	116
565	304	211
565	401	94
565	402	188
565	501	275
566	201	1934
566	202	1848
566	301	483
566	302	490
566	304	495
566	401	420
566	402	503
566	404	709
566	501	779
566	504	1069
567	201	1380
567	202	1391
567	301	361
567	302	418
567	304	474
567	401	564
567	402	523
567	404	1155
567	501	773
567	504	1281
568	201	1867
568	202	1423
568	301	497
568	302	314
568	304	417
568	401	401
568	402	530
568	404	1020
568	501	794
568	504	1074
569	201	106
569	202	155
569	304	249
569	401	83
569	402	152
569	501	228
570	201	298
570	202	1073
570	301	219
570	302	340
570	304	309
570	401	409
570	402	353
570	404	734
570	501	369
570	504	694
571	201	1566
571	202	1761
571	301	405
571	302	324
571	304	369
571	401	379
571	402	575
571	404	1053
571	501	644
571	504	1102
572	201	649
572	202	456
572	301	343
572	302	244
572	304	201
572	401	461
572	402	243
572	404	757
572	501	389
572	504	783
573	201	23
573	202	126
573	301	74
573	302	25
574	201	131
574	202	178
574	301	80
574	302	137
574	304	57
574	401	46
575	201	21
575	202	100
575	301	70
575	302	37
576	201	159
576	202	138
576	301	70
576	302	119
576	304	46
576	401	51
577	201	110
577	202	145
577	304	237
577	401	53
577	402	190
577	501	207
578	201	1043
578	202	1009
578	301	229
578	302	468
578	304	471
578	401	574
578	402	809
578	404	1109
578	501	561
578	504	716
579	201	1661
579	202	2045
579	301	380
579	302	637
579	304	780
579	401	356
579	402	813
579	404	1055
579	501	400
579	504	897
580	201	1831
580	202	1390
580	301	344
580	302	499
580	304	376
580	401	347
580	402	479
580	404	831
580	501	591
580	504	1231
581	201	30
581	202	87
581	301	81
581	302	23
582	201	293
582	202	1153
582	301	242
582	302	255
582	304	294
582	401	255
582	402	294
582	404	967
582	501	593
582	504	510
583	201	34
583	202	128
583	301	70
583	302	26
584	201	30
584	202	17
584	302	15
585	201	1725
585	202	1511
585	301	480
585	302	384
585	304	568
585	401	516
585	402	465
585	404	914
585	501	724
585	504	1192
586	201	5345
586	202	6639
586	301	906
586	302	904
586	304	1366
586	401	1138
586	402	800
586	404	1387
586	501	1626
586	504	2634
587	201	110
587	202	103
587	301	87
587	302	198
587	304	48
587	401	59
588	201	23
588	202	14
588	302	14
589	201	848
589	202	1182
589	301	353
589	302	293
589	304	218
589	401	242
589	402	306
589	404	977
589	501	528
589	504	771
590	201	172
590	202	158
590	304	272
590	401	79
590	402	226
590	501	244
591	201	699
591	202	720
591	301	391
591	302	378
591	304	224
591	401	366
591	402	256
591	404	746
591	501	529
591	504	690
592	201	758
592	202	1029
592	301	327
592	302	254
592	304	257
592	401	346
592	402	371
592	404	862
592	501	463
592	504	578
593	201	121
593	202	160
593	304	223
593	401	55
593	402	151
593	501	249
594	201	1182
594	202	834
594	301	320
594	302	460
594	304	578
594	401	282
594	402	537
594	404	1401
594	501	423
594	504	553
595	201	551
595	202	1132
595	301	392
595	302	253
595	304	430
595	401	496
595	402	352
595	404	527
595	501	452
595	504	641
596	201	5702
596	202	5841
596	301	817
596	302	960
596	304	1239
596	401	1236
596	402	761
596	404	1247
596	501	1784
596	504	2904
597	201	279
597	202	1014
597	301	313
597	302	373
597	304	219
597	401	308
597	402	381
597	404	932
597	501	586
597	504	698
598	201	976
598	202	262
598	301	260
598	302	297
598	304	491
598	401	349
598	402	362
598	404	606
598	501	470
598	504	508
599	201	840
599	202	411
599	301	227
599	302	253
599	304	238
599	401	369
599	402	250
599	404	828
599	501	504
599	504	586
600	201	963
600	202	261
600	301	493
600	302	209
600	304	243
600	401	563
600	402	646
600	404	547
600	501	1092
600	504	721
601	201	185
601	202	162
601	301	67
601	302	158
601	304	40
601	401	49
602	201	2073
602	202	1505
602	301	345
602	302	419
602	304	583
602	401	550
602	402	592
602	404	1014
602	501	655
602	504	1211
603	201	712
603	202	536
603	301	383
603	302	390
603	304	347
603	401	381
603	402	255
603	404	571
603	501	588
603	504	541
604	201	6195
604	202	6629
604	301	902
604	302	898
604	304	1285
604	401	1241
604	402	626
604	404	1003
604	501	1866
604	504	2396
605	201	494
605	202	449
605	301	372
605	302	204
605	304	396
605	401	339
605	402	316
605	404	536
605	501	315
605	504	582
606	201	29
606	202	102
606	301	62
606	302	26
607	201	166
607	202	111
607	301	76
607	302	166
607	304	49
607	401	35
608	201	305
608	202	557
608	301	217
608	302	216
608	304	381
608	401	335
608	402	214
608	404	856
608	501	391
608	504	785
609	201	1981
609	202	1566
609	301	436
609	302	305
609	304	544
609	401	552
609	402	456
609	404	1047
609	501	503
609	504	1060
610	201	38
610	202	116
610	301	85
610	302	40
611	201	35
611	202	12
611	302	17
612	201	1955
612	202	2086
612	301	320
612	302	381
612	304	401
612	401	589
612	402	401
612	404	869
612	501	633
612	504	1293
613	201	1931
613	202	1382
613	301	405
613	302	435
613	304	489
613	401	309
613	402	490
613	404	1110
613	501	788
613	504	1178
614	201	1442
614	202	2014
614	301	311
614	302	331
614	304	482
614	401	393
614	402	411
614	404	1073
614	501	660
614	504	1055
615	201	102
615	202	195
615	304	225
615	401	57
615	402	203
615	501	262
616	201	34
616	202	127
616	301	89
616	302	37
617	201	1523
617	202	1164
617	301	330
617	302	267
617	304	550
617	401	454
617	402	963
617	404	1018
617	501	460
617	504	800
618	201	390
618	202	989
618	301	285
618	302	355
618	304	422
618	401	424
618	402	387
618	404	718
618	501	338
618	504	641
619	201	1339
619	202	1228
619	301	359
619	302	400
619	304	427
619	401	321
619	402	516
619	404	835
619	501	642
619	504	1048
620	201	1095
620	202	1954
620	301	591
620	302	235
620	304	443
620	401	593
620	402	812
620	404	1196
620	501	829
620	504	671
621	201	1156
621	202	509
621	301	344
621	302	308
621	304	289
621	401	400
621	402	340
621	404	803
621	501	565
621	504	709
622	201	103
622	202	118
622	304	202
622	401	70
622	402	178
622	501	245
623	201	186
623	202	111
623	301	61
623	302	141
623	304	32
623	401	50
624	201	5565
624	202	7093
624	301	841
624	302	926
624	304	1293
624	401	1118
624	402	612
624	404	1421
624	501	1630
624	504	2880
625	201	1094
625	202	706
625	301	299
625	302	347
625	304	350
625	401	394
625	402	283
625	404	596
625	501	372
625	504	624
626	201	385
626	202	691
626	301	234
626	302	216
626	304	289
626	401	337
626	402	326
626	404	517
626	501	532
626	504	508
627	201	1069
627	202	1110
627	301	235
627	302	364
627	304	416
627	401	221
627	402	319
627	404	785
627	501	456
627	504	612
628	201	27
628	202	18
628	302	15
629	201	801
629	202	706
629	301	678
629	302	525
629	304	249
629	401	521
629	402	328
629	404	750
629	501	1003
629	504	651
630	201	1171
630	202	517
630	301	256
630	302	270
630	304	288
630	401	217
630	402	370
630	404	804
630	501	426
630	504	780
631	201	173
631	202	114
631	304	235
631	401	50
631	402	200
631	501	220
632	201	121
632	202	160
632	304	290
632	401	97
632	402	247
632	501	234
633	201	1062
633	202	1010
633	301	261
633	302	221
633	304	224
633	401	393
633	402	314
633	404	550
633	501	376
633	504	577
634	201	998
634	202	758
634	301	350
634	302	294
634	304	458
634	401	282
634	402	326
634	404	584
634	501	552
634	504	711
635	201	35
635	202	17
635	302	16
636	201	1681
636	202	1699
636	301	408
636	302	432
636	304	445
636	401	404
636	402	469
636	404	770
636	501	589
636	504	1028
637	201	36
637	202	15
637	302	11
638	201	181
638	202	121
638	304	227
638	401	83
638	402	232
638	501	275
639	201	1042
639	202	795
639	301	338
639	302	292
639	304	240
639	401	398
639	402	328
639	404	850
639	501	398
639	504	618
640	201	1867
640	202	1219
640	301	699
640	302	298
640	304	568
640	401	502
640	402	839
640	404	1329
640	501	328
640	504	953
641	201	146
641	202	129
641	301	77
641	302	110
641	304	30
641	401	55
642	201	108
642	202	153
642	301	89
642	302	182
642	304	55
642	401	42
643	201	1469
643	202	2025
643	301	447
643	302	415
643	304	539
643	401	576
643	402	579
643	404	712
643	501	573
643	504	1277
644	201	474
644	202	788
644	301	617
644	302	212
644	304	221
644	401	515
644	402	951
644	404	1445
644	501	336
644	504	862
645	201	38
645	202	109
645	301	61
645	302	27
646	201	6447
646	202	5546
646	301	895
646	302	821
646	304	1448
646	401	1061
646	402	655
646	404	1284
646	501	1624
646	504	2058
647	201	1406
647	202	254
647	301	426
647	302	573
647	304	358
647	401	247
647	402	212
647	404	1449
647	501	523
647	504	1195
648	201	1830
648	202	2124
648	301	451
648	302	470
648	304	562
648	401	310
648	402	537
648	404	878
648	501	727
648	504	1150
649	201	30
649	202	11
649	302	12
650	201	854
650	202	1023
650	301	279
650	302	364
650	304	364
650	401	313
650	402	395
650	404	719
650	501	428
650	504	749
651	201	182
651	202	176
651	304	296
651	401	81
651	402	154
651	501	296
652	201	2158
652	202	936
652	301	399
652	302	523
652	304	503
652	401	328
652	402	636
652	404	1140
652	501	1000
652	504	771
653	201	183
653	202	135
653	301	78
653	302	177
653	304	54
653	401	46
654	201	181
654	202	116
654	301	97
654	302	146
654	304	40
654	401	31
655	201	1784
655	202	1862
655	301	472
655	302	346
655	304	499
655	401	548
655	402	462
655	404	1096
655	501	757
655	504	1238
656	201	195
656	202	101
656	304	261
656	401	76
656	402	197
656	501	259
657	201	160
657	202	104
657	304	271
657	401	55
657	402	229
657	501	235
658	201	122
658	202	182
658	304	213
658	401	63
658	402	232
658	501	222
659	201	26
659	202	124
659	301	84
659	302	37
660	201	895
660	202	455
660	301	358
660	302	299
660	304	482
660	401	366
660	402	355
660	404	817
660	501	442
660	504	784
661	201	607
661	202	2065
661	301	617
661	302	505
661	304	740
661	401	339
661	402	208
661	404	882
661	501	520
661	504	733
662	201	23
662	202	114
662	301	60
662	302	26
663	201	855
663	202	477
663	301	267
663	302	360
663	304	206
663	401	434
663	402	245
663	404	978
663	501	320
663	504	694
664	201	1064
664	202	1185
664	301	408
664	302	394
664	304	589
664	401	286
664	402	478
664	404	550
664	501	1067
664	504	779
665	201	164
665	202	157
665	304	218
665	401	78
665	402	211
665	501	209
666	201	1755
666	202	1699
666	301	383
666	302	415
666	304	451
666	401	463
666	402	576
666	404	934
666	501	667
666	504	1006
667	201	118
667	202	143
667	304	280
667	401	96
667	402	172
667	501	284
668	201	1718
668	202	1649
668	301	422
668	302	493
668	304	403
668	401	562
668	402	431
668	404	805
668	501	742
668	504	1247
669	201	2164
669	202	1738
669	301	452
669	302	308
669	304	315
669	401	351
669	402	455
669	404	994
669	501	713
669	504	1099
670	201	1637
670	202	1569
670	301	347
670	302	361
670	304	329
670	401	546
670	402	502
670	404	921
670	501	714
670	504	1212
671	201	1448
671	202	1543
671	301	389
671	302	473
671	304	402
671	401	314
671	402	510
671	404	1002
671	501	668
671	504	1145
672	201	195
672	202	129
672	304	278
672	401	61
672	402	226
672	501	244
673	201	614
673	202	1145
673	301	441
673	302	232
673	304	424
673	401	558
673	402	829
673	404	1397
673	501	937
673	504	808
674	201	38
674	202	119
674	301	62
674	302	35
675	201	103
675	202	107
675	304	279
675	401	84
675	402	207
675	501	261
676	201	313
676	202	551
676	301	312
676	302	244
676	304	244
676	401	346
676	402	289
676	404	985
676	501	455
676	504	593
677	201	36
677	202	109
677	301	72
677	302	34
678	201	1687
678	202	1238
678	301	357
678	302	395
678	304	532
678	401	306
678	402	565
678	404	1126
678	501	768
678	504	1023
679	201	1218
679	202	1935
679	301	308
679	302	327
679	304	388
679	401	426
679	402	538
679	404	854
679	501	539
679	504	1288
680	201	151
680	202	129
680	304	235
680	401	80
680	402	227
680	501	205
681	201	197
681	202	161
681	304	247
681	401	82
681	402	182
681	501	283
682	201	6926
682	202	6336
682	301	952
682	302	975
682	304	1490
682	401	1260
682	402	736
682	404	1498
682	501	1539
682	504	2712
683	201	198
683	202	157
683	304	212
683	401	53
683	402	230
683	501	237
684	201	6579
684	202	6009
684	301	962
684	302	812
684	304	1376
684	401	1220
684	402	742
684	404	1145
684	501	1940
684	504	2329
685	201	165
685	202	154
685	304	296
685	401	74
685	402	165
685	501	254
686	201	194
686	202	150
686	301	110
686	302	169
686	304	34
686	401	54
687	201	40
687	202	119
687	301	92
687	302	38
688	201	6401
688	202	6910
688	301	832
688	302	934
688	304	1498
688	401	1252
688	402	772
688	404	1010
688	501	1646
688	504	2737
689	201	479
689	202	598
689	301	419
689	302	394
689	304	585
689	401	472
689	402	887
689	404	725
689	501	783
689	504	1016
690	201	2178
690	202	1955
690	301	370
690	302	666
690	304	614
690	401	625
690	402	436
690	404	852
690	501	1015
690	504	870
691	201	36
691	202	87
691	301	75
691	302	22
692	201	1907
692	202	1898
692	301	616
692	302	347
692	304	422
692	401	232
692	402	345
692	404	1223
692	501	689
692	504	712
693	201	33
693	202	102
693	301	65
693	302	36
694	201	868
694	202	946
694	301	277
694	302	261
694	304	460
694	401	427
694	402	305
694	404	953
694	501	433
694	504	657
695	201	116
695	202	194
695	304	272
695	401	72
695	402	199
695	501	217
696	201	986
696	202	1051
696	301	663
696	302	527
696	304	407
696	401	445
696	402	782
696	404	642
696	501	725
696	504	1002
697	201	141
697	202	138
697	304	221
697	401	91
697	402	191
697	501	228
698	201	736
698	202	480
698	301	344
698	302	244
698	304	422
698	401	439
698	402	230
698	404	945
698	501	561
698	504	562
699	201	1534
699	202	1489
699	301	312
699	302	670
699	304	677
699	401	232
699	402	583
699	404	1059
699	501	336
699	504	596
700	201	241
700	202	697
700	301	320
700	302	231
700	304	400
700	401	356
700	402	354
700	404	505
700	501	597
700	504	602
701	201	1615
701	202	2157
701	301	393
701	302	301
701	304	393
701	401	315
701	402	536
701	404	1143
701	501	636
701	504	1041
702	201	1678
702	202	1611
702	301	450
702	302	483
702	304	523
702	401	330
702	402	500
702	404	1153
702	501	588
702	504	1175
703	201	33
703	202	109
703	301	83
703	302	37
704	201	20
704	202	85
704	301	81
704	302	31
705	201	38
705	202	114
705	301	85
705	302	34
706	201	125
706	202	192
706	301	103
706	302	131
706	304	43
706	401	50
707	201	2160
707	202	2100
707	301	326
707	302	467
707	304	376
707	401	461
707	402	589
707	404	833
707	501	640
707	504	1261
708	201	1337
708	202	2129
708	301	384
708	302	350
708	304	370
708	401	444
708	402	430
708	404	886
708	501	576
708	504	1118
709	201	29
709	202	108
709	301	76
709	302	22
710	201	189
710	202	123
710	304	265
710	401	98
710	402	203
710	501	203
711	201	185
711	202	117
711	301	80
711	302	161
711	304	49
711	401	53
712	201	22
712	202	96
712	301	58
712	302	21
713	201	5566
713	202	5704
713	301	938
713	302	975
713	304	1480
713	401	1026
713	402	684
713	404	1499
713	501	1882
713	504	2020
714	201	191
714	202	129
714	304	230
714	401	68
714	402	174
714	501	267
715	201	143
715	202	154
715	301	80
715	302	111
715	304	49
715	401	47
716	201	26
716	202	16
716	302	16
717	201	531
717	202	631
717	301	290
717	302	244
717	304	353
717	401	206
717	402	279
717	404	556
717	501	380
717	504	697
718	201	35
718	202	80
718	301	69
718	302	21
719	201	186
719	202	124
719	301	93
719	302	102
719	304	53
719	401	52
720	201	244
720	202	1050
720	301	375
720	302	216
720	304	315
720	401	395
720	402	280
720	404	692
720	501	373
720	504	743
721	201	136
721	202	110
721	304	287
721	401	61
721	402	157
721	501	215
722	201	511
722	202	565
722	301	289
722	302	385
722	304	404
722	401	371
722	402	387
722	404	600
722	501	485
722	504	670
723	201	253
723	202	1153
723	301	334
723	302	230
723	304	424
723	401	283
723	402	273
723	404	605
723	501	398
723	504	550
724	201	647
724	202	861
724	301	221
724	302	223
724	304	364
724	401	203
724	402	293
724	404	515
724	501	357
724	504	660
725	201	132
725	202	199
725	304	257
725	401	88
725	402	237
725	501	227
726	201	160
726	202	127
726	304	253
726	401	90
726	402	152
726	501	299
727	201	28
727	202	112
727	301	73
727	302	37
728	201	5336
728	202	6959
728	301	908
728	302	1000
728	304	1260
728	401	1091
728	402	654
728	404	1009
728	501	1576
728	504	2562
729	201	31
729	202	125
729	301	81
729	302	28
730	201	2029
730	202	1880
730	301	315
730	302	305
730	304	467
730	401	435
730	402	411
730	404	707
730	501	640
730	504	1248
731	201	145
731	202	111
731	301	75
731	302	188
731	304	43
731	401	51
732	201	186
732	202	145
732	301	70
732	302	140
732	304	42
732	401	58
733	201	127
733	202	182
733	304	296
733	401	88
733	402	165
733	501	299
734	201	926
734	202	228
734	301	284
734	302	265
734	304	260
734	401	292
734	402	222
734	404	808
734	501	397
734	504	638
735	201	1784
735	202	1703
735	301	433
735	302	454
735	304	484
735	401	527
735	402	436
735	404	948
735	501	656
735	504	1225
736	201	21
736	202	90
736	301	69
736	302	30
737	201	903
737	202	750
737	301	585
737	302	221
737	304	392
737	401	227
737	402	587
737	404	886
737	501	726
737	504	1013
738	201	1569
738	202	1417
738	301	452
738	302	470
738	304	490
738	401	521
738	402	476
738	404	727
738	501	500
738	504	1044
739	201	6263
739	202	6913
739	301	952
739	302	858
739	304	1387
739	401	1153
739	402	786
739	404	1260
739	501	1771
739	504	2392
740	201	1723
740	202	328
740	301	553
740	302	382
740	304	339
740	401	447
740	402	406
740	404	554
740	501	424
740	504	629
\.


--
-- Data for Name: fleets; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.fleets (id, profile_id, name, planet_id, stance, engaged, ore_count, hydro_count, worker_count, scientist_count, soldier_count, cur_action_id) FROM stdin;
9	1	Rogue	1116	t	f	0	0	0	0	0	\N
10	1	Rogue	1118	t	f	0	0	0	0	0	\N
11	1	Rogue	1119	t	f	0	0	0	0	0	\N
12	1	Rogue	1120	t	f	0	0	0	0	0	\N
13	1	Rogue	1122	t	f	0	0	0	0	0	\N
14	1	Rogue	1123	t	f	0	0	0	0	0	\N
15	1	Rogue	1127	t	f	0	0	0	0	0	\N
16	1	Rogue	1133	t	f	0	0	0	0	0	\N
17	1	Rogue	1135	t	f	0	0	0	0	0	\N
18	1	Rogue	1136	t	f	0	0	0	0	0	\N
19	1	Rogue	1139	t	f	0	0	0	0	0	\N
20	1	Rogue	1140	t	f	0	0	0	0	0	\N
21	1	Rogue	1144	t	f	0	0	0	0	0	\N
22	1	Rogue	1149	t	f	0	0	0	0	0	\N
23	1	Rogue	1153	t	f	0	0	0	0	0	\N
24	1	Rogue	1154	t	f	0	0	0	0	0	\N
25	1	Rogue	1157	t	f	0	0	0	0	0	\N
26	1	Rogue	1159	t	f	0	0	0	0	0	\N
27	1	Rogue	1160	t	f	0	0	0	0	0	\N
28	1	Rogue	1164	t	f	0	0	0	0	0	\N
29	1	Rogue	1165	t	f	0	0	0	0	0	\N
30	1	Rogue	1168	t	f	0	0	0	0	0	\N
31	1	Rogue	1183	t	f	0	0	0	0	0	\N
32	1	Rogue	1188	t	f	0	0	0	0	0	\N
33	1	Rogue	1189	t	f	0	0	0	0	0	\N
34	1	Rogue	1191	t	f	0	0	0	0	0	\N
35	1	Rogue	1192	t	f	0	0	0	0	0	\N
36	1	Rogue	1193	t	f	0	0	0	0	0	\N
37	1	Rogue	1195	t	f	0	0	0	0	0	\N
38	1	Rogue	1197	t	f	0	0	0	0	0	\N
39	1	Rogue	1198	t	f	0	0	0	0	0	\N
40	1	Rogue	1200	t	f	0	0	0	0	0	\N
41	1	Rogue	1204	t	f	0	0	0	0	0	\N
42	1	Rogue	1205	t	f	0	0	0	0	0	\N
43	1	Rogue	1208	t	f	0	0	0	0	0	\N
44	1	Rogue	1215	t	f	0	0	0	0	0	\N
45	1	Rogue	1217	t	f	0	0	0	0	0	\N
46	1	Rogue	1218	t	f	0	0	0	0	0	\N
47	1	Rogue	1220	t	f	0	0	0	0	0	\N
48	1	Rogue	1223	t	f	0	0	0	0	0	\N
49	1	Rogue	1224	t	f	0	0	0	0	0	\N
50	1	Rogue	1225	t	f	0	0	0	0	0	\N
51	1	Rogue	1226	t	f	0	0	0	0	0	\N
52	1	Rogue	1227	t	f	0	0	0	0	0	\N
53	1	Rogue	1228	t	f	0	0	0	0	0	\N
54	1	Rogue	1233	t	f	0	0	0	0	0	\N
55	1	Rogue	1238	t	f	0	0	0	0	0	\N
56	1	Rogue	1241	t	f	0	0	0	0	0	\N
57	1	Rogue	1248	t	f	0	0	0	0	0	\N
58	1	Rogue	1249	t	f	0	0	0	0	0	\N
59	1	Rogue	1254	t	f	0	0	0	0	0	\N
60	1	Rogue	1257	t	f	0	0	0	0	0	\N
61	1	Rogue	1258	t	f	0	0	0	0	0	\N
62	1	Rogue	1259	t	f	0	0	0	0	0	\N
63	1	Rogue	1261	t	f	0	0	0	0	0	\N
64	1	Rogue	1262	t	f	0	0	0	0	0	\N
65	1	Rogue	1267	t	f	0	0	0	0	0	\N
66	1	Rogue	1268	t	f	0	0	0	0	0	\N
67	1	Rogue	1270	t	f	0	0	0	0	0	\N
68	1	Rogue	1271	t	f	0	0	0	0	0	\N
69	1	Rogue	1273	t	f	0	0	0	0	0	\N
70	1	Rogue	1278	t	f	0	0	0	0	0	\N
71	1	Rogue	1279	t	f	0	0	0	0	0	\N
72	1	Rogue	1280	t	f	0	0	0	0	0	\N
73	1	Rogue	1282	t	f	0	0	0	0	0	\N
74	1	Rogue	1284	t	f	0	0	0	0	0	\N
75	1	Rogue	1286	t	f	0	0	0	0	0	\N
76	1	Rogue	1289	t	f	0	0	0	0	0	\N
77	1	Rogue	1290	t	f	0	0	0	0	0	\N
78	1	Rogue	1292	t	f	0	0	0	0	0	\N
79	1	Rogue	1295	t	f	0	0	0	0	0	\N
80	1	Rogue	1296	t	f	0	0	0	0	0	\N
81	1	Rogue	1299	t	f	0	0	0	0	0	\N
82	1	Rogue	1300	t	f	0	0	0	0	0	\N
83	1	Rogue	1302	t	f	0	0	0	0	0	\N
84	1	Rogue	1304	t	f	0	0	0	0	0	\N
85	1	Rogue	1306	t	f	0	0	0	0	0	\N
86	1	Rogue	1311	t	f	0	0	0	0	0	\N
87	1	Rogue	1363	t	f	0	0	0	0	0	\N
88	1	Rogue	1367	t	f	0	0	0	0	0	\N
89	1	Rogue	1370	t	f	0	0	0	0	0	\N
90	1	Rogue	1371	t	f	0	0	0	0	0	\N
91	1	Rogue	1372	t	f	0	0	0	0	0	\N
92	1	Rogue	1373	t	f	0	0	0	0	0	\N
93	1	Rogue	1375	t	f	0	0	0	0	0	\N
94	1	Rogue	1376	t	f	0	0	0	0	0	\N
95	1	Rogue	1379	t	f	0	0	0	0	0	\N
96	1	Rogue	1380	t	f	0	0	0	0	0	\N
97	1	Rogue	1381	t	f	0	0	0	0	0	\N
98	1	Rogue	1382	t	f	0	0	0	0	0	\N
99	1	Rogue	1384	t	f	0	0	0	0	0	\N
100	1	Rogue	1386	t	f	0	0	0	0	0	\N
101	1	Rogue	1387	t	f	0	0	0	0	0	\N
102	1	Rogue	1390	t	f	0	0	0	0	0	\N
103	1	Rogue	1392	t	f	0	0	0	0	0	\N
104	1	Rogue	1394	t	f	0	0	0	0	0	\N
105	1	Rogue	1395	t	f	0	0	0	0	0	\N
106	1	Rogue	1396	t	f	0	0	0	0	0	\N
107	1	Rogue	1397	t	f	0	0	0	0	0	\N
108	1	Rogue	1398	t	f	0	0	0	0	0	\N
109	1	Rogue	1400	t	f	0	0	0	0	0	\N
110	1	Rogue	1403	t	f	0	0	0	0	0	\N
111	1	Rogue	1407	t	f	0	0	0	0	0	\N
112	1	Rogue	1408	t	f	0	0	0	0	0	\N
113	1	Rogue	1410	t	f	0	0	0	0	0	\N
114	1	Rogue	1411	t	f	0	0	0	0	0	\N
115	1	Rogue	1412	t	f	0	0	0	0	0	\N
116	1	Rogue	1413	t	f	0	0	0	0	0	\N
117	1	Rogue	1415	t	f	0	0	0	0	0	\N
118	1	Rogue	1416	t	f	0	0	0	0	0	\N
119	1	Rogue	1419	t	f	0	0	0	0	0	\N
120	1	Rogue	1421	t	f	0	0	0	0	0	\N
121	1	Rogue	1426	t	f	0	0	0	0	0	\N
122	1	Rogue	1427	t	f	0	0	0	0	0	\N
123	1	Rogue	1430	t	f	0	0	0	0	0	\N
124	1	Rogue	1431	t	f	0	0	0	0	0	\N
125	1	Rogue	1433	t	f	0	0	0	0	0	\N
126	1	Rogue	1434	t	f	0	0	0	0	0	\N
127	1	Rogue	1436	t	f	0	0	0	0	0	\N
128	1	Rogue	1437	t	f	0	0	0	0	0	\N
129	1	Rogue	1440	t	f	0	0	0	0	0	\N
130	1	Rogue	1444	t	f	0	0	0	0	0	\N
131	1	Rogue	1446	t	f	0	0	0	0	0	\N
132	1	Rogue	1448	t	f	0	0	0	0	0	\N
133	1	Rogue	1449	t	f	0	0	0	0	0	\N
134	1	Rogue	1450	t	f	0	0	0	0	0	\N
135	1	Rogue	1451	t	f	0	0	0	0	0	\N
136	1	Rogue	1452	t	f	0	0	0	0	0	\N
137	1	Rogue	1454	t	f	0	0	0	0	0	\N
138	1	Rogue	1457	t	f	0	0	0	0	0	\N
139	1	Rogue	1458	t	f	0	0	0	0	0	\N
140	1	Rogue	1460	t	f	0	0	0	0	0	\N
141	1	Rogue	1461	t	f	0	0	0	0	0	\N
142	1	Rogue	1464	t	f	0	0	0	0	0	\N
143	1	Rogue	1467	t	f	0	0	0	0	0	\N
144	1	Rogue	1473	t	f	0	0	0	0	0	\N
145	1	Rogue	1475	t	f	0	0	0	0	0	\N
146	1	Rogue	1476	t	f	0	0	0	0	0	\N
147	1	Rogue	1478	t	f	0	0	0	0	0	\N
148	1	Rogue	1479	t	f	0	0	0	0	0	\N
149	1	Rogue	1480	t	f	0	0	0	0	0	\N
150	1	Rogue	1482	t	f	0	0	0	0	0	\N
151	1	Rogue	1484	t	f	0	0	0	0	0	\N
152	1	Rogue	1485	t	f	0	0	0	0	0	\N
153	1	Rogue	1486	t	f	0	0	0	0	0	\N
154	1	Rogue	1488	t	f	0	0	0	0	0	\N
155	1	Rogue	1489	t	f	0	0	0	0	0	\N
156	1	Rogue	1491	t	f	0	0	0	0	0	\N
157	1	Rogue	1492	t	f	0	0	0	0	0	\N
158	1	Rogue	1495	t	f	0	0	0	0	0	\N
159	1	Rogue	1496	t	f	0	0	0	0	0	\N
160	1	Rogue	1500	t	f	0	0	0	0	0	\N
161	1	Rogue	1501	t	f	0	0	0	0	0	\N
162	1	Rogue	1502	t	f	0	0	0	0	0	\N
163	1	Rogue	1507	t	f	0	0	0	0	0	\N
164	1	Rogue	1508	t	f	0	0	0	0	0	\N
165	1	Rogue	1510	t	f	0	0	0	0	0	\N
166	1	Rogue	1513	t	f	0	0	0	0	0	\N
167	1	Rogue	1516	t	f	0	0	0	0	0	\N
168	1	Rogue	1518	t	f	0	0	0	0	0	\N
169	1	Rogue	1519	t	f	0	0	0	0	0	\N
170	1	Rogue	1522	t	f	0	0	0	0	0	\N
171	1	Rogue	1524	t	f	0	0	0	0	0	\N
172	1	Rogue	1526	t	f	0	0	0	0	0	\N
173	1	Rogue	1527	t	f	0	0	0	0	0	\N
174	1	Rogue	1528	t	f	0	0	0	0	0	\N
175	1	Rogue	1534	t	f	0	0	0	0	0	\N
176	1	Rogue	1537	t	f	0	0	0	0	0	\N
177	1	Rogue	1538	t	f	0	0	0	0	0	\N
178	1	Rogue	1542	t	f	0	0	0	0	0	\N
179	1	Rogue	1543	t	f	0	0	0	0	0	\N
180	1	Rogue	1545	t	f	0	0	0	0	0	\N
181	1	Rogue	1546	t	f	0	0	0	0	0	\N
182	1	Rogue	1554	t	f	0	0	0	0	0	\N
183	1	Rogue	1558	t	f	0	0	0	0	0	\N
184	1	Rogue	1559	t	f	0	0	0	0	0	\N
185	1	Rogue	1561	t	f	0	0	0	0	0	\N
186	1	Rogue	1613	t	f	0	0	0	0	0	\N
187	1	Rogue	1616	t	f	0	0	0	0	0	\N
188	1	Rogue	1618	t	f	0	0	0	0	0	\N
189	1	Rogue	1619	t	f	0	0	0	0	0	\N
190	1	Rogue	1622	t	f	0	0	0	0	0	\N
191	1	Rogue	1624	t	f	0	0	0	0	0	\N
192	1	Rogue	1625	t	f	0	0	0	0	0	\N
193	1	Rogue	1630	t	f	0	0	0	0	0	\N
194	1	Rogue	1632	t	f	0	0	0	0	0	\N
195	1	Rogue	1633	t	f	0	0	0	0	0	\N
196	1	Rogue	1636	t	f	0	0	0	0	0	\N
197	1	Rogue	1637	t	f	0	0	0	0	0	\N
198	1	Rogue	1643	t	f	0	0	0	0	0	\N
199	1	Rogue	1644	t	f	0	0	0	0	0	\N
200	1	Rogue	1645	t	f	0	0	0	0	0	\N
201	1	Rogue	1646	t	f	0	0	0	0	0	\N
202	1	Rogue	1647	t	f	0	0	0	0	0	\N
203	1	Rogue	1654	t	f	0	0	0	0	0	\N
204	1	Rogue	1656	t	f	0	0	0	0	0	\N
205	1	Rogue	1659	t	f	0	0	0	0	0	\N
206	1	Rogue	1663	t	f	0	0	0	0	0	\N
207	1	Rogue	1665	t	f	0	0	0	0	0	\N
208	1	Rogue	1667	t	f	0	0	0	0	0	\N
209	1	Rogue	1668	t	f	0	0	0	0	0	\N
210	1	Rogue	1670	t	f	0	0	0	0	0	\N
211	1	Rogue	1671	t	f	0	0	0	0	0	\N
212	1	Rogue	1672	t	f	0	0	0	0	0	\N
213	1	Rogue	1673	t	f	0	0	0	0	0	\N
214	1	Rogue	1676	t	f	0	0	0	0	0	\N
215	1	Rogue	1678	t	f	0	0	0	0	0	\N
216	1	Rogue	1682	t	f	0	0	0	0	0	\N
217	1	Rogue	1684	t	f	0	0	0	0	0	\N
218	1	Rogue	1686	t	f	0	0	0	0	0	\N
219	1	Rogue	1688	t	f	0	0	0	0	0	\N
220	1	Rogue	1693	t	f	0	0	0	0	0	\N
221	1	Rogue	1695	t	f	0	0	0	0	0	\N
222	1	Rogue	1703	t	f	0	0	0	0	0	\N
223	1	Rogue	1705	t	f	0	0	0	0	0	\N
224	1	Rogue	1708	t	f	0	0	0	0	0	\N
225	1	Rogue	1709	t	f	0	0	0	0	0	\N
226	1	Rogue	1711	t	f	0	0	0	0	0	\N
227	1	Rogue	1712	t	f	0	0	0	0	0	\N
228	1	Rogue	1713	t	f	0	0	0	0	0	\N
229	1	Rogue	1715	t	f	0	0	0	0	0	\N
230	1	Rogue	1716	t	f	0	0	0	0	0	\N
231	1	Rogue	1717	t	f	0	0	0	0	0	\N
232	1	Rogue	1718	t	f	0	0	0	0	0	\N
233	1	Rogue	1720	t	f	0	0	0	0	0	\N
234	1	Rogue	1721	t	f	0	0	0	0	0	\N
235	1	Rogue	1722	t	f	0	0	0	0	0	\N
236	1	Rogue	1723	t	f	0	0	0	0	0	\N
237	1	Rogue	1724	t	f	0	0	0	0	0	\N
238	1	Rogue	1726	t	f	0	0	0	0	0	\N
239	1	Rogue	1728	t	f	0	0	0	0	0	\N
240	1	Rogue	1729	t	f	0	0	0	0	0	\N
241	1	Rogue	1733	t	f	0	0	0	0	0	\N
242	1	Rogue	1734	t	f	0	0	0	0	0	\N
243	1	Rogue	1741	t	f	0	0	0	0	0	\N
244	1	Rogue	1743	t	f	0	0	0	0	0	\N
245	1	Rogue	1744	t	f	0	0	0	0	0	\N
246	1	Rogue	1745	t	f	0	0	0	0	0	\N
247	1	Rogue	1746	t	f	0	0	0	0	0	\N
248	1	Rogue	1747	t	f	0	0	0	0	0	\N
249	1	Rogue	1748	t	f	0	0	0	0	0	\N
250	1	Rogue	1753	t	f	0	0	0	0	0	\N
251	1	Rogue	1755	t	f	0	0	0	0	0	\N
252	1	Rogue	1759	t	f	0	0	0	0	0	\N
253	1	Rogue	1763	t	f	0	0	0	0	0	\N
254	1	Rogue	1769	t	f	0	0	0	0	0	\N
255	1	Rogue	1777	t	f	0	0	0	0	0	\N
256	1	Rogue	1779	t	f	0	0	0	0	0	\N
257	1	Rogue	1783	t	f	0	0	0	0	0	\N
258	1	Rogue	1784	t	f	0	0	0	0	0	\N
259	1	Rogue	1785	t	f	0	0	0	0	0	\N
260	1	Rogue	1786	t	f	0	0	0	0	0	\N
261	1	Rogue	1787	t	f	0	0	0	0	0	\N
262	1	Rogue	1789	t	f	0	0	0	0	0	\N
263	1	Rogue	1793	t	f	0	0	0	0	0	\N
264	1	Rogue	1794	t	f	0	0	0	0	0	\N
265	1	Rogue	1799	t	f	0	0	0	0	0	\N
266	1	Rogue	1800	t	f	0	0	0	0	0	\N
267	1	Rogue	1804	t	f	0	0	0	0	0	\N
268	1	Rogue	1805	t	f	0	0	0	0	0	\N
269	1	Rogue	1811	t	f	0	0	0	0	0	\N
270	1	Rogue	1865	t	f	0	0	0	0	0	\N
271	1	Rogue	1866	t	f	0	0	0	0	0	\N
272	1	Rogue	1870	t	f	0	0	0	0	0	\N
273	1	Rogue	1876	t	f	0	0	0	0	0	\N
274	1	Rogue	1877	t	f	0	0	0	0	0	\N
275	1	Rogue	1881	t	f	0	0	0	0	0	\N
276	1	Rogue	1885	t	f	0	0	0	0	0	\N
277	1	Rogue	1891	t	f	0	0	0	0	0	\N
278	1	Rogue	1892	t	f	0	0	0	0	0	\N
279	1	Rogue	1895	t	f	0	0	0	0	0	\N
280	1	Rogue	1896	t	f	0	0	0	0	0	\N
281	1	Rogue	1897	t	f	0	0	0	0	0	\N
282	1	Rogue	1902	t	f	0	0	0	0	0	\N
283	1	Rogue	1907	t	f	0	0	0	0	0	\N
284	1	Rogue	1909	t	f	0	0	0	0	0	\N
285	1	Rogue	1910	t	f	0	0	0	0	0	\N
286	1	Rogue	1912	t	f	0	0	0	0	0	\N
287	1	Rogue	1913	t	f	0	0	0	0	0	\N
288	1	Rogue	1914	t	f	0	0	0	0	0	\N
289	1	Rogue	1917	t	f	0	0	0	0	0	\N
290	1	Rogue	1923	t	f	0	0	0	0	0	\N
291	1	Rogue	1925	t	f	0	0	0	0	0	\N
292	1	Rogue	1926	t	f	0	0	0	0	0	\N
293	1	Rogue	1929	t	f	0	0	0	0	0	\N
294	1	Rogue	1931	t	f	0	0	0	0	0	\N
295	1	Rogue	1934	t	f	0	0	0	0	0	\N
296	1	Rogue	1936	t	f	0	0	0	0	0	\N
297	1	Rogue	1937	t	f	0	0	0	0	0	\N
298	1	Rogue	1943	t	f	0	0	0	0	0	\N
299	1	Rogue	1944	t	f	0	0	0	0	0	\N
300	1	Rogue	1948	t	f	0	0	0	0	0	\N
301	1	Rogue	1950	t	f	0	0	0	0	0	\N
302	1	Rogue	1951	t	f	0	0	0	0	0	\N
303	1	Rogue	1954	t	f	0	0	0	0	0	\N
304	1	Rogue	1955	t	f	0	0	0	0	0	\N
305	1	Rogue	1958	t	f	0	0	0	0	0	\N
306	1	Rogue	1960	t	f	0	0	0	0	0	\N
307	1	Rogue	1961	t	f	0	0	0	0	0	\N
308	1	Rogue	1962	t	f	0	0	0	0	0	\N
309	1	Rogue	1964	t	f	0	0	0	0	0	\N
310	1	Rogue	1966	t	f	0	0	0	0	0	\N
311	1	Rogue	1967	t	f	0	0	0	0	0	\N
312	1	Rogue	1970	t	f	0	0	0	0	0	\N
313	1	Rogue	1971	t	f	0	0	0	0	0	\N
314	1	Rogue	1972	t	f	0	0	0	0	0	\N
315	1	Rogue	1974	t	f	0	0	0	0	0	\N
316	1	Rogue	1975	t	f	0	0	0	0	0	\N
317	1	Rogue	1977	t	f	0	0	0	0	0	\N
318	1	Rogue	1978	t	f	0	0	0	0	0	\N
319	1	Rogue	1979	t	f	0	0	0	0	0	\N
320	1	Rogue	1980	t	f	0	0	0	0	0	\N
321	1	Rogue	1981	t	f	0	0	0	0	0	\N
322	1	Rogue	1985	t	f	0	0	0	0	0	\N
323	1	Rogue	1986	t	f	0	0	0	0	0	\N
324	1	Rogue	1987	t	f	0	0	0	0	0	\N
325	1	Rogue	1988	t	f	0	0	0	0	0	\N
326	1	Rogue	1990	t	f	0	0	0	0	0	\N
327	1	Rogue	1992	t	f	0	0	0	0	0	\N
328	1	Rogue	1994	t	f	0	0	0	0	0	\N
329	1	Rogue	1995	t	f	0	0	0	0	0	\N
330	1	Rogue	1996	t	f	0	0	0	0	0	\N
331	1	Rogue	1997	t	f	0	0	0	0	0	\N
332	1	Rogue	2003	t	f	0	0	0	0	0	\N
333	1	Rogue	2004	t	f	0	0	0	0	0	\N
334	1	Rogue	2008	t	f	0	0	0	0	0	\N
335	1	Rogue	2010	t	f	0	0	0	0	0	\N
336	1	Rogue	2017	t	f	0	0	0	0	0	\N
337	1	Rogue	2020	t	f	0	0	0	0	0	\N
338	1	Rogue	2025	t	f	0	0	0	0	0	\N
339	1	Rogue	2028	t	f	0	0	0	0	0	\N
340	1	Rogue	2031	t	f	0	0	0	0	0	\N
341	1	Rogue	2033	t	f	0	0	0	0	0	\N
342	1	Rogue	2039	t	f	0	0	0	0	0	\N
343	1	Rogue	2040	t	f	0	0	0	0	0	\N
344	1	Rogue	2041	t	f	0	0	0	0	0	\N
345	1	Rogue	2045	t	f	0	0	0	0	0	\N
346	1	Rogue	2048	t	f	0	0	0	0	0	\N
347	1	Rogue	2053	t	f	0	0	0	0	0	\N
348	1	Rogue	2054	t	f	0	0	0	0	0	\N
349	1	Rogue	2058	t	f	0	0	0	0	0	\N
350	1	Rogue	2061	t	f	0	0	0	0	0	\N
351	1	Rogue	2114	t	f	0	0	0	0	0	\N
352	1	Rogue	2118	t	f	0	0	0	0	0	\N
353	1	Rogue	2121	t	f	0	0	0	0	0	\N
354	1	Rogue	2122	t	f	0	0	0	0	0	\N
355	1	Rogue	2125	t	f	0	0	0	0	0	\N
356	1	Rogue	2127	t	f	0	0	0	0	0	\N
357	1	Rogue	2130	t	f	0	0	0	0	0	\N
358	1	Rogue	2132	t	f	0	0	0	0	0	\N
359	1	Rogue	2134	t	f	0	0	0	0	0	\N
360	1	Rogue	2140	t	f	0	0	0	0	0	\N
361	1	Rogue	2141	t	f	0	0	0	0	0	\N
362	1	Rogue	2142	t	f	0	0	0	0	0	\N
363	1	Rogue	2146	t	f	0	0	0	0	0	\N
364	1	Rogue	2149	t	f	0	0	0	0	0	\N
365	1	Rogue	2150	t	f	0	0	0	0	0	\N
366	1	Rogue	2151	t	f	0	0	0	0	0	\N
367	1	Rogue	2154	t	f	0	0	0	0	0	\N
368	1	Rogue	2156	t	f	0	0	0	0	0	\N
369	1	Rogue	2159	t	f	0	0	0	0	0	\N
370	1	Rogue	2160	t	f	0	0	0	0	0	\N
371	1	Rogue	2161	t	f	0	0	0	0	0	\N
372	1	Rogue	2164	t	f	0	0	0	0	0	\N
373	1	Rogue	2168	t	f	0	0	0	0	0	\N
374	1	Rogue	2170	t	f	0	0	0	0	0	\N
375	1	Rogue	2171	t	f	0	0	0	0	0	\N
376	1	Rogue	2172	t	f	0	0	0	0	0	\N
377	1	Rogue	2174	t	f	0	0	0	0	0	\N
378	1	Rogue	2175	t	f	0	0	0	0	0	\N
379	1	Rogue	2176	t	f	0	0	0	0	0	\N
380	1	Rogue	2180	t	f	0	0	0	0	0	\N
381	1	Rogue	2181	t	f	0	0	0	0	0	\N
382	1	Rogue	2182	t	f	0	0	0	0	0	\N
383	1	Rogue	2185	t	f	0	0	0	0	0	\N
384	1	Rogue	2186	t	f	0	0	0	0	0	\N
385	1	Rogue	2188	t	f	0	0	0	0	0	\N
386	1	Rogue	2191	t	f	0	0	0	0	0	\N
387	1	Rogue	2192	t	f	0	0	0	0	0	\N
388	1	Rogue	2195	t	f	0	0	0	0	0	\N
389	1	Rogue	2196	t	f	0	0	0	0	0	\N
390	1	Rogue	2197	t	f	0	0	0	0	0	\N
391	1	Rogue	2201	t	f	0	0	0	0	0	\N
392	1	Rogue	2203	t	f	0	0	0	0	0	\N
393	1	Rogue	2204	t	f	0	0	0	0	0	\N
394	1	Rogue	2212	t	f	0	0	0	0	0	\N
395	1	Rogue	2215	t	f	0	0	0	0	0	\N
396	1	Rogue	2218	t	f	0	0	0	0	0	\N
397	1	Rogue	2221	t	f	0	0	0	0	0	\N
398	1	Rogue	2222	t	f	0	0	0	0	0	\N
399	1	Rogue	2224	t	f	0	0	0	0	0	\N
400	1	Rogue	2225	t	f	0	0	0	0	0	\N
401	1	Rogue	2227	t	f	0	0	0	0	0	\N
402	1	Rogue	2228	t	f	0	0	0	0	0	\N
403	1	Rogue	2229	t	f	0	0	0	0	0	\N
404	1	Rogue	2230	t	f	0	0	0	0	0	\N
405	1	Rogue	2231	t	f	0	0	0	0	0	\N
406	1	Rogue	2232	t	f	0	0	0	0	0	\N
407	1	Rogue	2238	t	f	0	0	0	0	0	\N
408	1	Rogue	2242	t	f	0	0	0	0	0	\N
409	1	Rogue	2243	t	f	0	0	0	0	0	\N
410	1	Rogue	2245	t	f	0	0	0	0	0	\N
411	1	Rogue	2246	t	f	0	0	0	0	0	\N
412	1	Rogue	2249	t	f	0	0	0	0	0	\N
413	1	Rogue	2250	t	f	0	0	0	0	0	\N
414	1	Rogue	2251	t	f	0	0	0	0	0	\N
415	1	Rogue	2252	t	f	0	0	0	0	0	\N
416	1	Rogue	2254	t	f	0	0	0	0	0	\N
417	1	Rogue	2255	t	f	0	0	0	0	0	\N
418	1	Rogue	2256	t	f	0	0	0	0	0	\N
419	1	Rogue	2257	t	f	0	0	0	0	0	\N
420	1	Rogue	2258	t	f	0	0	0	0	0	\N
421	1	Rogue	2259	t	f	0	0	0	0	0	\N
422	1	Rogue	2262	t	f	0	0	0	0	0	\N
423	1	Rogue	2265	t	f	0	0	0	0	0	\N
424	1	Rogue	2266	t	f	0	0	0	0	0	\N
425	1	Rogue	2267	t	f	0	0	0	0	0	\N
426	1	Rogue	2271	t	f	0	0	0	0	0	\N
427	1	Rogue	2272	t	f	0	0	0	0	0	\N
428	1	Rogue	2273	t	f	0	0	0	0	0	\N
429	1	Rogue	2275	t	f	0	0	0	0	0	\N
430	1	Rogue	2278	t	f	0	0	0	0	0	\N
431	1	Rogue	2281	t	f	0	0	0	0	0	\N
432	1	Rogue	2283	t	f	0	0	0	0	0	\N
433	1	Rogue	2285	t	f	0	0	0	0	0	\N
434	1	Rogue	2286	t	f	0	0	0	0	0	\N
435	1	Rogue	2288	t	f	0	0	0	0	0	\N
436	1	Rogue	2289	t	f	0	0	0	0	0	\N
437	1	Rogue	2292	t	f	0	0	0	0	0	\N
438	1	Rogue	2295	t	f	0	0	0	0	0	\N
439	1	Rogue	2296	t	f	0	0	0	0	0	\N
440	1	Rogue	2298	t	f	0	0	0	0	0	\N
441	1	Rogue	2300	t	f	0	0	0	0	0	\N
442	1	Rogue	2305	t	f	0	0	0	0	0	\N
443	1	Rogue	2306	t	f	0	0	0	0	0	\N
444	1	Rogue	2307	t	f	0	0	0	0	0	\N
445	1	Rogue	2308	t	f	0	0	0	0	0	\N
446	1	Rogue	2310	t	f	0	0	0	0	0	\N
447	1	Rogue	2365	t	f	0	0	0	0	0	\N
448	1	Rogue	2367	t	f	0	0	0	0	0	\N
449	1	Rogue	2368	t	f	0	0	0	0	0	\N
450	1	Rogue	2369	t	f	0	0	0	0	0	\N
451	1	Rogue	2370	t	f	0	0	0	0	0	\N
452	1	Rogue	2371	t	f	0	0	0	0	0	\N
453	1	Rogue	2373	t	f	0	0	0	0	0	\N
454	1	Rogue	2375	t	f	0	0	0	0	0	\N
455	1	Rogue	2376	t	f	0	0	0	0	0	\N
456	1	Rogue	2377	t	f	0	0	0	0	0	\N
457	1	Rogue	2379	t	f	0	0	0	0	0	\N
458	1	Rogue	2381	t	f	0	0	0	0	0	\N
459	1	Rogue	2385	t	f	0	0	0	0	0	\N
460	1	Rogue	2387	t	f	0	0	0	0	0	\N
461	1	Rogue	2388	t	f	0	0	0	0	0	\N
462	1	Rogue	2389	t	f	0	0	0	0	0	\N
463	1	Rogue	2391	t	f	0	0	0	0	0	\N
464	1	Rogue	2397	t	f	0	0	0	0	0	\N
465	1	Rogue	2402	t	f	0	0	0	0	0	\N
466	1	Rogue	2403	t	f	0	0	0	0	0	\N
467	1	Rogue	2407	t	f	0	0	0	0	0	\N
468	1	Rogue	2408	t	f	0	0	0	0	0	\N
469	1	Rogue	2409	t	f	0	0	0	0	0	\N
470	1	Rogue	2412	t	f	0	0	0	0	0	\N
471	1	Rogue	2414	t	f	0	0	0	0	0	\N
472	1	Rogue	2417	t	f	0	0	0	0	0	\N
473	1	Rogue	2418	t	f	0	0	0	0	0	\N
474	1	Rogue	2419	t	f	0	0	0	0	0	\N
475	1	Rogue	2420	t	f	0	0	0	0	0	\N
476	1	Rogue	2423	t	f	0	0	0	0	0	\N
477	1	Rogue	2424	t	f	0	0	0	0	0	\N
478	1	Rogue	2426	t	f	0	0	0	0	0	\N
479	1	Rogue	2428	t	f	0	0	0	0	0	\N
480	1	Rogue	2429	t	f	0	0	0	0	0	\N
481	1	Rogue	2432	t	f	0	0	0	0	0	\N
482	1	Rogue	2438	t	f	0	0	0	0	0	\N
483	1	Rogue	2439	t	f	0	0	0	0	0	\N
484	1	Rogue	2440	t	f	0	0	0	0	0	\N
485	1	Rogue	2442	t	f	0	0	0	0	0	\N
486	1	Rogue	2443	t	f	0	0	0	0	0	\N
487	1	Rogue	2446	t	f	0	0	0	0	0	\N
488	1	Rogue	2447	t	f	0	0	0	0	0	\N
489	1	Rogue	2449	t	f	0	0	0	0	0	\N
490	1	Rogue	2450	t	f	0	0	0	0	0	\N
491	1	Rogue	2451	t	f	0	0	0	0	0	\N
492	1	Rogue	2452	t	f	0	0	0	0	0	\N
493	1	Rogue	2455	t	f	0	0	0	0	0	\N
494	1	Rogue	2458	t	f	0	0	0	0	0	\N
495	1	Rogue	2459	t	f	0	0	0	0	0	\N
496	1	Rogue	2461	t	f	0	0	0	0	0	\N
497	1	Rogue	2464	t	f	0	0	0	0	0	\N
498	1	Rogue	2465	t	f	0	0	0	0	0	\N
499	1	Rogue	2466	t	f	0	0	0	0	0	\N
500	1	Rogue	2467	t	f	0	0	0	0	0	\N
501	1	Rogue	2469	t	f	0	0	0	0	0	\N
502	1	Rogue	2470	t	f	0	0	0	0	0	\N
503	1	Rogue	2472	t	f	0	0	0	0	0	\N
504	1	Rogue	2473	t	f	0	0	0	0	0	\N
505	1	Rogue	2474	t	f	0	0	0	0	0	\N
506	1	Rogue	2477	t	f	0	0	0	0	0	\N
507	1	Rogue	2480	t	f	0	0	0	0	0	\N
508	1	Rogue	2487	t	f	0	0	0	0	0	\N
509	1	Rogue	2489	t	f	0	0	0	0	0	\N
510	1	Rogue	2490	t	f	0	0	0	0	0	\N
511	1	Rogue	2492	t	f	0	0	0	0	0	\N
512	1	Rogue	2496	t	f	0	0	0	0	0	\N
513	1	Rogue	2499	t	f	0	0	0	0	0	\N
514	1	Rogue	2500	t	f	0	0	0	0	0	\N
515	1	Rogue	2505	t	f	0	0	0	0	0	\N
516	1	Rogue	2506	t	f	0	0	0	0	0	\N
517	1	Rogue	2511	t	f	0	0	0	0	0	\N
518	1	Rogue	2514	t	f	0	0	0	0	0	\N
519	1	Rogue	2515	t	f	0	0	0	0	0	\N
520	1	Rogue	2516	t	f	0	0	0	0	0	\N
521	1	Rogue	2517	t	f	0	0	0	0	0	\N
522	1	Rogue	2518	t	f	0	0	0	0	0	\N
523	1	Rogue	2519	t	f	0	0	0	0	0	\N
524	1	Rogue	2520	t	f	0	0	0	0	0	\N
525	1	Rogue	2521	t	f	0	0	0	0	0	\N
526	1	Rogue	2523	t	f	0	0	0	0	0	\N
527	1	Rogue	2526	t	f	0	0	0	0	0	\N
528	1	Rogue	2527	t	f	0	0	0	0	0	\N
529	1	Rogue	2529	t	f	0	0	0	0	0	\N
530	1	Rogue	2531	t	f	0	0	0	0	0	\N
531	1	Rogue	2532	t	f	0	0	0	0	0	\N
532	1	Rogue	2534	t	f	0	0	0	0	0	\N
533	1	Rogue	2535	t	f	0	0	0	0	0	\N
534	1	Rogue	2537	t	f	0	0	0	0	0	\N
535	1	Rogue	2543	t	f	0	0	0	0	0	\N
536	1	Rogue	2545	t	f	0	0	0	0	0	\N
537	1	Rogue	2546	t	f	0	0	0	0	0	\N
538	1	Rogue	2551	t	f	0	0	0	0	0	\N
539	1	Rogue	2553	t	f	0	0	0	0	0	\N
540	1	Rogue	2556	t	f	0	0	0	0	0	\N
541	1	Rogue	2558	t	f	0	0	0	0	0	\N
542	1	Rogue	2560	t	f	0	0	0	0	0	\N
543	1	Rogue	2561	t	f	0	0	0	0	0	\N
544	1	Rogue	2562	t	f	0	0	0	0	0	\N
545	1	Rogue	2613	t	f	0	0	0	0	0	\N
546	1	Rogue	2614	t	f	0	0	0	0	0	\N
547	1	Rogue	2616	t	f	0	0	0	0	0	\N
548	1	Rogue	2617	t	f	0	0	0	0	0	\N
549	1	Rogue	2618	t	f	0	0	0	0	0	\N
550	1	Rogue	2619	t	f	0	0	0	0	0	\N
551	1	Rogue	2620	t	f	0	0	0	0	0	\N
552	1	Rogue	2621	t	f	0	0	0	0	0	\N
553	1	Rogue	2622	t	f	0	0	0	0	0	\N
554	1	Rogue	2624	t	f	0	0	0	0	0	\N
555	1	Rogue	2628	t	f	0	0	0	0	0	\N
556	1	Rogue	2634	t	f	0	0	0	0	0	\N
557	1	Rogue	2636	t	f	0	0	0	0	0	\N
558	1	Rogue	2638	t	f	0	0	0	0	0	\N
559	1	Rogue	2639	t	f	0	0	0	0	0	\N
560	1	Rogue	2642	t	f	0	0	0	0	0	\N
561	1	Rogue	2644	t	f	0	0	0	0	0	\N
562	1	Rogue	2646	t	f	0	0	0	0	0	\N
563	1	Rogue	2647	t	f	0	0	0	0	0	\N
564	1	Rogue	2648	t	f	0	0	0	0	0	\N
565	1	Rogue	2653	t	f	0	0	0	0	0	\N
566	1	Rogue	2656	t	f	0	0	0	0	0	\N
567	1	Rogue	2659	t	f	0	0	0	0	0	\N
568	1	Rogue	2660	t	f	0	0	0	0	0	\N
569	1	Rogue	2661	t	f	0	0	0	0	0	\N
570	1	Rogue	2664	t	f	0	0	0	0	0	\N
571	1	Rogue	2665	t	f	0	0	0	0	0	\N
572	1	Rogue	2667	t	f	0	0	0	0	0	\N
573	1	Rogue	2668	t	f	0	0	0	0	0	\N
574	1	Rogue	2670	t	f	0	0	0	0	0	\N
575	1	Rogue	2671	t	f	0	0	0	0	0	\N
576	1	Rogue	2672	t	f	0	0	0	0	0	\N
577	1	Rogue	2675	t	f	0	0	0	0	0	\N
578	1	Rogue	2676	t	f	0	0	0	0	0	\N
579	1	Rogue	2677	t	f	0	0	0	0	0	\N
580	1	Rogue	2680	t	f	0	0	0	0	0	\N
581	1	Rogue	2681	t	f	0	0	0	0	0	\N
582	1	Rogue	2693	t	f	0	0	0	0	0	\N
583	1	Rogue	2694	t	f	0	0	0	0	0	\N
584	1	Rogue	2696	t	f	0	0	0	0	0	\N
585	1	Rogue	2700	t	f	0	0	0	0	0	\N
586	1	Rogue	2701	t	f	0	0	0	0	0	\N
587	1	Rogue	2702	t	f	0	0	0	0	0	\N
588	1	Rogue	2706	t	f	0	0	0	0	0	\N
589	1	Rogue	2707	t	f	0	0	0	0	0	\N
590	1	Rogue	2711	t	f	0	0	0	0	0	\N
591	1	Rogue	2715	t	f	0	0	0	0	0	\N
592	1	Rogue	2718	t	f	0	0	0	0	0	\N
593	1	Rogue	2720	t	f	0	0	0	0	0	\N
594	1	Rogue	2721	t	f	0	0	0	0	0	\N
595	1	Rogue	2722	t	f	0	0	0	0	0	\N
596	1	Rogue	2724	t	f	0	0	0	0	0	\N
597	1	Rogue	2725	t	f	0	0	0	0	0	\N
598	1	Rogue	2731	t	f	0	0	0	0	0	\N
599	1	Rogue	2732	t	f	0	0	0	0	0	\N
600	1	Rogue	2734	t	f	0	0	0	0	0	\N
601	1	Rogue	2736	t	f	0	0	0	0	0	\N
602	1	Rogue	2737	t	f	0	0	0	0	0	\N
603	1	Rogue	2741	t	f	0	0	0	0	0	\N
604	1	Rogue	2742	t	f	0	0	0	0	0	\N
605	1	Rogue	2744	t	f	0	0	0	0	0	\N
606	1	Rogue	2745	t	f	0	0	0	0	0	\N
607	1	Rogue	2748	t	f	0	0	0	0	0	\N
608	1	Rogue	2750	t	f	0	0	0	0	0	\N
609	1	Rogue	2754	t	f	0	0	0	0	0	\N
610	1	Rogue	2755	t	f	0	0	0	0	0	\N
611	1	Rogue	2756	t	f	0	0	0	0	0	\N
612	1	Rogue	2757	t	f	0	0	0	0	0	\N
613	1	Rogue	2759	t	f	0	0	0	0	0	\N
614	1	Rogue	2763	t	f	0	0	0	0	0	\N
615	1	Rogue	2766	t	f	0	0	0	0	0	\N
616	1	Rogue	2767	t	f	0	0	0	0	0	\N
617	1	Rogue	2771	t	f	0	0	0	0	0	\N
618	1	Rogue	2772	t	f	0	0	0	0	0	\N
619	1	Rogue	2776	t	f	0	0	0	0	0	\N
620	1	Rogue	2779	t	f	0	0	0	0	0	\N
621	1	Rogue	2784	t	f	0	0	0	0	0	\N
622	1	Rogue	2788	t	f	0	0	0	0	0	\N
623	1	Rogue	2789	t	f	0	0	0	0	0	\N
624	1	Rogue	2791	t	f	0	0	0	0	0	\N
625	1	Rogue	2792	t	f	0	0	0	0	0	\N
626	1	Rogue	2794	t	f	0	0	0	0	0	\N
627	1	Rogue	2795	t	f	0	0	0	0	0	\N
628	1	Rogue	2796	t	f	0	0	0	0	0	\N
629	1	Rogue	2797	t	f	0	0	0	0	0	\N
630	1	Rogue	2798	t	f	0	0	0	0	0	\N
631	1	Rogue	2799	t	f	0	0	0	0	0	\N
632	1	Rogue	2800	t	f	0	0	0	0	0	\N
633	1	Rogue	2801	t	f	0	0	0	0	0	\N
634	1	Rogue	2809	t	f	0	0	0	0	0	\N
635	1	Rogue	2810	t	f	0	0	0	0	0	\N
636	1	Rogue	2866	t	f	0	0	0	0	0	\N
637	1	Rogue	2867	t	f	0	0	0	0	0	\N
638	1	Rogue	2868	t	f	0	0	0	0	0	\N
639	1	Rogue	2869	t	f	0	0	0	0	0	\N
640	1	Rogue	2871	t	f	0	0	0	0	0	\N
641	1	Rogue	2876	t	f	0	0	0	0	0	\N
642	1	Rogue	2881	t	f	0	0	0	0	0	\N
643	1	Rogue	2883	t	f	0	0	0	0	0	\N
644	1	Rogue	2884	t	f	0	0	0	0	0	\N
645	1	Rogue	2885	t	f	0	0	0	0	0	\N
646	1	Rogue	2886	t	f	0	0	0	0	0	\N
647	1	Rogue	2887	t	f	0	0	0	0	0	\N
648	1	Rogue	2888	t	f	0	0	0	0	0	\N
649	1	Rogue	2891	t	f	0	0	0	0	0	\N
650	1	Rogue	2892	t	f	0	0	0	0	0	\N
651	1	Rogue	2894	t	f	0	0	0	0	0	\N
652	1	Rogue	2895	t	f	0	0	0	0	0	\N
653	1	Rogue	2896	t	f	0	0	0	0	0	\N
654	1	Rogue	2898	t	f	0	0	0	0	0	\N
655	1	Rogue	2903	t	f	0	0	0	0	0	\N
656	1	Rogue	2904	t	f	0	0	0	0	0	\N
657	1	Rogue	2906	t	f	0	0	0	0	0	\N
658	1	Rogue	2911	t	f	0	0	0	0	0	\N
659	1	Rogue	2913	t	f	0	0	0	0	0	\N
660	1	Rogue	2914	t	f	0	0	0	0	0	\N
661	1	Rogue	2915	t	f	0	0	0	0	0	\N
662	1	Rogue	2916	t	f	0	0	0	0	0	\N
663	1	Rogue	2917	t	f	0	0	0	0	0	\N
664	1	Rogue	2918	t	f	0	0	0	0	0	\N
665	1	Rogue	2920	t	f	0	0	0	0	0	\N
666	1	Rogue	2921	t	f	0	0	0	0	0	\N
667	1	Rogue	2922	t	f	0	0	0	0	0	\N
668	1	Rogue	2927	t	f	0	0	0	0	0	\N
669	1	Rogue	2928	t	f	0	0	0	0	0	\N
670	1	Rogue	2929	t	f	0	0	0	0	0	\N
671	1	Rogue	2931	t	f	0	0	0	0	0	\N
672	1	Rogue	2932	t	f	0	0	0	0	0	\N
673	1	Rogue	2933	t	f	0	0	0	0	0	\N
674	1	Rogue	2934	t	f	0	0	0	0	0	\N
675	1	Rogue	2936	t	f	0	0	0	0	0	\N
676	1	Rogue	2937	t	f	0	0	0	0	0	\N
677	1	Rogue	2938	t	f	0	0	0	0	0	\N
678	1	Rogue	2939	t	f	0	0	0	0	0	\N
679	1	Rogue	2940	t	f	0	0	0	0	0	\N
680	1	Rogue	2941	t	f	0	0	0	0	0	\N
681	1	Rogue	2942	t	f	0	0	0	0	0	\N
682	1	Rogue	2947	t	f	0	0	0	0	0	\N
683	1	Rogue	2953	t	f	0	0	0	0	0	\N
684	1	Rogue	2954	t	f	0	0	0	0	0	\N
685	1	Rogue	2957	t	f	0	0	0	0	0	\N
686	1	Rogue	2959	t	f	0	0	0	0	0	\N
687	1	Rogue	2960	t	f	0	0	0	0	0	\N
688	1	Rogue	2962	t	f	0	0	0	0	0	\N
689	1	Rogue	2965	t	f	0	0	0	0	0	\N
690	1	Rogue	2966	t	f	0	0	0	0	0	\N
691	1	Rogue	2967	t	f	0	0	0	0	0	\N
692	1	Rogue	2968	t	f	0	0	0	0	0	\N
693	1	Rogue	2972	t	f	0	0	0	0	0	\N
694	1	Rogue	2976	t	f	0	0	0	0	0	\N
695	1	Rogue	2979	t	f	0	0	0	0	0	\N
696	1	Rogue	2983	t	f	0	0	0	0	0	\N
697	1	Rogue	2984	t	f	0	0	0	0	0	\N
698	1	Rogue	2985	t	f	0	0	0	0	0	\N
699	1	Rogue	2988	t	f	0	0	0	0	0	\N
700	1	Rogue	2989	t	f	0	0	0	0	0	\N
701	1	Rogue	2994	t	f	0	0	0	0	0	\N
702	1	Rogue	2996	t	f	0	0	0	0	0	\N
703	1	Rogue	2997	t	f	0	0	0	0	0	\N
704	1	Rogue	2998	t	f	0	0	0	0	0	\N
705	1	Rogue	2999	t	f	0	0	0	0	0	\N
706	1	Rogue	3003	t	f	0	0	0	0	0	\N
707	1	Rogue	3005	t	f	0	0	0	0	0	\N
708	1	Rogue	3006	t	f	0	0	0	0	0	\N
709	1	Rogue	3008	t	f	0	0	0	0	0	\N
710	1	Rogue	3011	t	f	0	0	0	0	0	\N
711	1	Rogue	3012	t	f	0	0	0	0	0	\N
712	1	Rogue	3013	t	f	0	0	0	0	0	\N
713	1	Rogue	3015	t	f	0	0	0	0	0	\N
714	1	Rogue	3016	t	f	0	0	0	0	0	\N
715	1	Rogue	3017	t	f	0	0	0	0	0	\N
716	1	Rogue	3019	t	f	0	0	0	0	0	\N
717	1	Rogue	3020	t	f	0	0	0	0	0	\N
718	1	Rogue	3021	t	f	0	0	0	0	0	\N
719	1	Rogue	3022	t	f	0	0	0	0	0	\N
720	1	Rogue	3024	t	f	0	0	0	0	0	\N
721	1	Rogue	3025	t	f	0	0	0	0	0	\N
722	1	Rogue	3026	t	f	0	0	0	0	0	\N
723	1	Rogue	3027	t	f	0	0	0	0	0	\N
724	1	Rogue	3032	t	f	0	0	0	0	0	\N
725	1	Rogue	3033	t	f	0	0	0	0	0	\N
726	1	Rogue	3035	t	f	0	0	0	0	0	\N
727	1	Rogue	3037	t	f	0	0	0	0	0	\N
728	1	Rogue	3038	t	f	0	0	0	0	0	\N
729	1	Rogue	3039	t	f	0	0	0	0	0	\N
730	1	Rogue	3040	t	f	0	0	0	0	0	\N
731	1	Rogue	3041	t	f	0	0	0	0	0	\N
732	1	Rogue	3042	t	f	0	0	0	0	0	\N
733	1	Rogue	3043	t	f	0	0	0	0	0	\N
734	1	Rogue	3047	t	f	0	0	0	0	0	\N
735	1	Rogue	3048	t	f	0	0	0	0	0	\N
736	1	Rogue	3050	t	f	0	0	0	0	0	\N
737	1	Rogue	3053	t	f	0	0	0	0	0	\N
738	1	Rogue	3054	t	f	0	0	0	0	0	\N
739	1	Rogue	3060	t	f	0	0	0	0	0	\N
740	1	Rogue	3062	t	f	0	0	0	0	0	\N
\.


--
-- Data for Name: galaxies; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.galaxies (id, allow_new_players, creation_date, name) FROM stdin;
1	t	2023-05-25 14:57:12.125081+00	Andromeda
\.


--
-- Data for Name: planet_building_pendings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_building_pendings (id, planet_id, db_building_id, starting_date, ending_time, loop, count) FROM stdin;
\.


--
-- Data for Name: planet_buildings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_buildings (planet_id, db_building_id, count) FROM stdin;
\.


--
-- Data for Name: planet_ship_pendings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_ship_pendings (id, planet_id, db_ship_id, starting_date, ending_date, count, loop) FROM stdin;
\.


--
-- Data for Name: planet_ships; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_ships (planet_id, db_ship_id, count) FROM stdin;
\.


--
-- Data for Name: planet_training_pendings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planet_training_pendings (id, planet_id, starting_date, ending_date, scientist_count, soldier_count, loop) FROM stdin;
\.


--
-- Data for Name: planets; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.planets (id, profile_id, name, galaxy_id, sector, number, floor_count, space_count, ore_count, hydro_count, energy_count, worker_count, scientist_count, soldier_count, prod_last_date, spawn_ore, spawn_hydro, orbit_ore, orbit_hydro, next_battle_date, recruit_worker) FROM stdin;
838	\N	\N	1	1	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
839	\N	\N	1	1	2	0	0	0	0	0	0	0	0	\N	23991	0	0	0	\N	t
840	\N	\N	1	1	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
841	\N	\N	1	1	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
842	\N	\N	1	1	5	0	0	0	0	0	0	0	0	\N	23136	0	0	0	\N	t
843	\N	\N	1	1	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
844	\N	\N	1	1	7	0	0	0	0	0	0	0	0	\N	24290	0	0	0	\N	t
845	\N	\N	1	1	8	0	0	0	0	0	0	0	0	\N	25721	0	0	0	\N	t
846	\N	\N	1	1	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
847	\N	\N	1	1	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
848	\N	\N	1	1	11	0	0	0	0	0	0	0	0	\N	0	22875	0	0	\N	t
849	\N	\N	1	1	12	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
850	\N	\N	1	1	13	0	0	0	0	0	0	0	0	\N	26784	0	0	0	\N	t
851	\N	\N	1	1	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
852	\N	\N	1	1	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
853	\N	\N	1	1	16	0	0	0	0	0	0	0	0	\N	24945	0	0	0	\N	t
854	\N	\N	1	1	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
855	\N	\N	1	1	18	0	0	0	0	0	0	0	0	\N	24250	0	0	0	\N	t
856	\N	\N	1	1	19	0	0	0	0	0	0	0	0	\N	0	24573	0	0	\N	t
857	\N	\N	1	1	20	0	0	0	0	0	0	0	0	\N	22437	0	0	0	\N	t
858	\N	\N	1	1	21	0	0	0	0	0	0	0	0	\N	26835	0	0	0	\N	t
859	\N	\N	1	1	22	0	0	0	0	0	0	0	0	\N	22982	0	0	0	\N	t
860	\N	\N	1	1	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
861	\N	\N	1	1	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
862	\N	\N	1	1	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
863	\N	\N	1	2	1	0	0	0	0	0	0	0	0	\N	22093	0	0	0	\N	t
864	\N	\N	1	2	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
865	\N	\N	1	2	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
866	\N	\N	1	2	4	0	0	0	0	0	0	0	0	\N	24340	0	0	0	\N	t
867	\N	\N	1	2	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
868	\N	\N	1	2	6	0	0	0	0	0	0	0	0	\N	0	25512	0	0	\N	t
869	\N	\N	1	2	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
870	\N	\N	1	2	8	0	0	0	0	0	0	0	0	\N	22380	0	0	0	\N	t
871	\N	\N	1	2	9	0	0	0	0	0	0	0	0	\N	23526	0	0	0	\N	t
872	\N	\N	1	2	10	0	0	0	0	0	0	0	0	\N	24808	0	0	0	\N	t
873	\N	\N	1	2	11	0	0	0	0	0	0	0	0	\N	23078	0	0	0	\N	t
874	\N	\N	1	2	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
875	\N	\N	1	2	13	0	0	0	0	0	0	0	0	\N	23620	0	0	0	\N	t
876	\N	\N	1	2	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
877	\N	\N	1	2	15	0	0	0	0	0	0	0	0	\N	24678	0	0	0	\N	t
878	\N	\N	1	2	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
879	\N	\N	1	2	17	0	0	0	0	0	0	0	0	\N	24336	0	0	0	\N	t
880	\N	\N	1	2	18	0	0	0	0	0	0	0	0	\N	25833	0	0	0	\N	t
881	\N	\N	1	2	19	0	0	0	0	0	0	0	0	\N	25916	0	0	0	\N	t
882	\N	\N	1	2	20	0	0	0	0	0	0	0	0	\N	24239	0	0	0	\N	t
883	\N	\N	1	2	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
884	\N	\N	1	2	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
885	\N	\N	1	2	23	0	0	0	0	0	0	0	0	\N	25980	0	0	0	\N	t
886	\N	\N	1	2	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
887	\N	\N	1	2	25	0	0	0	0	0	0	0	0	\N	22699	0	0	0	\N	t
888	\N	\N	1	3	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
889	\N	\N	1	3	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
890	\N	\N	1	3	3	0	0	0	0	0	0	0	0	\N	25711	0	0	0	\N	t
891	\N	\N	1	3	4	0	0	0	0	0	0	0	0	\N	0	22363	0	0	\N	t
892	\N	\N	1	3	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
893	\N	\N	1	3	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
894	\N	\N	1	3	7	0	0	0	0	0	0	0	0	\N	25987	0	0	0	\N	t
895	\N	\N	1	3	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
896	\N	\N	1	3	9	0	0	0	0	0	0	0	0	\N	0	22199	0	0	\N	t
897	\N	\N	1	3	10	0	0	0	0	0	0	0	0	\N	22261	0	0	0	\N	t
898	\N	\N	1	3	11	0	0	0	0	0	0	0	0	\N	26158	0	0	0	\N	t
899	\N	\N	1	3	12	0	0	0	0	0	0	0	0	\N	23784	0	0	0	\N	t
900	\N	\N	1	3	13	0	0	0	0	0	0	0	0	\N	23766	0	0	0	\N	t
901	\N	\N	1	3	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
902	\N	\N	1	3	15	0	0	0	0	0	0	0	0	\N	25984	0	0	0	\N	t
903	\N	\N	1	3	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
904	\N	\N	1	3	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
905	\N	\N	1	3	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
906	\N	\N	1	3	19	0	0	0	0	0	0	0	0	\N	0	22186	0	0	\N	t
907	\N	\N	1	3	20	0	0	0	0	0	0	0	0	\N	26512	0	0	0	\N	t
908	\N	\N	1	3	21	0	0	0	0	0	0	0	0	\N	0	22830	0	0	\N	t
909	\N	\N	1	3	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
910	\N	\N	1	3	23	0	0	0	0	0	0	0	0	\N	26099	0	0	0	\N	t
911	\N	\N	1	3	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
912	\N	\N	1	3	25	0	0	0	0	0	0	0	0	\N	25453	0	0	0	\N	t
913	\N	\N	1	4	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
914	\N	\N	1	4	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
915	\N	\N	1	4	3	0	0	0	0	0	0	0	0	\N	26196	0	0	0	\N	t
916	\N	\N	1	4	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
917	\N	\N	1	4	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
918	\N	\N	1	4	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
919	\N	\N	1	4	7	0	0	0	0	0	0	0	0	\N	0	25557	0	0	\N	t
920	\N	\N	1	4	8	0	0	0	0	0	0	0	0	\N	22824	0	0	0	\N	t
921	\N	\N	1	4	9	0	0	0	0	0	0	0	0	\N	24829	0	0	0	\N	t
922	\N	\N	1	4	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
923	\N	\N	1	4	11	0	0	0	0	0	0	0	0	\N	22770	0	0	0	\N	t
924	\N	\N	1	4	12	0	0	0	0	0	0	0	0	\N	26822	0	0	0	\N	t
925	\N	\N	1	4	13	0	0	0	0	0	0	0	0	\N	0	22962	0	0	\N	t
926	\N	\N	1	4	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
927	\N	\N	1	4	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
928	\N	\N	1	4	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
929	\N	\N	1	4	17	0	0	0	0	0	0	0	0	\N	25508	0	0	0	\N	t
930	\N	\N	1	4	18	0	0	0	0	0	0	0	0	\N	0	22028	0	0	\N	t
931	\N	\N	1	4	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
932	\N	\N	1	4	20	0	0	0	0	0	0	0	0	\N	0	25920	0	0	\N	t
933	\N	\N	1	4	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
934	\N	\N	1	4	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
935	\N	\N	1	4	23	0	0	0	0	0	0	0	0	\N	24275	0	0	0	\N	t
936	\N	\N	1	4	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
937	\N	\N	1	4	25	0	0	0	0	0	0	0	0	\N	26094	0	0	0	\N	t
938	\N	\N	1	5	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
939	\N	\N	1	5	2	0	0	0	0	0	0	0	0	\N	23484	0	0	0	\N	t
940	\N	\N	1	5	3	0	0	0	0	0	0	0	0	\N	0	25458	0	0	\N	t
941	\N	\N	1	5	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
942	\N	\N	1	5	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
943	\N	\N	1	5	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
944	\N	\N	1	5	7	0	0	0	0	0	0	0	0	\N	23983	0	0	0	\N	t
945	\N	\N	1	5	8	0	0	0	0	0	0	0	0	\N	26865	0	0	0	\N	t
946	\N	\N	1	5	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
947	\N	\N	1	5	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
948	\N	\N	1	5	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
949	\N	\N	1	5	12	0	0	0	0	0	0	0	0	\N	24552	0	0	0	\N	t
950	\N	\N	1	5	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
951	\N	\N	1	5	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
952	\N	\N	1	5	15	0	0	0	0	0	0	0	0	\N	23194	0	0	0	\N	t
953	\N	\N	1	5	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
954	\N	\N	1	5	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
955	\N	\N	1	5	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
956	\N	\N	1	5	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
957	\N	\N	1	5	20	0	0	0	0	0	0	0	0	\N	23677	0	0	0	\N	t
958	\N	\N	1	5	21	0	0	0	0	0	0	0	0	\N	25847	0	0	0	\N	t
959	\N	\N	1	5	22	0	0	0	0	0	0	0	0	\N	25872	0	0	0	\N	t
960	\N	\N	1	5	23	0	0	0	0	0	0	0	0	\N	25452	0	0	0	\N	t
961	\N	\N	1	5	24	0	0	0	0	0	0	0	0	\N	25755	0	0	0	\N	t
962	\N	\N	1	5	25	0	0	0	0	0	0	0	0	\N	22510	0	0	0	\N	t
963	\N	\N	1	6	1	0	0	0	0	0	0	0	0	\N	25336	0	0	0	\N	t
964	\N	\N	1	6	2	0	0	0	0	0	0	0	0	\N	23646	0	0	0	\N	t
965	\N	\N	1	6	3	0	0	0	0	0	0	0	0	\N	23410	0	0	0	\N	t
966	\N	\N	1	6	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
967	\N	\N	1	6	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
968	\N	\N	1	6	6	0	0	0	0	0	0	0	0	\N	24282	0	0	0	\N	t
969	\N	\N	1	6	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
970	\N	\N	1	6	8	0	0	0	0	0	0	0	0	\N	0	25937	0	0	\N	t
971	\N	\N	1	6	9	0	0	0	0	0	0	0	0	\N	26104	0	0	0	\N	t
972	\N	\N	1	6	10	0	0	0	0	0	0	0	0	\N	26586	0	0	0	\N	t
973	\N	\N	1	6	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
974	\N	\N	1	6	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
975	\N	\N	1	6	13	0	0	0	0	0	0	0	0	\N	23124	0	0	0	\N	t
976	\N	\N	1	6	14	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
977	\N	\N	1	6	15	0	0	0	0	0	0	0	0	\N	0	26161	0	0	\N	t
978	\N	\N	1	6	16	0	0	0	0	0	0	0	0	\N	25600	0	0	0	\N	t
979	\N	\N	1	6	17	0	0	0	0	0	0	0	0	\N	26401	0	0	0	\N	t
980	\N	\N	1	6	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
981	\N	\N	1	6	19	0	0	0	0	0	0	0	0	\N	26121	0	0	0	\N	t
982	\N	\N	1	6	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
983	\N	\N	1	6	21	0	0	0	0	0	0	0	0	\N	23914	0	0	0	\N	t
984	\N	\N	1	6	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
985	\N	\N	1	6	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
986	\N	\N	1	6	24	0	0	0	0	0	0	0	0	\N	24053	0	0	0	\N	t
987	\N	\N	1	6	25	0	0	0	0	0	0	0	0	\N	22586	0	0	0	\N	t
988	\N	\N	1	7	1	0	0	0	0	0	0	0	0	\N	0	25323	0	0	\N	t
989	\N	\N	1	7	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
990	\N	\N	1	7	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
991	\N	\N	1	7	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
992	\N	\N	1	7	5	0	0	0	0	0	0	0	0	\N	25271	0	0	0	\N	t
993	\N	\N	1	7	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
994	\N	\N	1	7	7	0	0	0	0	0	0	0	0	\N	0	22629	0	0	\N	t
995	\N	\N	1	7	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
996	\N	\N	1	7	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
997	\N	\N	1	7	10	0	0	0	0	0	0	0	0	\N	22275	0	0	0	\N	t
998	\N	\N	1	7	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
999	\N	\N	1	7	12	0	0	0	0	0	0	0	0	\N	22842	0	0	0	\N	t
1000	\N	\N	1	7	13	0	0	0	0	0	0	0	0	\N	24011	0	0	0	\N	t
1001	\N	\N	1	7	14	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1002	\N	\N	1	7	15	0	0	0	0	0	0	0	0	\N	23836	0	0	0	\N	t
1003	\N	\N	1	7	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1004	\N	\N	1	7	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1005	\N	\N	1	7	18	0	0	0	0	0	0	0	0	\N	26184	0	0	0	\N	t
1006	\N	\N	1	7	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1007	\N	\N	1	7	20	0	0	0	0	0	0	0	0	\N	25664	0	0	0	\N	t
1008	\N	\N	1	7	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1009	\N	\N	1	7	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1010	\N	\N	1	7	23	0	0	0	0	0	0	0	0	\N	23966	0	0	0	\N	t
1011	\N	\N	1	7	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1012	\N	\N	1	7	25	0	0	0	0	0	0	0	0	\N	22999	0	0	0	\N	t
1013	\N	\N	1	8	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1014	\N	\N	1	8	2	0	0	0	0	0	0	0	0	\N	25892	0	0	0	\N	t
1015	\N	\N	1	8	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1016	\N	\N	1	8	4	0	0	0	0	0	0	0	0	\N	24868	0	0	0	\N	t
1017	\N	\N	1	8	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1018	\N	\N	1	8	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1019	\N	\N	1	8	7	0	0	0	0	0	0	0	0	\N	23309	0	0	0	\N	t
1020	\N	\N	1	8	8	0	0	0	0	0	0	0	0	\N	24792	0	0	0	\N	t
1021	\N	\N	1	8	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1022	\N	\N	1	8	10	0	0	0	0	0	0	0	0	\N	24813	0	0	0	\N	t
1023	\N	\N	1	8	11	0	0	0	0	0	0	0	0	\N	24233	0	0	0	\N	t
1024	\N	\N	1	8	12	0	0	0	0	0	0	0	0	\N	22900	0	0	0	\N	t
1025	\N	\N	1	8	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1026	\N	\N	1	8	14	0	0	0	0	0	0	0	0	\N	26265	0	0	0	\N	t
1027	\N	\N	1	8	15	0	0	0	0	0	0	0	0	\N	0	23250	0	0	\N	t
1028	\N	\N	1	8	16	0	0	0	0	0	0	0	0	\N	25578	0	0	0	\N	t
1029	\N	\N	1	8	17	0	0	0	0	0	0	0	0	\N	26528	0	0	0	\N	t
1030	\N	\N	1	8	18	0	0	0	0	0	0	0	0	\N	23009	0	0	0	\N	t
1031	\N	\N	1	8	19	0	0	0	0	0	0	0	0	\N	24079	0	0	0	\N	t
1032	\N	\N	1	8	20	0	0	0	0	0	0	0	0	\N	24674	0	0	0	\N	t
1033	\N	\N	1	8	21	0	0	0	0	0	0	0	0	\N	0	22747	0	0	\N	t
1034	\N	\N	1	8	22	0	0	0	0	0	0	0	0	\N	26699	0	0	0	\N	t
1035	\N	\N	1	8	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1036	\N	\N	1	8	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1037	\N	\N	1	8	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1038	\N	\N	1	9	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1039	\N	\N	1	9	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1040	\N	\N	1	9	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1041	\N	\N	1	9	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1042	\N	\N	1	9	5	0	0	0	0	0	0	0	0	\N	23133	0	0	0	\N	t
1043	\N	\N	1	9	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1044	\N	\N	1	9	7	0	0	0	0	0	0	0	0	\N	0	22953	0	0	\N	t
1045	\N	\N	1	9	8	0	0	0	0	0	0	0	0	\N	24485	0	0	0	\N	t
1046	\N	\N	1	9	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1047	\N	\N	1	9	10	0	0	0	0	0	0	0	0	\N	0	24445	0	0	\N	t
1048	\N	\N	1	9	11	0	0	0	0	0	0	0	0	\N	0	26370	0	0	\N	t
1049	\N	\N	1	9	12	0	0	0	0	0	0	0	0	\N	0	24371	0	0	\N	t
1050	\N	\N	1	9	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1051	\N	\N	1	9	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1052	\N	\N	1	9	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1053	\N	\N	1	9	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1054	\N	\N	1	9	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1055	\N	\N	1	9	18	0	0	0	0	0	0	0	0	\N	24151	0	0	0	\N	t
1056	\N	\N	1	9	19	0	0	0	0	0	0	0	0	\N	0	24088	0	0	\N	t
1057	\N	\N	1	9	20	0	0	0	0	0	0	0	0	\N	25833	0	0	0	\N	t
1058	\N	\N	1	9	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1059	\N	\N	1	9	22	0	0	0	0	0	0	0	0	\N	24760	0	0	0	\N	t
1060	\N	\N	1	9	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1061	\N	\N	1	9	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1062	\N	\N	1	9	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1063	\N	\N	1	10	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1064	\N	\N	1	10	2	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1065	\N	\N	1	10	3	0	0	0	0	0	0	0	0	\N	23379	0	0	0	\N	t
1066	\N	\N	1	10	4	0	0	0	0	0	0	0	0	\N	24956	0	0	0	\N	t
1067	\N	\N	1	10	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1068	\N	\N	1	10	6	0	0	0	0	0	0	0	0	\N	24277	0	0	0	\N	t
1069	\N	\N	1	10	7	0	0	0	0	0	0	0	0	\N	22103	0	0	0	\N	t
1070	\N	\N	1	10	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1071	\N	\N	1	10	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1072	\N	\N	1	10	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1073	\N	\N	1	10	11	0	0	0	0	0	0	0	0	\N	22885	0	0	0	\N	t
1074	\N	\N	1	10	12	0	0	0	0	0	0	0	0	\N	26505	0	0	0	\N	t
1075	\N	\N	1	10	13	0	0	0	0	0	0	0	0	\N	22089	0	0	0	\N	t
1076	\N	\N	1	10	14	0	0	0	0	0	0	0	0	\N	23214	0	0	0	\N	t
1077	\N	\N	1	10	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1078	\N	\N	1	10	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1079	\N	\N	1	10	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1080	\N	\N	1	10	18	0	0	0	0	0	0	0	0	\N	25025	0	0	0	\N	t
1081	\N	\N	1	10	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1082	\N	\N	1	10	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1083	\N	\N	1	10	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1084	\N	\N	1	10	22	0	0	0	0	0	0	0	0	\N	26978	0	0	0	\N	t
1085	\N	\N	1	10	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1086	\N	\N	1	10	24	0	0	0	0	0	0	0	0	\N	22792	0	0	0	\N	t
1087	\N	\N	1	10	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1088	\N	\N	1	11	1	0	0	0	0	0	0	0	0	\N	26708	0	0	0	\N	t
1089	\N	\N	1	11	2	0	0	0	0	0	0	0	0	\N	25842	0	0	0	\N	t
1090	\N	\N	1	11	3	0	0	0	0	0	0	0	0	\N	0	25750	0	0	\N	t
1091	\N	\N	1	11	4	0	0	0	0	0	0	0	0	\N	0	22277	0	0	\N	t
1092	\N	\N	1	11	5	0	0	0	0	0	0	0	0	\N	25597	0	0	0	\N	t
1093	\N	\N	1	11	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1094	\N	\N	1	11	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1095	\N	\N	1	11	8	0	0	0	0	0	0	0	0	\N	23440	0	0	0	\N	t
1096	\N	\N	1	11	9	0	0	0	0	0	0	0	0	\N	22550	0	0	0	\N	t
1097	\N	\N	1	11	10	0	0	0	0	0	0	0	0	\N	23064	0	0	0	\N	t
1098	\N	\N	1	11	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1099	\N	\N	1	11	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1100	\N	\N	1	11	13	0	0	0	0	0	0	0	0	\N	24508	0	0	0	\N	t
1101	\N	\N	1	11	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1102	\N	\N	1	11	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1103	\N	\N	1	11	16	0	0	0	0	0	0	0	0	\N	26602	0	0	0	\N	t
1104	\N	\N	1	11	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1105	\N	\N	1	11	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1106	\N	\N	1	11	19	0	0	0	0	0	0	0	0	\N	0	26050	0	0	\N	t
1107	\N	\N	1	11	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1108	\N	\N	1	11	21	0	0	0	0	0	0	0	0	\N	23783	0	0	0	\N	t
1109	\N	\N	1	11	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1110	\N	\N	1	11	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1111	\N	\N	1	11	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1112	\N	\N	1	11	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1113	\N	\N	1	12	1	0	0	0	0	0	0	0	0	\N	26005	0	0	0	\N	t
1114	\N	\N	1	12	2	0	0	0	0	0	0	0	0	\N	0	26903	0	0	\N	t
1115	\N	\N	1	12	3	0	0	0	0	0	0	0	0	\N	23910	0	0	0	\N	t
1116	\N	\N	1	12	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1117	\N	\N	1	12	5	0	0	0	0	0	0	0	0	\N	26113	0	0	0	\N	t
1118	\N	\N	1	12	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1119	\N	\N	1	12	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1120	\N	\N	1	12	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1121	\N	\N	1	12	9	0	0	0	0	0	0	0	0	\N	0	23538	0	0	\N	t
1122	\N	\N	1	12	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1123	\N	\N	1	12	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1124	\N	\N	1	12	12	0	0	0	0	0	0	0	0	\N	22415	0	0	0	\N	t
1125	\N	\N	1	12	13	0	0	0	0	0	0	0	0	\N	22688	0	0	0	\N	t
1126	\N	\N	1	12	14	0	0	0	0	0	0	0	0	\N	0	22572	0	0	\N	t
1127	\N	\N	1	12	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1128	\N	\N	1	12	16	0	0	0	0	0	0	0	0	\N	25202	0	0	0	\N	t
1129	\N	\N	1	12	17	0	0	0	0	0	0	0	0	\N	25335	0	0	0	\N	t
1130	\N	\N	1	12	18	0	0	0	0	0	0	0	0	\N	26246	0	0	0	\N	t
1131	\N	\N	1	12	19	0	0	0	0	0	0	0	0	\N	22933	0	0	0	\N	t
1132	\N	\N	1	12	20	0	0	0	0	0	0	0	0	\N	22570	0	0	0	\N	t
1133	\N	\N	1	12	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1134	\N	\N	1	12	22	0	0	0	0	0	0	0	0	\N	24585	0	0	0	\N	t
1135	\N	\N	1	12	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1136	\N	\N	1	12	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1137	\N	\N	1	12	25	0	0	0	0	0	0	0	0	\N	25805	0	0	0	\N	t
1138	\N	\N	1	13	1	0	0	0	0	0	0	0	0	\N	24061	0	0	0	\N	t
1139	\N	\N	1	13	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1140	\N	\N	1	13	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1141	\N	\N	1	13	4	0	0	0	0	0	0	0	0	\N	0	23252	0	0	\N	t
1142	\N	\N	1	13	5	0	0	0	0	0	0	0	0	\N	26004	0	0	0	\N	t
1143	\N	\N	1	13	6	0	0	0	0	0	0	0	0	\N	0	25148	0	0	\N	t
1144	\N	\N	1	13	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1145	\N	\N	1	13	8	0	0	0	0	0	0	0	0	\N	23668	0	0	0	\N	t
1146	\N	\N	1	13	9	0	0	0	0	0	0	0	0	\N	23475	0	0	0	\N	t
1147	\N	\N	1	13	10	0	0	0	0	0	0	0	0	\N	25081	0	0	0	\N	t
1148	\N	\N	1	13	11	0	0	0	0	0	0	0	0	\N	26496	0	0	0	\N	t
1149	\N	\N	1	13	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1150	\N	\N	1	13	13	0	0	0	0	0	0	0	0	\N	24200	0	0	0	\N	t
1151	\N	\N	1	13	14	0	0	0	0	0	0	0	0	\N	22388	0	0	0	\N	t
1152	\N	\N	1	13	15	0	0	0	0	0	0	0	0	\N	26394	0	0	0	\N	t
1153	\N	\N	1	13	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1154	\N	\N	1	13	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1155	\N	\N	1	13	18	0	0	0	0	0	0	0	0	\N	25016	0	0	0	\N	t
1156	\N	\N	1	13	19	0	0	0	0	0	0	0	0	\N	25445	0	0	0	\N	t
1157	\N	\N	1	13	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1158	\N	\N	1	13	21	0	0	0	0	0	0	0	0	\N	26069	0	0	0	\N	t
1159	\N	\N	1	13	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1160	\N	\N	1	13	23	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1161	\N	\N	1	13	24	0	0	0	0	0	0	0	0	\N	0	22266	0	0	\N	t
1162	\N	\N	1	13	25	0	0	0	0	0	0	0	0	\N	26402	0	0	0	\N	t
1163	\N	\N	1	14	1	0	0	0	0	0	0	0	0	\N	25829	0	0	0	\N	t
1164	\N	\N	1	14	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1165	\N	\N	1	14	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1166	\N	\N	1	14	4	0	0	0	0	0	0	0	0	\N	25018	0	0	0	\N	t
1167	\N	\N	1	14	5	0	0	0	0	0	0	0	0	\N	0	24512	0	0	\N	t
1168	\N	\N	1	14	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1169	\N	\N	1	14	7	0	0	0	0	0	0	0	0	\N	23463	0	0	0	\N	t
1170	\N	\N	1	14	8	0	0	0	0	0	0	0	0	\N	26537	0	0	0	\N	t
1171	\N	\N	1	14	9	0	0	0	0	0	0	0	0	\N	0	22442	0	0	\N	t
1172	\N	\N	1	14	10	0	0	0	0	0	0	0	0	\N	22996	0	0	0	\N	t
1173	\N	\N	1	14	11	0	0	0	0	0	0	0	0	\N	22676	0	0	0	\N	t
1174	\N	\N	1	14	12	0	0	0	0	0	0	0	0	\N	25101	0	0	0	\N	t
1175	\N	\N	1	14	13	0	0	0	0	0	0	0	0	\N	22695	0	0	0	\N	t
1176	\N	\N	1	14	14	0	0	0	0	0	0	0	0	\N	24184	0	0	0	\N	t
1177	\N	\N	1	14	15	0	0	0	0	0	0	0	0	\N	22456	0	0	0	\N	t
1178	\N	\N	1	14	16	0	0	0	0	0	0	0	0	\N	0	25747	0	0	\N	t
1179	\N	\N	1	14	17	0	0	0	0	0	0	0	0	\N	22004	0	0	0	\N	t
1180	\N	\N	1	14	18	0	0	0	0	0	0	0	0	\N	22683	0	0	0	\N	t
1181	\N	\N	1	14	19	0	0	0	0	0	0	0	0	\N	25894	0	0	0	\N	t
1182	\N	\N	1	14	20	0	0	0	0	0	0	0	0	\N	25748	0	0	0	\N	t
1183	\N	\N	1	14	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1184	\N	\N	1	14	22	0	0	0	0	0	0	0	0	\N	26444	0	0	0	\N	t
1185	\N	\N	1	14	23	0	0	0	0	0	0	0	0	\N	22378	0	0	0	\N	t
1186	\N	\N	1	14	24	0	0	0	0	0	0	0	0	\N	0	23789	0	0	\N	t
1187	\N	\N	1	14	25	0	0	0	0	0	0	0	0	\N	24628	0	0	0	\N	t
1188	\N	\N	1	15	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1189	\N	\N	1	15	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1190	\N	\N	1	15	3	0	0	0	0	0	0	0	0	\N	26434	0	0	0	\N	t
1191	\N	\N	1	15	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1192	\N	\N	1	15	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1193	\N	\N	1	15	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1194	\N	\N	1	15	7	0	0	0	0	0	0	0	0	\N	0	25975	0	0	\N	t
1195	\N	\N	1	15	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1196	\N	\N	1	15	9	0	0	0	0	0	0	0	0	\N	25361	0	0	0	\N	t
1197	\N	\N	1	15	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1198	\N	\N	1	15	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1199	\N	\N	1	15	12	0	0	0	0	0	0	0	0	\N	22792	0	0	0	\N	t
1200	\N	\N	1	15	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1201	\N	\N	1	15	14	0	0	0	0	0	0	0	0	\N	22308	0	0	0	\N	t
1202	\N	\N	1	15	15	0	0	0	0	0	0	0	0	\N	24047	0	0	0	\N	t
1203	\N	\N	1	15	16	0	0	0	0	0	0	0	0	\N	0	25519	0	0	\N	t
1204	\N	\N	1	15	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1205	\N	\N	1	15	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1206	\N	\N	1	15	19	0	0	0	0	0	0	0	0	\N	25652	0	0	0	\N	t
1207	\N	\N	1	15	20	0	0	0	0	0	0	0	0	\N	0	26777	0	0	\N	t
1208	\N	\N	1	15	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1209	\N	\N	1	15	22	0	0	0	0	0	0	0	0	\N	24139	0	0	0	\N	t
1210	\N	\N	1	15	23	0	0	0	0	0	0	0	0	\N	23737	0	0	0	\N	t
1211	\N	\N	1	15	24	0	0	0	0	0	0	0	0	\N	0	24713	0	0	\N	t
1212	\N	\N	1	15	25	0	0	0	0	0	0	0	0	\N	23272	0	0	0	\N	t
1213	\N	\N	1	16	1	0	0	0	0	0	0	0	0	\N	0	23302	0	0	\N	t
1214	\N	\N	1	16	2	0	0	0	0	0	0	0	0	\N	24446	0	0	0	\N	t
1215	\N	\N	1	16	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1216	\N	\N	1	16	4	0	0	0	0	0	0	0	0	\N	26705	0	0	0	\N	t
1217	\N	\N	1	16	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1218	\N	\N	1	16	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1219	\N	\N	1	16	7	0	0	0	0	0	0	0	0	\N	25709	0	0	0	\N	t
1220	\N	\N	1	16	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1221	\N	\N	1	16	9	0	0	0	0	0	0	0	0	\N	0	25700	0	0	\N	t
1222	\N	\N	1	16	10	0	0	0	0	0	0	0	0	\N	23430	0	0	0	\N	t
1223	\N	\N	1	16	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1224	\N	\N	1	16	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1225	\N	\N	1	16	13	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1226	\N	\N	1	16	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1227	\N	\N	1	16	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1228	\N	\N	1	16	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1229	\N	\N	1	16	17	0	0	0	0	0	0	0	0	\N	24864	0	0	0	\N	t
1230	\N	\N	1	16	18	0	0	0	0	0	0	0	0	\N	25764	0	0	0	\N	t
1231	\N	\N	1	16	19	0	0	0	0	0	0	0	0	\N	26161	0	0	0	\N	t
1232	\N	\N	1	16	20	0	0	0	0	0	0	0	0	\N	25274	0	0	0	\N	t
1233	\N	\N	1	16	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1234	\N	\N	1	16	22	0	0	0	0	0	0	0	0	\N	24548	0	0	0	\N	t
1235	\N	\N	1	16	23	0	0	0	0	0	0	0	0	\N	23823	0	0	0	\N	t
1236	\N	\N	1	16	24	0	0	0	0	0	0	0	0	\N	26100	0	0	0	\N	t
1237	\N	\N	1	16	25	0	0	0	0	0	0	0	0	\N	25928	0	0	0	\N	t
1238	\N	\N	1	17	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1239	\N	\N	1	17	2	0	0	0	0	0	0	0	0	\N	0	23182	0	0	\N	t
1240	\N	\N	1	17	3	0	0	0	0	0	0	0	0	\N	22824	0	0	0	\N	t
1241	\N	\N	1	17	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1242	\N	\N	1	17	5	0	0	0	0	0	0	0	0	\N	23780	0	0	0	\N	t
1243	\N	\N	1	17	6	0	0	0	0	0	0	0	0	\N	22836	0	0	0	\N	t
1244	\N	\N	1	17	7	0	0	0	0	0	0	0	0	\N	25234	0	0	0	\N	t
1245	\N	\N	1	17	8	0	0	0	0	0	0	0	0	\N	24849	0	0	0	\N	t
1246	\N	\N	1	17	9	0	0	0	0	0	0	0	0	\N	25030	0	0	0	\N	t
1247	\N	\N	1	17	10	0	0	0	0	0	0	0	0	\N	24542	0	0	0	\N	t
1248	\N	\N	1	17	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1249	\N	\N	1	17	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1250	\N	\N	1	17	13	0	0	0	0	0	0	0	0	\N	0	23446	0	0	\N	t
1251	\N	\N	1	17	14	0	0	0	0	0	0	0	0	\N	25036	0	0	0	\N	t
1252	\N	\N	1	17	15	0	0	0	0	0	0	0	0	\N	25448	0	0	0	\N	t
1253	\N	\N	1	17	16	0	0	0	0	0	0	0	0	\N	24706	0	0	0	\N	t
1254	\N	\N	1	17	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1255	\N	\N	1	17	18	0	0	0	0	0	0	0	0	\N	0	25508	0	0	\N	t
1256	\N	\N	1	17	19	0	0	0	0	0	0	0	0	\N	26127	0	0	0	\N	t
1257	\N	\N	1	17	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1258	\N	\N	1	17	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1259	\N	\N	1	17	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1260	\N	\N	1	17	23	0	0	0	0	0	0	0	0	\N	22006	0	0	0	\N	t
1261	\N	\N	1	17	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1262	\N	\N	1	17	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1263	\N	\N	1	18	1	0	0	0	0	0	0	0	0	\N	22156	0	0	0	\N	t
1264	\N	\N	1	18	2	0	0	0	0	0	0	0	0	\N	23463	0	0	0	\N	t
1265	\N	\N	1	18	3	0	0	0	0	0	0	0	0	\N	0	23686	0	0	\N	t
1266	\N	\N	1	18	4	0	0	0	0	0	0	0	0	\N	26002	0	0	0	\N	t
1267	\N	\N	1	18	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1268	\N	\N	1	18	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1269	\N	\N	1	18	7	0	0	0	0	0	0	0	0	\N	24227	0	0	0	\N	t
1270	\N	\N	1	18	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1271	\N	\N	1	18	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1272	\N	\N	1	18	10	0	0	0	0	0	0	0	0	\N	25751	0	0	0	\N	t
1273	\N	\N	1	18	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1274	\N	\N	1	18	12	0	0	0	0	0	0	0	0	\N	0	24540	0	0	\N	t
1275	\N	\N	1	18	13	0	0	0	0	0	0	0	0	\N	22888	0	0	0	\N	t
1276	\N	\N	1	18	14	0	0	0	0	0	0	0	0	\N	23028	0	0	0	\N	t
1277	\N	\N	1	18	15	0	0	0	0	0	0	0	0	\N	22947	0	0	0	\N	t
1278	\N	\N	1	18	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1279	\N	\N	1	18	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1280	\N	\N	1	18	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1281	\N	\N	1	18	19	0	0	0	0	0	0	0	0	\N	26486	0	0	0	\N	t
1282	\N	\N	1	18	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1283	\N	\N	1	18	21	0	0	0	0	0	0	0	0	\N	25327	0	0	0	\N	t
1284	\N	\N	1	18	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1285	\N	\N	1	18	23	0	0	0	0	0	0	0	0	\N	0	25829	0	0	\N	t
1286	\N	\N	1	18	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1287	\N	\N	1	18	25	0	0	0	0	0	0	0	0	\N	22656	0	0	0	\N	t
1288	\N	\N	1	19	1	0	0	0	0	0	0	0	0	\N	22308	0	0	0	\N	t
1289	\N	\N	1	19	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1290	\N	\N	1	19	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1291	\N	\N	1	19	4	0	0	0	0	0	0	0	0	\N	0	22983	0	0	\N	t
1292	\N	\N	1	19	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1293	\N	\N	1	19	6	0	0	0	0	0	0	0	0	\N	22025	0	0	0	\N	t
1294	\N	\N	1	19	7	0	0	0	0	0	0	0	0	\N	0	26064	0	0	\N	t
1295	\N	\N	1	19	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1296	\N	\N	1	19	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1297	\N	\N	1	19	10	0	0	0	0	0	0	0	0	\N	24144	0	0	0	\N	t
1298	\N	\N	1	19	11	0	0	0	0	0	0	0	0	\N	23150	0	0	0	\N	t
1299	\N	\N	1	19	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1300	\N	\N	1	19	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1301	\N	\N	1	19	14	0	0	0	0	0	0	0	0	\N	25373	0	0	0	\N	t
1302	\N	\N	1	19	15	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1303	\N	\N	1	19	16	0	0	0	0	0	0	0	0	\N	25659	0	0	0	\N	t
1304	\N	\N	1	19	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1305	\N	\N	1	19	18	0	0	0	0	0	0	0	0	\N	22716	0	0	0	\N	t
1306	\N	\N	1	19	19	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1307	\N	\N	1	19	20	0	0	0	0	0	0	0	0	\N	25565	0	0	0	\N	t
1308	\N	\N	1	19	21	0	0	0	0	0	0	0	0	\N	23367	0	0	0	\N	t
1309	\N	\N	1	19	22	0	0	0	0	0	0	0	0	\N	22790	0	0	0	\N	t
1310	\N	\N	1	19	23	0	0	0	0	0	0	0	0	\N	26410	0	0	0	\N	t
1311	\N	\N	1	19	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1312	\N	\N	1	19	25	0	0	0	0	0	0	0	0	\N	26738	0	0	0	\N	t
1313	\N	\N	1	20	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1314	\N	\N	1	20	2	0	0	0	0	0	0	0	0	\N	22606	0	0	0	\N	t
1315	\N	\N	1	20	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1316	\N	\N	1	20	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1317	\N	\N	1	20	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1318	\N	\N	1	20	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1319	\N	\N	1	20	7	0	0	0	0	0	0	0	0	\N	25889	0	0	0	\N	t
1320	\N	\N	1	20	8	0	0	0	0	0	0	0	0	\N	22963	0	0	0	\N	t
1321	\N	\N	1	20	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1322	\N	\N	1	20	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1323	\N	\N	1	20	11	0	0	0	0	0	0	0	0	\N	0	24750	0	0	\N	t
1324	\N	\N	1	20	12	0	0	0	0	0	0	0	0	\N	0	22400	0	0	\N	t
1325	\N	\N	1	20	13	0	0	0	0	0	0	0	0	\N	22848	0	0	0	\N	t
1326	\N	\N	1	20	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1327	\N	\N	1	20	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1328	\N	\N	1	20	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1329	\N	\N	1	20	17	0	0	0	0	0	0	0	0	\N	24834	0	0	0	\N	t
1330	\N	\N	1	20	18	0	0	0	0	0	0	0	0	\N	23222	0	0	0	\N	t
1331	\N	\N	1	20	19	0	0	0	0	0	0	0	0	\N	25675	0	0	0	\N	t
1332	\N	\N	1	20	20	0	0	0	0	0	0	0	0	\N	22379	0	0	0	\N	t
1333	\N	\N	1	20	21	0	0	0	0	0	0	0	0	\N	22126	0	0	0	\N	t
1334	\N	\N	1	20	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1335	\N	\N	1	20	23	0	0	0	0	0	0	0	0	\N	26910	0	0	0	\N	t
1336	\N	\N	1	20	24	0	0	0	0	0	0	0	0	\N	23795	0	0	0	\N	t
1337	\N	\N	1	20	25	0	0	0	0	0	0	0	0	\N	22414	0	0	0	\N	t
1338	\N	\N	1	21	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1339	\N	\N	1	21	2	0	0	0	0	0	0	0	0	\N	25669	0	0	0	\N	t
1340	\N	\N	1	21	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1341	\N	\N	1	21	4	0	0	0	0	0	0	0	0	\N	0	23344	0	0	\N	t
1342	\N	\N	1	21	5	0	0	0	0	0	0	0	0	\N	26777	0	0	0	\N	t
1343	\N	\N	1	21	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1344	\N	\N	1	21	7	0	0	0	0	0	0	0	0	\N	24535	0	0	0	\N	t
1345	\N	\N	1	21	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1346	\N	\N	1	21	9	0	0	0	0	0	0	0	0	\N	0	23754	0	0	\N	t
1347	\N	\N	1	21	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1348	\N	\N	1	21	11	0	0	0	0	0	0	0	0	\N	0	23494	0	0	\N	t
1349	\N	\N	1	21	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1350	\N	\N	1	21	13	0	0	0	0	0	0	0	0	\N	25634	0	0	0	\N	t
1351	\N	\N	1	21	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1352	\N	\N	1	21	15	0	0	0	0	0	0	0	0	\N	0	24548	0	0	\N	t
1353	\N	\N	1	21	16	0	0	0	0	0	0	0	0	\N	25546	0	0	0	\N	t
1354	\N	\N	1	21	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1355	\N	\N	1	21	18	0	0	0	0	0	0	0	0	\N	22463	0	0	0	\N	t
1356	\N	\N	1	21	19	0	0	0	0	0	0	0	0	\N	25863	0	0	0	\N	t
1357	\N	\N	1	21	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1358	\N	\N	1	21	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1359	\N	\N	1	21	22	0	0	0	0	0	0	0	0	\N	25049	0	0	0	\N	t
1360	\N	\N	1	21	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1361	\N	\N	1	21	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1362	\N	\N	1	21	25	0	0	0	0	0	0	0	0	\N	24004	0	0	0	\N	t
1363	\N	\N	1	22	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1364	\N	\N	1	22	2	0	0	0	0	0	0	0	0	\N	22210	0	0	0	\N	t
1365	\N	\N	1	22	3	0	0	0	0	0	0	0	0	\N	24213	0	0	0	\N	t
1366	\N	\N	1	22	4	0	0	0	0	0	0	0	0	\N	22464	0	0	0	\N	t
1367	\N	\N	1	22	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1368	\N	\N	1	22	6	0	0	0	0	0	0	0	0	\N	22020	0	0	0	\N	t
1369	\N	\N	1	22	7	0	0	0	0	0	0	0	0	\N	24109	0	0	0	\N	t
1370	\N	\N	1	22	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1371	\N	\N	1	22	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1372	\N	\N	1	22	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1373	\N	\N	1	22	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1374	\N	\N	1	22	12	0	0	0	0	0	0	0	0	\N	24040	0	0	0	\N	t
1375	\N	\N	1	22	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1376	\N	\N	1	22	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1377	\N	\N	1	22	15	0	0	0	0	0	0	0	0	\N	0	25719	0	0	\N	t
1378	\N	\N	1	22	16	0	0	0	0	0	0	0	0	\N	0	26058	0	0	\N	t
1379	\N	\N	1	22	17	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1380	\N	\N	1	22	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1381	\N	\N	1	22	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1382	\N	\N	1	22	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1383	\N	\N	1	22	21	0	0	0	0	0	0	0	0	\N	25451	0	0	0	\N	t
1384	\N	\N	1	22	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1385	\N	\N	1	22	23	0	0	0	0	0	0	0	0	\N	26636	0	0	0	\N	t
1386	\N	\N	1	22	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1387	\N	\N	1	22	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1388	\N	\N	1	23	1	0	0	0	0	0	0	0	0	\N	23178	0	0	0	\N	t
1389	\N	\N	1	23	2	0	0	0	0	0	0	0	0	\N	25522	0	0	0	\N	t
1390	\N	\N	1	23	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1391	\N	\N	1	23	4	0	0	0	0	0	0	0	0	\N	0	24425	0	0	\N	t
1392	\N	\N	1	23	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1393	\N	\N	1	23	6	0	0	0	0	0	0	0	0	\N	0	26612	0	0	\N	t
1394	\N	\N	1	23	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1395	\N	\N	1	23	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1396	\N	\N	1	23	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1397	\N	\N	1	23	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1398	\N	\N	1	23	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1399	\N	\N	1	23	12	0	0	0	0	0	0	0	0	\N	25946	0	0	0	\N	t
1400	\N	\N	1	23	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1401	\N	\N	1	23	14	0	0	0	0	0	0	0	0	\N	24067	0	0	0	\N	t
1402	\N	\N	1	23	15	0	0	0	0	0	0	0	0	\N	0	24004	0	0	\N	t
1403	\N	\N	1	23	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1404	\N	\N	1	23	17	0	0	0	0	0	0	0	0	\N	24100	0	0	0	\N	t
1405	\N	\N	1	23	18	0	0	0	0	0	0	0	0	\N	23715	0	0	0	\N	t
1406	\N	\N	1	23	19	0	0	0	0	0	0	0	0	\N	24725	0	0	0	\N	t
1407	\N	\N	1	23	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1408	\N	\N	1	23	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1409	\N	\N	1	23	22	0	0	0	0	0	0	0	0	\N	25601	0	0	0	\N	t
1410	\N	\N	1	23	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1411	\N	\N	1	23	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1412	\N	\N	1	23	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1413	\N	\N	1	24	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1414	\N	\N	1	24	2	0	0	0	0	0	0	0	0	\N	26283	0	0	0	\N	t
1415	\N	\N	1	24	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1416	\N	\N	1	24	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1417	\N	\N	1	24	5	0	0	0	0	0	0	0	0	\N	25982	0	0	0	\N	t
1418	\N	\N	1	24	6	0	0	0	0	0	0	0	0	\N	24827	0	0	0	\N	t
1419	\N	\N	1	24	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1420	\N	\N	1	24	8	0	0	0	0	0	0	0	0	\N	23463	0	0	0	\N	t
1421	\N	\N	1	24	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1422	\N	\N	1	24	10	0	0	0	0	0	0	0	0	\N	22670	0	0	0	\N	t
1423	\N	\N	1	24	11	0	0	0	0	0	0	0	0	\N	23738	0	0	0	\N	t
1424	\N	\N	1	24	12	0	0	0	0	0	0	0	0	\N	26471	0	0	0	\N	t
1425	\N	\N	1	24	13	0	0	0	0	0	0	0	0	\N	24655	0	0	0	\N	t
1426	\N	\N	1	24	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1427	\N	\N	1	24	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1428	\N	\N	1	24	16	0	0	0	0	0	0	0	0	\N	22179	0	0	0	\N	t
1429	\N	\N	1	24	17	0	0	0	0	0	0	0	0	\N	0	22945	0	0	\N	t
1430	\N	\N	1	24	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1431	\N	\N	1	24	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1432	\N	\N	1	24	20	0	0	0	0	0	0	0	0	\N	23962	0	0	0	\N	t
1433	\N	\N	1	24	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1434	\N	\N	1	24	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1435	\N	\N	1	24	23	0	0	0	0	0	0	0	0	\N	25567	0	0	0	\N	t
1436	\N	\N	1	24	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1437	\N	\N	1	24	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1438	\N	\N	1	25	1	0	0	0	0	0	0	0	0	\N	23433	0	0	0	\N	t
1439	\N	\N	1	25	2	0	0	0	0	0	0	0	0	\N	0	24350	0	0	\N	t
1440	\N	\N	1	25	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1441	\N	\N	1	25	4	0	0	0	0	0	0	0	0	\N	24280	0	0	0	\N	t
1442	\N	\N	1	25	5	0	0	0	0	0	0	0	0	\N	26039	0	0	0	\N	t
1443	\N	\N	1	25	6	0	0	0	0	0	0	0	0	\N	22779	0	0	0	\N	t
1444	\N	\N	1	25	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1445	\N	\N	1	25	8	0	0	0	0	0	0	0	0	\N	23888	0	0	0	\N	t
1446	\N	\N	1	25	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1447	\N	\N	1	25	10	0	0	0	0	0	0	0	0	\N	25746	0	0	0	\N	t
1448	\N	\N	1	25	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1449	\N	\N	1	25	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1450	\N	\N	1	25	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1451	\N	\N	1	25	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1452	\N	\N	1	25	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1453	\N	\N	1	25	16	0	0	0	0	0	0	0	0	\N	25053	0	0	0	\N	t
1454	\N	\N	1	25	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1455	\N	\N	1	25	18	0	0	0	0	0	0	0	0	\N	23705	0	0	0	\N	t
1456	\N	\N	1	25	19	0	0	0	0	0	0	0	0	\N	26011	0	0	0	\N	t
1457	\N	\N	1	25	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1458	\N	\N	1	25	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1459	\N	\N	1	25	22	0	0	0	0	0	0	0	0	\N	25994	0	0	0	\N	t
1460	\N	\N	1	25	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1461	\N	\N	1	25	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1462	\N	\N	1	25	25	0	0	0	0	0	0	0	0	\N	22970	0	0	0	\N	t
1463	\N	\N	1	26	1	0	0	0	0	0	0	0	0	\N	22285	0	0	0	\N	t
1464	\N	\N	1	26	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1465	\N	\N	1	26	3	0	0	0	0	0	0	0	0	\N	0	24360	0	0	\N	t
1466	\N	\N	1	26	4	0	0	0	0	0	0	0	0	\N	22840	0	0	0	\N	t
1467	\N	\N	1	26	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1468	\N	\N	1	26	6	0	0	0	0	0	0	0	0	\N	22012	0	0	0	\N	t
1469	\N	\N	1	26	7	0	0	0	0	0	0	0	0	\N	0	23989	0	0	\N	t
1470	\N	\N	1	26	8	0	0	0	0	0	0	0	0	\N	0	24681	0	0	\N	t
1471	\N	\N	1	26	9	0	0	0	0	0	0	0	0	\N	25143	0	0	0	\N	t
1472	\N	\N	1	26	10	0	0	0	0	0	0	0	0	\N	23711	0	0	0	\N	t
1473	\N	\N	1	26	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1474	\N	\N	1	26	12	0	0	0	0	0	0	0	0	\N	22269	0	0	0	\N	t
1475	\N	\N	1	26	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1476	\N	\N	1	26	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1477	\N	\N	1	26	15	0	0	0	0	0	0	0	0	\N	24313	0	0	0	\N	t
1478	\N	\N	1	26	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1479	\N	\N	1	26	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1480	\N	\N	1	26	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1481	\N	\N	1	26	19	0	0	0	0	0	0	0	0	\N	24739	0	0	0	\N	t
1482	\N	\N	1	26	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1483	\N	\N	1	26	21	0	0	0	0	0	0	0	0	\N	23086	0	0	0	\N	t
1484	\N	\N	1	26	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1485	\N	\N	1	26	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1486	\N	\N	1	26	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1487	\N	\N	1	26	25	0	0	0	0	0	0	0	0	\N	26317	0	0	0	\N	t
1488	\N	\N	1	27	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1489	\N	\N	1	27	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1490	\N	\N	1	27	3	0	0	0	0	0	0	0	0	\N	24384	0	0	0	\N	t
1491	\N	\N	1	27	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1492	\N	\N	1	27	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1493	\N	\N	1	27	6	0	0	0	0	0	0	0	0	\N	0	25092	0	0	\N	t
1494	\N	\N	1	27	7	0	0	0	0	0	0	0	0	\N	25045	0	0	0	\N	t
1495	\N	\N	1	27	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1496	\N	\N	1	27	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1497	\N	\N	1	27	10	0	0	0	0	0	0	0	0	\N	26169	0	0	0	\N	t
1498	\N	\N	1	27	11	0	0	0	0	0	0	0	0	\N	22923	0	0	0	\N	t
1499	\N	\N	1	27	12	0	0	0	0	0	0	0	0	\N	24247	0	0	0	\N	t
1500	\N	\N	1	27	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1501	\N	\N	1	27	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1502	\N	\N	1	27	15	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1503	\N	\N	1	27	16	0	0	0	0	0	0	0	0	\N	0	26256	0	0	\N	t
1504	\N	\N	1	27	17	0	0	0	0	0	0	0	0	\N	0	22974	0	0	\N	t
1505	\N	\N	1	27	18	0	0	0	0	0	0	0	0	\N	24816	0	0	0	\N	t
1506	\N	\N	1	27	19	0	0	0	0	0	0	0	0	\N	0	26841	0	0	\N	t
1507	\N	\N	1	27	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1508	\N	\N	1	27	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1509	\N	\N	1	27	22	0	0	0	0	0	0	0	0	\N	22319	0	0	0	\N	t
1510	\N	\N	1	27	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1511	\N	\N	1	27	24	0	0	0	0	0	0	0	0	\N	23577	0	0	0	\N	t
1512	\N	\N	1	27	25	0	0	0	0	0	0	0	0	\N	25307	0	0	0	\N	t
1513	\N	\N	1	28	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1514	\N	\N	1	28	2	0	0	0	0	0	0	0	0	\N	26180	0	0	0	\N	t
1515	\N	\N	1	28	3	0	0	0	0	0	0	0	0	\N	24939	0	0	0	\N	t
1516	\N	\N	1	28	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1517	\N	\N	1	28	5	0	0	0	0	0	0	0	0	\N	0	24135	0	0	\N	t
1518	\N	\N	1	28	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1519	\N	\N	1	28	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1520	\N	\N	1	28	8	0	0	0	0	0	0	0	0	\N	23397	0	0	0	\N	t
1521	\N	\N	1	28	9	0	0	0	0	0	0	0	0	\N	22419	0	0	0	\N	t
1522	\N	\N	1	28	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1523	\N	\N	1	28	11	0	0	0	0	0	0	0	0	\N	23691	0	0	0	\N	t
1524	\N	\N	1	28	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1525	\N	\N	1	28	13	0	0	0	0	0	0	0	0	\N	0	25709	0	0	\N	t
1526	\N	\N	1	28	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1527	\N	\N	1	28	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1528	\N	\N	1	28	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1529	\N	\N	1	28	17	0	0	0	0	0	0	0	0	\N	26804	0	0	0	\N	t
1530	\N	\N	1	28	18	0	0	0	0	0	0	0	0	\N	24558	0	0	0	\N	t
1531	\N	\N	1	28	19	0	0	0	0	0	0	0	0	\N	25797	0	0	0	\N	t
1532	\N	\N	1	28	20	0	0	0	0	0	0	0	0	\N	25714	0	0	0	\N	t
1533	\N	\N	1	28	21	0	0	0	0	0	0	0	0	\N	22837	0	0	0	\N	t
1534	\N	\N	1	28	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1535	\N	\N	1	28	23	0	0	0	0	0	0	0	0	\N	26337	0	0	0	\N	t
1536	\N	\N	1	28	24	0	0	0	0	0	0	0	0	\N	26278	0	0	0	\N	t
1537	\N	\N	1	28	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1538	\N	\N	1	29	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1539	\N	\N	1	29	2	0	0	0	0	0	0	0	0	\N	22117	0	0	0	\N	t
1540	\N	\N	1	29	3	0	0	0	0	0	0	0	0	\N	25122	0	0	0	\N	t
1541	\N	\N	1	29	4	0	0	0	0	0	0	0	0	\N	0	26171	0	0	\N	t
1542	\N	\N	1	29	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1543	\N	\N	1	29	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1544	\N	\N	1	29	7	0	0	0	0	0	0	0	0	\N	24705	0	0	0	\N	t
1545	\N	\N	1	29	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1546	\N	\N	1	29	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1547	\N	\N	1	29	10	0	0	0	0	0	0	0	0	\N	25050	0	0	0	\N	t
1548	\N	\N	1	29	11	0	0	0	0	0	0	0	0	\N	0	25881	0	0	\N	t
1549	\N	\N	1	29	12	0	0	0	0	0	0	0	0	\N	0	24575	0	0	\N	t
1550	\N	\N	1	29	13	0	0	0	0	0	0	0	0	\N	26761	0	0	0	\N	t
1551	\N	\N	1	29	14	0	0	0	0	0	0	0	0	\N	0	23713	0	0	\N	t
1552	\N	\N	1	29	15	0	0	0	0	0	0	0	0	\N	22067	0	0	0	\N	t
1553	\N	\N	1	29	16	0	0	0	0	0	0	0	0	\N	22548	0	0	0	\N	t
1554	\N	\N	1	29	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1555	\N	\N	1	29	18	0	0	0	0	0	0	0	0	\N	23653	0	0	0	\N	t
1556	\N	\N	1	29	19	0	0	0	0	0	0	0	0	\N	25282	0	0	0	\N	t
1557	\N	\N	1	29	20	0	0	0	0	0	0	0	0	\N	25500	0	0	0	\N	t
1558	\N	\N	1	29	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1559	\N	\N	1	29	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1560	\N	\N	1	29	23	0	0	0	0	0	0	0	0	\N	25417	0	0	0	\N	t
1561	\N	\N	1	29	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1562	\N	\N	1	29	25	0	0	0	0	0	0	0	0	\N	25914	0	0	0	\N	t
1563	\N	\N	1	30	1	0	0	0	0	0	0	0	0	\N	25482	0	0	0	\N	t
1564	\N	\N	1	30	2	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1565	\N	\N	1	30	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1566	\N	\N	1	30	4	0	0	0	0	0	0	0	0	\N	25733	0	0	0	\N	t
1567	\N	\N	1	30	5	0	0	0	0	0	0	0	0	\N	0	25046	0	0	\N	t
1568	\N	\N	1	30	6	0	0	0	0	0	0	0	0	\N	23071	0	0	0	\N	t
1569	\N	\N	1	30	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1570	\N	\N	1	30	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1571	\N	\N	1	30	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1572	\N	\N	1	30	10	0	0	0	0	0	0	0	0	\N	0	22567	0	0	\N	t
1573	\N	\N	1	30	11	0	0	0	0	0	0	0	0	\N	23945	0	0	0	\N	t
1574	\N	\N	1	30	12	0	0	0	0	0	0	0	0	\N	24984	0	0	0	\N	t
1575	\N	\N	1	30	13	0	0	0	0	0	0	0	0	\N	22290	0	0	0	\N	t
1576	\N	\N	1	30	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1577	\N	\N	1	30	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1578	\N	\N	1	30	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1579	\N	\N	1	30	17	0	0	0	0	0	0	0	0	\N	26692	0	0	0	\N	t
1580	\N	\N	1	30	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1581	\N	\N	1	30	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1582	\N	\N	1	30	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1583	\N	\N	1	30	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1584	\N	\N	1	30	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1585	\N	\N	1	30	23	0	0	0	0	0	0	0	0	\N	24553	0	0	0	\N	t
1586	\N	\N	1	30	24	0	0	0	0	0	0	0	0	\N	0	24714	0	0	\N	t
1587	\N	\N	1	30	25	0	0	0	0	0	0	0	0	\N	0	24821	0	0	\N	t
1588	\N	\N	1	31	1	0	0	0	0	0	0	0	0	\N	23785	0	0	0	\N	t
1589	\N	\N	1	31	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1590	\N	\N	1	31	3	0	0	0	0	0	0	0	0	\N	24060	0	0	0	\N	t
1591	\N	\N	1	31	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1592	\N	\N	1	31	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1593	\N	\N	1	31	6	0	0	0	0	0	0	0	0	\N	0	24035	0	0	\N	t
1594	\N	\N	1	31	7	0	0	0	0	0	0	0	0	\N	25323	0	0	0	\N	t
1595	\N	\N	1	31	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1596	\N	\N	1	31	9	0	0	0	0	0	0	0	0	\N	0	24901	0	0	\N	t
1597	\N	\N	1	31	10	0	0	0	0	0	0	0	0	\N	26531	0	0	0	\N	t
1598	\N	\N	1	31	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1599	\N	\N	1	31	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1600	\N	\N	1	31	13	0	0	0	0	0	0	0	0	\N	24571	0	0	0	\N	t
1601	\N	\N	1	31	14	0	0	0	0	0	0	0	0	\N	22495	0	0	0	\N	t
1602	\N	\N	1	31	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1603	\N	\N	1	31	16	0	0	0	0	0	0	0	0	\N	23285	0	0	0	\N	t
1604	\N	\N	1	31	17	0	0	0	0	0	0	0	0	\N	24996	0	0	0	\N	t
1605	\N	\N	1	31	18	0	0	0	0	0	0	0	0	\N	23115	0	0	0	\N	t
1606	\N	\N	1	31	19	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1607	\N	\N	1	31	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1608	\N	\N	1	31	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1609	\N	\N	1	31	22	0	0	0	0	0	0	0	0	\N	23800	0	0	0	\N	t
1610	\N	\N	1	31	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1611	\N	\N	1	31	24	0	0	0	0	0	0	0	0	\N	22987	0	0	0	\N	t
1612	\N	\N	1	31	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1613	\N	\N	1	32	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1614	\N	\N	1	32	2	0	0	0	0	0	0	0	0	\N	24627	0	0	0	\N	t
1615	\N	\N	1	32	3	0	0	0	0	0	0	0	0	\N	24116	0	0	0	\N	t
1616	\N	\N	1	32	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1617	\N	\N	1	32	5	0	0	0	0	0	0	0	0	\N	24475	0	0	0	\N	t
1618	\N	\N	1	32	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1619	\N	\N	1	32	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1620	\N	\N	1	32	8	0	0	0	0	0	0	0	0	\N	0	24037	0	0	\N	t
1621	\N	\N	1	32	9	0	0	0	0	0	0	0	0	\N	23944	0	0	0	\N	t
1622	\N	\N	1	32	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1623	\N	\N	1	32	11	0	0	0	0	0	0	0	0	\N	0	25672	0	0	\N	t
1624	\N	\N	1	32	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1625	\N	\N	1	32	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1626	\N	\N	1	32	14	0	0	0	0	0	0	0	0	\N	0	23702	0	0	\N	t
1627	\N	\N	1	32	15	0	0	0	0	0	0	0	0	\N	26153	0	0	0	\N	t
1628	\N	\N	1	32	16	0	0	0	0	0	0	0	0	\N	22361	0	0	0	\N	t
1629	\N	\N	1	32	17	0	0	0	0	0	0	0	0	\N	25236	0	0	0	\N	t
1630	\N	\N	1	32	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1631	\N	\N	1	32	19	0	0	0	0	0	0	0	0	\N	25143	0	0	0	\N	t
1632	\N	\N	1	32	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1633	\N	\N	1	32	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1634	\N	\N	1	32	22	0	0	0	0	0	0	0	0	\N	25948	0	0	0	\N	t
1635	\N	\N	1	32	23	0	0	0	0	0	0	0	0	\N	26823	0	0	0	\N	t
1636	\N	\N	1	32	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1637	\N	\N	1	32	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1638	\N	\N	1	33	1	0	0	0	0	0	0	0	0	\N	24089	0	0	0	\N	t
1639	\N	\N	1	33	2	0	0	0	0	0	0	0	0	\N	24128	0	0	0	\N	t
1640	\N	\N	1	33	3	0	0	0	0	0	0	0	0	\N	24231	0	0	0	\N	t
1641	\N	\N	1	33	4	0	0	0	0	0	0	0	0	\N	26638	0	0	0	\N	t
1642	\N	\N	1	33	5	0	0	0	0	0	0	0	0	\N	26879	0	0	0	\N	t
1643	\N	\N	1	33	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1644	\N	\N	1	33	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1645	\N	\N	1	33	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1646	\N	\N	1	33	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1647	\N	\N	1	33	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1648	\N	\N	1	33	11	0	0	0	0	0	0	0	0	\N	25925	0	0	0	\N	t
1649	\N	\N	1	33	12	0	0	0	0	0	0	0	0	\N	24498	0	0	0	\N	t
1650	\N	\N	1	33	13	0	0	0	0	0	0	0	0	\N	0	25952	0	0	\N	t
1651	\N	\N	1	33	14	0	0	0	0	0	0	0	0	\N	24176	0	0	0	\N	t
1652	\N	\N	1	33	15	0	0	0	0	0	0	0	0	\N	22819	0	0	0	\N	t
1653	\N	\N	1	33	16	0	0	0	0	0	0	0	0	\N	22882	0	0	0	\N	t
1654	\N	\N	1	33	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1655	\N	\N	1	33	18	0	0	0	0	0	0	0	0	\N	25097	0	0	0	\N	t
1656	\N	\N	1	33	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1657	\N	\N	1	33	20	0	0	0	0	0	0	0	0	\N	25106	0	0	0	\N	t
1658	\N	\N	1	33	21	0	0	0	0	0	0	0	0	\N	0	22854	0	0	\N	t
1659	\N	\N	1	33	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1660	\N	\N	1	33	23	0	0	0	0	0	0	0	0	\N	0	24889	0	0	\N	t
1661	\N	\N	1	33	24	0	0	0	0	0	0	0	0	\N	0	26755	0	0	\N	t
1662	\N	\N	1	33	25	0	0	0	0	0	0	0	0	\N	22021	0	0	0	\N	t
1663	\N	\N	1	34	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1664	\N	\N	1	34	2	0	0	0	0	0	0	0	0	\N	22069	0	0	0	\N	t
1665	\N	\N	1	34	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1666	\N	\N	1	34	4	0	0	0	0	0	0	0	0	\N	0	24556	0	0	\N	t
1667	\N	\N	1	34	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1668	\N	\N	1	34	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1669	\N	\N	1	34	7	0	0	0	0	0	0	0	0	\N	24063	0	0	0	\N	t
1670	\N	\N	1	34	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1671	\N	\N	1	34	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1672	\N	\N	1	34	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1673	\N	\N	1	34	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1674	\N	\N	1	34	12	0	0	0	0	0	0	0	0	\N	26578	0	0	0	\N	t
1675	\N	\N	1	34	13	0	0	0	0	0	0	0	0	\N	0	25401	0	0	\N	t
1676	\N	\N	1	34	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1677	\N	\N	1	34	15	0	0	0	0	0	0	0	0	\N	25799	0	0	0	\N	t
1678	\N	\N	1	34	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1679	\N	\N	1	34	17	0	0	0	0	0	0	0	0	\N	23384	0	0	0	\N	t
1680	\N	\N	1	34	18	0	0	0	0	0	0	0	0	\N	23964	0	0	0	\N	t
1681	\N	\N	1	34	19	0	0	0	0	0	0	0	0	\N	26446	0	0	0	\N	t
1682	\N	\N	1	34	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1683	\N	\N	1	34	21	0	0	0	0	0	0	0	0	\N	25196	0	0	0	\N	t
1684	\N	\N	1	34	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1685	\N	\N	1	34	23	0	0	0	0	0	0	0	0	\N	23342	0	0	0	\N	t
1686	\N	\N	1	34	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1687	\N	\N	1	34	25	0	0	0	0	0	0	0	0	\N	25095	0	0	0	\N	t
1688	\N	\N	1	35	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1689	\N	\N	1	35	2	0	0	0	0	0	0	0	0	\N	25777	0	0	0	\N	t
1690	\N	\N	1	35	3	0	0	0	0	0	0	0	0	\N	24938	0	0	0	\N	t
1691	\N	\N	1	35	4	0	0	0	0	0	0	0	0	\N	26861	0	0	0	\N	t
1692	\N	\N	1	35	5	0	0	0	0	0	0	0	0	\N	26403	0	0	0	\N	t
1693	\N	\N	1	35	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1694	\N	\N	1	35	7	0	0	0	0	0	0	0	0	\N	0	22259	0	0	\N	t
1695	\N	\N	1	35	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1696	\N	\N	1	35	9	0	0	0	0	0	0	0	0	\N	25128	0	0	0	\N	t
1697	\N	\N	1	35	10	0	0	0	0	0	0	0	0	\N	26136	0	0	0	\N	t
1698	\N	\N	1	35	11	0	0	0	0	0	0	0	0	\N	25749	0	0	0	\N	t
1699	\N	\N	1	35	12	0	0	0	0	0	0	0	0	\N	23427	0	0	0	\N	t
1700	\N	\N	1	35	13	0	0	0	0	0	0	0	0	\N	25594	0	0	0	\N	t
1701	\N	\N	1	35	14	0	0	0	0	0	0	0	0	\N	0	24518	0	0	\N	t
1702	\N	\N	1	35	15	0	0	0	0	0	0	0	0	\N	26702	0	0	0	\N	t
1703	\N	\N	1	35	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1704	\N	\N	1	35	17	0	0	0	0	0	0	0	0	\N	23586	0	0	0	\N	t
1705	\N	\N	1	35	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1706	\N	\N	1	35	19	0	0	0	0	0	0	0	0	\N	24563	0	0	0	\N	t
1707	\N	\N	1	35	20	0	0	0	0	0	0	0	0	\N	26814	0	0	0	\N	t
1708	\N	\N	1	35	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1709	\N	\N	1	35	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1710	\N	\N	1	35	23	0	0	0	0	0	0	0	0	\N	23071	0	0	0	\N	t
1711	\N	\N	1	35	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1712	\N	\N	1	35	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1713	\N	\N	1	36	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1714	\N	\N	1	36	2	0	0	0	0	0	0	0	0	\N	26588	0	0	0	\N	t
1715	\N	\N	1	36	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1716	\N	\N	1	36	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1717	\N	\N	1	36	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1718	\N	\N	1	36	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1719	\N	\N	1	36	7	0	0	0	0	0	0	0	0	\N	0	23819	0	0	\N	t
1720	\N	\N	1	36	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1721	\N	\N	1	36	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1722	\N	\N	1	36	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1723	\N	\N	1	36	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1724	\N	\N	1	36	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1725	\N	\N	1	36	13	0	0	0	0	0	0	0	0	\N	25158	0	0	0	\N	t
1726	\N	\N	1	36	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1727	\N	\N	1	36	15	0	0	0	0	0	0	0	0	\N	23143	0	0	0	\N	t
1728	\N	\N	1	36	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1729	\N	\N	1	36	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1730	\N	\N	1	36	18	0	0	0	0	0	0	0	0	\N	24280	0	0	0	\N	t
1731	\N	\N	1	36	19	0	0	0	0	0	0	0	0	\N	23899	0	0	0	\N	t
1732	\N	\N	1	36	20	0	0	0	0	0	0	0	0	\N	24583	0	0	0	\N	t
1733	\N	\N	1	36	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1734	\N	\N	1	36	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1735	\N	\N	1	36	23	0	0	0	0	0	0	0	0	\N	25662	0	0	0	\N	t
1736	\N	\N	1	36	24	0	0	0	0	0	0	0	0	\N	24810	0	0	0	\N	t
1737	\N	\N	1	36	25	0	0	0	0	0	0	0	0	\N	22889	0	0	0	\N	t
1738	\N	\N	1	37	1	0	0	0	0	0	0	0	0	\N	22454	0	0	0	\N	t
1739	\N	\N	1	37	2	0	0	0	0	0	0	0	0	\N	0	26000	0	0	\N	t
1740	\N	\N	1	37	3	0	0	0	0	0	0	0	0	\N	23258	0	0	0	\N	t
1741	\N	\N	1	37	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1742	\N	\N	1	37	5	0	0	0	0	0	0	0	0	\N	24419	0	0	0	\N	t
1743	\N	\N	1	37	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1744	\N	\N	1	37	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1745	\N	\N	1	37	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1746	\N	\N	1	37	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1747	\N	\N	1	37	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1748	\N	\N	1	37	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1749	\N	\N	1	37	12	0	0	0	0	0	0	0	0	\N	23462	0	0	0	\N	t
1750	\N	\N	1	37	13	0	0	0	0	0	0	0	0	\N	24116	0	0	0	\N	t
1751	\N	\N	1	37	14	0	0	0	0	0	0	0	0	\N	26817	0	0	0	\N	t
1752	\N	\N	1	37	15	0	0	0	0	0	0	0	0	\N	22996	0	0	0	\N	t
1753	\N	\N	1	37	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1754	\N	\N	1	37	17	0	0	0	0	0	0	0	0	\N	0	25539	0	0	\N	t
1755	\N	\N	1	37	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1756	\N	\N	1	37	19	0	0	0	0	0	0	0	0	\N	26445	0	0	0	\N	t
1757	\N	\N	1	37	20	0	0	0	0	0	0	0	0	\N	0	22627	0	0	\N	t
1758	\N	\N	1	37	21	0	0	0	0	0	0	0	0	\N	26853	0	0	0	\N	t
1759	\N	\N	1	37	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1760	\N	\N	1	37	23	0	0	0	0	0	0	0	0	\N	25198	0	0	0	\N	t
1761	\N	\N	1	37	24	0	0	0	0	0	0	0	0	\N	22371	0	0	0	\N	t
1762	\N	\N	1	37	25	0	0	0	0	0	0	0	0	\N	25743	0	0	0	\N	t
1763	\N	\N	1	38	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1764	\N	\N	1	38	2	0	0	0	0	0	0	0	0	\N	0	23003	0	0	\N	t
1765	\N	\N	1	38	3	0	0	0	0	0	0	0	0	\N	22918	0	0	0	\N	t
1766	\N	\N	1	38	4	0	0	0	0	0	0	0	0	\N	25378	0	0	0	\N	t
1767	\N	\N	1	38	5	0	0	0	0	0	0	0	0	\N	22118	0	0	0	\N	t
1768	\N	\N	1	38	6	0	0	0	0	0	0	0	0	\N	23819	0	0	0	\N	t
1769	\N	\N	1	38	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1770	\N	\N	1	38	8	0	0	0	0	0	0	0	0	\N	0	22138	0	0	\N	t
1771	\N	\N	1	38	9	0	0	0	0	0	0	0	0	\N	22932	0	0	0	\N	t
1772	\N	\N	1	38	10	0	0	0	0	0	0	0	0	\N	0	22878	0	0	\N	t
1773	\N	\N	1	38	11	0	0	0	0	0	0	0	0	\N	0	25495	0	0	\N	t
1774	\N	\N	1	38	12	0	0	0	0	0	0	0	0	\N	22126	0	0	0	\N	t
1775	\N	\N	1	38	13	0	0	0	0	0	0	0	0	\N	22485	0	0	0	\N	t
1776	\N	\N	1	38	14	0	0	0	0	0	0	0	0	\N	24890	0	0	0	\N	t
1777	\N	\N	1	38	15	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1778	\N	\N	1	38	16	0	0	0	0	0	0	0	0	\N	0	23261	0	0	\N	t
1779	\N	\N	1	38	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1780	\N	\N	1	38	18	0	0	0	0	0	0	0	0	\N	23478	0	0	0	\N	t
1781	\N	\N	1	38	19	0	0	0	0	0	0	0	0	\N	0	24342	0	0	\N	t
1782	\N	\N	1	38	20	0	0	0	0	0	0	0	0	\N	0	22410	0	0	\N	t
1783	\N	\N	1	38	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1784	\N	\N	1	38	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1785	\N	\N	1	38	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1786	\N	\N	1	38	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1787	\N	\N	1	38	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1788	\N	\N	1	39	1	0	0	0	0	0	0	0	0	\N	25196	0	0	0	\N	t
1789	\N	\N	1	39	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1790	\N	\N	1	39	3	0	0	0	0	0	0	0	0	\N	0	24229	0	0	\N	t
1791	\N	\N	1	39	4	0	0	0	0	0	0	0	0	\N	25882	0	0	0	\N	t
1792	\N	\N	1	39	5	0	0	0	0	0	0	0	0	\N	22253	0	0	0	\N	t
1793	\N	\N	1	39	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1794	\N	\N	1	39	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1795	\N	\N	1	39	8	0	0	0	0	0	0	0	0	\N	22023	0	0	0	\N	t
1796	\N	\N	1	39	9	0	0	0	0	0	0	0	0	\N	26740	0	0	0	\N	t
1797	\N	\N	1	39	10	0	0	0	0	0	0	0	0	\N	26397	0	0	0	\N	t
1798	\N	\N	1	39	11	0	0	0	0	0	0	0	0	\N	0	22927	0	0	\N	t
1799	\N	\N	1	39	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1800	\N	\N	1	39	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1801	\N	\N	1	39	14	0	0	0	0	0	0	0	0	\N	23891	0	0	0	\N	t
1802	\N	\N	1	39	15	0	0	0	0	0	0	0	0	\N	23035	0	0	0	\N	t
1803	\N	\N	1	39	16	0	0	0	0	0	0	0	0	\N	0	23718	0	0	\N	t
1804	\N	\N	1	39	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1805	\N	\N	1	39	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1806	\N	\N	1	39	19	0	0	0	0	0	0	0	0	\N	25736	0	0	0	\N	t
1807	\N	\N	1	39	20	0	0	0	0	0	0	0	0	\N	23185	0	0	0	\N	t
1808	\N	\N	1	39	21	0	0	0	0	0	0	0	0	\N	23417	0	0	0	\N	t
1809	\N	\N	1	39	22	0	0	0	0	0	0	0	0	\N	24488	0	0	0	\N	t
1810	\N	\N	1	39	23	0	0	0	0	0	0	0	0	\N	24346	0	0	0	\N	t
1811	\N	\N	1	39	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1812	\N	\N	1	39	25	0	0	0	0	0	0	0	0	\N	22925	0	0	0	\N	t
1813	\N	\N	1	40	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1814	\N	\N	1	40	2	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1815	\N	\N	1	40	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1816	\N	\N	1	40	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1817	\N	\N	1	40	5	0	0	0	0	0	0	0	0	\N	26725	0	0	0	\N	t
1818	\N	\N	1	40	6	0	0	0	0	0	0	0	0	\N	25665	0	0	0	\N	t
1819	\N	\N	1	40	7	0	0	0	0	0	0	0	0	\N	22716	0	0	0	\N	t
1820	\N	\N	1	40	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1821	\N	\N	1	40	9	0	0	0	0	0	0	0	0	\N	25373	0	0	0	\N	t
1822	\N	\N	1	40	10	0	0	0	0	0	0	0	0	\N	25338	0	0	0	\N	t
1823	\N	\N	1	40	11	0	0	0	0	0	0	0	0	\N	23977	0	0	0	\N	t
1824	\N	\N	1	40	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1825	\N	\N	1	40	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1826	\N	\N	1	40	14	0	0	0	0	0	0	0	0	\N	22963	0	0	0	\N	t
1827	\N	\N	1	40	15	0	0	0	0	0	0	0	0	\N	25504	0	0	0	\N	t
1828	\N	\N	1	40	16	0	0	0	0	0	0	0	0	\N	23051	0	0	0	\N	t
1829	\N	\N	1	40	17	0	0	0	0	0	0	0	0	\N	0	22618	0	0	\N	t
1830	\N	\N	1	40	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1831	\N	\N	1	40	19	0	0	0	0	0	0	0	0	\N	26170	0	0	0	\N	t
1832	\N	\N	1	40	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1833	\N	\N	1	40	21	0	0	0	0	0	0	0	0	\N	22124	0	0	0	\N	t
1834	\N	\N	1	40	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1835	\N	\N	1	40	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1836	\N	\N	1	40	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1837	\N	\N	1	40	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1838	\N	\N	1	41	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1839	\N	\N	1	41	2	0	0	0	0	0	0	0	0	\N	23443	0	0	0	\N	t
1840	\N	\N	1	41	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1841	\N	\N	1	41	4	0	0	0	0	0	0	0	0	\N	24524	0	0	0	\N	t
1842	\N	\N	1	41	5	0	0	0	0	0	0	0	0	\N	26902	0	0	0	\N	t
1843	\N	\N	1	41	6	0	0	0	0	0	0	0	0	\N	23560	0	0	0	\N	t
1844	\N	\N	1	41	7	0	0	0	0	0	0	0	0	\N	25864	0	0	0	\N	t
1845	\N	\N	1	41	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1846	\N	\N	1	41	9	0	0	0	0	0	0	0	0	\N	0	26289	0	0	\N	t
1847	\N	\N	1	41	10	0	0	0	0	0	0	0	0	\N	22817	0	0	0	\N	t
1848	\N	\N	1	41	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1849	\N	\N	1	41	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1850	\N	\N	1	41	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1851	\N	\N	1	41	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1852	\N	\N	1	41	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1853	\N	\N	1	41	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1854	\N	\N	1	41	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1855	\N	\N	1	41	18	0	0	0	0	0	0	0	0	\N	25088	0	0	0	\N	t
1856	\N	\N	1	41	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1857	\N	\N	1	41	20	0	0	0	0	0	0	0	0	\N	26562	0	0	0	\N	t
1858	\N	\N	1	41	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1859	\N	\N	1	41	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1860	\N	\N	1	41	23	0	0	0	0	0	0	0	0	\N	0	23908	0	0	\N	t
1861	\N	\N	1	41	24	0	0	0	0	0	0	0	0	\N	26806	0	0	0	\N	t
1862	\N	\N	1	41	25	0	0	0	0	0	0	0	0	\N	22352	0	0	0	\N	t
1863	\N	\N	1	42	1	0	0	0	0	0	0	0	0	\N	0	26193	0	0	\N	t
1864	\N	\N	1	42	2	0	0	0	0	0	0	0	0	\N	23977	0	0	0	\N	t
1865	\N	\N	1	42	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1866	\N	\N	1	42	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1867	\N	\N	1	42	5	0	0	0	0	0	0	0	0	\N	25068	0	0	0	\N	t
1868	\N	\N	1	42	6	0	0	0	0	0	0	0	0	\N	22689	0	0	0	\N	t
1869	\N	\N	1	42	7	0	0	0	0	0	0	0	0	\N	25706	0	0	0	\N	t
1870	\N	\N	1	42	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1871	\N	\N	1	42	9	0	0	0	0	0	0	0	0	\N	0	23689	0	0	\N	t
1872	\N	\N	1	42	10	0	0	0	0	0	0	0	0	\N	22730	0	0	0	\N	t
1873	\N	\N	1	42	11	0	0	0	0	0	0	0	0	\N	0	25832	0	0	\N	t
1874	\N	\N	1	42	12	0	0	0	0	0	0	0	0	\N	0	24808	0	0	\N	t
1875	\N	\N	1	42	13	0	0	0	0	0	0	0	0	\N	23610	0	0	0	\N	t
1876	\N	\N	1	42	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1877	\N	\N	1	42	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1878	\N	\N	1	42	16	0	0	0	0	0	0	0	0	\N	24270	0	0	0	\N	t
1879	\N	\N	1	42	17	0	0	0	0	0	0	0	0	\N	23529	0	0	0	\N	t
1880	\N	\N	1	42	18	0	0	0	0	0	0	0	0	\N	24011	0	0	0	\N	t
1881	\N	\N	1	42	19	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1882	\N	\N	1	42	20	0	0	0	0	0	0	0	0	\N	24936	0	0	0	\N	t
1883	\N	\N	1	42	21	0	0	0	0	0	0	0	0	\N	24882	0	0	0	\N	t
1884	\N	\N	1	42	22	0	0	0	0	0	0	0	0	\N	26326	0	0	0	\N	t
1885	\N	\N	1	42	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1886	\N	\N	1	42	24	0	0	0	0	0	0	0	0	\N	26885	0	0	0	\N	t
1887	\N	\N	1	42	25	0	0	0	0	0	0	0	0	\N	23457	0	0	0	\N	t
1888	\N	\N	1	43	1	0	0	0	0	0	0	0	0	\N	26553	0	0	0	\N	t
1889	\N	\N	1	43	2	0	0	0	0	0	0	0	0	\N	25136	0	0	0	\N	t
1890	\N	\N	1	43	3	0	0	0	0	0	0	0	0	\N	0	25336	0	0	\N	t
1891	\N	\N	1	43	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1892	\N	\N	1	43	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1893	\N	\N	1	43	6	0	0	0	0	0	0	0	0	\N	22637	0	0	0	\N	t
1894	\N	\N	1	43	7	0	0	0	0	0	0	0	0	\N	26785	0	0	0	\N	t
1895	\N	\N	1	43	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1896	\N	\N	1	43	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1897	\N	\N	1	43	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1898	\N	\N	1	43	11	0	0	0	0	0	0	0	0	\N	25686	0	0	0	\N	t
1899	\N	\N	1	43	12	0	0	0	0	0	0	0	0	\N	0	24007	0	0	\N	t
1900	\N	\N	1	43	13	0	0	0	0	0	0	0	0	\N	23449	0	0	0	\N	t
1901	\N	\N	1	43	14	0	0	0	0	0	0	0	0	\N	0	23924	0	0	\N	t
1902	\N	\N	1	43	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1903	\N	\N	1	43	16	0	0	0	0	0	0	0	0	\N	0	22268	0	0	\N	t
1904	\N	\N	1	43	17	0	0	0	0	0	0	0	0	\N	22541	0	0	0	\N	t
1905	\N	\N	1	43	18	0	0	0	0	0	0	0	0	\N	0	24604	0	0	\N	t
1906	\N	\N	1	43	19	0	0	0	0	0	0	0	0	\N	26677	0	0	0	\N	t
1907	\N	\N	1	43	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1908	\N	\N	1	43	21	0	0	0	0	0	0	0	0	\N	22733	0	0	0	\N	t
1909	\N	\N	1	43	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1910	\N	\N	1	43	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1911	\N	\N	1	43	24	0	0	0	0	0	0	0	0	\N	0	24691	0	0	\N	t
1912	\N	\N	1	43	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1913	\N	\N	1	44	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1914	\N	\N	1	44	2	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1915	\N	\N	1	44	3	0	0	0	0	0	0	0	0	\N	22500	0	0	0	\N	t
1916	\N	\N	1	44	4	0	0	0	0	0	0	0	0	\N	24554	0	0	0	\N	t
1917	\N	\N	1	44	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1918	\N	\N	1	44	6	0	0	0	0	0	0	0	0	\N	23099	0	0	0	\N	t
1919	\N	\N	1	44	7	0	0	0	0	0	0	0	0	\N	25785	0	0	0	\N	t
1920	\N	\N	1	44	8	0	0	0	0	0	0	0	0	\N	0	23699	0	0	\N	t
1921	\N	\N	1	44	9	0	0	0	0	0	0	0	0	\N	24378	0	0	0	\N	t
1922	\N	\N	1	44	10	0	0	0	0	0	0	0	0	\N	24491	0	0	0	\N	t
1923	\N	\N	1	44	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1924	\N	\N	1	44	12	0	0	0	0	0	0	0	0	\N	24838	0	0	0	\N	t
1925	\N	\N	1	44	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1926	\N	\N	1	44	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1927	\N	\N	1	44	15	0	0	0	0	0	0	0	0	\N	24485	0	0	0	\N	t
1928	\N	\N	1	44	16	0	0	0	0	0	0	0	0	\N	23358	0	0	0	\N	t
1929	\N	\N	1	44	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1930	\N	\N	1	44	18	0	0	0	0	0	0	0	0	\N	24021	0	0	0	\N	t
1931	\N	\N	1	44	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1932	\N	\N	1	44	20	0	0	0	0	0	0	0	0	\N	25820	0	0	0	\N	t
1933	\N	\N	1	44	21	0	0	0	0	0	0	0	0	\N	22619	0	0	0	\N	t
1934	\N	\N	1	44	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1935	\N	\N	1	44	23	0	0	0	0	0	0	0	0	\N	24999	0	0	0	\N	t
1936	\N	\N	1	44	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1937	\N	\N	1	44	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1938	\N	\N	1	45	1	0	0	0	0	0	0	0	0	\N	24187	0	0	0	\N	t
1939	\N	\N	1	45	2	0	0	0	0	0	0	0	0	\N	23925	0	0	0	\N	t
1940	\N	\N	1	45	3	0	0	0	0	0	0	0	0	\N	22620	0	0	0	\N	t
1941	\N	\N	1	45	4	0	0	0	0	0	0	0	0	\N	23944	0	0	0	\N	t
1942	\N	\N	1	45	5	0	0	0	0	0	0	0	0	\N	25205	0	0	0	\N	t
1943	\N	\N	1	45	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1944	\N	\N	1	45	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1945	\N	\N	1	45	8	0	0	0	0	0	0	0	0	\N	0	24166	0	0	\N	t
1946	\N	\N	1	45	9	0	0	0	0	0	0	0	0	\N	24503	0	0	0	\N	t
1947	\N	\N	1	45	10	0	0	0	0	0	0	0	0	\N	24704	0	0	0	\N	t
1948	\N	\N	1	45	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1949	\N	\N	1	45	12	0	0	0	0	0	0	0	0	\N	23028	0	0	0	\N	t
1950	\N	\N	1	45	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1951	\N	\N	1	45	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1952	\N	\N	1	45	15	0	0	0	0	0	0	0	0	\N	25683	0	0	0	\N	t
1953	\N	\N	1	45	16	0	0	0	0	0	0	0	0	\N	22999	0	0	0	\N	t
1954	\N	\N	1	45	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1955	\N	\N	1	45	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1956	\N	\N	1	45	19	0	0	0	0	0	0	0	0	\N	23390	0	0	0	\N	t
1957	\N	\N	1	45	20	0	0	0	0	0	0	0	0	\N	24718	0	0	0	\N	t
1958	\N	\N	1	45	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1959	\N	\N	1	45	22	0	0	0	0	0	0	0	0	\N	0	26824	0	0	\N	t
1960	\N	\N	1	45	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1961	\N	\N	1	45	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1962	\N	\N	1	45	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1963	\N	\N	1	46	1	0	0	0	0	0	0	0	0	\N	23458	0	0	0	\N	t
1964	\N	\N	1	46	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1965	\N	\N	1	46	3	0	0	0	0	0	0	0	0	\N	0	24481	0	0	\N	t
1966	\N	\N	1	46	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1967	\N	\N	1	46	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1968	\N	\N	1	46	6	0	0	0	0	0	0	0	0	\N	0	24036	0	0	\N	t
1969	\N	\N	1	46	7	0	0	0	0	0	0	0	0	\N	24769	0	0	0	\N	t
1970	\N	\N	1	46	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1971	\N	\N	1	46	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1972	\N	\N	1	46	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1973	\N	\N	1	46	11	0	0	0	0	0	0	0	0	\N	22014	0	0	0	\N	t
1974	\N	\N	1	46	12	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1975	\N	\N	1	46	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1976	\N	\N	1	46	14	0	0	0	0	0	0	0	0	\N	24126	0	0	0	\N	t
1977	\N	\N	1	46	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1978	\N	\N	1	46	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1979	\N	\N	1	46	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1980	\N	\N	1	46	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1981	\N	\N	1	46	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1982	\N	\N	1	46	20	0	0	0	0	0	0	0	0	\N	0	26015	0	0	\N	t
1983	\N	\N	1	46	21	0	0	0	0	0	0	0	0	\N	26068	0	0	0	\N	t
1984	\N	\N	1	46	22	0	0	0	0	0	0	0	0	\N	22129	0	0	0	\N	t
1985	\N	\N	1	46	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1986	\N	\N	1	46	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1987	\N	\N	1	46	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1988	\N	\N	1	47	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1989	\N	\N	1	47	2	0	0	0	0	0	0	0	0	\N	22767	0	0	0	\N	t
1990	\N	\N	1	47	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1991	\N	\N	1	47	4	0	0	0	0	0	0	0	0	\N	25656	0	0	0	\N	t
1992	\N	\N	1	47	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1993	\N	\N	1	47	6	0	0	0	0	0	0	0	0	\N	23952	0	0	0	\N	t
1994	\N	\N	1	47	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1995	\N	\N	1	47	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1996	\N	\N	1	47	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1997	\N	\N	1	47	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
1998	\N	\N	1	47	11	0	0	0	0	0	0	0	0	\N	0	22874	0	0	\N	t
1999	\N	\N	1	47	12	0	0	0	0	0	0	0	0	\N	26340	0	0	0	\N	t
2000	\N	\N	1	47	13	0	0	0	0	0	0	0	0	\N	24937	0	0	0	\N	t
2001	\N	\N	1	47	14	0	0	0	0	0	0	0	0	\N	23454	0	0	0	\N	t
2002	\N	\N	1	47	15	0	0	0	0	0	0	0	0	\N	26085	0	0	0	\N	t
2003	\N	\N	1	47	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2004	\N	\N	1	47	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2005	\N	\N	1	47	18	0	0	0	0	0	0	0	0	\N	24694	0	0	0	\N	t
2006	\N	\N	1	47	19	0	0	0	0	0	0	0	0	\N	24233	0	0	0	\N	t
2007	\N	\N	1	47	20	0	0	0	0	0	0	0	0	\N	0	25983	0	0	\N	t
2008	\N	\N	1	47	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2009	\N	\N	1	47	22	0	0	0	0	0	0	0	0	\N	26077	0	0	0	\N	t
2010	\N	\N	1	47	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2011	\N	\N	1	47	24	0	0	0	0	0	0	0	0	\N	24891	0	0	0	\N	t
2012	\N	\N	1	47	25	0	0	0	0	0	0	0	0	\N	0	24923	0	0	\N	t
2013	\N	\N	1	48	1	0	0	0	0	0	0	0	0	\N	23786	0	0	0	\N	t
2014	\N	\N	1	48	2	0	0	0	0	0	0	0	0	\N	0	23404	0	0	\N	t
2015	\N	\N	1	48	3	0	0	0	0	0	0	0	0	\N	25211	0	0	0	\N	t
2016	\N	\N	1	48	4	0	0	0	0	0	0	0	0	\N	24330	0	0	0	\N	t
2017	\N	\N	1	48	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2018	\N	\N	1	48	6	0	0	0	0	0	0	0	0	\N	0	26629	0	0	\N	t
2019	\N	\N	1	48	7	0	0	0	0	0	0	0	0	\N	0	23633	0	0	\N	t
2020	\N	\N	1	48	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2021	\N	\N	1	48	9	0	0	0	0	0	0	0	0	\N	24072	0	0	0	\N	t
2022	\N	\N	1	48	10	0	0	0	0	0	0	0	0	\N	25704	0	0	0	\N	t
2023	\N	\N	1	48	11	0	0	0	0	0	0	0	0	\N	22115	0	0	0	\N	t
2024	\N	\N	1	48	12	0	0	0	0	0	0	0	0	\N	24217	0	0	0	\N	t
2025	\N	\N	1	48	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2026	\N	\N	1	48	14	0	0	0	0	0	0	0	0	\N	22358	0	0	0	\N	t
2027	\N	\N	1	48	15	0	0	0	0	0	0	0	0	\N	22532	0	0	0	\N	t
2028	\N	\N	1	48	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2029	\N	\N	1	48	17	0	0	0	0	0	0	0	0	\N	0	24996	0	0	\N	t
2030	\N	\N	1	48	18	0	0	0	0	0	0	0	0	\N	23031	0	0	0	\N	t
2031	\N	\N	1	48	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2032	\N	\N	1	48	20	0	0	0	0	0	0	0	0	\N	26619	0	0	0	\N	t
2033	\N	\N	1	48	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2034	\N	\N	1	48	22	0	0	0	0	0	0	0	0	\N	24556	0	0	0	\N	t
2035	\N	\N	1	48	23	0	0	0	0	0	0	0	0	\N	23052	0	0	0	\N	t
2036	\N	\N	1	48	24	0	0	0	0	0	0	0	0	\N	26474	0	0	0	\N	t
2037	\N	\N	1	48	25	0	0	0	0	0	0	0	0	\N	23501	0	0	0	\N	t
2038	\N	\N	1	49	1	0	0	0	0	0	0	0	0	\N	25676	0	0	0	\N	t
2039	\N	\N	1	49	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2040	\N	\N	1	49	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2041	\N	\N	1	49	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2042	\N	\N	1	49	5	0	0	0	0	0	0	0	0	\N	0	22542	0	0	\N	t
2043	\N	\N	1	49	6	0	0	0	0	0	0	0	0	\N	26950	0	0	0	\N	t
2044	\N	\N	1	49	7	0	0	0	0	0	0	0	0	\N	24779	0	0	0	\N	t
2045	\N	\N	1	49	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2046	\N	\N	1	49	9	0	0	0	0	0	0	0	0	\N	23612	0	0	0	\N	t
2047	\N	\N	1	49	10	0	0	0	0	0	0	0	0	\N	23191	0	0	0	\N	t
2048	\N	\N	1	49	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2049	\N	\N	1	49	12	0	0	0	0	0	0	0	0	\N	26808	0	0	0	\N	t
2050	\N	\N	1	49	13	0	0	0	0	0	0	0	0	\N	26016	0	0	0	\N	t
2051	\N	\N	1	49	14	0	0	0	0	0	0	0	0	\N	0	22700	0	0	\N	t
2052	\N	\N	1	49	15	0	0	0	0	0	0	0	0	\N	0	25725	0	0	\N	t
2053	\N	\N	1	49	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2054	\N	\N	1	49	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2055	\N	\N	1	49	18	0	0	0	0	0	0	0	0	\N	24762	0	0	0	\N	t
2056	\N	\N	1	49	19	0	0	0	0	0	0	0	0	\N	0	24735	0	0	\N	t
2057	\N	\N	1	49	20	0	0	0	0	0	0	0	0	\N	22762	0	0	0	\N	t
2058	\N	\N	1	49	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2059	\N	\N	1	49	22	0	0	0	0	0	0	0	0	\N	22723	0	0	0	\N	t
2060	\N	\N	1	49	23	0	0	0	0	0	0	0	0	\N	22658	0	0	0	\N	t
2061	\N	\N	1	49	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2062	\N	\N	1	49	25	0	0	0	0	0	0	0	0	\N	26762	0	0	0	\N	t
2063	\N	\N	1	50	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2064	\N	\N	1	50	2	0	0	0	0	0	0	0	0	\N	25276	0	0	0	\N	t
2065	\N	\N	1	50	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2066	\N	\N	1	50	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2067	\N	\N	1	50	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2068	\N	\N	1	50	6	0	0	0	0	0	0	0	0	\N	25055	0	0	0	\N	t
2069	\N	\N	1	50	7	0	0	0	0	0	0	0	0	\N	0	22816	0	0	\N	t
2070	\N	\N	1	50	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2071	\N	\N	1	50	9	0	0	0	0	0	0	0	0	\N	23648	0	0	0	\N	t
2072	\N	\N	1	50	10	0	0	0	0	0	0	0	0	\N	22676	0	0	0	\N	t
2073	\N	\N	1	50	11	0	0	0	0	0	0	0	0	\N	23851	0	0	0	\N	t
2074	\N	\N	1	50	12	0	0	0	0	0	0	0	0	\N	24173	0	0	0	\N	t
2075	\N	\N	1	50	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2076	\N	\N	1	50	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2077	\N	\N	1	50	15	0	0	0	0	0	0	0	0	\N	22122	0	0	0	\N	t
2078	\N	\N	1	50	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2079	\N	\N	1	50	17	0	0	0	0	0	0	0	0	\N	22460	0	0	0	\N	t
2080	\N	\N	1	50	18	0	0	0	0	0	0	0	0	\N	24362	0	0	0	\N	t
2081	\N	\N	1	50	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2082	\N	\N	1	50	20	0	0	0	0	0	0	0	0	\N	25123	0	0	0	\N	t
2083	\N	\N	1	50	21	0	0	0	0	0	0	0	0	\N	25217	0	0	0	\N	t
2084	\N	\N	1	50	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2085	\N	\N	1	50	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2086	\N	\N	1	50	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2087	\N	\N	1	50	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2088	\N	\N	1	51	1	0	0	0	0	0	0	0	0	\N	22549	0	0	0	\N	t
2089	\N	\N	1	51	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2090	\N	\N	1	51	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2091	\N	\N	1	51	4	0	0	0	0	0	0	0	0	\N	22648	0	0	0	\N	t
2092	\N	\N	1	51	5	0	0	0	0	0	0	0	0	\N	23273	0	0	0	\N	t
2093	\N	\N	1	51	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2094	\N	\N	1	51	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2095	\N	\N	1	51	8	0	0	0	0	0	0	0	0	\N	0	26636	0	0	\N	t
2096	\N	\N	1	51	9	0	0	0	0	0	0	0	0	\N	22435	0	0	0	\N	t
2097	\N	\N	1	51	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2098	\N	\N	1	51	11	0	0	0	0	0	0	0	0	\N	25089	0	0	0	\N	t
2099	\N	\N	1	51	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2100	\N	\N	1	51	13	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2101	\N	\N	1	51	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2102	\N	\N	1	51	15	0	0	0	0	0	0	0	0	\N	26984	0	0	0	\N	t
2103	\N	\N	1	51	16	0	0	0	0	0	0	0	0	\N	26471	0	0	0	\N	t
2104	\N	\N	1	51	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2105	\N	\N	1	51	18	0	0	0	0	0	0	0	0	\N	25521	0	0	0	\N	t
2106	\N	\N	1	51	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2107	\N	\N	1	51	20	0	0	0	0	0	0	0	0	\N	25136	0	0	0	\N	t
2108	\N	\N	1	51	21	0	0	0	0	0	0	0	0	\N	24630	0	0	0	\N	t
2109	\N	\N	1	51	22	0	0	0	0	0	0	0	0	\N	26545	0	0	0	\N	t
2110	\N	\N	1	51	23	0	0	0	0	0	0	0	0	\N	0	24817	0	0	\N	t
2111	\N	\N	1	51	24	0	0	0	0	0	0	0	0	\N	25254	0	0	0	\N	t
2112	\N	\N	1	51	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2113	\N	\N	1	52	1	0	0	0	0	0	0	0	0	\N	26924	0	0	0	\N	t
2114	\N	\N	1	52	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2115	\N	\N	1	52	3	0	0	0	0	0	0	0	0	\N	26205	0	0	0	\N	t
2116	\N	\N	1	52	4	0	0	0	0	0	0	0	0	\N	23269	0	0	0	\N	t
2117	\N	\N	1	52	5	0	0	0	0	0	0	0	0	\N	26683	0	0	0	\N	t
2118	\N	\N	1	52	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2119	\N	\N	1	52	7	0	0	0	0	0	0	0	0	\N	0	26986	0	0	\N	t
2120	\N	\N	1	52	8	0	0	0	0	0	0	0	0	\N	26867	0	0	0	\N	t
2121	\N	\N	1	52	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2122	\N	\N	1	52	10	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2123	\N	\N	1	52	11	0	0	0	0	0	0	0	0	\N	22287	0	0	0	\N	t
2124	\N	\N	1	52	12	0	0	0	0	0	0	0	0	\N	26678	0	0	0	\N	t
2125	\N	\N	1	52	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2126	\N	\N	1	52	14	0	0	0	0	0	0	0	0	\N	26082	0	0	0	\N	t
2127	\N	\N	1	52	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2128	\N	\N	1	52	16	0	0	0	0	0	0	0	0	\N	22737	0	0	0	\N	t
2129	\N	\N	1	52	17	0	0	0	0	0	0	0	0	\N	23519	0	0	0	\N	t
2130	\N	\N	1	52	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2131	\N	\N	1	52	19	0	0	0	0	0	0	0	0	\N	0	26091	0	0	\N	t
2132	\N	\N	1	52	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2133	\N	\N	1	52	21	0	0	0	0	0	0	0	0	\N	25792	0	0	0	\N	t
2134	\N	\N	1	52	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2135	\N	\N	1	52	23	0	0	0	0	0	0	0	0	\N	24574	0	0	0	\N	t
2136	\N	\N	1	52	24	0	0	0	0	0	0	0	0	\N	0	25357	0	0	\N	t
2137	\N	\N	1	52	25	0	0	0	0	0	0	0	0	\N	25886	0	0	0	\N	t
2138	\N	\N	1	53	1	0	0	0	0	0	0	0	0	\N	25019	0	0	0	\N	t
2139	\N	\N	1	53	2	0	0	0	0	0	0	0	0	\N	25224	0	0	0	\N	t
2140	\N	\N	1	53	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2141	\N	\N	1	53	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2142	\N	\N	1	53	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2143	\N	\N	1	53	6	0	0	0	0	0	0	0	0	\N	0	24522	0	0	\N	t
2144	\N	\N	1	53	7	0	0	0	0	0	0	0	0	\N	24421	0	0	0	\N	t
2145	\N	\N	1	53	8	0	0	0	0	0	0	0	0	\N	22887	0	0	0	\N	t
2146	\N	\N	1	53	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2147	\N	\N	1	53	10	0	0	0	0	0	0	0	0	\N	26977	0	0	0	\N	t
2148	\N	\N	1	53	11	0	0	0	0	0	0	0	0	\N	22929	0	0	0	\N	t
2149	\N	\N	1	53	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2150	\N	\N	1	53	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2151	\N	\N	1	53	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2152	\N	\N	1	53	15	0	0	0	0	0	0	0	0	\N	24426	0	0	0	\N	t
2153	\N	\N	1	53	16	0	0	0	0	0	0	0	0	\N	25741	0	0	0	\N	t
2154	\N	\N	1	53	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2155	\N	\N	1	53	18	0	0	0	0	0	0	0	0	\N	22974	0	0	0	\N	t
2156	\N	\N	1	53	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2157	\N	\N	1	53	20	0	0	0	0	0	0	0	0	\N	26926	0	0	0	\N	t
2158	\N	\N	1	53	21	0	0	0	0	0	0	0	0	\N	26467	0	0	0	\N	t
2159	\N	\N	1	53	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2160	\N	\N	1	53	23	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2161	\N	\N	1	53	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2162	\N	\N	1	53	25	0	0	0	0	0	0	0	0	\N	23277	0	0	0	\N	t
2163	\N	\N	1	54	1	0	0	0	0	0	0	0	0	\N	25852	0	0	0	\N	t
2164	\N	\N	1	54	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2165	\N	\N	1	54	3	0	0	0	0	0	0	0	0	\N	24759	0	0	0	\N	t
2166	\N	\N	1	54	4	0	0	0	0	0	0	0	0	\N	0	26606	0	0	\N	t
2167	\N	\N	1	54	5	0	0	0	0	0	0	0	0	\N	0	22541	0	0	\N	t
2168	\N	\N	1	54	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2169	\N	\N	1	54	7	0	0	0	0	0	0	0	0	\N	23046	0	0	0	\N	t
2170	\N	\N	1	54	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2171	\N	\N	1	54	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2172	\N	\N	1	54	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2173	\N	\N	1	54	11	0	0	0	0	0	0	0	0	\N	0	26091	0	0	\N	t
2174	\N	\N	1	54	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2175	\N	\N	1	54	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2176	\N	\N	1	54	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2177	\N	\N	1	54	15	0	0	0	0	0	0	0	0	\N	24257	0	0	0	\N	t
2178	\N	\N	1	54	16	0	0	0	0	0	0	0	0	\N	0	25482	0	0	\N	t
2179	\N	\N	1	54	17	0	0	0	0	0	0	0	0	\N	24718	0	0	0	\N	t
2180	\N	\N	1	54	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2181	\N	\N	1	54	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2182	\N	\N	1	54	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2183	\N	\N	1	54	21	0	0	0	0	0	0	0	0	\N	26410	0	0	0	\N	t
2184	\N	\N	1	54	22	0	0	0	0	0	0	0	0	\N	23173	0	0	0	\N	t
2185	\N	\N	1	54	23	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2186	\N	\N	1	54	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2187	\N	\N	1	54	25	0	0	0	0	0	0	0	0	\N	0	23790	0	0	\N	t
2188	\N	\N	1	55	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2189	\N	\N	1	55	2	0	0	0	0	0	0	0	0	\N	24637	0	0	0	\N	t
2190	\N	\N	1	55	3	0	0	0	0	0	0	0	0	\N	25360	0	0	0	\N	t
2191	\N	\N	1	55	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2192	\N	\N	1	55	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2193	\N	\N	1	55	6	0	0	0	0	0	0	0	0	\N	24688	0	0	0	\N	t
2194	\N	\N	1	55	7	0	0	0	0	0	0	0	0	\N	23220	0	0	0	\N	t
2195	\N	\N	1	55	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2196	\N	\N	1	55	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2197	\N	\N	1	55	10	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2198	\N	\N	1	55	11	0	0	0	0	0	0	0	0	\N	23406	0	0	0	\N	t
2199	\N	\N	1	55	12	0	0	0	0	0	0	0	0	\N	25759	0	0	0	\N	t
2200	\N	\N	1	55	13	0	0	0	0	0	0	0	0	\N	22891	0	0	0	\N	t
2201	\N	\N	1	55	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2202	\N	\N	1	55	15	0	0	0	0	0	0	0	0	\N	23921	0	0	0	\N	t
2203	\N	\N	1	55	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2204	\N	\N	1	55	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2205	\N	\N	1	55	18	0	0	0	0	0	0	0	0	\N	22157	0	0	0	\N	t
2206	\N	\N	1	55	19	0	0	0	0	0	0	0	0	\N	0	22587	0	0	\N	t
2207	\N	\N	1	55	20	0	0	0	0	0	0	0	0	\N	0	24838	0	0	\N	t
2208	\N	\N	1	55	21	0	0	0	0	0	0	0	0	\N	26413	0	0	0	\N	t
2209	\N	\N	1	55	22	0	0	0	0	0	0	0	0	\N	22536	0	0	0	\N	t
2210	\N	\N	1	55	23	0	0	0	0	0	0	0	0	\N	0	22452	0	0	\N	t
2211	\N	\N	1	55	24	0	0	0	0	0	0	0	0	\N	26884	0	0	0	\N	t
2212	\N	\N	1	55	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2213	\N	\N	1	56	1	0	0	0	0	0	0	0	0	\N	25414	0	0	0	\N	t
2214	\N	\N	1	56	2	0	0	0	0	0	0	0	0	\N	0	26651	0	0	\N	t
2215	\N	\N	1	56	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2216	\N	\N	1	56	4	0	0	0	0	0	0	0	0	\N	23278	0	0	0	\N	t
2217	\N	\N	1	56	5	0	0	0	0	0	0	0	0	\N	23113	0	0	0	\N	t
2218	\N	\N	1	56	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2219	\N	\N	1	56	7	0	0	0	0	0	0	0	0	\N	25722	0	0	0	\N	t
2220	\N	\N	1	56	8	0	0	0	0	0	0	0	0	\N	24190	0	0	0	\N	t
2221	\N	\N	1	56	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2222	\N	\N	1	56	10	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2223	\N	\N	1	56	11	0	0	0	0	0	0	0	0	\N	26089	0	0	0	\N	t
2224	\N	\N	1	56	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2225	\N	\N	1	56	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2226	\N	\N	1	56	14	0	0	0	0	0	0	0	0	\N	24279	0	0	0	\N	t
2227	\N	\N	1	56	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2228	\N	\N	1	56	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2229	\N	\N	1	56	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2230	\N	\N	1	56	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2231	\N	\N	1	56	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2232	\N	\N	1	56	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2233	\N	\N	1	56	21	0	0	0	0	0	0	0	0	\N	26632	0	0	0	\N	t
2234	\N	\N	1	56	22	0	0	0	0	0	0	0	0	\N	0	26907	0	0	\N	t
2235	\N	\N	1	56	23	0	0	0	0	0	0	0	0	\N	0	25224	0	0	\N	t
2236	\N	\N	1	56	24	0	0	0	0	0	0	0	0	\N	22939	0	0	0	\N	t
2237	\N	\N	1	56	25	0	0	0	0	0	0	0	0	\N	23840	0	0	0	\N	t
2238	\N	\N	1	57	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2239	\N	\N	1	57	2	0	0	0	0	0	0	0	0	\N	22393	0	0	0	\N	t
2240	\N	\N	1	57	3	0	0	0	0	0	0	0	0	\N	23537	0	0	0	\N	t
2241	\N	\N	1	57	4	0	0	0	0	0	0	0	0	\N	22501	0	0	0	\N	t
2242	\N	\N	1	57	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2243	\N	\N	1	57	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2244	\N	\N	1	57	7	0	0	0	0	0	0	0	0	\N	0	26528	0	0	\N	t
2245	\N	\N	1	57	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2246	\N	\N	1	57	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2247	\N	\N	1	57	10	0	0	0	0	0	0	0	0	\N	22919	0	0	0	\N	t
2248	\N	\N	1	57	11	0	0	0	0	0	0	0	0	\N	0	22994	0	0	\N	t
2249	\N	\N	1	57	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2250	\N	\N	1	57	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2251	\N	\N	1	57	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2252	\N	\N	1	57	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2253	\N	\N	1	57	16	0	0	0	0	0	0	0	0	\N	22229	0	0	0	\N	t
2254	\N	\N	1	57	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2255	\N	\N	1	57	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2256	\N	\N	1	57	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2257	\N	\N	1	57	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2258	\N	\N	1	57	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2259	\N	\N	1	57	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2260	\N	\N	1	57	23	0	0	0	0	0	0	0	0	\N	26103	0	0	0	\N	t
2261	\N	\N	1	57	24	0	0	0	0	0	0	0	0	\N	22529	0	0	0	\N	t
2262	\N	\N	1	57	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2263	\N	\N	1	58	1	0	0	0	0	0	0	0	0	\N	26359	0	0	0	\N	t
2264	\N	\N	1	58	2	0	0	0	0	0	0	0	0	\N	0	26087	0	0	\N	t
2265	\N	\N	1	58	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2266	\N	\N	1	58	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2267	\N	\N	1	58	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2268	\N	\N	1	58	6	0	0	0	0	0	0	0	0	\N	22568	0	0	0	\N	t
2269	\N	\N	1	58	7	0	0	0	0	0	0	0	0	\N	23690	0	0	0	\N	t
2270	\N	\N	1	58	8	0	0	0	0	0	0	0	0	\N	23377	0	0	0	\N	t
2271	\N	\N	1	58	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2272	\N	\N	1	58	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2273	\N	\N	1	58	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2274	\N	\N	1	58	12	0	0	0	0	0	0	0	0	\N	0	26886	0	0	\N	t
2275	\N	\N	1	58	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2276	\N	\N	1	58	14	0	0	0	0	0	0	0	0	\N	22653	0	0	0	\N	t
2277	\N	\N	1	58	15	0	0	0	0	0	0	0	0	\N	0	25824	0	0	\N	t
2278	\N	\N	1	58	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2279	\N	\N	1	58	17	0	0	0	0	0	0	0	0	\N	24829	0	0	0	\N	t
2280	\N	\N	1	58	18	0	0	0	0	0	0	0	0	\N	22544	0	0	0	\N	t
2281	\N	\N	1	58	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2282	\N	\N	1	58	20	0	0	0	0	0	0	0	0	\N	25009	0	0	0	\N	t
2283	\N	\N	1	58	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2284	\N	\N	1	58	22	0	0	0	0	0	0	0	0	\N	25321	0	0	0	\N	t
2285	\N	\N	1	58	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2286	\N	\N	1	58	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2287	\N	\N	1	58	25	0	0	0	0	0	0	0	0	\N	24525	0	0	0	\N	t
2288	\N	\N	1	59	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2289	\N	\N	1	59	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2290	\N	\N	1	59	3	0	0	0	0	0	0	0	0	\N	24533	0	0	0	\N	t
2291	\N	\N	1	59	4	0	0	0	0	0	0	0	0	\N	0	25870	0	0	\N	t
2292	\N	\N	1	59	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2293	\N	\N	1	59	6	0	0	0	0	0	0	0	0	\N	25039	0	0	0	\N	t
2294	\N	\N	1	59	7	0	0	0	0	0	0	0	0	\N	26948	0	0	0	\N	t
2295	\N	\N	1	59	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2296	\N	\N	1	59	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2297	\N	\N	1	59	10	0	0	0	0	0	0	0	0	\N	0	23759	0	0	\N	t
2298	\N	\N	1	59	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2299	\N	\N	1	59	12	0	0	0	0	0	0	0	0	\N	24647	0	0	0	\N	t
2300	\N	\N	1	59	13	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2301	\N	\N	1	59	14	0	0	0	0	0	0	0	0	\N	22544	0	0	0	\N	t
2302	\N	\N	1	59	15	0	0	0	0	0	0	0	0	\N	24729	0	0	0	\N	t
2303	\N	\N	1	59	16	0	0	0	0	0	0	0	0	\N	26056	0	0	0	\N	t
2304	\N	\N	1	59	17	0	0	0	0	0	0	0	0	\N	25299	0	0	0	\N	t
2305	\N	\N	1	59	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2306	\N	\N	1	59	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2307	\N	\N	1	59	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2308	\N	\N	1	59	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2309	\N	\N	1	59	22	0	0	0	0	0	0	0	0	\N	22889	0	0	0	\N	t
2310	\N	\N	1	59	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2311	\N	\N	1	59	24	0	0	0	0	0	0	0	0	\N	22157	0	0	0	\N	t
2312	\N	\N	1	59	25	0	0	0	0	0	0	0	0	\N	0	24438	0	0	\N	t
2313	\N	\N	1	60	1	0	0	0	0	0	0	0	0	\N	24725	0	0	0	\N	t
2314	\N	\N	1	60	2	0	0	0	0	0	0	0	0	\N	22552	0	0	0	\N	t
2315	\N	\N	1	60	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2316	\N	\N	1	60	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2317	\N	\N	1	60	5	0	0	0	0	0	0	0	0	\N	26099	0	0	0	\N	t
2318	\N	\N	1	60	6	0	0	0	0	0	0	0	0	\N	26841	0	0	0	\N	t
2319	\N	\N	1	60	7	0	0	0	0	0	0	0	0	\N	22887	0	0	0	\N	t
2320	\N	\N	1	60	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2321	\N	\N	1	60	9	0	0	0	0	0	0	0	0	\N	22495	0	0	0	\N	t
2322	\N	\N	1	60	10	0	0	0	0	0	0	0	0	\N	0	24750	0	0	\N	t
2323	\N	\N	1	60	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2324	\N	\N	1	60	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2325	\N	\N	1	60	13	0	0	0	0	0	0	0	0	\N	26041	0	0	0	\N	t
2326	\N	\N	1	60	14	0	0	0	0	0	0	0	0	\N	26115	0	0	0	\N	t
2327	\N	\N	1	60	15	0	0	0	0	0	0	0	0	\N	0	25271	0	0	\N	t
2328	\N	\N	1	60	16	0	0	0	0	0	0	0	0	\N	26695	0	0	0	\N	t
2329	\N	\N	1	60	17	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2330	\N	\N	1	60	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2331	\N	\N	1	60	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2332	\N	\N	1	60	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2333	\N	\N	1	60	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2334	\N	\N	1	60	22	0	0	0	0	0	0	0	0	\N	0	22805	0	0	\N	t
2335	\N	\N	1	60	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2336	\N	\N	1	60	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2337	\N	\N	1	60	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2338	\N	\N	1	61	1	0	0	0	0	0	0	0	0	\N	26516	0	0	0	\N	t
2339	\N	\N	1	61	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2340	\N	\N	1	61	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2341	\N	\N	1	61	4	0	0	0	0	0	0	0	0	\N	23178	0	0	0	\N	t
2342	\N	\N	1	61	5	0	0	0	0	0	0	0	0	\N	23093	0	0	0	\N	t
2343	\N	\N	1	61	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2344	\N	\N	1	61	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2345	\N	\N	1	61	8	0	0	0	0	0	0	0	0	\N	0	24474	0	0	\N	t
2346	\N	\N	1	61	9	0	0	0	0	0	0	0	0	\N	0	24543	0	0	\N	t
2347	\N	\N	1	61	10	0	0	0	0	0	0	0	0	\N	24166	0	0	0	\N	t
2348	\N	\N	1	61	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2349	\N	\N	1	61	12	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2350	\N	\N	1	61	13	0	0	0	0	0	0	0	0	\N	25291	0	0	0	\N	t
2351	\N	\N	1	61	14	0	0	0	0	0	0	0	0	\N	24543	0	0	0	\N	t
2352	\N	\N	1	61	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2353	\N	\N	1	61	16	0	0	0	0	0	0	0	0	\N	22746	0	0	0	\N	t
2354	\N	\N	1	61	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2355	\N	\N	1	61	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2356	\N	\N	1	61	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2357	\N	\N	1	61	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2358	\N	\N	1	61	21	0	0	0	0	0	0	0	0	\N	24753	0	0	0	\N	t
2359	\N	\N	1	61	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2360	\N	\N	1	61	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2361	\N	\N	1	61	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2362	\N	\N	1	61	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2363	\N	\N	1	62	1	0	0	0	0	0	0	0	0	\N	25814	0	0	0	\N	t
2364	\N	\N	1	62	2	0	0	0	0	0	0	0	0	\N	0	26090	0	0	\N	t
2365	\N	\N	1	62	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2366	\N	\N	1	62	4	0	0	0	0	0	0	0	0	\N	26078	0	0	0	\N	t
2367	\N	\N	1	62	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2368	\N	\N	1	62	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2369	\N	\N	1	62	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2370	\N	\N	1	62	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2371	\N	\N	1	62	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2372	\N	\N	1	62	10	0	0	0	0	0	0	0	0	\N	0	23900	0	0	\N	t
2373	\N	\N	1	62	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2374	\N	\N	1	62	12	0	0	0	0	0	0	0	0	\N	25410	0	0	0	\N	t
2375	\N	\N	1	62	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2376	\N	\N	1	62	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2377	\N	\N	1	62	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2378	\N	\N	1	62	16	0	0	0	0	0	0	0	0	\N	22873	0	0	0	\N	t
2379	\N	\N	1	62	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2380	\N	\N	1	62	18	0	0	0	0	0	0	0	0	\N	24177	0	0	0	\N	t
2381	\N	\N	1	62	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2382	\N	\N	1	62	20	0	0	0	0	0	0	0	0	\N	26721	0	0	0	\N	t
2383	\N	\N	1	62	21	0	0	0	0	0	0	0	0	\N	26068	0	0	0	\N	t
2384	\N	\N	1	62	22	0	0	0	0	0	0	0	0	\N	25534	0	0	0	\N	t
2385	\N	\N	1	62	23	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2386	\N	\N	1	62	24	0	0	0	0	0	0	0	0	\N	24156	0	0	0	\N	t
2387	\N	\N	1	62	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2388	\N	\N	1	63	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2389	\N	\N	1	63	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2390	\N	\N	1	63	3	0	0	0	0	0	0	0	0	\N	25415	0	0	0	\N	t
2391	\N	\N	1	63	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2392	\N	\N	1	63	5	0	0	0	0	0	0	0	0	\N	26502	0	0	0	\N	t
2393	\N	\N	1	63	6	0	0	0	0	0	0	0	0	\N	24326	0	0	0	\N	t
2394	\N	\N	1	63	7	0	0	0	0	0	0	0	0	\N	25701	0	0	0	\N	t
2395	\N	\N	1	63	8	0	0	0	0	0	0	0	0	\N	26688	0	0	0	\N	t
2396	\N	\N	1	63	9	0	0	0	0	0	0	0	0	\N	22108	0	0	0	\N	t
2397	\N	\N	1	63	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2398	\N	\N	1	63	11	0	0	0	0	0	0	0	0	\N	23929	0	0	0	\N	t
2399	\N	\N	1	63	12	0	0	0	0	0	0	0	0	\N	0	24473	0	0	\N	t
2400	\N	\N	1	63	13	0	0	0	0	0	0	0	0	\N	23633	0	0	0	\N	t
2401	\N	\N	1	63	14	0	0	0	0	0	0	0	0	\N	22414	0	0	0	\N	t
2402	\N	\N	1	63	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2403	\N	\N	1	63	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2404	\N	\N	1	63	17	0	0	0	0	0	0	0	0	\N	25843	0	0	0	\N	t
2405	\N	\N	1	63	18	0	0	0	0	0	0	0	0	\N	25857	0	0	0	\N	t
2406	\N	\N	1	63	19	0	0	0	0	0	0	0	0	\N	24839	0	0	0	\N	t
2407	\N	\N	1	63	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2408	\N	\N	1	63	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2409	\N	\N	1	63	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2410	\N	\N	1	63	23	0	0	0	0	0	0	0	0	\N	24743	0	0	0	\N	t
2411	\N	\N	1	63	24	0	0	0	0	0	0	0	0	\N	22190	0	0	0	\N	t
2412	\N	\N	1	63	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2413	\N	\N	1	64	1	0	0	0	0	0	0	0	0	\N	26718	0	0	0	\N	t
2414	\N	\N	1	64	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2415	\N	\N	1	64	3	0	0	0	0	0	0	0	0	\N	26261	0	0	0	\N	t
2416	\N	\N	1	64	4	0	0	0	0	0	0	0	0	\N	26969	0	0	0	\N	t
2417	\N	\N	1	64	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2418	\N	\N	1	64	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2419	\N	\N	1	64	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2420	\N	\N	1	64	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2421	\N	\N	1	64	9	0	0	0	0	0	0	0	0	\N	0	23715	0	0	\N	t
2422	\N	\N	1	64	10	0	0	0	0	0	0	0	0	\N	26592	0	0	0	\N	t
2423	\N	\N	1	64	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2424	\N	\N	1	64	12	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2425	\N	\N	1	64	13	0	0	0	0	0	0	0	0	\N	23502	0	0	0	\N	t
2426	\N	\N	1	64	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2427	\N	\N	1	64	15	0	0	0	0	0	0	0	0	\N	25363	0	0	0	\N	t
2428	\N	\N	1	64	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2429	\N	\N	1	64	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2430	\N	\N	1	64	18	0	0	0	0	0	0	0	0	\N	26278	0	0	0	\N	t
2431	\N	\N	1	64	19	0	0	0	0	0	0	0	0	\N	24196	0	0	0	\N	t
2432	\N	\N	1	64	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2433	\N	\N	1	64	21	0	0	0	0	0	0	0	0	\N	26166	0	0	0	\N	t
2434	\N	\N	1	64	22	0	0	0	0	0	0	0	0	\N	26998	0	0	0	\N	t
2435	\N	\N	1	64	23	0	0	0	0	0	0	0	0	\N	23862	0	0	0	\N	t
2436	\N	\N	1	64	24	0	0	0	0	0	0	0	0	\N	25684	0	0	0	\N	t
2437	\N	\N	1	64	25	0	0	0	0	0	0	0	0	\N	0	24570	0	0	\N	t
2438	\N	\N	1	65	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2439	\N	\N	1	65	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2440	\N	\N	1	65	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2441	\N	\N	1	65	4	0	0	0	0	0	0	0	0	\N	23142	0	0	0	\N	t
2442	\N	\N	1	65	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2443	\N	\N	1	65	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2444	\N	\N	1	65	7	0	0	0	0	0	0	0	0	\N	0	26885	0	0	\N	t
2445	\N	\N	1	65	8	0	0	0	0	0	0	0	0	\N	24403	0	0	0	\N	t
2446	\N	\N	1	65	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2447	\N	\N	1	65	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2448	\N	\N	1	65	11	0	0	0	0	0	0	0	0	\N	23130	0	0	0	\N	t
2449	\N	\N	1	65	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2450	\N	\N	1	65	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2451	\N	\N	1	65	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2452	\N	\N	1	65	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2453	\N	\N	1	65	16	0	0	0	0	0	0	0	0	\N	22233	0	0	0	\N	t
2454	\N	\N	1	65	17	0	0	0	0	0	0	0	0	\N	26613	0	0	0	\N	t
2455	\N	\N	1	65	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2456	\N	\N	1	65	19	0	0	0	0	0	0	0	0	\N	24632	0	0	0	\N	t
2457	\N	\N	1	65	20	0	0	0	0	0	0	0	0	\N	25227	0	0	0	\N	t
2458	\N	\N	1	65	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2459	\N	\N	1	65	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2460	\N	\N	1	65	23	0	0	0	0	0	0	0	0	\N	22770	0	0	0	\N	t
2461	\N	\N	1	65	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2462	\N	\N	1	65	25	0	0	0	0	0	0	0	0	\N	26793	0	0	0	\N	t
2463	\N	\N	1	66	1	0	0	0	0	0	0	0	0	\N	24514	0	0	0	\N	t
2464	\N	\N	1	66	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2465	\N	\N	1	66	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2466	\N	\N	1	66	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2467	\N	\N	1	66	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2468	\N	\N	1	66	6	0	0	0	0	0	0	0	0	\N	23670	0	0	0	\N	t
2469	\N	\N	1	66	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2470	\N	\N	1	66	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2471	\N	\N	1	66	9	0	0	0	0	0	0	0	0	\N	25426	0	0	0	\N	t
2472	\N	\N	1	66	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2473	\N	\N	1	66	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2474	\N	\N	1	66	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2475	\N	\N	1	66	13	0	0	0	0	0	0	0	0	\N	26545	0	0	0	\N	t
2476	\N	\N	1	66	14	0	0	0	0	0	0	0	0	\N	22962	0	0	0	\N	t
2477	\N	\N	1	66	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2478	\N	\N	1	66	16	0	0	0	0	0	0	0	0	\N	25497	0	0	0	\N	t
2479	\N	\N	1	66	17	0	0	0	0	0	0	0	0	\N	25927	0	0	0	\N	t
2480	\N	\N	1	66	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2481	\N	\N	1	66	19	0	0	0	0	0	0	0	0	\N	24318	0	0	0	\N	t
2482	\N	\N	1	66	20	0	0	0	0	0	0	0	0	\N	25492	0	0	0	\N	t
2483	\N	\N	1	66	21	0	0	0	0	0	0	0	0	\N	24178	0	0	0	\N	t
2484	\N	\N	1	66	22	0	0	0	0	0	0	0	0	\N	26889	0	0	0	\N	t
2485	\N	\N	1	66	23	0	0	0	0	0	0	0	0	\N	23009	0	0	0	\N	t
2486	\N	\N	1	66	24	0	0	0	0	0	0	0	0	\N	23814	0	0	0	\N	t
2487	\N	\N	1	66	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2488	\N	\N	1	67	1	0	0	0	0	0	0	0	0	\N	22933	0	0	0	\N	t
2489	\N	\N	1	67	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2490	\N	\N	1	67	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2491	\N	\N	1	67	4	0	0	0	0	0	0	0	0	\N	26512	0	0	0	\N	t
2492	\N	\N	1	67	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2493	\N	\N	1	67	6	0	0	0	0	0	0	0	0	\N	25736	0	0	0	\N	t
2494	\N	\N	1	67	7	0	0	0	0	0	0	0	0	\N	26750	0	0	0	\N	t
2495	\N	\N	1	67	8	0	0	0	0	0	0	0	0	\N	0	24383	0	0	\N	t
2496	\N	\N	1	67	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2497	\N	\N	1	67	10	0	0	0	0	0	0	0	0	\N	25211	0	0	0	\N	t
2498	\N	\N	1	67	11	0	0	0	0	0	0	0	0	\N	25916	0	0	0	\N	t
2499	\N	\N	1	67	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2500	\N	\N	1	67	13	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2501	\N	\N	1	67	14	0	0	0	0	0	0	0	0	\N	22337	0	0	0	\N	t
2502	\N	\N	1	67	15	0	0	0	0	0	0	0	0	\N	24863	0	0	0	\N	t
2503	\N	\N	1	67	16	0	0	0	0	0	0	0	0	\N	22057	0	0	0	\N	t
2504	\N	\N	1	67	17	0	0	0	0	0	0	0	0	\N	26307	0	0	0	\N	t
2505	\N	\N	1	67	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2506	\N	\N	1	67	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2507	\N	\N	1	67	20	0	0	0	0	0	0	0	0	\N	0	23272	0	0	\N	t
2508	\N	\N	1	67	21	0	0	0	0	0	0	0	0	\N	22762	0	0	0	\N	t
2509	\N	\N	1	67	22	0	0	0	0	0	0	0	0	\N	26736	0	0	0	\N	t
2510	\N	\N	1	67	23	0	0	0	0	0	0	0	0	\N	0	22323	0	0	\N	t
2511	\N	\N	1	67	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2512	\N	\N	1	67	25	0	0	0	0	0	0	0	0	\N	25747	0	0	0	\N	t
2513	\N	\N	1	68	1	0	0	0	0	0	0	0	0	\N	25521	0	0	0	\N	t
2514	\N	\N	1	68	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2515	\N	\N	1	68	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2516	\N	\N	1	68	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2517	\N	\N	1	68	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2518	\N	\N	1	68	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2519	\N	\N	1	68	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2520	\N	\N	1	68	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2521	\N	\N	1	68	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2522	\N	\N	1	68	10	0	0	0	0	0	0	0	0	\N	22769	0	0	0	\N	t
2523	\N	\N	1	68	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2524	\N	\N	1	68	12	0	0	0	0	0	0	0	0	\N	0	24027	0	0	\N	t
2525	\N	\N	1	68	13	0	0	0	0	0	0	0	0	\N	22116	0	0	0	\N	t
2526	\N	\N	1	68	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2527	\N	\N	1	68	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2528	\N	\N	1	68	16	0	0	0	0	0	0	0	0	\N	25348	0	0	0	\N	t
2529	\N	\N	1	68	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2530	\N	\N	1	68	18	0	0	0	0	0	0	0	0	\N	25008	0	0	0	\N	t
2531	\N	\N	1	68	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2532	\N	\N	1	68	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2533	\N	\N	1	68	21	0	0	0	0	0	0	0	0	\N	0	26252	0	0	\N	t
2534	\N	\N	1	68	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2535	\N	\N	1	68	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2536	\N	\N	1	68	24	0	0	0	0	0	0	0	0	\N	22322	0	0	0	\N	t
2537	\N	\N	1	68	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2538	\N	\N	1	69	1	0	0	0	0	0	0	0	0	\N	22201	0	0	0	\N	t
2539	\N	\N	1	69	2	0	0	0	0	0	0	0	0	\N	25468	0	0	0	\N	t
2540	\N	\N	1	69	3	0	0	0	0	0	0	0	0	\N	26986	0	0	0	\N	t
2541	\N	\N	1	69	4	0	0	0	0	0	0	0	0	\N	22818	0	0	0	\N	t
2542	\N	\N	1	69	5	0	0	0	0	0	0	0	0	\N	24516	0	0	0	\N	t
2543	\N	\N	1	69	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2544	\N	\N	1	69	7	0	0	0	0	0	0	0	0	\N	0	23466	0	0	\N	t
2545	\N	\N	1	69	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2546	\N	\N	1	69	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2547	\N	\N	1	69	10	0	0	0	0	0	0	0	0	\N	26522	0	0	0	\N	t
2548	\N	\N	1	69	11	0	0	0	0	0	0	0	0	\N	22674	0	0	0	\N	t
2549	\N	\N	1	69	12	0	0	0	0	0	0	0	0	\N	24116	0	0	0	\N	t
2550	\N	\N	1	69	13	0	0	0	0	0	0	0	0	\N	0	22445	0	0	\N	t
2551	\N	\N	1	69	14	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2552	\N	\N	1	69	15	0	0	0	0	0	0	0	0	\N	0	22287	0	0	\N	t
2553	\N	\N	1	69	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2554	\N	\N	1	69	17	0	0	0	0	0	0	0	0	\N	26409	0	0	0	\N	t
2555	\N	\N	1	69	18	0	0	0	0	0	0	0	0	\N	0	24990	0	0	\N	t
2556	\N	\N	1	69	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2557	\N	\N	1	69	20	0	0	0	0	0	0	0	0	\N	26065	0	0	0	\N	t
2558	\N	\N	1	69	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2559	\N	\N	1	69	22	0	0	0	0	0	0	0	0	\N	0	25042	0	0	\N	t
2560	\N	\N	1	69	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2561	\N	\N	1	69	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2562	\N	\N	1	69	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2563	\N	\N	1	70	1	0	0	0	0	0	0	0	0	\N	23434	0	0	0	\N	t
2564	\N	\N	1	70	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2565	\N	\N	1	70	3	0	0	0	0	0	0	0	0	\N	23874	0	0	0	\N	t
2566	\N	\N	1	70	4	0	0	0	0	0	0	0	0	\N	23377	0	0	0	\N	t
2567	\N	\N	1	70	5	0	0	0	0	0	0	0	0	\N	25858	0	0	0	\N	t
2568	\N	\N	1	70	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2569	\N	\N	1	70	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2570	\N	\N	1	70	8	0	0	0	0	0	0	0	0	\N	0	23563	0	0	\N	t
2571	\N	\N	1	70	9	0	0	0	0	0	0	0	0	\N	22033	0	0	0	\N	t
2572	\N	\N	1	70	10	0	0	0	0	0	0	0	0	\N	26261	0	0	0	\N	t
2573	\N	\N	1	70	11	0	0	0	0	0	0	0	0	\N	24332	0	0	0	\N	t
2574	\N	\N	1	70	12	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2575	\N	\N	1	70	13	0	0	0	0	0	0	0	0	\N	24127	0	0	0	\N	t
2576	\N	\N	1	70	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2577	\N	\N	1	70	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2578	\N	\N	1	70	16	0	0	0	0	0	0	0	0	\N	23826	0	0	0	\N	t
2579	\N	\N	1	70	17	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2580	\N	\N	1	70	18	0	0	0	0	0	0	0	0	\N	26770	0	0	0	\N	t
2581	\N	\N	1	70	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2582	\N	\N	1	70	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2583	\N	\N	1	70	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2584	\N	\N	1	70	22	0	0	0	0	0	0	0	0	\N	0	25198	0	0	\N	t
2585	\N	\N	1	70	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2586	\N	\N	1	70	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2587	\N	\N	1	70	25	0	0	0	0	0	0	0	0	\N	0	22309	0	0	\N	t
2588	\N	\N	1	71	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2589	\N	\N	1	71	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2590	\N	\N	1	71	3	0	0	0	0	0	0	0	0	\N	25962	0	0	0	\N	t
2591	\N	\N	1	71	4	0	0	0	0	0	0	0	0	\N	24575	0	0	0	\N	t
2592	\N	\N	1	71	5	0	0	0	0	0	0	0	0	\N	0	26682	0	0	\N	t
2593	\N	\N	1	71	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2594	\N	\N	1	71	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2595	\N	\N	1	71	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2596	\N	\N	1	71	9	0	0	0	0	0	0	0	0	\N	25337	0	0	0	\N	t
2597	\N	\N	1	71	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2598	\N	\N	1	71	11	0	0	0	0	0	0	0	0	\N	23158	0	0	0	\N	t
2599	\N	\N	1	71	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2600	\N	\N	1	71	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2601	\N	\N	1	71	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2602	\N	\N	1	71	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2603	\N	\N	1	71	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2604	\N	\N	1	71	17	0	0	0	0	0	0	0	0	\N	26466	0	0	0	\N	t
2605	\N	\N	1	71	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2606	\N	\N	1	71	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2607	\N	\N	1	71	20	0	0	0	0	0	0	0	0	\N	22850	0	0	0	\N	t
2608	\N	\N	1	71	21	0	0	0	0	0	0	0	0	\N	22712	0	0	0	\N	t
2609	\N	\N	1	71	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2610	\N	\N	1	71	23	0	0	0	0	0	0	0	0	\N	0	26441	0	0	\N	t
2611	\N	\N	1	71	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2612	\N	\N	1	71	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2613	\N	\N	1	72	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2614	\N	\N	1	72	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2615	\N	\N	1	72	3	0	0	0	0	0	0	0	0	\N	0	25583	0	0	\N	t
2616	\N	\N	1	72	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2617	\N	\N	1	72	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2618	\N	\N	1	72	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2619	\N	\N	1	72	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2620	\N	\N	1	72	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2621	\N	\N	1	72	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2622	\N	\N	1	72	10	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2623	\N	\N	1	72	11	0	0	0	0	0	0	0	0	\N	26393	0	0	0	\N	t
2624	\N	\N	1	72	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2625	\N	\N	1	72	13	0	0	0	0	0	0	0	0	\N	0	25377	0	0	\N	t
2626	\N	\N	1	72	14	0	0	0	0	0	0	0	0	\N	24047	0	0	0	\N	t
2627	\N	\N	1	72	15	0	0	0	0	0	0	0	0	\N	22678	0	0	0	\N	t
2628	\N	\N	1	72	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2629	\N	\N	1	72	17	0	0	0	0	0	0	0	0	\N	23683	0	0	0	\N	t
2630	\N	\N	1	72	18	0	0	0	0	0	0	0	0	\N	24965	0	0	0	\N	t
2631	\N	\N	1	72	19	0	0	0	0	0	0	0	0	\N	22980	0	0	0	\N	t
2632	\N	\N	1	72	20	0	0	0	0	0	0	0	0	\N	0	22787	0	0	\N	t
2633	\N	\N	1	72	21	0	0	0	0	0	0	0	0	\N	26076	0	0	0	\N	t
2634	\N	\N	1	72	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2635	\N	\N	1	72	23	0	0	0	0	0	0	0	0	\N	26678	0	0	0	\N	t
2636	\N	\N	1	72	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2637	\N	\N	1	72	25	0	0	0	0	0	0	0	0	\N	22912	0	0	0	\N	t
2638	\N	\N	1	73	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2639	\N	\N	1	73	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2640	\N	\N	1	73	3	0	0	0	0	0	0	0	0	\N	24185	0	0	0	\N	t
2641	\N	\N	1	73	4	0	0	0	0	0	0	0	0	\N	26939	0	0	0	\N	t
2642	\N	\N	1	73	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2643	\N	\N	1	73	6	0	0	0	0	0	0	0	0	\N	24588	0	0	0	\N	t
2644	\N	\N	1	73	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2645	\N	\N	1	73	8	0	0	0	0	0	0	0	0	\N	23422	0	0	0	\N	t
2646	\N	\N	1	73	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2647	\N	\N	1	73	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2648	\N	\N	1	73	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2649	\N	\N	1	73	12	0	0	0	0	0	0	0	0	\N	22356	0	0	0	\N	t
2650	\N	\N	1	73	13	0	0	0	0	0	0	0	0	\N	0	26378	0	0	\N	t
2651	\N	\N	1	73	14	0	0	0	0	0	0	0	0	\N	25553	0	0	0	\N	t
2652	\N	\N	1	73	15	0	0	0	0	0	0	0	0	\N	22033	0	0	0	\N	t
2653	\N	\N	1	73	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2654	\N	\N	1	73	17	0	0	0	0	0	0	0	0	\N	24277	0	0	0	\N	t
2655	\N	\N	1	73	18	0	0	0	0	0	0	0	0	\N	26185	0	0	0	\N	t
2656	\N	\N	1	73	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2657	\N	\N	1	73	20	0	0	0	0	0	0	0	0	\N	24191	0	0	0	\N	t
2658	\N	\N	1	73	21	0	0	0	0	0	0	0	0	\N	0	23626	0	0	\N	t
2659	\N	\N	1	73	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2660	\N	\N	1	73	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2661	\N	\N	1	73	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2662	\N	\N	1	73	25	0	0	0	0	0	0	0	0	\N	0	23659	0	0	\N	t
2663	\N	\N	1	74	1	0	0	0	0	0	0	0	0	\N	0	22470	0	0	\N	t
2664	\N	\N	1	74	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2665	\N	\N	1	74	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2666	\N	\N	1	74	4	0	0	0	0	0	0	0	0	\N	22294	0	0	0	\N	t
2667	\N	\N	1	74	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2668	\N	\N	1	74	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2669	\N	\N	1	74	7	0	0	0	0	0	0	0	0	\N	0	22546	0	0	\N	t
2670	\N	\N	1	74	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2671	\N	\N	1	74	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2672	\N	\N	1	74	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2673	\N	\N	1	74	11	0	0	0	0	0	0	0	0	\N	23740	0	0	0	\N	t
2674	\N	\N	1	74	12	0	0	0	0	0	0	0	0	\N	25212	0	0	0	\N	t
2675	\N	\N	1	74	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2676	\N	\N	1	74	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2677	\N	\N	1	74	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2678	\N	\N	1	74	16	0	0	0	0	0	0	0	0	\N	22923	0	0	0	\N	t
2679	\N	\N	1	74	17	0	0	0	0	0	0	0	0	\N	24465	0	0	0	\N	t
2680	\N	\N	1	74	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2681	\N	\N	1	74	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2682	\N	\N	1	74	20	0	0	0	0	0	0	0	0	\N	23767	0	0	0	\N	t
2683	\N	\N	1	74	21	0	0	0	0	0	0	0	0	\N	24591	0	0	0	\N	t
2684	\N	\N	1	74	22	0	0	0	0	0	0	0	0	\N	26838	0	0	0	\N	t
2685	\N	\N	1	74	23	0	0	0	0	0	0	0	0	\N	25607	0	0	0	\N	t
2686	\N	\N	1	74	24	0	0	0	0	0	0	0	0	\N	25376	0	0	0	\N	t
2687	\N	\N	1	74	25	0	0	0	0	0	0	0	0	\N	25232	0	0	0	\N	t
2688	\N	\N	1	75	1	0	0	0	0	0	0	0	0	\N	22376	0	0	0	\N	t
2689	\N	\N	1	75	2	0	0	0	0	0	0	0	0	\N	25828	0	0	0	\N	t
2690	\N	\N	1	75	3	0	0	0	0	0	0	0	0	\N	26812	0	0	0	\N	t
2691	\N	\N	1	75	4	0	0	0	0	0	0	0	0	\N	23131	0	0	0	\N	t
2692	\N	\N	1	75	5	0	0	0	0	0	0	0	0	\N	25109	0	0	0	\N	t
2693	\N	\N	1	75	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2694	\N	\N	1	75	7	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2695	\N	\N	1	75	8	0	0	0	0	0	0	0	0	\N	23634	0	0	0	\N	t
2696	\N	\N	1	75	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2697	\N	\N	1	75	10	0	0	0	0	0	0	0	0	\N	26809	0	0	0	\N	t
2698	\N	\N	1	75	11	0	0	0	0	0	0	0	0	\N	23414	0	0	0	\N	t
2699	\N	\N	1	75	12	0	0	0	0	0	0	0	0	\N	22237	0	0	0	\N	t
2700	\N	\N	1	75	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2701	\N	\N	1	75	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2702	\N	\N	1	75	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2703	\N	\N	1	75	16	0	0	0	0	0	0	0	0	\N	25514	0	0	0	\N	t
2704	\N	\N	1	75	17	0	0	0	0	0	0	0	0	\N	24846	0	0	0	\N	t
2705	\N	\N	1	75	18	0	0	0	0	0	0	0	0	\N	26737	0	0	0	\N	t
2706	\N	\N	1	75	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2707	\N	\N	1	75	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2708	\N	\N	1	75	21	0	0	0	0	0	0	0	0	\N	24970	0	0	0	\N	t
2709	\N	\N	1	75	22	0	0	0	0	0	0	0	0	\N	25990	0	0	0	\N	t
2710	\N	\N	1	75	23	0	0	0	0	0	0	0	0	\N	26688	0	0	0	\N	t
2711	\N	\N	1	75	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2712	\N	\N	1	75	25	0	0	0	0	0	0	0	0	\N	25644	0	0	0	\N	t
2713	\N	\N	1	76	1	0	0	0	0	0	0	0	0	\N	0	25599	0	0	\N	t
2714	\N	\N	1	76	2	0	0	0	0	0	0	0	0	\N	0	26553	0	0	\N	t
2715	\N	\N	1	76	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2716	\N	\N	1	76	4	0	0	0	0	0	0	0	0	\N	0	22251	0	0	\N	t
2717	\N	\N	1	76	5	0	0	0	0	0	0	0	0	\N	23185	0	0	0	\N	t
2718	\N	\N	1	76	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2719	\N	\N	1	76	7	0	0	0	0	0	0	0	0	\N	24471	0	0	0	\N	t
2720	\N	\N	1	76	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2721	\N	\N	1	76	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2722	\N	\N	1	76	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2723	\N	\N	1	76	11	0	0	0	0	0	0	0	0	\N	0	26474	0	0	\N	t
2724	\N	\N	1	76	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2725	\N	\N	1	76	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2726	\N	\N	1	76	14	0	0	0	0	0	0	0	0	\N	0	26210	0	0	\N	t
2727	\N	\N	1	76	15	0	0	0	0	0	0	0	0	\N	0	26984	0	0	\N	t
2728	\N	\N	1	76	16	0	0	0	0	0	0	0	0	\N	24476	0	0	0	\N	t
2729	\N	\N	1	76	17	0	0	0	0	0	0	0	0	\N	26848	0	0	0	\N	t
2730	\N	\N	1	76	18	0	0	0	0	0	0	0	0	\N	0	22621	0	0	\N	t
2731	\N	\N	1	76	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2732	\N	\N	1	76	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2733	\N	\N	1	76	21	0	0	0	0	0	0	0	0	\N	22271	0	0	0	\N	t
2734	\N	\N	1	76	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2735	\N	\N	1	76	23	0	0	0	0	0	0	0	0	\N	26319	0	0	0	\N	t
2736	\N	\N	1	76	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2737	\N	\N	1	76	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2738	\N	\N	1	77	1	0	0	0	0	0	0	0	0	\N	25331	0	0	0	\N	t
2739	\N	\N	1	77	2	0	0	0	0	0	0	0	0	\N	25656	0	0	0	\N	t
2740	\N	\N	1	77	3	0	0	0	0	0	0	0	0	\N	24158	0	0	0	\N	t
2741	\N	\N	1	77	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2742	\N	\N	1	77	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2743	\N	\N	1	77	6	0	0	0	0	0	0	0	0	\N	23260	0	0	0	\N	t
2744	\N	\N	1	77	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2745	\N	\N	1	77	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2746	\N	\N	1	77	9	0	0	0	0	0	0	0	0	\N	22117	0	0	0	\N	t
2747	\N	\N	1	77	10	0	0	0	0	0	0	0	0	\N	0	26117	0	0	\N	t
2748	\N	\N	1	77	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2749	\N	\N	1	77	12	0	0	0	0	0	0	0	0	\N	23219	0	0	0	\N	t
2750	\N	\N	1	77	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2751	\N	\N	1	77	14	0	0	0	0	0	0	0	0	\N	24511	0	0	0	\N	t
2752	\N	\N	1	77	15	0	0	0	0	0	0	0	0	\N	0	25818	0	0	\N	t
2753	\N	\N	1	77	16	0	0	0	0	0	0	0	0	\N	25167	0	0	0	\N	t
2754	\N	\N	1	77	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2755	\N	\N	1	77	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2756	\N	\N	1	77	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2757	\N	\N	1	77	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2758	\N	\N	1	77	21	0	0	0	0	0	0	0	0	\N	23675	0	0	0	\N	t
2759	\N	\N	1	77	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2760	\N	\N	1	77	23	0	0	0	0	0	0	0	0	\N	26526	0	0	0	\N	t
2761	\N	\N	1	77	24	0	0	0	0	0	0	0	0	\N	0	25994	0	0	\N	t
2762	\N	\N	1	77	25	0	0	0	0	0	0	0	0	\N	26009	0	0	0	\N	t
2763	\N	\N	1	78	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2764	\N	\N	1	78	2	0	0	0	0	0	0	0	0	\N	23214	0	0	0	\N	t
2765	\N	\N	1	78	3	0	0	0	0	0	0	0	0	\N	26205	0	0	0	\N	t
2766	\N	\N	1	78	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2767	\N	\N	1	78	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2768	\N	\N	1	78	6	0	0	0	0	0	0	0	0	\N	24100	0	0	0	\N	t
2769	\N	\N	1	78	7	0	0	0	0	0	0	0	0	\N	22983	0	0	0	\N	t
2770	\N	\N	1	78	8	0	0	0	0	0	0	0	0	\N	23128	0	0	0	\N	t
2771	\N	\N	1	78	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2772	\N	\N	1	78	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2773	\N	\N	1	78	11	0	0	0	0	0	0	0	0	\N	25989	0	0	0	\N	t
2774	\N	\N	1	78	12	0	0	0	0	0	0	0	0	\N	22632	0	0	0	\N	t
2775	\N	\N	1	78	13	0	0	0	0	0	0	0	0	\N	22390	0	0	0	\N	t
2776	\N	\N	1	78	14	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2777	\N	\N	1	78	15	0	0	0	0	0	0	0	0	\N	0	22380	0	0	\N	t
2778	\N	\N	1	78	16	0	0	0	0	0	0	0	0	\N	24148	0	0	0	\N	t
2779	\N	\N	1	78	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2780	\N	\N	1	78	18	0	0	0	0	0	0	0	0	\N	22574	0	0	0	\N	t
2781	\N	\N	1	78	19	0	0	0	0	0	0	0	0	\N	24165	0	0	0	\N	t
2782	\N	\N	1	78	20	0	0	0	0	0	0	0	0	\N	0	24364	0	0	\N	t
2783	\N	\N	1	78	21	0	0	0	0	0	0	0	0	\N	22058	0	0	0	\N	t
2784	\N	\N	1	78	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2785	\N	\N	1	78	23	0	0	0	0	0	0	0	0	\N	24993	0	0	0	\N	t
2786	\N	\N	1	78	24	0	0	0	0	0	0	0	0	\N	0	24216	0	0	\N	t
2787	\N	\N	1	78	25	0	0	0	0	0	0	0	0	\N	24538	0	0	0	\N	t
2788	\N	\N	1	79	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2789	\N	\N	1	79	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2790	\N	\N	1	79	3	0	0	0	0	0	0	0	0	\N	24657	0	0	0	\N	t
2791	\N	\N	1	79	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2792	\N	\N	1	79	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2793	\N	\N	1	79	6	0	0	0	0	0	0	0	0	\N	0	25822	0	0	\N	t
2794	\N	\N	1	79	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2795	\N	\N	1	79	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2796	\N	\N	1	79	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2797	\N	\N	1	79	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2798	\N	\N	1	79	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2799	\N	\N	1	79	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2800	\N	\N	1	79	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2801	\N	\N	1	79	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2802	\N	\N	1	79	15	0	0	0	0	0	0	0	0	\N	22411	0	0	0	\N	t
2803	\N	\N	1	79	16	0	0	0	0	0	0	0	0	\N	23287	0	0	0	\N	t
2804	\N	\N	1	79	17	0	0	0	0	0	0	0	0	\N	24566	0	0	0	\N	t
2805	\N	\N	1	79	18	0	0	0	0	0	0	0	0	\N	22596	0	0	0	\N	t
2806	\N	\N	1	79	19	0	0	0	0	0	0	0	0	\N	25800	0	0	0	\N	t
2807	\N	\N	1	79	20	0	0	0	0	0	0	0	0	\N	24763	0	0	0	\N	t
2808	\N	\N	1	79	21	0	0	0	0	0	0	0	0	\N	25279	0	0	0	\N	t
2809	\N	\N	1	79	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2810	\N	\N	1	79	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2811	\N	\N	1	79	24	0	0	0	0	0	0	0	0	\N	22856	0	0	0	\N	t
2812	\N	\N	1	79	25	0	0	0	0	0	0	0	0	\N	26257	0	0	0	\N	t
2813	\N	\N	1	80	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2814	\N	\N	1	80	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2815	\N	\N	1	80	3	0	0	0	0	0	0	0	0	\N	24723	0	0	0	\N	t
2816	\N	\N	1	80	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2817	\N	\N	1	80	5	0	0	0	0	0	0	0	0	\N	23487	0	0	0	\N	t
2818	\N	\N	1	80	6	0	0	0	0	0	0	0	0	\N	0	23912	0	0	\N	t
2819	\N	\N	1	80	7	0	0	0	0	0	0	0	0	\N	22703	0	0	0	\N	t
2820	\N	\N	1	80	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2821	\N	\N	1	80	9	0	0	0	0	0	0	0	0	\N	0	23989	0	0	\N	t
2822	\N	\N	1	80	10	0	0	0	0	0	0	0	0	\N	23440	0	0	0	\N	t
2823	\N	\N	1	80	11	0	0	0	0	0	0	0	0	\N	22225	0	0	0	\N	t
2824	\N	\N	1	80	12	0	0	0	0	0	0	0	0	\N	25433	0	0	0	\N	t
2825	\N	\N	1	80	13	0	0	0	0	0	0	0	0	\N	26607	0	0	0	\N	t
2826	\N	\N	1	80	14	0	0	0	0	0	0	0	0	\N	0	25921	0	0	\N	t
2827	\N	\N	1	80	15	0	0	0	0	0	0	0	0	\N	22217	0	0	0	\N	t
2828	\N	\N	1	80	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2829	\N	\N	1	80	17	0	0	0	0	0	0	0	0	\N	23785	0	0	0	\N	t
2830	\N	\N	1	80	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2831	\N	\N	1	80	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2832	\N	\N	1	80	20	0	0	0	0	0	0	0	0	\N	22234	0	0	0	\N	t
2833	\N	\N	1	80	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2834	\N	\N	1	80	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2835	\N	\N	1	80	23	0	0	0	0	0	0	0	0	\N	22554	0	0	0	\N	t
2836	\N	\N	1	80	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2837	\N	\N	1	80	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2838	\N	\N	1	81	1	0	0	0	0	0	0	0	0	\N	24178	0	0	0	\N	t
2839	\N	\N	1	81	2	0	0	0	0	0	0	0	0	\N	26683	0	0	0	\N	t
2840	\N	\N	1	81	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2841	\N	\N	1	81	4	0	0	0	0	0	0	0	0	\N	24984	0	0	0	\N	t
2842	\N	\N	1	81	5	0	0	0	0	0	0	0	0	\N	26091	0	0	0	\N	t
2843	\N	\N	1	81	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2844	\N	\N	1	81	7	0	0	0	0	0	0	0	0	\N	25266	0	0	0	\N	t
2845	\N	\N	1	81	8	0	0	0	0	0	0	0	0	\N	26240	0	0	0	\N	t
2846	\N	\N	1	81	9	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2847	\N	\N	1	81	10	0	0	0	0	0	0	0	0	\N	22488	0	0	0	\N	t
2848	\N	\N	1	81	11	0	0	0	0	0	0	0	0	\N	26735	0	0	0	\N	t
2849	\N	\N	1	81	12	0	0	0	0	0	0	0	0	\N	25080	0	0	0	\N	t
2850	\N	\N	1	81	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2851	\N	\N	1	81	14	0	0	0	0	0	0	0	0	\N	26200	0	0	0	\N	t
2852	\N	\N	1	81	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2853	\N	\N	1	81	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2854	\N	\N	1	81	17	0	0	0	0	0	0	0	0	\N	23404	0	0	0	\N	t
2855	\N	\N	1	81	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2856	\N	\N	1	81	19	0	0	0	0	0	0	0	0	\N	0	22975	0	0	\N	t
2857	\N	\N	1	81	20	0	0	0	0	0	0	0	0	\N	25062	0	0	0	\N	t
2858	\N	\N	1	81	21	0	0	0	0	0	0	0	0	\N	25939	0	0	0	\N	t
2859	\N	\N	1	81	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2860	\N	\N	1	81	23	0	0	0	0	0	0	0	0	\N	0	22466	0	0	\N	t
2861	\N	\N	1	81	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2862	\N	\N	1	81	25	0	0	0	0	0	0	0	0	\N	24617	0	0	0	\N	t
2863	\N	\N	1	82	1	0	0	0	0	0	0	0	0	\N	0	26561	0	0	\N	t
2864	\N	\N	1	82	2	0	0	0	0	0	0	0	0	\N	24826	0	0	0	\N	t
2865	\N	\N	1	82	3	0	0	0	0	0	0	0	0	\N	25178	0	0	0	\N	t
2866	\N	\N	1	82	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2867	\N	\N	1	82	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2868	\N	\N	1	82	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2869	\N	\N	1	82	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2870	\N	\N	1	82	8	0	0	0	0	0	0	0	0	\N	25823	0	0	0	\N	t
2871	\N	\N	1	82	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2872	\N	\N	1	82	10	0	0	0	0	0	0	0	0	\N	25491	0	0	0	\N	t
2873	\N	\N	1	82	11	0	0	0	0	0	0	0	0	\N	24666	0	0	0	\N	t
2874	\N	\N	1	82	12	0	0	0	0	0	0	0	0	\N	23470	0	0	0	\N	t
2875	\N	\N	1	82	13	0	0	0	0	0	0	0	0	\N	26201	0	0	0	\N	t
2876	\N	\N	1	82	14	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2877	\N	\N	1	82	15	0	0	0	0	0	0	0	0	\N	24292	0	0	0	\N	t
2878	\N	\N	1	82	16	0	0	0	0	0	0	0	0	\N	23371	0	0	0	\N	t
2879	\N	\N	1	82	17	0	0	0	0	0	0	0	0	\N	0	23740	0	0	\N	t
2880	\N	\N	1	82	18	0	0	0	0	0	0	0	0	\N	0	24963	0	0	\N	t
2881	\N	\N	1	82	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2882	\N	\N	1	82	20	0	0	0	0	0	0	0	0	\N	24104	0	0	0	\N	t
2883	\N	\N	1	82	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2884	\N	\N	1	82	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2885	\N	\N	1	82	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2886	\N	\N	1	82	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2887	\N	\N	1	82	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2888	\N	\N	1	83	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2889	\N	\N	1	83	2	0	0	0	0	0	0	0	0	\N	0	26540	0	0	\N	t
2890	\N	\N	1	83	3	0	0	0	0	0	0	0	0	\N	26869	0	0	0	\N	t
2891	\N	\N	1	83	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2892	\N	\N	1	83	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2893	\N	\N	1	83	6	0	0	0	0	0	0	0	0	\N	22198	0	0	0	\N	t
2894	\N	\N	1	83	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2895	\N	\N	1	83	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2896	\N	\N	1	83	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2897	\N	\N	1	83	10	0	0	0	0	0	0	0	0	\N	25052	0	0	0	\N	t
2898	\N	\N	1	83	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2899	\N	\N	1	83	12	0	0	0	0	0	0	0	0	\N	26299	0	0	0	\N	t
2900	\N	\N	1	83	13	0	0	0	0	0	0	0	0	\N	25892	0	0	0	\N	t
2901	\N	\N	1	83	14	0	0	0	0	0	0	0	0	\N	26208	0	0	0	\N	t
2902	\N	\N	1	83	15	0	0	0	0	0	0	0	0	\N	24930	0	0	0	\N	t
2903	\N	\N	1	83	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2904	\N	\N	1	83	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2905	\N	\N	1	83	18	0	0	0	0	0	0	0	0	\N	24484	0	0	0	\N	t
2906	\N	\N	1	83	19	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2907	\N	\N	1	83	20	0	0	0	0	0	0	0	0	\N	23919	0	0	0	\N	t
2908	\N	\N	1	83	21	0	0	0	0	0	0	0	0	\N	0	26054	0	0	\N	t
2909	\N	\N	1	83	22	0	0	0	0	0	0	0	0	\N	24771	0	0	0	\N	t
2910	\N	\N	1	83	23	0	0	0	0	0	0	0	0	\N	25107	0	0	0	\N	t
2911	\N	\N	1	83	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2912	\N	\N	1	83	25	0	0	0	0	0	0	0	0	\N	0	22506	0	0	\N	t
2913	\N	\N	1	84	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2914	\N	\N	1	84	2	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2915	\N	\N	1	84	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2916	\N	\N	1	84	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2917	\N	\N	1	84	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2918	\N	\N	1	84	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2919	\N	\N	1	84	7	0	0	0	0	0	0	0	0	\N	23263	0	0	0	\N	t
2920	\N	\N	1	84	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2921	\N	\N	1	84	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2922	\N	\N	1	84	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2923	\N	\N	1	84	11	0	0	0	0	0	0	0	0	\N	22568	0	0	0	\N	t
2924	\N	\N	1	84	12	0	0	0	0	0	0	0	0	\N	22643	0	0	0	\N	t
2925	\N	\N	1	84	13	0	0	0	0	0	0	0	0	\N	22479	0	0	0	\N	t
2926	\N	\N	1	84	14	0	0	0	0	0	0	0	0	\N	0	23860	0	0	\N	t
2927	\N	\N	1	84	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2928	\N	\N	1	84	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2929	\N	\N	1	84	17	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2930	\N	\N	1	84	18	0	0	0	0	0	0	0	0	\N	25356	0	0	0	\N	t
2931	\N	\N	1	84	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2932	\N	\N	1	84	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2933	\N	\N	1	84	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2934	\N	\N	1	84	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2935	\N	\N	1	84	23	0	0	0	0	0	0	0	0	\N	0	25550	0	0	\N	t
2936	\N	\N	1	84	24	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2937	\N	\N	1	84	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2938	\N	\N	1	85	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2939	\N	\N	1	85	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2940	\N	\N	1	85	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2941	\N	\N	1	85	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2942	\N	\N	1	85	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2943	\N	\N	1	85	6	0	0	0	0	0	0	0	0	\N	23606	0	0	0	\N	t
2944	\N	\N	1	85	7	0	0	0	0	0	0	0	0	\N	26532	0	0	0	\N	t
2945	\N	\N	1	85	8	0	0	0	0	0	0	0	0	\N	26827	0	0	0	\N	t
2946	\N	\N	1	85	9	0	0	0	0	0	0	0	0	\N	26541	0	0	0	\N	t
2947	\N	\N	1	85	10	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2948	\N	\N	1	85	11	0	0	0	0	0	0	0	0	\N	0	23339	0	0	\N	t
2949	\N	\N	1	85	12	0	0	0	0	0	0	0	0	\N	23484	0	0	0	\N	t
2950	\N	\N	1	85	13	0	0	0	0	0	0	0	0	\N	24634	0	0	0	\N	t
2951	\N	\N	1	85	14	0	0	0	0	0	0	0	0	\N	24818	0	0	0	\N	t
2952	\N	\N	1	85	15	0	0	0	0	0	0	0	0	\N	25137	0	0	0	\N	t
2953	\N	\N	1	85	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2954	\N	\N	1	85	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2955	\N	\N	1	85	18	0	0	0	0	0	0	0	0	\N	0	26219	0	0	\N	t
2956	\N	\N	1	85	19	0	0	0	0	0	0	0	0	\N	22460	0	0	0	\N	t
2957	\N	\N	1	85	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2958	\N	\N	1	85	21	0	0	0	0	0	0	0	0	\N	26429	0	0	0	\N	t
2959	\N	\N	1	85	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2960	\N	\N	1	85	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2961	\N	\N	1	85	24	0	0	0	0	0	0	0	0	\N	22056	0	0	0	\N	t
2962	\N	\N	1	85	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2963	\N	\N	1	86	1	0	0	0	0	0	0	0	0	\N	26962	0	0	0	\N	t
2964	\N	\N	1	86	2	0	0	0	0	0	0	0	0	\N	22302	0	0	0	\N	t
2965	\N	\N	1	86	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2966	\N	\N	1	86	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2967	\N	\N	1	86	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2968	\N	\N	1	86	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2969	\N	\N	1	86	7	0	0	0	0	0	0	0	0	\N	24625	0	0	0	\N	t
2970	\N	\N	1	86	8	0	0	0	0	0	0	0	0	\N	26351	0	0	0	\N	t
2971	\N	\N	1	86	9	0	0	0	0	0	0	0	0	\N	25742	0	0	0	\N	t
2972	\N	\N	1	86	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2973	\N	\N	1	86	11	0	0	0	0	0	0	0	0	\N	0	22925	0	0	\N	t
2974	\N	\N	1	86	12	0	0	0	0	0	0	0	0	\N	25355	0	0	0	\N	t
2975	\N	\N	1	86	13	0	0	0	0	0	0	0	0	\N	0	25426	0	0	\N	t
2976	\N	\N	1	86	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2977	\N	\N	1	86	15	0	0	0	0	0	0	0	0	\N	26729	0	0	0	\N	t
2978	\N	\N	1	86	16	0	0	0	0	0	0	0	0	\N	0	26211	0	0	\N	t
2979	\N	\N	1	86	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2980	\N	\N	1	86	18	0	0	0	0	0	0	0	0	\N	0	26948	0	0	\N	t
2981	\N	\N	1	86	19	0	0	0	0	0	0	0	0	\N	25569	0	0	0	\N	t
2982	\N	\N	1	86	20	0	0	0	0	0	0	0	0	\N	23261	0	0	0	\N	t
2983	\N	\N	1	86	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2984	\N	\N	1	86	22	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2985	\N	\N	1	86	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2986	\N	\N	1	86	24	0	0	0	0	0	0	0	0	\N	25298	0	0	0	\N	t
2987	\N	\N	1	86	25	0	0	0	0	0	0	0	0	\N	23994	0	0	0	\N	t
2988	\N	\N	1	87	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2989	\N	\N	1	87	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2990	\N	\N	1	87	3	0	0	0	0	0	0	0	0	\N	23222	0	0	0	\N	t
2991	\N	\N	1	87	4	0	0	0	0	0	0	0	0	\N	25135	0	0	0	\N	t
2992	\N	\N	1	87	5	0	0	0	0	0	0	0	0	\N	23541	0	0	0	\N	t
2993	\N	\N	1	87	6	0	0	0	0	0	0	0	0	\N	23137	0	0	0	\N	t
2994	\N	\N	1	87	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2995	\N	\N	1	87	8	0	0	0	0	0	0	0	0	\N	23055	0	0	0	\N	t
2996	\N	\N	1	87	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2997	\N	\N	1	87	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2998	\N	\N	1	87	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
2999	\N	\N	1	87	12	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3000	\N	\N	1	87	13	0	0	0	0	0	0	0	0	\N	25108	0	0	0	\N	t
3001	\N	\N	1	87	14	0	0	0	0	0	0	0	0	\N	24236	0	0	0	\N	t
3002	\N	\N	1	87	15	0	0	0	0	0	0	0	0	\N	0	26884	0	0	\N	t
3003	\N	\N	1	87	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3004	\N	\N	1	87	17	0	0	0	0	0	0	0	0	\N	24970	0	0	0	\N	t
3005	\N	\N	1	87	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3006	\N	\N	1	87	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3007	\N	\N	1	87	20	0	0	0	0	0	0	0	0	\N	26195	0	0	0	\N	t
3008	\N	\N	1	87	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3009	\N	\N	1	87	22	0	0	0	0	0	0	0	0	\N	26211	0	0	0	\N	t
3010	\N	\N	1	87	23	0	0	0	0	0	0	0	0	\N	0	25688	0	0	\N	t
3011	\N	\N	1	87	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3012	\N	\N	1	87	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3013	\N	\N	1	88	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3014	\N	\N	1	88	2	0	0	0	0	0	0	0	0	\N	24294	0	0	0	\N	t
3015	\N	\N	1	88	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3016	\N	\N	1	88	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3017	\N	\N	1	88	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3018	\N	\N	1	88	6	0	0	0	0	0	0	0	0	\N	26525	0	0	0	\N	t
3019	\N	\N	1	88	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3020	\N	\N	1	88	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3021	\N	\N	1	88	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3022	\N	\N	1	88	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3023	\N	\N	1	88	11	0	0	0	0	0	0	0	0	\N	23106	0	0	0	\N	t
3024	\N	\N	1	88	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3025	\N	\N	1	88	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3026	\N	\N	1	88	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3027	\N	\N	1	88	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3028	\N	\N	1	88	16	0	0	0	0	0	0	0	0	\N	22815	0	0	0	\N	t
3029	\N	\N	1	88	17	0	0	0	0	0	0	0	0	\N	0	22860	0	0	\N	t
3030	\N	\N	1	88	18	0	0	0	0	0	0	0	0	\N	26103	0	0	0	\N	t
3031	\N	\N	1	88	19	0	0	0	0	0	0	0	0	\N	0	24745	0	0	\N	t
3032	\N	\N	1	88	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3033	\N	\N	1	88	21	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3034	\N	\N	1	88	22	0	0	0	0	0	0	0	0	\N	23046	0	0	0	\N	t
3035	\N	\N	1	88	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3036	\N	\N	1	88	24	0	0	0	0	0	0	0	0	\N	0	24169	0	0	\N	t
3037	\N	\N	1	88	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3038	\N	\N	1	89	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3039	\N	\N	1	89	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3040	\N	\N	1	89	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3041	\N	\N	1	89	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3042	\N	\N	1	89	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3043	\N	\N	1	89	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3044	\N	\N	1	89	7	0	0	0	0	0	0	0	0	\N	24024	0	0	0	\N	t
3045	\N	\N	1	89	8	0	0	0	0	0	0	0	0	\N	0	25417	0	0	\N	t
3046	\N	\N	1	89	9	0	0	0	0	0	0	0	0	\N	26353	0	0	0	\N	t
3047	\N	\N	1	89	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3048	\N	\N	1	89	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3049	\N	\N	1	89	12	0	0	0	0	0	0	0	0	\N	24878	0	0	0	\N	t
3050	\N	\N	1	89	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3051	\N	\N	1	89	14	0	0	0	0	0	0	0	0	\N	26828	0	0	0	\N	t
3052	\N	\N	1	89	15	0	0	0	0	0	0	0	0	\N	23811	0	0	0	\N	t
3053	\N	\N	1	89	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3054	\N	\N	1	89	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3055	\N	\N	1	89	18	0	0	0	0	0	0	0	0	\N	25021	0	0	0	\N	t
3056	\N	\N	1	89	19	0	0	0	0	0	0	0	0	\N	22394	0	0	0	\N	t
3057	\N	\N	1	89	20	0	0	0	0	0	0	0	0	\N	0	24048	0	0	\N	t
3058	\N	\N	1	89	21	0	0	0	0	0	0	0	0	\N	22919	0	0	0	\N	t
3059	\N	\N	1	89	22	0	0	0	0	0	0	0	0	\N	23588	0	0	0	\N	t
3060	\N	\N	1	89	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3061	\N	\N	1	89	24	0	0	0	0	0	0	0	0	\N	0	22469	0	0	\N	t
3062	\N	\N	1	89	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3063	\N	\N	1	90	1	0	0	0	0	0	0	0	0	\N	22857	0	0	0	\N	t
3064	\N	\N	1	90	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3065	\N	\N	1	90	3	0	0	0	0	0	0	0	0	\N	26506	0	0	0	\N	t
3066	\N	\N	1	90	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3067	\N	\N	1	90	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3068	\N	\N	1	90	6	0	0	0	0	0	0	0	0	\N	0	22593	0	0	\N	t
3069	\N	\N	1	90	7	0	0	0	0	0	0	0	0	\N	25754	0	0	0	\N	t
3070	\N	\N	1	90	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3071	\N	\N	1	90	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3072	\N	\N	1	90	10	0	0	0	0	0	0	0	0	\N	25198	0	0	0	\N	t
3073	\N	\N	1	90	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3074	\N	\N	1	90	12	0	0	0	0	0	0	0	0	\N	22886	0	0	0	\N	t
3075	\N	\N	1	90	13	0	0	0	0	0	0	0	0	\N	24869	0	0	0	\N	t
3076	\N	\N	1	90	14	0	0	0	0	0	0	0	0	\N	24850	0	0	0	\N	t
3077	\N	\N	1	90	15	0	0	0	0	0	0	0	0	\N	26712	0	0	0	\N	t
3078	\N	\N	1	90	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3079	\N	\N	1	90	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3080	\N	\N	1	90	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3081	\N	\N	1	90	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3082	\N	\N	1	90	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3083	\N	\N	1	90	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3084	\N	\N	1	90	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3085	\N	\N	1	90	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3086	\N	\N	1	90	24	0	0	0	0	0	0	0	0	\N	25624	0	0	0	\N	t
3087	\N	\N	1	90	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3088	\N	\N	1	91	1	0	0	0	0	0	0	0	0	\N	24414	0	0	0	\N	t
3089	\N	\N	1	91	2	0	0	0	0	0	0	0	0	\N	23603	0	0	0	\N	t
3090	\N	\N	1	91	3	0	0	0	0	0	0	0	0	\N	26589	0	0	0	\N	t
3091	\N	\N	1	91	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3092	\N	\N	1	91	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3093	\N	\N	1	91	6	0	0	0	0	0	0	0	0	\N	25039	0	0	0	\N	t
3094	\N	\N	1	91	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3095	\N	\N	1	91	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3096	\N	\N	1	91	9	0	0	0	0	0	0	0	0	\N	22612	0	0	0	\N	t
3097	\N	\N	1	91	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3098	\N	\N	1	91	11	0	0	0	0	0	0	0	0	\N	23321	0	0	0	\N	t
3099	\N	\N	1	91	12	0	0	0	0	0	0	0	0	\N	0	23632	0	0	\N	t
3100	\N	\N	1	91	13	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3101	\N	\N	1	91	14	0	0	0	0	0	0	0	0	\N	23879	0	0	0	\N	t
3102	\N	\N	1	91	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3103	\N	\N	1	91	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3104	\N	\N	1	91	17	0	0	0	0	0	0	0	0	\N	26555	0	0	0	\N	t
3105	\N	\N	1	91	18	0	0	0	0	0	0	0	0	\N	23343	0	0	0	\N	t
3106	\N	\N	1	91	19	0	0	0	0	0	0	0	0	\N	24539	0	0	0	\N	t
3107	\N	\N	1	91	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3108	\N	\N	1	91	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3109	\N	\N	1	91	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3110	\N	\N	1	91	23	0	0	0	0	0	0	0	0	\N	23047	0	0	0	\N	t
3111	\N	\N	1	91	24	0	0	0	0	0	0	0	0	\N	25068	0	0	0	\N	t
3112	\N	\N	1	91	25	0	0	0	0	0	0	0	0	\N	0	22926	0	0	\N	t
3113	\N	\N	1	92	1	0	0	0	0	0	0	0	0	\N	24937	0	0	0	\N	t
3114	\N	\N	1	92	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3115	\N	\N	1	92	3	0	0	0	0	0	0	0	0	\N	24960	0	0	0	\N	t
3116	\N	\N	1	92	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3117	\N	\N	1	92	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3118	\N	\N	1	92	6	0	0	0	0	0	0	0	0	\N	22604	0	0	0	\N	t
3119	\N	\N	1	92	7	0	0	0	0	0	0	0	0	\N	22523	0	0	0	\N	t
3120	\N	\N	1	92	8	0	0	0	0	0	0	0	0	\N	24641	0	0	0	\N	t
3121	\N	\N	1	92	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3122	\N	\N	1	92	10	0	0	0	0	0	0	0	0	\N	24051	0	0	0	\N	t
3123	\N	\N	1	92	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3124	\N	\N	1	92	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3125	\N	\N	1	92	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3126	\N	\N	1	92	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3127	\N	\N	1	92	15	0	0	0	0	0	0	0	0	\N	0	23386	0	0	\N	t
3128	\N	\N	1	92	16	0	0	0	0	0	0	0	0	\N	23370	0	0	0	\N	t
3129	\N	\N	1	92	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3130	\N	\N	1	92	18	0	0	0	0	0	0	0	0	\N	0	25802	0	0	\N	t
3131	\N	\N	1	92	19	0	0	0	0	0	0	0	0	\N	23654	0	0	0	\N	t
3132	\N	\N	1	92	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3133	\N	\N	1	92	21	0	0	0	0	0	0	0	0	\N	22710	0	0	0	\N	t
3134	\N	\N	1	92	22	0	0	0	0	0	0	0	0	\N	0	23196	0	0	\N	t
3135	\N	\N	1	92	23	0	0	0	0	0	0	0	0	\N	24868	0	0	0	\N	t
3136	\N	\N	1	92	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3137	\N	\N	1	92	25	0	0	0	0	0	0	0	0	\N	0	25779	0	0	\N	t
3138	\N	\N	1	93	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3139	\N	\N	1	93	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3140	\N	\N	1	93	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3141	\N	\N	1	93	4	0	0	0	0	0	0	0	0	\N	24845	0	0	0	\N	t
3142	\N	\N	1	93	5	0	0	0	0	0	0	0	0	\N	26296	0	0	0	\N	t
3143	\N	\N	1	93	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3144	\N	\N	1	93	7	0	0	0	0	0	0	0	0	\N	0	24613	0	0	\N	t
3145	\N	\N	1	93	8	0	0	0	0	0	0	0	0	\N	23817	0	0	0	\N	t
3146	\N	\N	1	93	9	0	0	0	0	0	0	0	0	\N	25616	0	0	0	\N	t
3147	\N	\N	1	93	10	0	0	0	0	0	0	0	0	\N	26457	0	0	0	\N	t
3148	\N	\N	1	93	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3149	\N	\N	1	93	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3150	\N	\N	1	93	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3151	\N	\N	1	93	14	0	0	0	0	0	0	0	0	\N	25313	0	0	0	\N	t
3152	\N	\N	1	93	15	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3153	\N	\N	1	93	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3154	\N	\N	1	93	17	0	0	0	0	0	0	0	0	\N	0	24164	0	0	\N	t
3155	\N	\N	1	93	18	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3156	\N	\N	1	93	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3157	\N	\N	1	93	20	0	0	0	0	0	0	0	0	\N	25967	0	0	0	\N	t
3158	\N	\N	1	93	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3159	\N	\N	1	93	22	0	0	0	0	0	0	0	0	\N	22299	0	0	0	\N	t
3160	\N	\N	1	93	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3161	\N	\N	1	93	24	0	0	0	0	0	0	0	0	\N	23693	0	0	0	\N	t
3162	\N	\N	1	93	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3163	\N	\N	1	94	1	0	0	0	0	0	0	0	0	\N	23542	0	0	0	\N	t
3164	\N	\N	1	94	2	0	0	0	0	0	0	0	0	\N	23067	0	0	0	\N	t
3165	\N	\N	1	94	3	0	0	0	0	0	0	0	0	\N	0	22032	0	0	\N	t
3166	\N	\N	1	94	4	0	0	0	0	0	0	0	0	\N	23826	0	0	0	\N	t
3167	\N	\N	1	94	5	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3168	\N	\N	1	94	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3169	\N	\N	1	94	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3170	\N	\N	1	94	8	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3171	\N	\N	1	94	9	0	0	0	0	0	0	0	0	\N	0	24950	0	0	\N	t
3172	\N	\N	1	94	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3173	\N	\N	1	94	11	0	0	0	0	0	0	0	0	\N	22024	0	0	0	\N	t
3174	\N	\N	1	94	12	0	0	0	0	0	0	0	0	\N	23857	0	0	0	\N	t
3175	\N	\N	1	94	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3176	\N	\N	1	94	14	0	0	0	0	0	0	0	0	\N	24065	0	0	0	\N	t
3177	\N	\N	1	94	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3178	\N	\N	1	94	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3179	\N	\N	1	94	17	0	0	0	0	0	0	0	0	\N	25467	0	0	0	\N	t
3180	\N	\N	1	94	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3181	\N	\N	1	94	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3182	\N	\N	1	94	20	0	0	0	0	0	0	0	0	\N	22355	0	0	0	\N	t
3183	\N	\N	1	94	21	0	0	0	0	0	0	0	0	\N	26705	0	0	0	\N	t
3184	\N	\N	1	94	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3185	\N	\N	1	94	23	0	0	0	0	0	0	0	0	\N	25240	0	0	0	\N	t
3186	\N	\N	1	94	24	0	0	0	0	0	0	0	0	\N	24616	0	0	0	\N	t
3187	\N	\N	1	94	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3188	\N	\N	1	95	1	0	0	0	0	0	0	0	0	\N	24169	0	0	0	\N	t
3189	\N	\N	1	95	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3190	\N	\N	1	95	3	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3191	\N	\N	1	95	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3192	\N	\N	1	95	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3193	\N	\N	1	95	6	0	0	0	0	0	0	0	0	\N	0	23618	0	0	\N	t
3194	\N	\N	1	95	7	0	0	0	0	0	0	0	0	\N	25544	0	0	0	\N	t
3195	\N	\N	1	95	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3196	\N	\N	1	95	9	0	0	0	0	0	0	0	0	\N	24924	0	0	0	\N	t
3197	\N	\N	1	95	10	0	0	0	0	0	0	0	0	\N	25832	0	0	0	\N	t
3198	\N	\N	1	95	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3199	\N	\N	1	95	12	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3200	\N	\N	1	95	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3201	\N	\N	1	95	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3202	\N	\N	1	95	15	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3203	\N	\N	1	95	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3204	\N	\N	1	95	17	0	0	0	0	0	0	0	0	\N	24667	0	0	0	\N	t
3205	\N	\N	1	95	18	0	0	0	0	0	0	0	0	\N	22422	0	0	0	\N	t
3206	\N	\N	1	95	19	0	0	0	0	0	0	0	0	\N	24623	0	0	0	\N	t
3207	\N	\N	1	95	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3208	\N	\N	1	95	21	0	0	0	0	0	0	0	0	\N	24284	0	0	0	\N	t
3209	\N	\N	1	95	22	0	0	0	0	0	0	0	0	\N	23282	0	0	0	\N	t
3210	\N	\N	1	95	23	0	0	0	0	0	0	0	0	\N	23281	0	0	0	\N	t
3211	\N	\N	1	95	24	0	0	0	0	0	0	0	0	\N	0	22058	0	0	\N	t
3212	\N	\N	1	95	25	0	0	0	0	0	0	0	0	\N	23076	0	0	0	\N	t
3213	\N	\N	1	96	1	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3214	\N	\N	1	96	2	0	0	0	0	0	0	0	0	\N	0	22626	0	0	\N	t
3215	\N	\N	1	96	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3216	\N	\N	1	96	4	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3217	\N	\N	1	96	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3218	\N	\N	1	96	6	0	0	0	0	0	0	0	0	\N	24008	0	0	0	\N	t
3219	\N	\N	1	96	7	0	0	0	0	0	0	0	0	\N	23068	0	0	0	\N	t
3220	\N	\N	1	96	8	0	0	0	0	0	0	0	0	\N	23333	0	0	0	\N	t
3221	\N	\N	1	96	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3222	\N	\N	1	96	10	0	0	0	0	0	0	0	0	\N	0	25275	0	0	\N	t
3223	\N	\N	1	96	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3224	\N	\N	1	96	12	0	0	0	0	0	0	0	0	\N	24568	0	0	0	\N	t
3225	\N	\N	1	96	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3226	\N	\N	1	96	14	0	0	0	0	0	0	0	0	\N	22611	0	0	0	\N	t
3227	\N	\N	1	96	15	0	0	0	0	0	0	0	0	\N	22686	0	0	0	\N	t
3228	\N	\N	1	96	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3229	\N	\N	1	96	17	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3230	\N	\N	1	96	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3231	\N	\N	1	96	19	0	0	0	0	0	0	0	0	\N	24870	0	0	0	\N	t
3232	\N	\N	1	96	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3233	\N	\N	1	96	21	0	0	0	0	0	0	0	0	\N	24867	0	0	0	\N	t
3234	\N	\N	1	96	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3235	\N	\N	1	96	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3236	\N	\N	1	96	24	0	0	0	0	0	0	0	0	\N	25812	0	0	0	\N	t
3237	\N	\N	1	96	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3238	\N	\N	1	97	1	0	0	0	0	0	0	0	0	\N	25345	0	0	0	\N	t
3239	\N	\N	1	97	2	0	0	0	0	0	0	0	0	\N	26620	0	0	0	\N	t
3240	\N	\N	1	97	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3241	\N	\N	1	97	4	0	0	0	0	0	0	0	0	\N	0	24177	0	0	\N	t
3242	\N	\N	1	97	5	0	0	0	0	0	0	0	0	\N	22878	0	0	0	\N	t
3243	\N	\N	1	97	6	0	0	0	0	0	0	0	0	\N	24042	0	0	0	\N	t
3244	\N	\N	1	97	7	0	0	0	0	0	0	0	0	\N	25107	0	0	0	\N	t
3245	\N	\N	1	97	8	0	0	0	0	0	0	0	0	\N	26351	0	0	0	\N	t
3246	\N	\N	1	97	9	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3247	\N	\N	1	97	10	0	0	0	0	0	0	0	0	\N	24228	0	0	0	\N	t
3248	\N	\N	1	97	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3249	\N	\N	1	97	12	0	0	0	0	0	0	0	0	\N	26139	0	0	0	\N	t
3250	\N	\N	1	97	13	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3251	\N	\N	1	97	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3252	\N	\N	1	97	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3253	\N	\N	1	97	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3254	\N	\N	1	97	17	0	0	0	0	0	0	0	0	\N	0	26006	0	0	\N	t
3255	\N	\N	1	97	18	0	0	0	0	0	0	0	0	\N	26065	0	0	0	\N	t
3256	\N	\N	1	97	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3257	\N	\N	1	97	20	0	0	0	0	0	0	0	0	\N	26740	0	0	0	\N	t
3258	\N	\N	1	97	21	0	0	0	0	0	0	0	0	\N	25366	0	0	0	\N	t
3259	\N	\N	1	97	22	0	0	0	0	0	0	0	0	\N	25166	0	0	0	\N	t
3260	\N	\N	1	97	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3261	\N	\N	1	97	24	0	0	0	0	0	0	0	0	\N	25695	0	0	0	\N	t
3262	\N	\N	1	97	25	0	0	0	0	0	0	0	0	\N	24603	0	0	0	\N	t
3263	\N	\N	1	98	1	0	0	0	0	0	0	0	0	\N	25759	0	0	0	\N	t
3264	\N	\N	1	98	2	0	0	0	0	0	0	0	0	\N	22337	0	0	0	\N	t
3265	\N	\N	1	98	3	0	0	0	0	0	0	0	0	\N	23187	0	0	0	\N	t
3266	\N	\N	1	98	4	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3267	\N	\N	1	98	5	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3268	\N	\N	1	98	6	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3269	\N	\N	1	98	7	0	0	0	0	0	0	0	0	\N	22042	0	0	0	\N	t
3270	\N	\N	1	98	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3271	\N	\N	1	98	9	0	0	0	0	0	0	0	0	\N	23271	0	0	0	\N	t
3272	\N	\N	1	98	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3273	\N	\N	1	98	11	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3274	\N	\N	1	98	12	0	0	0	0	0	0	0	0	\N	0	23821	0	0	\N	t
3275	\N	\N	1	98	13	0	0	0	0	0	0	0	0	\N	22587	0	0	0	\N	t
3276	\N	\N	1	98	14	0	0	0	0	0	0	0	0	\N	24096	0	0	0	\N	t
3277	\N	\N	1	98	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3278	\N	\N	1	98	16	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3279	\N	\N	1	98	17	0	0	0	0	0	0	0	0	\N	24933	0	0	0	\N	t
3280	\N	\N	1	98	18	0	0	0	0	0	0	0	0	\N	25428	0	0	0	\N	t
3281	\N	\N	1	98	19	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3282	\N	\N	1	98	20	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3283	\N	\N	1	98	21	0	0	0	0	0	0	0	0	\N	26628	0	0	0	\N	t
3284	\N	\N	1	98	22	0	0	0	0	0	0	0	0	\N	24943	0	0	0	\N	t
3285	\N	\N	1	98	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3286	\N	\N	1	98	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3287	\N	\N	1	98	25	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3288	\N	\N	1	99	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3289	\N	\N	1	99	2	0	0	0	0	0	0	0	0	\N	24041	0	0	0	\N	t
3290	\N	\N	1	99	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3291	\N	\N	1	99	4	0	0	0	0	0	0	0	0	\N	0	26646	0	0	\N	t
3292	\N	\N	1	99	5	0	0	0	0	0	0	0	0	\N	24761	0	0	0	\N	t
3293	\N	\N	1	99	6	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3294	\N	\N	1	99	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3295	\N	\N	1	99	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3296	\N	\N	1	99	9	0	0	0	0	0	0	0	0	\N	22775	0	0	0	\N	t
3297	\N	\N	1	99	10	0	0	0	0	0	0	0	0	\N	24903	0	0	0	\N	t
3298	\N	\N	1	99	11	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3299	\N	\N	1	99	12	0	0	0	0	0	0	0	0	\N	24109	0	0	0	\N	t
3300	\N	\N	1	99	13	0	0	0	0	0	0	0	0	\N	0	22069	0	0	\N	t
3301	\N	\N	1	99	14	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3302	\N	\N	1	99	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3303	\N	\N	1	99	16	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3304	\N	\N	1	99	17	0	0	0	0	0	0	0	0	\N	23589	0	0	0	\N	t
3305	\N	\N	1	99	18	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3306	\N	\N	1	99	19	80	10	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3307	\N	\N	1	99	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3308	\N	\N	1	99	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3309	\N	\N	1	99	22	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3310	\N	\N	1	99	23	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3311	\N	\N	1	99	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3312	\N	\N	1	99	25	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3313	\N	\N	1	100	1	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3314	\N	\N	1	100	2	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3315	\N	\N	1	100	3	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3316	\N	\N	1	100	4	0	0	0	0	0	0	0	0	\N	23309	0	0	0	\N	t
3317	\N	\N	1	100	5	0	0	0	0	0	0	0	0	\N	24289	0	0	0	\N	t
3318	\N	\N	1	100	6	0	0	0	0	0	0	0	0	\N	25493	0	0	0	\N	t
3319	\N	\N	1	100	7	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3320	\N	\N	1	100	8	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3321	\N	\N	1	100	9	0	0	0	0	0	0	0	0	\N	0	22238	0	0	\N	t
3322	\N	\N	1	100	10	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3323	\N	\N	1	100	11	0	0	0	0	0	0	0	0	\N	22400	0	0	0	\N	t
3324	\N	\N	1	100	12	0	0	0	0	0	0	0	0	\N	24689	0	0	0	\N	t
3325	\N	\N	1	100	13	0	0	0	0	0	0	0	0	\N	23803	0	0	0	\N	t
3326	\N	\N	1	100	14	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3327	\N	\N	1	100	15	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3328	\N	\N	1	100	16	0	0	0	0	0	0	0	0	\N	0	24995	0	0	\N	t
3329	\N	\N	1	100	17	0	0	0	0	0	0	0	0	\N	0	25081	0	0	\N	t
3330	\N	\N	1	100	18	0	0	0	0	0	0	0	0	\N	26749	0	0	0	\N	t
3331	\N	\N	1	100	19	0	0	0	0	0	0	0	0	\N	26248	0	0	0	\N	t
3332	\N	\N	1	100	20	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3333	\N	\N	1	100	21	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3334	\N	\N	1	100	22	0	0	0	0	0	0	0	0	\N	26672	0	0	0	\N	t
3335	\N	\N	1	100	23	0	0	0	0	0	0	0	0	\N	24131	0	0	0	\N	t
3336	\N	\N	1	100	24	0	0	0	0	0	0	0	0	\N	0	0	0	0	\N	t
3337	\N	\N	1	100	25	0	0	0	0	0	0	0	0	\N	22311	0	0	0	\N	t
\.


--
-- Data for Name: profile_connections; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_connections (id, profile_id, ip_address, forwarded, user_agent) FROM stdin;
3	6	127.0.0.1		Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
\.


--
-- Data for Name: profile_reports; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_reports (id, profile_id, type, creation_date, reading_date, data) FROM stdin;
\.


--
-- Data for Name: profile_ship_kills; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_ship_kills (profile_id, db_ship_id, count) FROM stdin;
\.


--
-- Data for Name: profile_tech_pendings; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_tech_pendings (id, profile_id, db_tech_id, starting_date, ending_date, loop) FROM stdin;
\.


--
-- Data for Name: profile_techs; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profile_techs (profile_id, db_tech_id, level) FROM stdin;
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.profiles (id, status, username, credit_count, avatar_url, cur_planet_id, deletion_date, last_connection_date, reset_count, starting_date, prestige_count) FROM stdin;
3	0	Guilde marchande	0		\N	\N	2023-05-25 13:29:06.894155+00	1	2006-09-01 00:00:00+00	0
1	0	Les fossoyeurs	0		\N	\N	2023-05-25 13:29:06.894155+00	1	2006-09-01 00:00:00+00	0
2	0	Nation oubliée	0		\N	\N	2023-05-25 13:29:06.894155+00	1	2006-09-01 00:00:00+00	0
6	-3	\N	3500	\N	\N	\N	2023-05-25 13:29:06.894155+00	0	\N	0
\.


--
-- Data for Name: server_processes; Type: TABLE DATA; Schema: ng0; Owner: freddec
--

COPY ng0.server_processes (process, lastrun_date, frequency, lastrun_result) FROM stdin;
\.


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

SELECT pg_catalog.setval('ng0.fleets_id_seq', 740, true);


--
-- Name: planet_building_pendings_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.planet_building_pendings_id_seq', 1, false);


--
-- Name: planet_ship_pendings_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.planet_ship_pendings_id_seq', 1, false);


--
-- Name: planet_training_pendings_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.planet_training_pendings_id_seq', 1, false);


--
-- Name: planets_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.planets_id_seq', 3337, true);


--
-- Name: profile_connections_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.profile_connections_id_seq', 4, true);


--
-- Name: profile_reports_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.profile_reports_id_seq', 1, false);


--
-- Name: profile_tech_pendings_id_seq; Type: SEQUENCE SET; Schema: ng0; Owner: freddec
--

SELECT pg_catalog.setval('ng0.profile_tech_pendings_id_seq', 1, false);


--
-- Name: battle_fleet_ship_kills battle_fleet_ship_kills_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ship_kills
    ADD CONSTRAINT battle_fleet_ship_kills_pkey PRIMARY KEY (battle_fleet_ship_id, db_ship_id);


--
-- Name: battle_fleet_ships battle_fleet_ships_battle_fleet_id_db_ship_id_key; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battle_fleet_ships_battle_fleet_id_db_ship_id_key UNIQUE (battle_fleet_id, db_ship_id);


--
-- Name: battle_fleet_ships battle_fleet_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battle_fleet_ships_pkey PRIMARY KEY (id);


--
-- Name: battle_fleets battles_fleets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets
    ADD CONSTRAINT battles_fleets_pkey PRIMARY KEY (id);


--
-- Name: battles battles_key_key; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battles
    ADD CONSTRAINT battles_key_key UNIQUE (key);


--
-- Name: battles battles_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battles
    ADD CONSTRAINT battles_pkey PRIMARY KEY (id);


--
-- Name: db_buildings db_buildings_name_key; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_buildings
    ADD CONSTRAINT db_buildings_name_key UNIQUE (name);


--
-- Name: db_buildings db_buildings_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_buildings
    ADD CONSTRAINT db_buildings_pkey PRIMARY KEY (id);


--
-- Name: db_building_building_reqs db_buildings_req_building_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_building_building_reqs
    ADD CONSTRAINT db_buildings_req_building_pkey PRIMARY KEY (db_building_id, req_id);


--
-- Name: db_building_tech_reqs db_buildings_req_research_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_building_tech_reqs
    ADD CONSTRAINT db_buildings_req_research_pkey PRIMARY KEY (db_building_id, req_id);


--
-- Name: db_tech_tech_reqs db_research_req_research_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_tech_tech_reqs
    ADD CONSTRAINT db_research_req_research_pkey PRIMARY KEY (db_tech_id, req_id);


--
-- Name: db_ships db_ships_name_key; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ships
    ADD CONSTRAINT db_ships_name_key UNIQUE (name);


--
-- Name: db_ships db_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ships
    ADD CONSTRAINT db_ships_pkey PRIMARY KEY (id);


--
-- Name: db_ship_building_reqs db_ships_req_building_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ship_building_reqs
    ADD CONSTRAINT db_ships_req_building_pkey PRIMARY KEY (db_ship_id, req_id);


--
-- Name: db_ship_tech_reqs db_ships_req_research_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ship_tech_reqs
    ADD CONSTRAINT db_ships_req_research_pkey PRIMARY KEY (db_ship_id, req_id);


--
-- Name: db_techs db_techs_name_key; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_techs
    ADD CONSTRAINT db_techs_name_key UNIQUE (name);


--
-- Name: db_techs db_techs_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_techs
    ADD CONSTRAINT db_techs_pkey PRIMARY KEY (id);


--
-- Name: fleet_actions fleet_actions_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_pkey PRIMARY KEY (id);


--
-- Name: fleets fleets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_pkey PRIMARY KEY (id);


--
-- Name: fleet_ships fleets_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_ships
    ADD CONSTRAINT fleets_ships_pkey PRIMARY KEY (fleet_id, db_ship_id);


--
-- Name: galaxies galaxies_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.galaxies
    ADD CONSTRAINT galaxies_pkey PRIMARY KEY (id);


--
-- Name: planet_building_pendings planet_buildings_pending_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_building_pendings
    ADD CONSTRAINT planet_buildings_pending_pkey PRIMARY KEY (id);


--
-- Name: planet_building_pendings planet_buildings_pending_unique; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_building_pendings
    ADD CONSTRAINT planet_buildings_pending_unique UNIQUE (planet_id, db_building_id);


--
-- Name: planet_buildings planet_buildings_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings
    ADD CONSTRAINT planet_buildings_pkey PRIMARY KEY (planet_id, db_building_id);


--
-- Name: planet_ship_pendings planet_ships_pending_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ship_pendings
    ADD CONSTRAINT planet_ships_pending_pkey PRIMARY KEY (id);


--
-- Name: planet_ships planet_ships_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ships
    ADD CONSTRAINT planet_ships_pkey PRIMARY KEY (planet_id, db_ship_id);


--
-- Name: planet_training_pendings planet_training_pending_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_training_pendings
    ADD CONSTRAINT planet_training_pending_pkey PRIMARY KEY (id);


--
-- Name: planets planets_location_unique; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_location_unique UNIQUE (galaxy_id, sector, number);


--
-- Name: planets planets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_pkey PRIMARY KEY (id);


--
-- Name: profile_connections profile_connections_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_connections
    ADD CONSTRAINT profile_connections_pkey PRIMARY KEY (id);


--
-- Name: profile_reports reports_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);


--
-- Name: profile_tech_pendings researches_pending_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_tech_pendings
    ADD CONSTRAINT researches_pending_pkey PRIMARY KEY (id);


--
-- Name: profile_techs researches_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_techs
    ADD CONSTRAINT researches_pkey PRIMARY KEY (profile_id, db_tech_id);


--
-- Name: server_processes sys_processes_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.server_processes
    ADD CONSTRAINT sys_processes_pkey PRIMARY KEY (process);


--
-- Name: profiles users_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: profile_ship_kills users_stats_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_ship_kills
    ADD CONSTRAINT users_stats_pkey PRIMARY KEY (profile_id, db_ship_id);


--
-- Name: battles_fleets_battleid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX battles_fleets_battleid_idx ON ng0.battle_fleets USING btree (battle_id);


--
-- Name: battles_time_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX battles_time_idx ON ng0.battles USING btree (creation_date);


--
-- Name: db_buildings_id; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX db_buildings_id ON ng0.db_buildings USING btree (id);


--
-- Name: fki_battles_fleets_ships_fleetid; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_battles_fleets_ships_fleetid ON ng0.battle_fleet_ships USING btree (battle_fleet_id);


--
-- Name: fki_battles_fleets_ships_kills_destroyed_shipid; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_battles_fleets_ships_kills_destroyed_shipid ON ng0.battle_fleet_ship_kills USING btree (db_ship_id);


--
-- Name: fki_battles_fleets_ships_kills_shipid; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_battles_fleets_ships_kills_shipid ON ng0.battle_fleet_ship_kills USING btree (battle_fleet_ship_id);


--
-- Name: fki_battles_fleets_ships_shipid; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_battles_fleets_ships_shipid ON ng0.battle_fleet_ships USING btree (db_ship_id);


--
-- Name: fki_buildingid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_buildingid_fk ON ng0.db_building_building_reqs USING btree (db_building_id);


--
-- Name: fki_db_buildings_req_research_buildingid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_buildings_req_research_buildingid_fk ON ng0.db_building_tech_reqs USING btree (db_building_id);


--
-- Name: fki_db_buildings_req_research_required_research_id; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_buildings_req_research_required_research_id ON ng0.db_building_tech_reqs USING btree (req_id);


--
-- Name: fki_db_research_req_research_required_researchid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_research_req_research_required_researchid_fk ON ng0.db_tech_tech_reqs USING btree (req_id);


--
-- Name: fki_db_research_req_research_researchid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_research_req_research_researchid_fk ON ng0.db_tech_tech_reqs USING btree (db_tech_id);


--
-- Name: fki_db_ships_buildingid_fkey; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_ships_buildingid_fkey ON ng0.db_ships USING btree (db_building_id);


--
-- Name: fki_db_ships_req_building_required_buildingid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_ships_req_building_required_buildingid_fk ON ng0.db_ship_building_reqs USING btree (req_id);


--
-- Name: fki_db_ships_req_building_shipid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_ships_req_building_shipid_fk ON ng0.db_ship_building_reqs USING btree (db_ship_id);


--
-- Name: fki_db_ships_req_research_required_researchid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_ships_req_research_required_researchid_fk ON ng0.db_ship_tech_reqs USING btree (req_id);


--
-- Name: fki_db_ships_req_research_shipid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_db_ships_req_research_shipid_fk ON ng0.db_ship_tech_reqs USING btree (db_ship_id);


--
-- Name: fki_fleet_actions_fleetid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_fleet_actions_fleetid_fk ON ng0.fleet_actions USING btree (fleet_id);


--
-- Name: fki_planet_buildings_pending_buildingid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_planet_buildings_pending_buildingid_fk ON ng0.planet_building_pendings USING btree (db_building_id);


--
-- Name: fki_planet_buildings_pending_planetid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_planet_buildings_pending_planetid_fk ON ng0.planet_building_pendings USING btree (planet_id);


--
-- Name: fki_planet_ships_pending_planetid_fkey; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_planet_ships_pending_planetid_fkey ON ng0.planet_ship_pendings USING btree (planet_id);


--
-- Name: fki_planet_ships_pending_shipid_fkey; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_planet_ships_pending_shipid_fkey ON ng0.planet_ship_pendings USING btree (db_ship_id);


--
-- Name: fki_planet_ships_shipid_fkey; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_planet_ships_shipid_fkey ON ng0.planet_ships USING btree (db_ship_id);


--
-- Name: fki_required_buildingid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_required_buildingid_fk ON ng0.db_building_building_reqs USING btree (req_id);


--
-- Name: fki_researches_researchid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_researches_researchid_fk ON ng0.profile_techs USING btree (db_tech_id);


--
-- Name: fki_researches_userid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fki_researches_userid_fk ON ng0.profile_techs USING btree (profile_id);


--
-- Name: fleets_engaged_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fleets_engaged_idx ON ng0.fleets USING btree (engaged) WHERE engaged;


--
-- Name: fleets_next_waypointid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fleets_next_waypointid_idx ON ng0.fleets USING btree (cur_action_id) WHERE (cur_action_id IS NOT NULL);


--
-- Name: fleets_ownerid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fleets_ownerid_idx ON ng0.fleets USING btree (profile_id);


--
-- Name: fleets_planetid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX fleets_planetid_idx ON ng0.fleets USING btree (planet_id) WHERE (planet_id IS NOT NULL);


--
-- Name: planet_buildings_pending_end_time; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planet_buildings_pending_end_time ON ng0.planet_building_pendings USING btree (ending_time) WHERE (ending_time IS NOT NULL);


--
-- Name: planet_ships_pending_end_time; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planet_ships_pending_end_time ON ng0.planet_ship_pendings USING btree (ending_date) WHERE (ending_date IS NOT NULL);


--
-- Name: planet_training_pending_end_time_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planet_training_pending_end_time_idx ON ng0.planet_training_pendings USING btree (ending_date) WHERE (ending_date IS NOT NULL);


--
-- Name: planet_training_pending_planetid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planet_training_pending_planetid_idx ON ng0.planet_training_pendings USING btree (planet_id);


--
-- Name: planets_galaxy_owner_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planets_galaxy_owner_idx ON ng0.planets USING btree (galaxy_id, profile_id) WHERE (profile_id IS NOT NULL);


--
-- Name: planets_galaxy_sector_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planets_galaxy_sector_idx ON ng0.planets USING btree (galaxy_id, sector) WHERE (profile_id IS NOT NULL);


--
-- Name: planets_galaxy_sector_ownerid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planets_galaxy_sector_ownerid_idx ON ng0.planets USING btree (galaxy_id, sector, profile_id) WHERE (profile_id IS NOT NULL);


--
-- Name: planets_next_battle; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planets_next_battle ON ng0.planets USING btree (next_battle_date) WHERE (next_battle_date IS NOT NULL);


--
-- Name: planets_ownerid_notnull_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planets_ownerid_notnull_idx ON ng0.planets USING btree (profile_id) WHERE (profile_id IS NOT NULL);


--
-- Name: planets_spawn_planet_id; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX planets_spawn_planet_id ON ng0.planets USING btree (id) WHERE ((spawn_ore > 0) OR (spawn_hydro > 0));


--
-- Name: reports_datetime_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX reports_datetime_idx ON ng0.profile_reports USING btree (creation_date);


--
-- Name: reports_ownerid_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX reports_ownerid_idx ON ng0.profile_reports USING btree (profile_id);


--
-- Name: reports_type_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX reports_type_idx ON ng0.profile_reports USING btree (type);


--
-- Name: researches_pending_end_time; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX researches_pending_end_time ON ng0.profile_tech_pendings USING btree (ending_date);


--
-- Name: researches_pending_researchid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX researches_pending_researchid_fk ON ng0.profile_tech_pendings USING btree (db_tech_id);


--
-- Name: researches_pending_userid_fk; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE UNIQUE INDEX researches_pending_userid_fk ON ng0.profile_tech_pendings USING btree (profile_id);


--
-- Name: users_deletion_date_idx; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX users_deletion_date_idx ON ng0.profiles USING btree (deletion_date) WHERE (deletion_date IS NOT NULL);


--
-- Name: users_login_unique; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE UNIQUE INDEX users_login_unique ON ng0.profiles USING btree (upper((username)::text)) WHERE (username IS NOT NULL);


--
-- Name: users_privilege; Type: INDEX; Schema: ng0; Owner: freddec
--

CREATE INDEX users_privilege ON ng0.profiles USING btree (status);


--
-- Name: profile_connections profileconnections_beforeinsert; Type: TRIGGER; Schema: ng0; Owner: freddec
--

CREATE TRIGGER profileconnections_beforeinsert BEFORE INSERT ON ng0.profile_connections FOR EACH ROW EXECUTE FUNCTION ng0.trigger_profileconnections_beforeinsert();


--
-- Name: battle_fleet_ship_kills battle_fleet_ship_kills_battle_fleet_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ship_kills
    ADD CONSTRAINT battle_fleet_ship_kills_battle_fleet_ship_id_fkey FOREIGN KEY (battle_fleet_ship_id) REFERENCES ng0.battle_fleet_ships(id) ON DELETE CASCADE;


--
-- Name: battle_fleet_ship_kills battle_fleet_ship_kills_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ship_kills
    ADD CONSTRAINT battle_fleet_ship_kills_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleet_ships battle_fleet_ships_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battle_fleet_ships_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleets battle_fleets_fleet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets
    ADD CONSTRAINT battle_fleets_fleet_id_fkey FOREIGN KEY (fleet_id) REFERENCES ng0.fleets(id) ON DELETE SET NULL;


--
-- Name: battle_fleets battle_fleets_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets
    ADD CONSTRAINT battle_fleets_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON DELETE SET NULL;


--
-- Name: battle_fleets battles_fleets_battleid; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleets
    ADD CONSTRAINT battles_fleets_battleid FOREIGN KEY (battle_id) REFERENCES ng0.battles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battle_fleet_ships battles_fleets_ships_fleetid; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battle_fleet_ships
    ADD CONSTRAINT battles_fleets_ships_fleetid FOREIGN KEY (battle_fleet_id) REFERENCES ng0.battle_fleets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: battles battles_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.battles
    ADD CONSTRAINT battles_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON DELETE CASCADE;


--
-- Name: db_building_building_reqs db_building_building_reqs_db_building_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_building_building_reqs
    ADD CONSTRAINT db_building_building_reqs_db_building_id_fkey FOREIGN KEY (db_building_id) REFERENCES ng0.db_buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_building_building_reqs db_building_building_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_building_building_reqs
    ADD CONSTRAINT db_building_building_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.db_buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_building_tech_reqs db_building_tech_reqs_db_building_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_building_tech_reqs
    ADD CONSTRAINT db_building_tech_reqs_db_building_id_fkey FOREIGN KEY (db_building_id) REFERENCES ng0.db_buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_ship_building_reqs db_ship_building_reqs_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ship_building_reqs
    ADD CONSTRAINT db_ship_building_reqs_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_ship_building_reqs db_ship_building_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ship_building_reqs
    ADD CONSTRAINT db_ship_building_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.db_buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_ship_tech_reqs db_ship_tech_reqs_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ship_tech_reqs
    ADD CONSTRAINT db_ship_tech_reqs_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_ship_tech_reqs db_ship_tech_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_ship_tech_reqs
    ADD CONSTRAINT db_ship_tech_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.db_techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_tech_tech_reqs db_tech_tech_reqs_db_tech_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_tech_tech_reqs
    ADD CONSTRAINT db_tech_tech_reqs_db_tech_id_fkey FOREIGN KEY (db_tech_id) REFERENCES ng0.db_techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: db_tech_tech_reqs db_tech_tech_reqs_req_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.db_tech_tech_reqs
    ADD CONSTRAINT db_tech_tech_reqs_req_id_fkey FOREIGN KEY (req_id) REFERENCES ng0.db_techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleet_actions fleet_actions_dest_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_dest_planet_id_fkey FOREIGN KEY (dest_planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleet_actions fleet_actions_fleet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_fleet_id_fkey FOREIGN KEY (fleet_id) REFERENCES ng0.fleets(id) ON DELETE CASCADE;


--
-- Name: fleet_actions fleet_actions_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_actions
    ADD CONSTRAINT fleet_actions_planet_id_fkey FOREIGN KEY (origin_planet_id) REFERENCES ng0.planets(id) ON DELETE CASCADE;


--
-- Name: fleet_ships fleet_ships_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_ships
    ADD CONSTRAINT fleet_ships_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleets fleets_next_waypointid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_next_waypointid_fkey FOREIGN KEY (cur_action_id) REFERENCES ng0.fleet_actions(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: fleets fleets_ownerid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_ownerid_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fleets fleets_planetid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleets
    ADD CONSTRAINT fleets_planetid_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: fleet_ships fleets_ships_fleetid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.fleet_ships
    ADD CONSTRAINT fleets_ships_fleetid_fkey FOREIGN KEY (fleet_id) REFERENCES ng0.fleets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_building_pendings planet_building_pendings_db_building_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_building_pendings
    ADD CONSTRAINT planet_building_pendings_db_building_id_fkey FOREIGN KEY (db_building_id) REFERENCES ng0.db_buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_buildings planet_buildings_db_building_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings
    ADD CONSTRAINT planet_buildings_db_building_id_fkey FOREIGN KEY (db_building_id) REFERENCES ng0.db_buildings(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_building_pendings planet_buildings_pending_planetid_fk; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_building_pendings
    ADD CONSTRAINT planet_buildings_pending_planetid_fk FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_ship_pendings planet_ship_pendings_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ship_pendings
    ADD CONSTRAINT planet_ship_pendings_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_ships planet_ships_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ships
    ADD CONSTRAINT planet_ships_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_ship_pendings planet_ships_pending_planetid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ship_pendings
    ADD CONSTRAINT planet_ships_pending_planetid_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_ships planet_ships_planetid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_ships
    ADD CONSTRAINT planet_ships_planetid_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_training_pendings planet_training_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_training_pendings
    ADD CONSTRAINT planet_training_fkey FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet_buildings planetid_fk; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planet_buildings
    ADD CONSTRAINT planetid_fk FOREIGN KEY (planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planets planets_galaxy_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_galaxy_fkey FOREIGN KEY (galaxy_id) REFERENCES ng0.galaxies(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planets planets_ownerid_fk; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_ownerid_fk FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profile_connections profile_connections_profile_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_connections
    ADD CONSTRAINT profile_connections_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_ship_kills profile_ship_kills_db_ship_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_ship_kills
    ADD CONSTRAINT profile_ship_kills_db_ship_id_fkey FOREIGN KEY (db_ship_id) REFERENCES ng0.db_ships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_tech_pendings profile_tech_pendings_db_tech_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_tech_pendings
    ADD CONSTRAINT profile_tech_pendings_db_tech_id_fkey FOREIGN KEY (db_tech_id) REFERENCES ng0.db_techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_techs profile_techs_db_tech_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_techs
    ADD CONSTRAINT profile_techs_db_tech_id_fkey FOREIGN KEY (db_tech_id) REFERENCES ng0.db_techs(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_reports reports_ownerid_fk; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_reports
    ADD CONSTRAINT reports_ownerid_fk FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_tech_pendings researches_pending_userid_fk; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_tech_pendings
    ADD CONSTRAINT researches_pending_userid_fk FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profile_techs researches_userid_fk; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_techs
    ADD CONSTRAINT researches_userid_fk FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profiles users_lastplanetid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT users_lastplanetid_fkey FOREIGN KEY (cur_planet_id) REFERENCES ng0.planets(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: profile_ship_kills users_stats_userid_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profile_ship_kills
    ADD CONSTRAINT users_stats_userid_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--
