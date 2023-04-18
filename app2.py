from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace, baggage, context
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from opentelemetry.exporter.jaeger.thrift import JaegerExporter

jaeger_exporter = JaegerExporter(
        collector_endpoint='http://localhost:14268/api/traces'
        )

resource = Resource(attributes={
        SERVICE_NAME: "app2"
        })

jaeger_processor = BatchSpanProcessor(jaeger_exporter)
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
provider.add_span_processor(jaeger_processor)
trace.set_tracer_provider(provider)

app = Flask('service2')
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def proxy():
    # try to inject some baggage
    current_ctx = context.get_current() 
    baggage.set_baggage('text', 'hey! This is baggage from app2!', current_ctx)
    return 'hello from app2'


