from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "user" ADD "type" VARCHAR(9) NOT NULL  DEFAULT 'user';
        ALTER TABLE "user" ADD "status" VARCHAR(8) NOT NULL  DEFAULT 'inactive';
        ALTER TABLE "user" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "user" DROP COLUMN "is_active";
        ALTER TABLE "user" DROP COLUMN "is_superuser";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_active" BOOL NOT NULL  DEFAULT True;
        ALTER TABLE "user" ADD "is_superuser" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" DROP COLUMN "updated_at";
        ALTER TABLE "user" DROP COLUMN "type";
        ALTER TABLE "user" DROP COLUMN "status";
        ALTER TABLE "user" DROP COLUMN "created_at";"""
