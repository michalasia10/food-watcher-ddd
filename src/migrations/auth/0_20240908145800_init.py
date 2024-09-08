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
CREATE TABLE IF NOT EXISTS "settings" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "age" INT NOT NULL,
    "gender" VARCHAR(11) NOT NULL  DEFAULT 'unspecified',
    "user_id" UUID NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "settings"."gender" IS 'MALE: male\nFEMALE: female\nOTHER: other\nUNSPECIFIED: unspecified';
CREATE TABLE IF NOT EXISTS "macro" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "proteins" DOUBLE PRECISION NOT NULL,
    "fats" DOUBLE PRECISION NOT NULL,
    "carbs" DOUBLE PRECISION NOT NULL,
    "calories" DOUBLE PRECISION NOT NULL,
    "settings_id" UUID NOT NULL UNIQUE REFERENCES "settings" ("id") ON DELETE CASCADE
);
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
    "proteins_100g" DOUBLE PRECISION,
    "user_id" UUID REFERENCES "user" ("id") ON DELETE CASCADE
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
);
CREATE TABLE IF NOT EXISTS "daily_user_product" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "weight_in_grams" DOUBLE PRECISION NOT NULL,
    "type" VARCHAR(9) NOT NULL  DEFAULT 'lunch',
    "proteins" DOUBLE PRECISION NOT NULL,
    "fats" DOUBLE PRECISION NOT NULL,
    "carbohydrates" DOUBLE PRECISION NOT NULL,
    "calories" DOUBLE PRECISION NOT NULL,
    "day_id" UUID NOT NULL REFERENCES "daily_user_consumption" ("id") ON DELETE CASCADE,
    "product_id" UUID NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "daily_user_product"."type" IS 'BREAKFAST: breakfast\nLUNCH: lunch\nDINNER: dinner';
CREATE TABLE IF NOT EXISTS "recipe" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "link" VARCHAR(255),
    "description" TEXT,
    "summary_calories" DOUBLE PRECISION,
    "summary_proteins" DOUBLE PRECISION,
    "summary_fats" DOUBLE PRECISION,
    "summary_carbohydrates" DOUBLE PRECISION,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "product_for_recipe" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "weight_in_grams" DOUBLE PRECISION NOT NULL,
    "proteins" DOUBLE PRECISION NOT NULL,
    "fats" DOUBLE PRECISION NOT NULL,
    "carbohydrates" DOUBLE PRECISION NOT NULL,
    "calories" DOUBLE PRECISION NOT NULL,
    "product_id" UUID NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "recipe_id" UUID NOT NULL REFERENCES "recipe" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
