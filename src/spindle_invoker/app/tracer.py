import os

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# https://cloud.google.com/trace/docs/setup/python-ot?hl=ja


tracer_provider = TracerProvider()

if os.getenv("ENV", "dev") != "ci":
    cloud_trace_exporter = CloudTraceSpanExporter(
        project_id=os.environ["GCP_PROJECT_ID"]
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(cloud_trace_exporter)
    )

    trace.set_tracer_provider(tracer_provider)


tracer = trace.get_tracer(__name__)
