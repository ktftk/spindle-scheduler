from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .config import GCP_PROJECT_ID

# https://cloud.google.com/trace/docs/setup/python-ot?hl=ja


tracer_provider = TracerProvider()

cloud_trace_exporter = CloudTraceSpanExporter(project_id=GCP_PROJECT_ID)

tracer_provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))

trace.set_tracer_provider(tracer_provider)


tracer = trace.get_tracer(__name__)
