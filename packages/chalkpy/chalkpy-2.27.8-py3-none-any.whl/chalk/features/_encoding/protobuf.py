from chalk.parsed.proto import arrow_pb2 as pb

PROTOBUF_TO_UNIT = {
    pb.TimeUnit.Second: "s",
    pb.TimeUnit.Millisecond: "ms",
    pb.TimeUnit.Microsecond: "us",
    pb.TimeUnit.Nanosecond: "ns",
}


UNIT_TO_PROTOBUF = {
    "s": pb.TimeUnit.Second,
    "ms": pb.TimeUnit.Millisecond,
    "us": pb.TimeUnit.Microsecond,
    "ns": pb.TimeUnit.Nanosecond,
}
