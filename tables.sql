create table public.users
(
    id       text not null
        constraint users_pk
            primary key,
    username text not null,
    image    text,
    password text not null
);

alter table public.users
    owner to postgres;

create unique index users_username_uindex
    on public.users (username);

create table public.chats
(
    id        text                    not null
        constraint chats_pk
            primary key,
    name      text                    not null,
    image     text,
    owner_id  text                    not null
        constraint chats_users_id_fk
            references public.users,
    relevance timestamp default now() not null
);

alter table public.chats
    owner to postgres;

create table public.members
(
    chat_id text not null
        constraint members_chats_id_fk
            references public.chats
            on delete cascade,
    user_id text not null
        constraint members_users_id_fk
            references public.users
            on delete cascade
);

alter table public.members
    owner to postgres;

create unique index members_chat_id_user_id_uindex
    on public.members (chat_id, user_id);

create table public.messages
(
    id        text                    not null
        constraint messages_pk
            primary key,
    content   text,
    file      text,
    relevance timestamp default now() not null,
    user_id   text                    not null
        constraint messages_users_id_fk
            references public.users,
    chat_id   text                    not null
);

alter table public.messages
    owner to postgres;

