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

ALTER TABLE ONLY ng0.profiles DROP CONSTRAINT profiles_cur_planet_id_fkey;
ALTER TABLE ONLY ng0.planets DROP CONSTRAINT planets_owner_id_fkey;
ALTER TABLE ONLY ng0.planets DROP CONSTRAINT planets_galaxy_id_fkey;
ALTER TABLE ONLY ng0.profiles DROP CONSTRAINT profiles_pkey;
ALTER TABLE ONLY ng0.planets DROP CONSTRAINT planets_pkey;
ALTER TABLE ONLY ng0.galaxies DROP CONSTRAINT galaxies_pkey;
ALTER TABLE ng0.planets ALTER COLUMN id DROP DEFAULT;
ALTER TABLE ng0.galaxies ALTER COLUMN id DROP DEFAULT;
DROP VIEW ng0.vw_galaxies;
DROP TABLE ng0.profiles;
DROP SEQUENCE ng0.planets_id_seq;
DROP TABLE ng0.planets;
DROP SEQUENCE ng0.galaxies_id_seq;
DROP TABLE ng0.galaxies;
DROP FUNCTION ng0.sp_profile_reset(_profile_id integer, _galaxy_id integer);
DROP FUNCTION ng0.sp_profile_connect(_user_id integer);
DROP FUNCTION ng0.sp_galaxy_generate(_galaxy_id integer);
DROP SCHEMA ng0;
--
-- Name: ng0; Type: SCHEMA; Schema: -; Owner: freddec
--

CREATE SCHEMA ng0;


ALTER SCHEMA ng0 OWNER TO freddec;

--
-- Name: sp_galaxy_generate(integer); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.sp_galaxy_generate(_galaxy_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   sector integer;
   number integer;

   planet_id integer;
   planet_type integer;

BEGIN

   FOR sector IN 1..100 LOOP

      FOR number IN 1..25 LOOP

         planet_type := int2(100 * random());
         IF planet_type < 45 THEN planet_type := 0; -- empty location
         ELSEIF planet_type >= 98 THEN planet_type := 2; -- auto-spawn of ore in orbit
         ELSEIF planet_type >= 96 THEN planet_type := 3; -- auto-spawn of hydro in orbit
         ELSE planet_type := 1; -- normal planet
         END IF;

         IF planet_type = 0 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number)
               VALUES(_galaxy_id, sector, number)
               RETURNING id INTO planet_id;

            PERFORM sp_fleet_generate_orbiting_rogue(planet_id, 1 + int2(4 * random()));

         ELSEIF planet_type = 1 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number, floor_count, space_count, img)
               VALUES(_galaxy_id, sector, number, 80, 10, 'planet' + 1 + int2(19 * random()) + '.png')
               RETURNING id INTO planet_id;

            PERFORM sp_fleet_generate_orbiting_rogue(planet_id, 1 + int2(4 * random()));

         ELSEIF planet_type = 2 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number, spawn_ore)
               VALUES(_galaxy_id, sector, number, 22000 + 5000 * random());

         ELSEIF planet_type = 3 THEN

            INSERT INTO ng0.planets(galaxy_id, sector, number, spawn_hydro)
               VALUES(_galaxy_id, sector, number, 22000 + 5000 * random());

         END IF;

      END LOOP;

   END LOOP;

END;$$;


ALTER FUNCTION ng0.sp_galaxy_generate(_galaxy_id integer) OWNER TO freddec;

