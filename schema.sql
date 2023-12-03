DROP TABLE IF EXISTS "recipe";
DROP TABLE IF EXISTS "user";

CREATE TABLE "user"
(
    "id"       INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT UNIQUE NOT NULL,
    "password" TEXT        NOT NULL,
    "role"     TEXT        NOT NULL
);

CREATE TABLE "recipe"
(
    "id"          INTEGER PRIMARY KEY AUTOINCREMENT,
    "category"    TEXT    NOT NULL,
    "name"        TEXT    NOT NULL,
    "description" TEXT    NOT NULL,
    "difficulty"  INTEGER NOT NULL
);