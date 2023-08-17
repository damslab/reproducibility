DROP TABLE IF EXISTS aka_name;
DROP TABLE IF EXISTS aka_title;
DROP TABLE IF EXISTS cast_info;
DROP TABLE IF EXISTS char_name;
DROP TABLE IF EXISTS comp_cast_type;
DROP TABLE IF EXISTS company_name;
DROP TABLE IF EXISTS company_type;
DROP TABLE IF EXISTS complete_cast;
DROP TABLE IF EXISTS info_type;
DROP TABLE IF EXISTS keyword;
DROP TABLE IF EXISTS kind_type;
DROP TABLE IF EXISTS link_type;
DROP TABLE IF EXISTS movie_companies;
DROP TABLE IF EXISTS movie_info;
DROP TABLE IF EXISTS movie_info_idx;
DROP TABLE IF EXISTS movie_keyword;
DROP TABLE IF EXISTS movie_link;
DROP TABLE IF EXISTS name;
DROP TABLE IF EXISTS person_info;
DROP TABLE IF EXISTS role_type;
DROP TABLE IF EXISTS title;

CREATE TABLE aka_name (
                          id integer NOT NULL PRIMARY KEY,
                          person_id integer NOT NULL,
                          name text NOT NULL,
                          imdb_index character varying(12),
                          name_pcode_cf character varying(5),
                          name_pcode_nf character varying(5),
                          surname_pcode character varying(5),
                          md5sum character varying(32)
);

CREATE TABLE aka_title (
                           id integer NOT NULL PRIMARY KEY,
                           movie_id integer NOT NULL,
                           title text NOT NULL,
                           imdb_index character varying(12),
                           kind_id integer NOT NULL,
                           production_year integer,
                           phonetic_code character varying(5),
                           episode_of_id integer,
                           season_nr integer,
                           episode_nr integer,
                           note text,
                           md5sum character varying(32)
);

CREATE TABLE cast_info (
                           id integer NOT NULL PRIMARY KEY,
                           person_id integer NOT NULL,
                           movie_id integer NOT NULL,
                           person_role_id integer,
                           note text,
                           nr_order integer,
                           role_id integer NOT NULL
);

CREATE TABLE char_name (
                           id integer NOT NULL PRIMARY KEY,
                           name text NOT NULL,
                           imdb_index character varying(12),
                           imdb_id integer,
                           name_pcode_nf character varying(5),
                           surname_pcode character varying(5),
                           md5sum character varying(32)
);

CREATE TABLE comp_cast_type (
                                id integer NOT NULL PRIMARY KEY,
                                kind character varying(32) NOT NULL
);

CREATE TABLE company_name (
                              id integer NOT NULL PRIMARY KEY,
                              name text NOT NULL,
                              country_code character varying(255),
                              imdb_id integer,
                              name_pcode_nf character varying(5),
                              name_pcode_sf character varying(5),
                              md5sum character varying(32)
);

CREATE TABLE company_type (
                              id integer NOT NULL PRIMARY KEY,
                              kind character varying(32) NOT NULL
);

CREATE TABLE complete_cast (
                               id integer NOT NULL PRIMARY KEY,
                               movie_id integer,
                               subject_id integer NOT NULL,
                               status_id integer NOT NULL
);

CREATE TABLE info_type (
                           id integer NOT NULL PRIMARY KEY,
                           info character varying(32) NOT NULL
);

CREATE TABLE keyword (
                         id integer NOT NULL PRIMARY KEY,
                         keyword text NOT NULL,
                         phonetic_code character varying(5)
);

CREATE TABLE kind_type (
                           id integer NOT NULL PRIMARY KEY,
                           kind character varying(15) NOT NULL
);

CREATE TABLE link_type (
                           id integer NOT NULL PRIMARY KEY,
                           link character varying(32) NOT NULL
);

CREATE TABLE movie_companies (
                                 id integer NOT NULL PRIMARY KEY,
                                 movie_id integer NOT NULL,
                                 company_id integer NOT NULL,
                                 company_type_id integer NOT NULL,
                                 note text
);

CREATE TABLE movie_info (
                            id integer NOT NULL PRIMARY KEY,
                            movie_id integer NOT NULL,
                            info_type_id integer NOT NULL,
                            info text NOT NULL,
                            note text
);

CREATE TABLE movie_info_idx (
                                id integer NOT NULL PRIMARY KEY,
                                movie_id integer NOT NULL,
                                info_type_id integer NOT NULL,
                                info text NOT NULL,
                                note text
);

CREATE TABLE movie_keyword (
                               id integer NOT NULL PRIMARY KEY,
                               movie_id integer NOT NULL,
                               keyword_id integer NOT NULL
);

CREATE TABLE movie_link (
                            id integer NOT NULL PRIMARY KEY,
                            movie_id integer NOT NULL,
                            linked_movie_id integer NOT NULL,
                            link_type_id integer NOT NULL
);

CREATE TABLE name (
                      id integer NOT NULL PRIMARY KEY,
                      name text NOT NULL,
                      imdb_index character varying(12),
                      imdb_id integer,
                      gender character varying(1),
                      name_pcode_cf character varying(5),
                      name_pcode_nf character varying(5),
                      surname_pcode character varying(5),
                      md5sum character varying(32)
);

CREATE TABLE person_info (
                             id integer NOT NULL PRIMARY KEY,
                             person_id integer NOT NULL,
                             info_type_id integer NOT NULL,
                             info text NOT NULL,
                             note text
);

CREATE TABLE role_type (
                           id integer NOT NULL PRIMARY KEY,
                           role character varying(32) NOT NULL
);

CREATE TABLE title (
                       id integer NOT NULL PRIMARY KEY,
                       title text NOT NULL,
                       imdb_index character varying(12),
                       kind_id integer NOT NULL,
                       production_year integer,
                       imdb_id integer,
                       phonetic_code character varying(5),
                       episode_of_id integer,
                       season_nr integer,
                       episode_nr integer,
                       series_years character varying(49),
                       md5sum character varying(32)
);

COPY aka_name FROM 'PATHVAR/data/imdb/aka_name.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY aka_title FROM 'PATHVAR/data/imdb/aka_title.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY cast_info FROM 'PATHVAR/data/imdb/cast_info.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY char_name FROM 'PATHVAR/data/imdb/char_name.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY comp_cast_type FROM 'PATHVAR/data/imdb/comp_cast_type.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY company_name FROM 'PATHVAR/data/imdb/company_name.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY company_type FROM 'PATHVAR/data/imdb/company_type.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY complete_cast FROM 'PATHVAR/data/imdb/complete_cast.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY info_type FROM 'PATHVAR/data/imdb/info_type.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY keyword FROM 'PATHVAR/data/imdb/keyword.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY kind_type FROM 'PATHVAR/data/imdb/kind_type.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY link_type FROM 'PATHVAR/data/imdb/link_type.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY movie_companies FROM 'PATHVAR/data/imdb/movie_companies.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY movie_info FROM 'PATHVAR/data/imdb/movie_info.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY movie_info_idx FROM 'PATHVAR/data/imdb/movie_info_idx.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY movie_keyword FROM 'PATHVAR/data/imdb/movie_keyword.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY movie_link FROM 'PATHVAR/data/imdb/movie_link.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY name FROM 'PATHVAR/data/imdb/name.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY person_info FROM 'PATHVAR/data/imdb/person_info.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY role_type FROM 'PATHVAR/data/imdb/role_type.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY title FROM 'PATHVAR/data/imdb/title.tbl' ( FORMAT CSV, DELIMITER '|' );
