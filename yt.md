
# Order created
{
  "eventId": "evt-78291",
  "orderId": 1045,
  "customerId": 501,
  "totalAmount": 2499,
  "createdAt": "2026-08-20T11:30:00Z"
}

# Order service

# Payment Service processes the payment.

# Inventory Service reserves or reduces stock.

# Notification Service sends email, SMS, or WhatsApp confirmation.

# Analytics Service records sales information.



@Service
public class OrderEventProducer {

    private final KafkaTemplate<String, OrderCreatedEvent> kafkaTemplate;

    public OrderEventProducer(
            KafkaTemplate<String, OrderCreatedEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publish(OrderCreatedEvent event) {
        kafkaTemplate.send(
            "order-created",
            event.orderId().toString(),
            event
        );
    }
}


