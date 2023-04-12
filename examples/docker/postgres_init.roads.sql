CREATE SCHEMA IF NOT EXISTS roads;

DROP TABLE IF EXISTS roads.municipality_municipality_type;
DROP TABLE IF EXISTS roads.municipality_type;
DROP TABLE IF EXISTS roads.repair_order_details;
DROP TABLE IF EXISTS roads.repair_orders;
DROP TABLE IF EXISTS roads.municipality;
DROP TABLE IF EXISTS roads.repair_type;
DROP TABLE IF EXISTS roads.dispatchers;
DROP TABLE IF EXISTS roads.contractors;
DROP TABLE IF EXISTS roads.us_states;
DROP TABLE IF EXISTS roads.us_region;
DROP TABLE IF EXISTS roads.hard_hats;
DROP TABLE IF EXISTS roads.hard_hat_state;

CREATE TABLE roads.repair_type (
    repair_type_id smallint NOT NULL,
    repair_type_name character varying(50) NOT NULL,
    contractor_id text
);
INSERT INTO roads.repair_type VALUES (1, 'Asphalt Overlay', 'Asphalt overlays restore roads to a smooth condition. This resurfacing uses the deteriorating asphalt as a base for which the new layer is added on top of, instead of tearing up the worsening one.');
INSERT INTO roads.repair_type VALUES (2, 'Patching', 'Patching is the process of filling potholes or excavated areas in the asphalt pavement. Quick repair of potholes or other pavement disintegration helps control further deterioration and expensive repair of the pavement. Without timely patching, water can enter the sub-grade and cause larger and more serious pavement failures.');
INSERT INTO roads.repair_type VALUES (3, 'Reshaping', 'This is necessary when a road surface it too damaged to be smoothed. Using a grader blade and scarifying if necessary, you rework the gravel sub-base to eliminate large potholes and rebuild a flattened crown.');
INSERT INTO roads.repair_type VALUES (4, 'Slab Replacement', 'This refers to replacing sections of paved roads. It is a good option for when slabs are chipped, cracked, or uneven, and mitigates the need to replace the entire road when just a small section is damaged.');
INSERT INTO roads.repair_type VALUES (5, 'Smoothing', 'This is when you lightly rework the gravel of a road without digging in too far to the sub-base. Typically, a motor grader is used in this operation with an attached blade. Smoothing is done when the road has minor damage or is just worn down a bit from use.');
INSERT INTO roads.repair_type VALUES (6, 'Reconstruction', 'When roads have deteriorated to a point that it is no longer cost-effective to maintain, the entire street or road needs to be rebuilt. Typically, this work is done in phases to limit traffic restrictions. As part of reconstruction, the street may be realigned to improve safety or operations, grading may be changed to improve storm water flow, underground utilities may be added, upgraded or relocated, traffic signals and street lights may be relocated, and street trees and pedestrian ramps may be added.');

CREATE TABLE roads.municipality (
    municipality_id character varying(20) NOT NULL,
    contact_name character varying(30),
    contact_title character varying(50),
    local_region character varying(30),
    phone character varying(30),
    state_id smallint NOT NULL
);
INSERT INTO roads.municipality VALUES ('New York', 'Alexander Wilkinson', 'Assistant City Clerk', 'Manhattan', '505-101-1929', 33);
INSERT INTO roads.municipality VALUES ('Los Angeles', 'Hugh Moser', 'Administrative Assistant', 'Santa Monica', '505-122-1929', 5 );
INSERT INTO roads.municipality VALUES ('Chicago', 'Phillip Bradshaw', 'Director of Community Engagement', 'West Ridge', '102-222-2033', 14);
INSERT INTO roads.municipality VALUES ('Houston', 'Leo Ackerman', 'Municipal Roads Specialist', 'The Woodlands', '303-111-1929', 44);
INSERT INTO roads.municipality VALUES ('Phoenix', 'Jessie Paul', 'Director of Finance and Administration', 'Old Town Scottsdale', '122-101-1111',3);
INSERT INTO roads.municipality VALUES ('Philadelphia', 'Willie Chaney', 'Municipal Manager', 'Center City', '241-223-3224', 39);
INSERT INTO roads.municipality VALUES ('San Antonio', 'Chester Lyon', 'Treasurer', 'Alamo Heights', '412-987-8236', 44);
INSERT INTO roads.municipality VALUES ('San Diego', 'Ralph Helms', 'Senior Electrical Project Manager', 'Del Mar', '324-443-1157', 5);
INSERT INTO roads.municipality VALUES ('Dallas', 'Virgil Craft', 'Assistant Assessor (Town/Municipality)', 'Deep Ellum', '442-101-3429', 44);
INSERT INTO roads.municipality VALUES ('San Jose', 'Charles Carney', 'Municipal Accounting Manager', 'Santana Row', '408-331-1245', 5);

