import argparse
from budgetguard.core.pipelines.pipeline import Pipeline


parser = argparse.ArgumentParser()

parser.add_argument(
    "-pid",
    "--partition-id",
    help="The partition of the datalake to read from.",
    type=str,
    required=True,
)

parser.add_argument(
    "-t",
    "--task",
    help="The task to run.",
    type=str,
    required=True,
)


def run_task(pipeline: Pipeline):
    pipeline.run()


def run(task: str, partition_id: str):
    if task == "ingest_account_data":
        from budgetguard.core.pipelines.ingest_account_data import (
            IngestAccountData,
        )

        pipeline = IngestAccountData(partition_id)
        run_task(pipeline=pipeline)
    else:
        raise ValueError(f"Unknown task: {task}")


if __name__ == "__main__":
    args = parser.parse_args()
    run(args.task, args.partition_id)
