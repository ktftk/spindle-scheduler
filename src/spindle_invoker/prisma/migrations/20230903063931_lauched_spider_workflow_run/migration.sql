/*
  Warnings:

  - You are about to drop the column `params` on the `completed_spider_workflow_run` table. All the data in the column will be lost.
  - You are about to drop the column `spider_name` on the `completed_spider_workflow_run` table. All the data in the column will be lost.
  - You are about to drop the column `target_period` on the `completed_spider_workflow_run` table. All the data in the column will be lost.
  - You are about to drop the column `trigger_type` on the `completed_spider_workflow_run` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "completed_spider_workflow_run" DROP COLUMN "params",
DROP COLUMN "spider_name",
DROP COLUMN "target_period",
DROP COLUMN "trigger_type";

-- CreateTable
CREATE TABLE IF NOT EXISTS "launched_spider_run_workflow" (
    "workflow_execution_id" TEXT NOT NULL,
    "trigger_type" TEXT NOT NULL,
    "spider_name" TEXT NOT NULL,
    "params" JSONB NOT NULL,
    "target_period" DATE NOT NULL,
    "launched_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "launched_spider_run_workflow_pkey" PRIMARY KEY ("workflow_execution_id")
);
