from budgetguard.core.pipelines.pipeline import Pipeline
import sys


def run_task(pipeline: Pipeline):
    pipeline.run()


def run(task: str, partition_id: str):
    if task == "ingest_account_data":
        from budgetguard.core.pipelines.ingest_account_data import (
            IngestAccountData,
        )

        pipeline = IngestAccountData(partition_id)
        run_task(pipeline=pipeline)
    elif task == "dummy":
        from budgetguard.core.pipelines.dummy_pipeline import DummyPipeline

        pipeline = DummyPipeline(partition_id)
        run_task(pipeline=pipeline)
    else:
        raise ValueError(f"Unknown task: {task}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
