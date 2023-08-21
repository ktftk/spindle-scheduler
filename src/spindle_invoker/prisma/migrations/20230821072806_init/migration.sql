-- CreateTable
CREATE TABLE "invoked_spider_run_task" (
    "hash" TEXT NOT NULL,
    "invoked_at" TIMESTAMP(3) NOT NULL,
    "workflow_execution_id" TEXT NOT NULL,

    CONSTRAINT "invoked_spider_run_task_pkey" PRIMARY KEY ("hash")
);
