-- migrate:up
insert into api_data.users(name, birthday)
values ('Fedor', '2006-02-15'),
        ('Cat', '2003-01-25'),
        ('Dog', '2007-08-10'),
        ('Clown', '2011-10-09');

insert into api_data.buttons(description, title, parent_id)
values ('fikdodr', 'Coffee', Null),
        ('fjjfjfj', 'Shop', Null),
        ('djfjjf', 'Hospital', Null),
        ('sjdjjd', 'Sochi park', Null);



insert into api_data.buttons(description, title, parent_id)
values ('fikdodr', 'Where to buy coffee', (select id from api_data.buttons where title = 'Coffee')),
        ('fkfkkf', 'Where is shop', (select id from api_data.buttons where title = 'Shop')),
        ('fkfkf', 'Where is hospital', (select id from api_data.buttons where title = 'Hospital')),
        ('fkfkkf', 'Where is sochi park', (select id from api_data.buttons where title = 'Sochi park'));



insert into api_data.useractions(user_id, button_id, time)
values ((select id from api_data.users where name = 'Fedor'), (select id from api_data.buttons where title = 'Coffee'), '2024-02-23 17:40:05'),
        ((select id from api_data.users where name = 'Dog'), (select id from api_data.buttons where title = 'Shop'), '2023-11-12 13:39:22'),
        ((select id from api_data.users where name = 'Cat'), (select id from api_data.buttons where title = 'Hospital'), '2024-04-28 18:05:13'),
        ((select id from api_data.users where name = 'Clown'), (select id from api_data.buttons where title = 'Sochi park'), '2024-01-21 19:08:25');




-- migrate:down

