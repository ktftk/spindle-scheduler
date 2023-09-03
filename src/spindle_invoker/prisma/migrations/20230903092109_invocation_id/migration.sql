/*
  Warnings:

  - The primary key for the `completed_spider_workflow_run` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `workflow_execution_id` on the `completed_spider_workflow_run` table. All the data in the column will be lost.
  - You are about to drop the column `workflow_execution_id` on the `invoked_spider_run_task` table. All the data in the column will be lost.
  - The primary key for the `launched_spider_run_workflow` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `trigger_type` on the `launched_spider_run_workflow` table. All the data in the column will be lost.
  - You are about to drop the column `workflow_execution_id` on the `launched_spider_run_workflow` table. All the data in the column will be lost.
  - Added the required column `invocation_id` to the `completed_spider_workflow_run` table without a default value. This is not possible if the table is not empty.
  - Added the required column `execution_id` to the `invoked_spider_run_task` table without a default value. This is not possible if the table is not empty.
  - Added the required column `invocation_id` to the `invoked_spider_run_task` table without a default value. This is not possible if the table is not empty.
  - Added the required column `invocation_id` to the `launched_spider_run_workflow` table without a default value. This is not possible if the table is not empty.
  - Added the required column `invocation_type` to the `launched_spider_run_workflow` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "completed_spider_workflow_run" DROP CONSTRAINT "completed_spider_workflow_run_pkey",
DROP COLUMN "workflow_execution_id",
ADD COLUMN     "invocation_id" TEXT NOT NULL,
ADD CONSTRAINT "completed_spider_workflow_run_pkey" PRIMARY KEY ("invocation_id");

-- AlterTable
ALTER TABLE "invoked_spider_run_task" DROP COLUMN "workflow_execution_id",
ADD COLUMN     "execution_id" TEXT NOT NULL,
ADD COLUMN     "invocation_id" TEXT NOT NULL;

-- AlterTable
ALTER TABLE "launched_spider_run_workflow" DROP CONSTRAINT "launched_spider_run_workflow_pkey",
DROP COLUMN "trigger_type",
DROP COLUMN "workflow_execution_id",
ADD COLUMN     "invocation_id" TEXT NOT NULL,
ADD COLUMN     "invocation_type" TEXT NOT NULL,
ADD CONSTRAINT "launched_spider_run_workflow_pkey" PRIMARY KEY ("invocation_id");