CREATE TABLE roads.hard_hats (
    hard_hat_id smallint NOT NULL,
    last_name character varying(20) NOT NULL,
    first_name character varying(10) NOT NULL,
    title character varying(30),
    birth_date date,
    hire_date date,
    address character varying(60),
    city character varying(15),
    state character varying(15),
    postal_code character varying(10),
    country character varying(15),
    manager smallint,
    contractor_id smallint
);
INSERT INTO roads.hard_hats VALUES (1, 'Brian', 'Perkins', 'Construction Laborer', '1978-11-28', '2009-02-06', '4 Jennings Ave.', 'Jersey City', 'NJ', '37421', 'USA', 9, 1);
INSERT INTO roads.hard_hats VALUES (2, 'Nicholas', 'Massey', 'Carpenter', '1993-02-19', '2003-04-14', '9373 Southampton Street', 'Middletown', 'CT', '27292', 'USA', 9, 1);
INSERT INTO roads.hard_hats VALUES (3, 'Cathy', 'Best', 'Framer', '1994-08-30', '1990-07-02', '4 Hillside Street', 'Billerica', 'MA', '13440', 'USA', 9, 2);
INSERT INTO roads.hard_hats VALUES (4, 'Melanie', 'Stafford', 'Construction Manager', '1966-03-19', '2003-02-02', '77 Studebaker Lane', 'Southampton', 'PA', '71730', 'USA', 9, 2);
INSERT INTO roads.hard_hats VALUES (5, 'Donna', 'Riley', 'Pre-construction Manager', '1983-03-14', '2012-01-13', '82 Taylor Drive', 'Southgate', 'MI', '33125', 'USA', 9, 4);
INSERT INTO roads.hard_hats VALUES (6, 'Alfred', 'Clarke', 'Construction Superintendent', '1979-01-12', '2013-10-17', '7729 Catherine Street', 'Powder Springs', 'GA', '42001', 'USA', 9, 2);
INSERT INTO roads.hard_hats VALUES (7, 'William', 'Boone', 'Construction Laborer', '1970-02-28', '2013-01-02', '1 Border St.', 'Niagara Falls', 'NY', '14304', 'USA', 9, 4);
INSERT INTO roads.hard_hats VALUES (8, 'Luka', 'Henderson', 'Construction Laborer', '1988-12-09', '2013-03-05', '794 S. Chapel Ave.', 'Phoenix', 'AZ', '85021', 'USA', 9, 1);
INSERT INTO roads.hard_hats VALUES (9, 'Patrick', 'Ziegler', 'Construction Laborer', '1976-11-27', '2020-11-15', '321 Gainsway Circle', 'Muskogee', 'OK', '74403', 'USA', 9, 3);

CREATE TABLE roads.hard_hat_state (
    hard_hat_id smallint NOT NULL,
    state_id smallint NOT NULL
);
INSERT INTO roads.hard_hat_state VALUES (1, 2);
INSERT INTO roads.hard_hat_state VALUES (2, 32);
INSERT INTO roads.hard_hat_state VALUES (3, 28);
INSERT INTO roads.hard_hat_state VALUES (4, 12);
INSERT INTO roads.hard_hat_state VALUES (5, 5);
INSERT INTO roads.hard_hat_state VALUES (6, 3);
INSERT INTO roads.hard_hat_state VALUES (7, 16);
INSERT INTO roads.hard_hat_state VALUES (8, 32);
INSERT INTO roads.hard_hat_state VALUES (9, 41);

