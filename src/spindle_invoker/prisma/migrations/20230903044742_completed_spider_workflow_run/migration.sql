-- CreateTable
CREATE TABLE IF NOT EXISTS "completed_spider_workflow_run" (
    "workflow_execution_id" TEXT NOT NULL,
    "trigger_type" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "spider_name" TEXT NOT NULL,
    "params" JSONB NOT NULL,
    "target_period" DATE NOT NULL,
    "completed_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "completed_spider_workflow_run_pkey" PRIMARY KEY ("workflow_execution_id")
);
