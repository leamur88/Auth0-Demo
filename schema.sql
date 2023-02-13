create table facts (
    id serial primary key,
    source text,
    fact text
);

create table bad_way_to_do_users (
    id serial primary key,
    username text,
    password text
);