CREATE TABLE roads.repair_order_details (
    repair_order_id smallint NOT NULL,
    repair_type_id smallint NOT NULL,
    price real NOT NULL,
    quantity smallint NOT NULL,
    discount real NOT NULL
);
INSERT INTO roads.repair_order_details VALUES (10001, 1, 63708, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10002, 4, 67253, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10003, 2, 66808, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10004, 4, 18497, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10005, 7, 76463, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10006, 4, 87858, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10007, 1, 63918, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10008, 6, 21083, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10009, 3, 74555, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10010, 5, 27222, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10011, 5, 73600, 1, 0.05);
INSERT INTO roads.repair_order_details VALUES (10012, 3, 54901, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10013, 5, 51594, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10014, 1, 65114, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10015, 1, 48919, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10016, 3, 70418, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10017, 1, 29684, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10018, 2, 62928, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10019, 2, 97916, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10020, 5, 44120, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10021, 1, 53374, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10022, 2, 87289, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10023, 2, 92366, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10024, 2, 47857, 1, 0.01);
INSERT INTO roads.repair_order_details VALUES (10025, 1, 68745, 1, 0.01);

CREATE TABLE roads.repair_orders (
    repair_order_id smallint NOT NULL,
    municipality_id character varying(20),
    hard_hat_id smallint,
    order_date date,
    required_date date,
    dispatched_date date,
    dispatcher_id smallint
);
INSERT INTO roads.repair_orders VALUES (10001, 'New York', 1, '2007-07-04', '2009-07-18', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10002, 'New York', 3, '2007-07-05', '2009-08-28', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10003, 'New York', 5, '2007-07-08', '2009-08-12', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10004, 'Dallas', 1, '2007-07-08', '2009-08-01', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10005, 'San Antonio', 8, '2007-07-09', '2009-08-01', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10006, 'New York', 3, '2007-07-10', '2009-08-01', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10007, 'Philadelphia', 4, '2007-04-21', '2009-08-08', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10008, 'Philadelphia', 5, '2007-04-22', '2009-08-09', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10009, 'Philadelphia', 3, '2007-04-25', '2009-08-12', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10010, 'Philadelphia', 4, '2007-04-26', '2009-08-13', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10011, 'Philadelphia', 4, '2007-04-27', '2009-08-14', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10012, 'Philadelphia', 8, '2007-04-28', '2009-08-15', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10013, 'Philadelphia', 4, '2007-04-29', '2009-08-16', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10014, 'Philadelphia', 6, '2007-04-29', '2009-08-16', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10015, 'Philadelphia', 2, '2007-04-12', '2009-08-19', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10016, 'Philadelphia', 9, '2007-04-13', '2009-08-20', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10017, 'Philadelphia', 2, '2007-04-14', '2009-08-21', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10018, 'Philadelphia', 6, '2007-04-15', '2009-08-22', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10019, 'Philadelphia', 5, '2007-05-16', '2009-09-06', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10020, 'Philadelphia', 1, '2007-05-19', '2009-08-26', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10021, 'Philadelphia', 7, '2007-05-10', '2009-08-27', '2007-12-01', 3);
INSERT INTO roads.repair_orders VALUES (10022, 'Philadelphia', 5, '2007-05-11', '2009-08-14', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10023, 'Philadelphia', 1, '2007-05-11', '2009-08-29', '2007-12-01', 1);
INSERT INTO roads.repair_orders VALUES (10024, 'Philadelphia', 5, '2007-05-11', '2009-08-29', '2007-12-01', 2);
INSERT INTO roads.repair_orders VALUES (10025, 'Philadelphia', 6, '2007-05-12', '2009-08-30', '2007-12-01', 2);

