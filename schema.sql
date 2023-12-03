DROP TABLE IF EXISTS "recipes";
DROP TABLE IF EXISTS "users";

CREATE TABLE "users"
(
    "id"       INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT UNIQUE NOT NULL,
    "password" TEXT        NOT NULL,
    "role"     TEXT        NOT NULL
);

CREATE TABLE "recipes"
(
    "id"          INTEGER PRIMARY KEY AUTOINCREMENT,
    "category"    TEXT    NOT NULL,
    "name"        TEXT    NOT NULL,
    "description" TEXT    NOT NULL,
    "difficulty"  INTEGER NOT NULL
);