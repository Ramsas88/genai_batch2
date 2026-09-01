// 1. Add Spring AI OpenAI dependency
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>

import org.springframework.ai.chat.client.ChatClient;

// 2. Configure API key
spring.ai.openai.api-key=${OPENAI_API_KEY}


// 3. Inject ChatClient
@RestController
class ChatController {

    private final ChatClient chatClient;

    ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    // 4. Send prompt and return AI response
    @GetMapping("/chat")
    String chat(@RequestParam String message) {

        return chatClient
                .prompt()
                .user(message)
                .call()
                .content();
    }
}