CREATE TABLE roads.dispatchers (
    dispatcher_id smallint NOT NULL,
    company_name character varying(40) NOT NULL,
    phone character varying(24)
);
INSERT INTO roads.dispatchers VALUES (1, 'Pothole Pete', '(111) 111-1111');
INSERT INTO roads.dispatchers VALUES (2, 'Asphalts R Us', '(222) 222-2222');
INSERT INTO roads.dispatchers VALUES (3, 'Federal Roads Group', '(333) 333-3333');
INSERT INTO roads.dispatchers VALUES (4, 'Local Patchers', '1-800-888-8888');
INSERT INTO roads.dispatchers VALUES (5, 'Gravel INC', '1-800-000-0000');
INSERT INTO roads.dispatchers VALUES (6, 'DJ Developers', '1-111-111-1111');

CREATE TABLE roads.contractors (
    contractor_id smallint NOT NULL,
    company_name character varying(40) NOT NULL,
    contact_name character varying(30),
    contact_title character varying(30),
    address character varying(60),
    city character varying(15),
    state character varying(15),
    postal_code character varying(10),
    country character varying(15),
    phone character varying(24)
);
INSERT INTO roads.contractors VALUES (1, 'You Need Em We Find Em', 'Max Potter', 'Assistant Director', '4 Plumb Branch Lane', 'Goshen', 'IN', '46526', 'USA', '(111) 111-1111');
INSERT INTO roads.contractors VALUES (2, 'Call Forwarding', 'Sylvester English', 'Administrator', '9650 Mill Lane', 'Raeford', 'NC', '28376', 'USA', '(222) 222-2222');
INSERT INTO roads.contractors VALUES (3, 'The Connect', 'Paul Raymond', 'Administrator', '7587 Myrtle Ave.', 'Chaska', 'MN', '55318', 'USA', '(333) 333-3333');

CREATE TABLE roads.us_region (
    us_region_id smallint NOT NULL,
    us_region_description character varying(60) NOT NULL
);
INSERT INTO roads.us_region VALUES (1, 'Eastern');
INSERT INTO roads.us_region VALUES (2, 'Western');
INSERT INTO roads.us_region VALUES (3, 'Northern');
INSERT INTO roads.us_region VALUES (4, 'Southern');

