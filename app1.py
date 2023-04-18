from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace, propagators
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

import opentelemetry.instrumentation.requests
import requests

jaeger_exporter = JaegerExporter(
        collector_endpoint='http://localhost:14268/api/traces'
        )

resource = Resource(attributes={
        SERVICE_NAME: "app1"
        })


jaeger_processor = BatchSpanProcessor(jaeger_exporter)
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
provider.add_span_processor(jaeger_processor)
trace.set_tracer_provider(provider)


app = Flask('service1')
FlaskInstrumentor().instrument_app(app)
opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()

@app.route('/')
def proxy():
    resp = requests.get('http://localhost:8080/')
    print(resp)
    return 'hello from app1'
