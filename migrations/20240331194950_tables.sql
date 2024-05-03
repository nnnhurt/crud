-- migrate:up
create extension if not exists "uuid-ossp";

create schema api_data;

create table api_data.users
(
    id uuid primary key DEFAULT uuid_generate_v4(),
    name varchar(20),
    birthday date
);

create table api_data.buttons
(
    id uuid primary key DEFAULT uuid_generate_v4(),
    description text,
    title VARCHAR(20) NOT NULL,
    parent_id uuid REFERENCES api_data.buttons(id)
);

create table api_data.useractions
(
    user_id uuid REFERENCES api_data.users(id),
    button_id uuid REFERENCES api_data.buttons(id),
    time TIMESTAMP,
    PRIMARY KEY(user_id, button_id)
);
-- migrate:down
