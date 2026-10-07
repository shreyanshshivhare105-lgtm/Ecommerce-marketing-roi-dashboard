Create database xyz_sales_analysis ;
-- Create Campaigns Master Table
Create table Campiagn (
Campaign_id Varchar(20) Primary key,
Campaign_name varchar(100) Not null,
channel_ Varchar(60) not null,
ad_type Varchar(60) not null ,
category Varchar(60) not null ,
target_audience Varchar(20)
);
Alter table Campiagn Rename to Campaign ;
-- Create Daily Ad Performance Table
create table ad_performance (
performance_id int primary key ,
spent_date date not null,
Campaign_id Varchar(20) not null ,
imperssions int default 0 ,
clicks int default 0,
ad_spent_inr decimal(10,2) not null ,
foreign key (Campaign_id) references Campaign(Campaign_id) On delete cascade
);
-- Create Granular Customer Leads Table (2,000 Records)
Create table customer_leads (
lead_id Varchar(20) Primary key ,
created_at date not null ,
Campaign_id varchar(20) not null ,
channel_ varchar(30) not null , 
city_area varchar(60) not null ,
age_group varchar(15) not null ,
gender varchar(10) not null,
is_converted boolean not null default false ,
order_value_inr decimal(10,2) default 0.00 ,
customer_is_new boolean default true,
FOREIGN KEY (Campaign_id) REFERENCES Campaign(Campaign_id) ON DELETE CASCADE
);