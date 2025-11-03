import os
import json
import time
from kafka import KafkaProducer
from rest_framework.views import  APIView
from rest_framework.views import  Response
from rest_framework.views import  status
from .serializers import LogSerializer

# Kafka configuration from environment
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC","logs")

# Function to initialize Kafka producer
def get_producer():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP.split(","),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        retries=5,
    )
    return producer

class healthAPIView(APIView):
    def get(self, request):
        return Response({"status": "ok"})

class LogProducerAPIView(APIView):
    """
    API endpoint: /api/log/
    Accepts POST with JSON:
    {
        "message": "string",
        "source": "optional string"
    }
    """

    def post(self, request):
        print("🔹 [DEBUG] Raw request data:", request.data)
        # Validate input data
        serializer = LogSerializer(data=request.data)
        print("🔹 [DEBUG] Serializer instance created:", serializer)
        if not serializer.is_valid():
            print("❌ [DEBUG] Validation failed:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        print("✅ [DEBUG] Validated data:", data)
        producer = get_producer()
        print("🚀 [DEBUG] Kafka producer created:", producer)
        
        try:
            # Send to Kafka topic
            producer.send(KAFKA_TOPIC, value=data)
            producer.flush()  # ensure message is sent
            print("✅ [DEBUG] Message sent to Kafka topic:", KAFKA_TOPIC)
            return Response({"status": "sent"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("💥 [ERROR] Failed to send message:", str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )