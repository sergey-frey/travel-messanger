import faust

from pkg.kafka.channel import Channel, MyModel

app = faust.App(
    "access-logs",
    broker="kafka://localhost:9092",
    value_serializer="json",
)

transfer_counts = app.Table(
    "transfer_counts",
    default=int,
    key_type=str,
    value_type=int,
)
access_topic = app.topic("access")


@app.agent(access_topic)
async def access_logs(stream):
    async for event in stream:
        print("event", event["message"])


@app.timer(1.0)
async def populate():
    await Channel.send(value=MyModel(303))


# async def main():
#     channel = app.channel()

#     await channel.put(1)
#     async for event in channel:
#         print(event.value)
#         # the channel is infinite so we break after first event
#         break
