-- CreateTable
CREATE TABLE IF NOT EXISTS "spider_run_task" (
    "hash" TEXT NOT NULL,
    "spider_run_rule_id" TEXT NOT NULL,
    "spider_name" TEXT NOT NULL,
    "release_group_code" TEXT NOT NULL,
    "invoke_delay" INTEGER,
    "input_params" JSONB,
    "target_period" DATE NOT NULL,
    "release_period" DATE NOT NULL,
    "release_scheduled_at" TIMESTAMP(3) NOT NULL,
    "scheduled_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "spider_run_task_pkey" PRIMARY KEY ("hash")
);

-- CreateTable
CREATE TABLE IF NOT EXISTS "invoked_spider_run_task" (
    "hash" TEXT NOT NULL,
    "invoked_at" TIMESTAMP(3) NOT NULL,
    "workflow_execution_id" TEXT NOT NULL,

    CONSTRAINT "invoked_spider_run_task_pkey" PRIMARY KEY ("hash")
);
