CREATE TABLE "results" (
  "id" SERIAL PRIMARY KEY,
  "job_id" integer UNIQUE NOT NULL,
  "img" text NOT NULL
);

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" text UNIQUE NOT NULL,
  "password" text NOT NULL,
  "email" text NOT NULL
);

CREATE TABLE "deconvolution_jobs" (
  "id" SERIAL PRIMARY KEY,
  "status" text NOT NULL,
  "img" text NOT NULL,
  "user_id" integer NOT NULL
);

ALTER TABLE "deconvolution_jobs" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "results" ADD FOREIGN KEY ("job_id") REFERENCES "deconvolution_jobs" ("id");
