CREATE TABLE "users"(
    "id" BIGINT NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL,
    "full_name" VARCHAR(100) NOT NULL,
    "phone_number" VARCHAR(20) NULL,
    "profile_picture_url" VARCHAR(500) NULL,
    "latitude" DECIMAL(10, 8) NULL,
    "longitude" DECIMAL(11, 8) NULL,
    "city" VARCHAR(100) NULL,
    "stats" jsonb NULL DEFAULT 'ARRAY["plants_grown": 0 ,  "plants_harvested": 0 ,  "total_yield_kg": 0 ,  "total_savings": 0]',
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
CREATE TABLE "plants"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "scientific_name" VARCHAR(150) NULL,
    "description" TEXT NULL,
    "category" INTEGER NOT NULL,
    "image_url" VARCHAR(500) NULL,
    "requirements" jsonb NOT NULL,
    "market_price_per_kg" DECIMAL(12, 2) NULL,
    "yield_per_plant_kg" DECIMAL(8, 3) NULL,
    "growth_phases" jsonb NULL,
    "common_diseases" jsonb NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "plants" ADD PRIMARY KEY("id");
CREATE TABLE "user_environments"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "land_type" VARCHAR(50) NOT NULL,
    "area_length_cm" INTEGER NULL,
    "area_width_cm" INTEGER NULL,
    "sunlight_hours" DECIMAL(4, 2) NULL,
    "sunlight_intensity" VARCHAR(20) NULL,
    "photo_url" VARCHAR(500) NULL,
    "notes" TEXT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "user_environments" ADD PRIMARY KEY("id");
CREATE TABLE "recommendations"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "environment_id" BIGINT NULL,
    "input_data" jsonb NULL,
    "results" jsonb NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "recommendations_user_id_created_at_index" ON
    "recommendations"("user_id", "created_at");
ALTER TABLE
    "recommendations" ADD PRIMARY KEY("id");
CREATE TABLE "chat_sessions"(
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" BIGINT NOT NULL,
    "title" VARCHAR(255) NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "chat_sessions" ADD PRIMARY KEY("id");
CREATE INDEX "chat_sessions_user_id_created_at_index" ON
    "chat_sessions"("user_id", "created_at");
CREATE TABLE "chats"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "session_id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "role" VARCHAR(10) NOT NULL,
    "content" TEXT NULL,
    "image_url" VARCHAR(500) NULL,
    "voice_url" VARCHAR(500) NULL,
    "ai_metadata" jsonb NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "chats_user_id_session_id_created_at_index" ON
    "chats"(
        "user_id",
        "session_id",
        "created_at"
    );
ALTER TABLE
    "chats" ADD PRIMARY KEY("id");
CREATE TABLE "scans"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "garden_id" BIGINT NULL,
    "scan_type" INTEGER NOT NULL,
    "image_url" VARCHAR(500) NOT NULL,
    "results" jsonb NOT NULL,
    "confidence" DECIMAL(5, 2) NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "scans_user_id_created_at_index" ON
    "scans"("user_id", "created_at");
ALTER TABLE
    "scans" ADD PRIMARY KEY("id");
CREATE TABLE "garden_designs"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "environment_id" BIGINT NULL,
    "name" VARCHAR(100) NULL,
    "input_photo_url" VARCHAR(500) NOT NULL,
    "preferences" jsonb NULL,
    "design_output" jsonb NULL,
    "is_implemented" BOOLEAN NULL DEFAULT 'DEFAULT FALSE',
    "rating" INTEGER NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "garden_designs_user_id_created_at_index" ON
    "garden_designs"("user_id", "created_at");
ALTER TABLE
    "garden_designs" ADD PRIMARY KEY("id");
CREATE TABLE "user_gardens"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "environment_id" BIGINT NULL,
    "design_id" BIGINT NULL,
    "name" VARCHAR(100) NOT NULL,
    "status" INTEGER NULL DEFAULT 'aktif',
    "started_at" DATE NOT NULL,
    "ended_at" DATE NULL,
    "photo_url" VARCHAR(500) NULL,
    "plants" jsonb NOT NULL DEFAULT '[]',
    "activity_logs" jsonb NULL DEFAULT '[]',
    "notes" TEXT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "user_gardens_user_id_status_index" ON
    "user_gardens"("user_id", "status");
ALTER TABLE
    "user_gardens" ADD PRIMARY KEY("id");
CREATE TABLE "knowledge_base"(
    "id" BIGINT NOT NULL,
    "source" VARCHAR(200) NOT NULL,
    "source_type" VARCHAR(50) NOT NULL,
    "title" VARCHAR(300) NOT NULL,
    "content" TEXT NOT NULL,
    "embedding" INTEGER NULL,
    "tags" TEXT[] NULL,
    "is_active" BOOLEAN NULL DEFAULT 'DEFAULT TRUE',
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "knowledge_base" ADD PRIMARY KEY("id");
ALTER TABLE
    "user_gardens" ADD CONSTRAINT "user_gardens_design_id_foreign" FOREIGN KEY("design_id") REFERENCES "garden_designs"("id");
ALTER TABLE
    "recommendations" ADD CONSTRAINT "recommendations_environment_id_foreign" FOREIGN KEY("environment_id") REFERENCES "user_environments"("id");
ALTER TABLE
    "scans" ADD CONSTRAINT "scans_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "user_gardens" ADD CONSTRAINT "user_gardens_environment_id_foreign" FOREIGN KEY("environment_id") REFERENCES "user_environments"("id");
ALTER TABLE
    "user_environments" ADD CONSTRAINT "user_environments_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "garden_designs" ADD CONSTRAINT "garden_designs_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "garden_designs" ADD CONSTRAINT "garden_designs_environment_id_foreign" FOREIGN KEY("environment_id") REFERENCES "user_environments"("id");
ALTER TABLE
    "chats" ADD CONSTRAINT "chats_session_id_foreign" FOREIGN KEY("session_id") REFERENCES "chat_sessions"("id");
ALTER TABLE
    "chats" ADD CONSTRAINT "chats_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "chat_sessions" ADD CONSTRAINT "chat_sessions_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "user_gardens" ADD CONSTRAINT "user_gardens_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "recommendations" ADD CONSTRAINT "recommendations_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");