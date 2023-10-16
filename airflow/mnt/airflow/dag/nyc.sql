CREATE TABLE IF NOT EXISTS nyc (
    taxitype VARCHAR(250),
    lastmonthprocessed DATE);
	
INSERT INTO nyc(taxitype, lastmonthprocessed)
values 
('yellow','2019-12-01'),
('green','2019-12-01'),
('fhv','2019-12-01'),
('fhvhv','2019-12-01')

UPDATE nyc
SET lastmonthprocessed  = '2020-01-01'