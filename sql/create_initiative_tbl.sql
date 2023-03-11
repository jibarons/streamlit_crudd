CREATE TABLE public.initiatives (
  id SERIAL,
	submit_date DATE,
	submit_name VARCHAR(50),
	submit_email VARCHAR(50),
	fields VARCHAR(50),
	values VARCHAR(750),
	init_id VARCHAR(50),
	init_uuid VARCHAR(50),
	init_formid VARCHAR(50),
  PRIMARY KEY (id)
)
;
ALTER TABLE IF EXISTS public.initiatives
    OWNER to postgres;

COPY initiatives 
FROM 'C:\Program Files\PostgreSQL\14\data\initiatives_to_sql.csv'
  DELIMITERS ','
  CSV HEADER


--DROP TABLE opportunity

CREATE TABLE public.opportunity (
  id SERIAL,
	oppo_date VARCHAR(10),
	init_name VARCHAR(50),
	oppo_feed VARCHAR(50),
	init_id VARCHAR(50),
	init_uuid VARCHAR(50),
	init_formid VARCHAR(50),
  PRIMARY KEY (id)
)
;
ALTER TABLE IF EXISTS public.opportunity
    OWNER to postgres;