import os.path

from hamilton import driver

import tests.resources.basic_dag_with_config
import tests.resources.parallel_dag
from dagworks import adapters


adapter_kwargs = dict(
    project_id=19319,
    api_key="l-PlUq02JLQR6rAvO4x7VTttNTtprj1Tz5zBZ0ARpQ4olb8TK4hlgY2pennFhvsR1DxpYMQ-TLm0JknXVn7y9A",
    username="stefan@dagworks.io",
    tags={"env": "dev", "status": "development"},
)


def test_adapters():
    kwargs = adapter_kwargs | dict(
        dag_name="test_dag",
    )
    lifecycle_adapters = [adapters.DAGWorksTracker(**kwargs)]
    dr = (
        driver.Builder()
        .with_modules(tests.resources.basic_dag_with_config)
        .with_config({"foo": "baz"})
        .with_adapters(*lifecycle_adapters)
        .build()
    )
    result = dr.execute(final_vars=["a", "b", "c"], inputs={"a": 1})
    assert result == {"a": 1, "b": 3, "c": 6}


def test_async():
    # TODO: complete Async
    kwargs = adapter_kwargs | dict(
        dag_name="async_test_dag",
    )
    [adapters.AsyncDAGWorksAdapter(**kwargs)]


def test_parallel():
    from hamilton.plugins import h_ray
    import ray

    kwargs = adapter_kwargs | dict(
        dag_name="parallel_test_dag",
    )
    lifecycle_adapters = [adapters.DAGWorksTracker(**kwargs)]
    remote_executor = h_ray.RayTaskExecutor(None)
    # remote_executor = executors.SynchronousLocalTaskExecutor()
    shutdown = ray.shutdown
    dr = (
        driver.Builder()
        .enable_dynamic_execution(allow_experimental_mode=True)
        .with_remote_executor(remote_executor)  # We only need to specify remote executor
        # The local executor just runs it synchronously
        .with_modules(tests.resources.parallel_dag)
        .with_adapters(*lifecycle_adapters)
        .build()
    )
    data_dir = os.path.join(os.path.dirname(__file__), "resources", "data")
    print(
        dr.execute(final_vars=["statistics_by_city"], inputs={"data_dir": data_dir})[
            "statistics_by_city"
        ]
    )
    if shutdown:
        shutdown()


if __name__ == "__main__":
    test_adapters()
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    test_async()
    test_parallel(os.path.expanduser("~/temp"))
