from grafanalib.core import (
    Dashboard, Graph, Row, XAxis, SECONDS_FORMAT, BYTES_FORMAT, OPS_FORMAT,
    single_y_axis, Target
)

dashboard = Dashboard(
    title="Test Resolver dashboard",
    rows=[
        Row(panels=[
            Graph(
                title="gRPC Rate",
                dataSource='Prometheus',
                targets=[
                    Target(
                        expr='rate(grpc_server_handled_total{grpc_service="ResolverService"}[1m])',
                        legendFormat="Total-{{pod}}",
                        refId='A',
                    ),
                    Target(
                        expr='rate(grpc_server_handled_total{grpc_method="Resolve", grpc_service="ResolverService"}[1m])',
                        legendFormat="Resolve-{{pod}}",
                        refId='B',
                    )],
                xAxis=XAxis(mode="time"),
                yAxes=single_y_axis(format=OPS_FORMAT, min=None),
            ),
        ]),
        Row(panels=[
            Graph(
                title="gRPC latency",
                dataSource='Prometheus',
                targets=[
                    Target(
                        expr='histogram_quantile(0.95, sum(rate(grpc_server_handled_latency_seconds_bucket{service="monitoring-compute-resolver-primary", grpc_service="ResolverService", grpc_method="Resolve"}[1m])) by (le))',
                        legendFormat="Resolve p95",
                        refId='A',
                    ),
                ],
                xAxis=XAxis(mode="time"),
                yAxes=single_y_axis(format=SECONDS_FORMAT, min=None),
            ),
        ]),
        Row(panels=[
            Graph(
                title="Memory usage",
                dataSource='Prometheus',
                targets=[
                    Target(
                        expr='process_resident_memory_bytes{service="monitoring-compute-resolver-primary"}',
                        legendFormat="{{pod}}",
                        refId='A',
                    ),
                ],
                xAxis=XAxis(mode="time"),
                yAxes=single_y_axis(format=BYTES_FORMAT, min=None),
            ),
        ])
    ],
).auto_panel_ids()