CREATE TABLE roads.us_states (
    state_id smallint NOT NULL,
    state_name character varying(100),
    state_abbr character varying(2),
    state_region character varying(50)
);
INSERT INTO roads.us_states VALUES (1, 'Alabama', 'AL', 'Southern');
INSERT INTO roads.us_states VALUES (2, 'Alaska', 'AK', 'Northern');
INSERT INTO roads.us_states VALUES (3, 'Arizona', 'AZ', 'Western');
INSERT INTO roads.us_states VALUES (4, 'Arkansas', 'AR', 'Southern');
INSERT INTO roads.us_states VALUES (5, 'California', 'CA', 'Western');
INSERT INTO roads.us_states VALUES (6, 'Colorado', 'CO', 'Western');
INSERT INTO roads.us_states VALUES (7, 'Connecticut', 'CT', 'Eastern');
INSERT INTO roads.us_states VALUES (8, 'Delaware', 'DE', 'Eastern');
INSERT INTO roads.us_states VALUES (9, 'District of Columbia', 'DC', 'Eastern');
INSERT INTO roads.us_states VALUES (10, 'Florida', 'FL', 'Southern');
INSERT INTO roads.us_states VALUES (11, 'Georgia', 'GA', 'Southern');
INSERT INTO roads.us_states VALUES (12, 'Hawaii', 'HI', 'Western');
INSERT INTO roads.us_states VALUES (13, 'Idaho', 'ID', 'Western');
INSERT INTO roads.us_states VALUES (14, 'Illinois', 'IL', 'Western');
INSERT INTO roads.us_states VALUES (15, 'Indiana', 'IN', 'Western');
INSERT INTO roads.us_states VALUES (16, 'Iowa', 'IO', 'Western');
INSERT INTO roads.us_states VALUES (17, 'Kansas', 'KS', 'Western');
INSERT INTO roads.us_states VALUES (18, 'Kentucky', 'KY', 'Southern');
INSERT INTO roads.us_states VALUES (19, 'Louisiana', 'LA', 'Southern');
INSERT INTO roads.us_states VALUES (20, 'Maine', 'ME', 'Northern');
INSERT INTO roads.us_states VALUES (21, 'Maryland', 'MD', 'Eastern');
INSERT INTO roads.us_states VALUES (22, 'Massachusetts', 'MA', 'Northern');
INSERT INTO roads.us_states VALUES (23, 'Michigan', 'MI', 'Northern');
INSERT INTO roads.us_states VALUES (24, 'Minnesota', 'MN', 'Northern');
INSERT INTO roads.us_states VALUES (25, 'Mississippi', 'MS', 'Southern');
INSERT INTO roads.us_states VALUES (26, 'Missouri', 'MO', 'Southern');
INSERT INTO roads.us_states VALUES (27, 'Montana', 'MT', 'Western');
INSERT INTO roads.us_states VALUES (28, 'Nebraska', 'NE', 'Western');
INSERT INTO roads.us_states VALUES (29, 'Nevada', 'NV', 'Western');
INSERT INTO roads.us_states VALUES (30, 'New Hampshire', 'NH', 'Eastern');
INSERT INTO roads.us_states VALUES (31, 'New Jersey', 'NJ', 'Eastern');
INSERT INTO roads.us_states VALUES (32, 'New Mexico', 'NM', 'Western');
INSERT INTO roads.us_states VALUES (33, 'New York', 'NY', 'Eastern');
INSERT INTO roads.us_states VALUES (34, 'North Carolina', 'NC', 'Eastern');
INSERT INTO roads.us_states VALUES (35, 'North Dakota', 'ND', 'Western');
INSERT INTO roads.us_states VALUES (36, 'Ohio', 'OH', 'Western');
INSERT INTO roads.us_states VALUES (37, 'Oklahoma', 'OK', 'Western');
INSERT INTO roads.us_states VALUES (38, 'Oregon', 'OR', 'Western');
INSERT INTO roads.us_states VALUES (39, 'Pennsylvania', 'PA', 'Eastern');
INSERT INTO roads.us_states VALUES (40, 'Rhode Island', 'RI', 'Eastern');
INSERT INTO roads.us_states VALUES (41, 'South Carolina', 'SC', 'Eastern');
INSERT INTO roads.us_states VALUES (42, 'South Dakota', 'SD', 'Western');
INSERT INTO roads.us_states VALUES (43, 'Tennessee', 'TN', 'Western');
INSERT INTO roads.us_states VALUES (44, 'Texas', 'TX', 'Western');
INSERT INTO roads.us_states VALUES (45, 'Utah', 'UT', 'Western');
INSERT INTO roads.us_states VALUES (46, 'Vermont', 'VT', 'Eastern');
INSERT INTO roads.us_states VALUES (47, 'Virginia', 'VA', 'Eastern');
INSERT INTO roads.us_states VALUES (48, 'Washington', 'WA', 'Western');
INSERT INTO roads.us_states VALUES (49, 'West Virginia', 'WV', 'Southern');
INSERT INTO roads.us_states VALUES (50, 'Wisconsin', 'WI', 'Western');
INSERT INTO roads.us_states VALUES (51, 'Wyoming', 'WY', 'Western');

