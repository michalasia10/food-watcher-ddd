from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "status" VARCHAR(8) NOT NULL  DEFAULT 'inactive',
    "type" VARCHAR(9) NOT NULL  DEFAULT 'user'
);
COMMENT ON COLUMN "user"."status" IS 'ACTIVE: active\nINACTIVE: inactive';
COMMENT ON COLUMN "user"."type" IS 'ADMIN: admin\nUSER: user\nDIETITIAN: dietitian';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "product" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "code" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "quantity" VARCHAR(255),
    "brand" VARCHAR(255),
    "size" VARCHAR(255),
    "groups" VARCHAR(255),
    "category" VARCHAR(255),
    "energy_kcal_100g" DOUBLE PRECISION NOT NULL,
    "fat_100g" DOUBLE PRECISION,
    "carbohydrates_100g" DOUBLE PRECISION,
    "sugars_100g" DOUBLE PRECISION,
    "proteins_100g" DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS "daily_user_consumption" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "date" DATE NOT NULL,
    "summary_calories" DOUBLE PRECISION NOT NULL,
    "summary_proteins" DOUBLE PRECISION NOT NULL,
    "summary_fats" DOUBLE PRECISION NOT NULL,
    "summary_carbohydrates" DOUBLE PRECISION NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
