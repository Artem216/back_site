--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Debian 15.5-1.pgdg120+1)
-- Dumped by pg_dump version 15.5 (Debian 15.5-1.pgdg120+1)

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
-- Name: dealtype; Type: TYPE; Schema: public; Owner: postgress
--

CREATE TYPE public.dealtype AS ENUM (
    'buy',
    'sell'
);


ALTER TYPE public.dealtype OWNER TO postgress;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgress
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgress;

--
-- Name: associated_user_instruments; Type: TABLE; Schema: public; Owner: postgress
--

CREATE TABLE public.associated_user_instruments (
    id uuid NOT NULL,
    code character varying(30) NOT NULL
);


ALTER TABLE public.associated_user_instruments OWNER TO postgress;

--
-- Name: deals; Type: TABLE; Schema: public; Owner: postgress
--

CREATE TABLE public.deals (
    id integer NOT NULL,
    price numeric NOT NULL,
    quantity integer NOT NULL,
    deal_type public.dealtype NOT NULL,
    user_id uuid NOT NULL,
    instrument_code character varying(30) NOT NULL,
    date_time timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.deals OWNER TO postgress;

--
-- Name: deals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgress
--

CREATE SEQUENCE public.deals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.deals_id_seq OWNER TO postgress;

--
-- Name: deals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgress
--

ALTER SEQUENCE public.deals_id_seq OWNED BY public.deals.id;


--
-- Name: instruments; Type: TABLE; Schema: public; Owner: postgress
--

CREATE TABLE public.instruments (
    code character varying(30) NOT NULL,
    title character varying NOT NULL,
    "group" character varying(30) NOT NULL,
    has_model boolean DEFAULT false NOT NULL
);


ALTER TABLE public.instruments OWNER TO postgress;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgress
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.users OWNER TO postgress;

--
-- Name: deals id; Type: DEFAULT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.deals ALTER COLUMN id SET DEFAULT nextval('public.deals_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgress
--

COPY public.alembic_version (version_num) FROM stdin;
d5f3a6dd0227
\.


--
-- Data for Name: associated_user_instruments; Type: TABLE DATA; Schema: public; Owner: postgress
--

COPY public.associated_user_instruments (id, code) FROM stdin;
\.


--
-- Data for Name: deals; Type: TABLE DATA; Schema: public; Owner: postgress
--

COPY public.deals (id, price, quantity, deal_type, user_id, instrument_code, date_time) FROM stdin;
1	200.0	11	buy	332097ee-807e-4958-b053-1bbf8c35e846	AIG-RM	2023-12-07 10:53:07.49872
2	210.0	11	sell	332097ee-807e-4958-b053-1bbf8c35e846	AIG-RM	2023-12-07 10:53:07.49872
3	10.0	1	buy	332097ee-807e-4958-b053-1bbf8c35e846	AMEZ	2023-12-07 10:53:07.49872
4	5.0	1	sell	332097ee-807e-4958-b053-1bbf8c35e846	AMEZ	2023-12-07 10:53:07.49872
5	1000.0	13	buy	332097ee-807e-4958-b053-1bbf8c35e846	MAGEP	2023-12-07 10:53:07.49872
6	1080.0	13	sell	332097ee-807e-4958-b053-1bbf8c35e846	MAGEP	2023-12-07 10:53:07.49872
\.


--
-- Data for Name: instruments; Type: TABLE DATA; Schema: public; Owner: postgress
--

COPY public.instruments (code, title, "group", has_model) FROM stdin;
A-RM	Agilent TechnologiesORD SHS	stock_shares	t
BLK-RM	BlackRock Inc.	stock_shares	t
AIG-RM	American International ORD SHS	stock_shares	t
AMEZ	Ашинский метзавод ПАО ао	stock_shares	t
MAGEP	&quot;Магаданэнерго&quot; ПАО ап	stock_shares	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgress
--

COPY public.users (id, first_name, last_name, email, password) FROM stdin;
332097ee-807e-4958-b053-1bbf8c35e846	test	test	test1@example.com	$2b$12$mJ3lho3XeiKf2Le8EqNbvOfhDEkMgQ983zOMmKgJjXj/Os4qzcLjW
7f6d7fbe-e165-4681-86ca-7e75e2644b95	test2	test2	test2@example.com	$2b$12$8.iVwrn0IvEoi2INH0c6pOpp8aDqYuRDvP6GgGCkAyhhpX21fOGMe
\.


--
-- Name: deals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgress
--

SELECT pg_catalog.setval('public.deals_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: associated_user_instruments associated_user_instruments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.associated_user_instruments
    ADD CONSTRAINT associated_user_instruments_pkey PRIMARY KEY (id, code);


--
-- Name: deals deals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_pkey PRIMARY KEY (id);


--
-- Name: instruments instruments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.instruments
    ADD CONSTRAINT instruments_pkey PRIMARY KEY (code);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: associated_user_instruments associated_user_instruments_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.associated_user_instruments
    ADD CONSTRAINT associated_user_instruments_code_fkey FOREIGN KEY (code) REFERENCES public.instruments(code);


--
-- Name: associated_user_instruments associated_user_instruments_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.associated_user_instruments
    ADD CONSTRAINT associated_user_instruments_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: deals deals_instrument_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_instrument_code_fkey FOREIGN KEY (instrument_code) REFERENCES public.instruments(code);


--
-- Name: deals deals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgress
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