CREATE TABLE roads.municipality_municipality_type (
    municipality_id character varying(20) NOT NULL,
    municipality_type_id character varying(1) NOT NULL
);
INSERT INTO roads.municipality_municipality_type VALUES ('New York', 'A');
INSERT INTO roads.municipality_municipality_type VALUES ('Los Angeles', 'B');
INSERT INTO roads.municipality_municipality_type VALUES ('Chicago', 'B');
INSERT INTO roads.municipality_municipality_type VALUES ('Houston', 'A');
INSERT INTO roads.municipality_municipality_type VALUES ('Phoenix', 'A');
INSERT INTO roads.municipality_municipality_type VALUES ('Philadelphia', 'B');
INSERT INTO roads.municipality_municipality_type VALUES ('San Antonio', 'A');
INSERT INTO roads.municipality_municipality_type VALUES ('San Diego', 'B');
INSERT INTO roads.municipality_municipality_type VALUES ('Dallas', 'A');
INSERT INTO roads.municipality_municipality_type VALUES ('San Jose', 'B');

CREATE TABLE roads.municipality_type (
    municipality_type_id character varying(1) NOT NULL,
    municipality_type_desc text
);
INSERT INTO roads.municipality_type VALUES ('A', 'Primary');
INSERT INTO roads.municipality_type VALUES ('A', 'Secondary');

-- Bodega Salon
create schema if not exists bodegasalon;

drop table if exists bodegasalon.incoming_customer_service;
drop table if exists bodegasalon.outgoing_customer_service;
drop table if exists bodegasalon.customer_d;
drop table if exists bodegasalon.purchase_events;
drop table if exists bodegasalon.customer_accounts;
drop table if exists bodegasalon.service_items;
drop table if exists bodegasalon.consumable_items;
drop table if exists bodegasalon.membership_discounts;

create table incoming_customer_service (
    call_id int,
    call_start timestamp,
    call_end timestamp,
    rep varchar,
    customer_id int,
    notes_id int,
    category varchar
);

insert into incoming_customer_service values
(1, now()::timestamp - interval '1 hours', now(), 'Peter Davidson', 1, 1, 'billing'),
(2, now()::timestamp - interval '2 hours', now(), 'Siena Shannon', 2, 2, 'technical'),
(3, now()::timestamp - interval '3 hours', now(), 'Melissa Richards', 2, 3, 'technical'),
(4, now()::timestamp - interval '4 hours', now(), 'Billy Poole', 2, 4, 'technical'),
(5, now()::timestamp - interval '5 hours', now(), 'Dominic Mason', 1, 5, 'billing');


create table outgoing_customer_service (
    call_id int,
    call_start timestamp,
    call_end timestamp,
    rep varchar,
    customer_id int,
    notes_id int,
    category varchar
);
insert into outgoing_customer_service values
(1, now()::timestamp - interval '1 hours', now(), 'Carolyn Gregory', 1, 1, 'billing'),
(2, now()::timestamp - interval '2 hours', now(), 'Camila Mcknight', 1, 2, 'billing'),
(3, now()::timestamp - interval '3 hours', now(), 'Erin Taylor', 1, 3, 'billing'),
(4, now()::timestamp - interval '4 hours', now(), 'Darian Miller', 1, 4, 'billing'),
(5, now()::timestamp - interval '5 hours', now(), 'Heath Hendricks', 2, 5, 'technical');

create table customer_d (
    customer_id int,
    first_name varchar,
    last_name varchar
);
insert into customer_d values
(1, 'Fry', 'Jacobson'),
(2, 'Morty', 'Michaels');

create table purchase_events (
    purchase_id int,
    item_id int,
    item_type varchar,
    account_id int,
    purchase_country varchar,
    purchase_time timestamp
);
insert into purchase_events values
(1, 4, 'consumable', 1, 'US', now()::timestamp - interval '1 hours'),
(2, 5, 'consumable', 2, 'CA', now()::timestamp - interval '2 hours'),
(3, 4, 'salon', 2, 'CA', now()::timestamp - interval '3 hours'),
(4, 4, 'salon', 1, 'US', now()::timestamp - interval '4 hours'),
(5, 4, 'salon', 3, 'UK', now()::timestamp - interval '5 hours'),
(6, 4, 'salon', 3, 'FR', now()::timestamp - interval '6 hours'),
(7, 4, 'salon', 2, 'UK', now()::timestamp - interval '7 hours'),
(8, 4, 'consumable', 2, 'UK', now()::timestamp - interval '8 hours'),
(9, 4, 'consumable', 1, 'US', now()::timestamp - interval '9 hours'),
(10, 4, 'salon', 1, 'CA', now()::timestamp - interval '10 hours');

