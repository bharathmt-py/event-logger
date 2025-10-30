import json
import os
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from logs_app.models import LogEntry

class Command(BaseCommand):
    help = "Starts Kafka consumer to store log messages into MySQL"

    def handle(self, *args, **options):
        topic = os.getenv("KAFKA_TOPIC", "logs")
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

        self.stdout.write(self.style.SUCCESS(f"Listening to Kafka topic: {topic}"))

        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers.split(","),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="log-consumer-group",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

        for message in consumer:
            data = message.value
            print("::::::::Consumer Data::::::::::",data)
            try:
                msg = data.get("message")
                src = data.get("source")
                LogEntry.objects.create(message=msg, source=src)
                self.stdout.write(self.style.SUCCESS(f"✅ Saved log: {msg}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ Error saving message: {e}"))
