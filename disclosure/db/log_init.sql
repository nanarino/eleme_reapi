CREATE TABLE "stdupc" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "time" TEXT DEFAULT NULL,
  "barcode" TEXT DEFAULT NULL,
  "std_flag" TEXT DEFAULT NULL,
  "except" TEXT
);
CREATE TABLE "skuMap" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "time" TEXT DEFAULT NULL,
  "goodscode" TEXT DEFAULT NULL,
  "errno" integer DEFAULT 0,
  "error" TEXT
);
CREATE TABLE "catMap" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "time" TEXT DEFAULT NULL,
  "goodscode" TEXT DEFAULT NULL,
  "errno" integer DEFAULT 0,
  "error" TEXT
);
CREATE TABLE "syncFailed" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "time" TEXT DEFAULT NULL,
  "shop_id" TEXT DEFAULT NULL,
  "goodscode" TEXT DEFAULT NULL,
  "errno" integer DEFAULT 0,
  "error" TEXT
);