create table customer_accounts (
    account_id int,
    account_type varchar,
    customer_id int,
    home_country varchar
);
insert into customer_accounts values
(1, 'preloaded', 1, 'US'),
(2, 'preloaded', 1, 'US'),
(3, 'debit', 2, 'UK');

create table service_items (
    service_item_id int,
    description varchar,
    category varchar,
    price decimal
);
insert into service_items values
(1, 'Blow dry', 'salon', 60.0),
(2, 'Change of Polish', 'salon', 10.0),
(3, 'Regular Manicure', 'salon', 20.0),
(4, 'Eyebrows', 'salon', 40.0),
(5, 'Full Makeup', 'salon', 100.0),
(6, 'Highlights', 'salon', 150.0),
(7, 'Gloss', 'salon', 75.0),
(8, 'Updos', 'salon', 100.0),
(9, 'Haircut', 'salon', 80.0),
(10, 'Keratin Conditioning', 'salon', 350.0);

create table consumable_items (
    consumable_item_id int,
    description varchar,
    category varchar,
    price decimal
);
insert into consumable_items values
(1, 'Kirkland Signature All Chocolate Bag, 90 oz','food', 21.99),
(2, 'The Fruit Companys Columbia River Fruit Basket','food', 69.99),
(3, 'Pendleton Pet Kuddler Bed','pets', 59.99),
(4, 'Planters Dry Roasted Peanuts, 52 oz','food', 6.59),
(5, 'Pierre Signatures Angus Cheeseburger, 6.2 oz, 8-count','food', 14.99),
(6, 'Chefs Banquet One Month Emergency Food Supply (380 Total Servings)','food', 139.99),
(7, 'Tide Pods HE Laundry Detergent Pods, Free & Gentle, 152-count','cleaning', 30.99),
(8, 'Clorox ToiletWand Disposable Toilet Cleaning System with 36 Refills','cleaning', 18.29),
(9, 'St Michel Madeleine, Classic French Sponge Cake 100 - count','food', 37.99),
(10, 'Nescafé Tasters Choice Decaf House Blend Instant Coffee, 14 oz','food', 17.99),
(11, 'Scoop Away Complete Performance, Scented Cat Litter, 42 Pounds','pets', 18.89),
(12, 'Honey Bunches of Oats with Almonds Cereal, 50 oz','food', 7.19),
(13, 'Nature Valley Sweet and Salty Granola Bar, Peanut, 1.2 oz, 48-count','food', 14.49),
(14, 'Zoe Super Bars Beef Recipe 2/2lb Bags','food', 29.99),
(15, 'Crest 3D White Advanced Whitening Toothpaste, 5.2 oz, 5-count','food', 13.99);

create table membership_discounts (
    membership_id int,
    item_id int,
    discount decimal
);
insert into membership_discounts values
(1, 1, 0.5),
(1, 2, 0.5),
(1, 3, 0.5),
(1, 4, 0.5),
(1, 5, 0.5),
(1, 6, 0.5),
(1, 7, 0.5),
(1, 8, 0.5),
(1, 9, 0.5),
(1, 10, 0.5),
(1, 11, 0.5),
(1, 12, 0.5),
(1, 13, 0.5),
(1, 14, 0.5),
(1, 15, 0.5),
(2, 1, 0.1),
(2, 2, 0.1),
(2, 3, 0.1),
(2, 4, 0.1),
(2, 5, 0.1),
(2, 6, 0.1),
(2, 7, 0.1),
(2, 8, 0.1),
(2, 9, 0.1),
(2, 10, 0.1),
(2, 11, 0.1),
(2, 12, 0.1),
(2, 13, 0.1),
(2, 14, 0.1),
(2, 15, 0.1),
(3, 3, 0.3),
(3, 10, 0.3);