--
-- Name: sp_profile_connect(integer); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.sp_profile_connect(_user_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

   profile record;

BEGIN

   -- create a profile if it doesn't exist

   SELECT INTO profile * FROM ng0.profiles WHERE id = _user_id LIMIT 1;

   IF NOT FOUND THEN

      INSERT INTO ng0.profiles(id) VALUES(_user_id);

   END IF;

END;
$$;


ALTER FUNCTION ng0.sp_profile_connect(_user_id integer) OWNER TO freddec;

--
-- Name: sp_profile_reset(integer, integer); Type: FUNCTION; Schema: ng0; Owner: freddec
--

CREATE FUNCTION ng0.sp_profile_reset(_profile_id integer, _galaxy_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$DECLARE

   planet_id integer;
   planet_count integer;

BEGIN

   -- check player has no planets

   SELECT INTO planet_count COUNT(1) FROM planets WHERE owner_id = _profile_id;
   
   IF planet_count > 0 THEN

      -- user still have 1 planet at least

      RETURN 1; 

   END IF;

   -- select a new planet

   SELECT INTO planet_id id
      FROM planets INNER JOIN galaxies ON (galaxies.id = planets.galaxy_id)
      WHERE profile_id IS NULL AND allow_new_player AND galaxies.id = _galaxy_id AND floor_count > 0 AND space_count > 0 AND (sector % 10 = 0 OR sector % 10 = 1 OR sector <= 10 OR sector > 90);

   IF NOT FOUND THEN

      -- no available planet found

      RETURN 2;

   END IF;

   PERFORM sp_planet_clear(planet_id);

   INSERT INTO planet_buildings(planet_id, building_id, count) VALUES(planet_id, 'colony', 1);

   UPDATE planets
      SET profile_id = _profile_id,
          ore_count = 10000,
          hydro_count = 10000,
          worker_count = 10000,
          scientist_count = 50,
          soldier_count = 50
   WHERE id = planet_id;

   -- give player fleets to rogue nation

   UPDATE fleets SET owner_id = 2 WHERE owner_id = _profile_id;

   -- make orbitting fleets to go elsewhere

   PERFORM sp_fleet_move(fleets.profile_id, fleets.id, sp_planet_find_nearest(fleets.profile_id, planets.id))
      FROM planets INNER JOIN fleets ON (fleets.action <> 'return' AND fleets.action <> 'move' AND fleets.planet_id = planets.id AND fleets.profile_id <> planets.profile_id)
      WHERE planets .id = planet_id;

   -- reset techs

   DELETE FROM profile_tech_pendings WHERE profile_id = _profile_id;

   INSERT INTO profile_techs(profile_id, tech_id, level)
      SELECT _profile_id, id, default_level FROM db_techs WHERE default_level > 0 AND NOT EXISTS(SELECT 1 FROM profile_techs WHERE profile_id = _profile_id AND tech_id = db_techs.id);

   -- reset profile

   UPDATE profiles
      SET credit_count = DEFAULT,
          prestige_count = DEFAULT,
          score = DEFAULT,
          starting_date = DEFAULT,
          cur_planet_id = planet_id,
          reset_count = reset_count + 1,
          status = -1
      WHERE id = _profile_id;

   RETURN 0;

END;$$;


ALTER FUNCTION ng0.sp_profile_reset(_profile_id integer, _galaxy_id integer) OWNER TO freddec;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: galaxies; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.galaxies (
    id integer NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL
    name character varying(16) NOT NULL,
    allow_new_player boolean DEFAULT true NOT NULL,
);


ALTER TABLE ng0.galaxies OWNER TO freddec;

--
-- Name: galaxies_id_seq; Type: SEQUENCE; Schema: ng0; Owner: freddec
--

CREATE SEQUENCE ng0.galaxies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ng0.galaxies_id_seq OWNER TO freddec;

--
-- Name: galaxies_id_seq; Type: SEQUENCE OWNED BY; Schema: ng0; Owner: freddec
--

ALTER SEQUENCE ng0.galaxies_id_seq OWNED BY ng0.galaxies.id;


--
-- Name: planets; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.planets (
    id integer NOT NULL,
    galaxy_id integer NOT NULL,
    sector integer NOT NULL,
    number integer NOT NULL,
    floor_count integer DEFAULT 0 NOT NULL,
    space_count integer DEFAULT 0 NOT NULL,
    profile_id integer,
    img character varying(32),
    spawn_ore integer DEFAULT 0 NOT NULL,
    spawn_hydro integer DEFAULT 0 NOT NULL
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
-- Name: profiles; Type: TABLE; Schema: ng0; Owner: freddec
--

CREATE TABLE ng0.profiles (
    id integer NOT NULL,
    status integer DEFAULT '-2'::integer NOT NULL,
    planet_count integer DEFAULT 0 NOT NULL,
    cur_planet_id integer,
    username character varying(12),
    reset_count integer DEFAULT 0 NOT NULL,
    creation_date timestamp without time zone DEFAULT now() NOT NULL,
    starting_date timestamp without time zone,
    credit_count integer DEFAULT 0 NOT NULL,
    prestige_count integer DEFAULT 0 NOT NULL,
    score integer DEFAULT 0 NOT NULL
);


ALTER TABLE ng0.profiles OWNER TO freddec;

--
-- Name: vw_galaxies; Type: VIEW; Schema: ng0; Owner: freddec
--

CREATE VIEW ng0.vw_galaxies AS
 SELECT galaxies.id,
    galaxies.name,
        CASE
            WHEN ((galaxies.creation_date + '1 mon'::interval) >= now()) THEN true
            ELSE false
        END AS is_protected,
    galaxies.allow_new_player,
    ( SELECT count(1) AS count
           FROM (ng0.planets
             JOIN ng0.galaxies galaxies_1 ON ((galaxies_1.id = planets.galaxy_id)))
          WHERE ((planets.profile_id IS NULL) AND (planets.floor_count > 0) AND (planets.space_count > 0) AND (((planets.sector % 10) = 0) OR ((planets.sector % 10) = 1) OR (planets.sector <= 10) OR (planets.sector > 90)) AND galaxies_1.allow_new_player)) AS new_player_free_planet_count,
    ( SELECT count(1) AS count
           FROM (ng0.planets
             JOIN ng0.galaxies galaxies_1 ON ((galaxies_1.id = planets.galaxy_id)))
          WHERE ((planets.floor_count > 0) AND (planets.space_count > 0))) AS planet_count,
    ( SELECT count(1) AS count
           FROM (ng0.planets
             JOIN ng0.galaxies galaxies_1 ON ((galaxies_1.id = planets.galaxy_id)))
          WHERE ((planets.profile_id IS NOT NULL) AND (planets.floor_count > 0) AND (planets.space_count > 0))) AS colony_count
   FROM ng0.galaxies;


ALTER TABLE ng0.vw_galaxies OWNER TO freddec;

--
-- Name: galaxies id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.galaxies ALTER COLUMN id SET DEFAULT nextval('ng0.galaxies_id_seq'::regclass);


--
-- Name: planets id; Type: DEFAULT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets ALTER COLUMN id SET DEFAULT nextval('ng0.planets_id_seq'::regclass);


--
-- Name: galaxies galaxies_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.galaxies
    ADD CONSTRAINT galaxies_pkey PRIMARY KEY (id);


--
-- Name: planets planets_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: planets planets_galaxy_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_galaxy_id_fkey FOREIGN KEY (galaxy_id) REFERENCES ng0.galaxies(id);


--
-- Name: planets planets_owner_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.planets
    ADD CONSTRAINT planets_owner_id_fkey FOREIGN KEY (profile_id) REFERENCES ng0.profiles(id);


--
-- Name: profiles profiles_cur_planet_id_fkey; Type: FK CONSTRAINT; Schema: ng0; Owner: freddec
--

ALTER TABLE ONLY ng0.profiles
    ADD CONSTRAINT profiles_cur_planet_id_fkey FOREIGN KEY (cur_planet_id) REFERENCES ng0.planets(id);


--
-- PostgreSQL database dump complete
--

