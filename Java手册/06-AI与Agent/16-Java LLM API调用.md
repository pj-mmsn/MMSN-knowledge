---
title: Java LLM API 调用与 Function Calling
tags: [Java, LLM, API, OkHttp, Function Calling, 原生调用, DeepSeek]
难度: 进阶
---

# Java LLM API 调用与 Function Calling

> **一句话**:不用任何框架，只用 Java 原生能力调 LLM API——当你想控制每一行代码、不想引入额外依赖时，这是最干净的方式。

## 核心概念

所有 LLM API 本质上就是一个 HTTP 接口：POST 一个 JSON body → 返回一个 JSON response。Java 调用 LLM 只需要三步：

```java
// 1. 构造 HTTP 请求（JSON 是请求体）
String requestJson = """
{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}]
}
""";

// 2. 发送 HTTP POST
HttpResponse<String> response = httpClient.send(request);

// 3. 解析 JSON 响应
String content = JsonPath.parse(response.body())
    .read("$.choices[0].message.content");
```

## 代码实例

### 1. 基础调用（Java 11+ HttpClient）

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class LLMClient {
    private static final String API_KEY = System.getenv("DEEPSEEK_API_KEY");
    private static final String BASE_URL = "https://api.deepseek.com/v1";
    private static final HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();

    public static String chat(String userMessage) throws Exception {
        String json = STR."""
            {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是一个Java技术专家"},
                    {"role": "user", "content": "\{userMessage}"}
                ],
                "temperature": 0
            }
            """;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(STR."\{BASE_URL}/chat/completions"))
                .header("Content-Type", "application/json")
                .header("Authorization", STR."Bearer \{API_KEY}")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .timeout(Duration.ofSeconds(60))
                .build();

        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() != 200) {
            throw new RuntimeException(STR."API错误: \{response.statusCode()} \{response.body()}");
        }

        // 用 Jackson 或 fastjson 解析
        // ObjectMapper mapper = new ObjectMapper();
        // JsonNode root = mapper.readTree(response.body());
        // return root.get("choices").get(0).get("message").get("content").asText();

        return response.body();  // 简化版，实际要解析
    }
}
```

### 2. Function Calling（不依赖框架）

```java
/**
 * Java 原生 Function Calling 实现
 * 不依赖 Spring AI / LangChain4j
 */

// ===== 1. 定义工具 =====
public class ToolDefinition {
    String name;
    String description;
    Map<String, Object> parameters;

    public static ToolDefinition weather() {
        ToolDefinition tool = new ToolDefinition();
        tool.name = "get_weather";
        tool.description = "获取指定城市的天气";
        tool.parameters = Map.of(
            "type", "object",
            "properties", Map.of(
                "city", Map.of("type", "string", "description", "城市名称")
            ),
            "required", new String[]{"city"}
        );
        return tool;
    }
}

// ===== 2. Agent 循环 =====
public class JavaAgent {

    private final HttpClient client = HttpClient.newHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();

    public String run(String question) throws Exception {
        List<Map<String, Object>> messages = new ArrayList<>();
        messages.add(Map.of("role", "user", "content", question));

        int maxSteps = 5;
        for (int step = 0; step < maxSteps; step++) {

            // 调用 LLM
            Map<String, Object> request = Map.of(
                "model", "deepseek-chat",
                "messages", messages,
                "tools", List.of(ToolDefinition.weather())
            );

            String json = mapper.writeValueAsString(request);
            HttpRequest httpReq = HttpRequest.newBuilder()
                .uri(URI.create("https://api.deepseek.com/v1/chat/completions"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + System.getenv("DEEPSEEK_API_KEY"))
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

            HttpResponse<String> resp = client.send(httpReq, HttpResponse.BodyHandlers.ofString());
            JsonNode root = mapper.readTree(resp.body());
            JsonNode message = root.get("choices").get(0).get("message");

            // 没有工具调用 → 直接返回
            if (!message.has("tool_calls")) {
                return message.get("content").asText();
            }

            messages.add(Map.of(
                "role", "assistant",
                "content", message.has("content") ? message.get("content").asText() : null,
                "tool_calls", message.get("tool_calls")
            ));

            // 执行工具
            for (JsonNode tc : message.get("tool_calls")) {
                String funcName = tc.get("function").get("name").asText();
                String funcArgs = tc.get("function").get("arguments").asText();

                // 调用实际方法
                String result;
                if ("get_weather".equals(funcName)) {
                    String city = mapper.readTree(funcArgs).get("city").asText();
                    result = STR."\{city}天气: 晴, 25°C";
                } else {
                    result = "未知工具";
                }

                messages.add(Map.of(
                    "role", "tool",
                    "tool_call_id", tc.get("id").asText(),
                    "content", result
                ));
            }
        }

        return "达到最大步数限制";
    }
}
```

### 3. 流式输出处理

```java
/**
 * Java 处理 SSE 流式输出
 */
import java.net.http.HttpResponse;
import java.util.concurrent.Flow.*;

public class StreamHandler implements Flow.Subscriber<String> {

    private Flow.Subscription subscription;
    private final StringBuilder content = new StringBuilder();

    @Override
    public void onSubscribe(Flow.Subscription subscription) {
        this.subscription = subscription;
        subscription.request(1);  // 请求第一个数据
    }

    @Override
    public void onNext(String line) {
        // 处理 SSE 数据行: data: {"choices":[{"delta":{"content":"你好"}}]}
        if (line.startsWith("data: ")) {
            String data = line.substring(6);
            if ("[DONE]".equals(data)) {
                subscription.cancel();
                return;
            }
            try {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode delta = mapper.readTree(data)
                    .get("choices").get(0).get("delta");
                if (delta.has("content")) {
                    String token = delta.get("content").asText();
                    content.append(token);
                    System.out.print(token);  // 逐个 token 输出
                }
            } catch (Exception e) {
                // 跳过解析错误
            }
        }
        subscription.request(1);  // 请求下一个数据
    }

    @Override
    public void onError(Throwable throwable) {
        System.err.println("流式错误: " + throwable);
    }

    @Override
    public void onComplete() {
        System.out.println("\n流式输出完成");
    }
}
```

### 4. Spring Boot 中的封装（轻量版）

```java
@Component
public class LLMService {

    private final RestTemplate restTemplate;
    private final String apiKey = System.getenv("DEEPSEEK_API_KEY");

    public LLMService() {
        this.restTemplate = new RestTemplate();
        restTemplate.getInterceptors().add((req, body, exec) -> {
            req.getHeaders().setBearerAuth(apiKey);
            return exec.execute(req, body);
        });
    }

    public String call(String prompt) {
        Map<String, Object> request = new HashMap<>();
        request.put("model", "deepseek-chat");
        request.put("messages", List.of(
            Map.of("role", "user", "content", prompt)
        ));

        String url = "https://api.deepseek.com/v1/chat/completions";
        JsonNode response = restTemplate.postForObject(url, request, JsonNode.class);

        return response.get("choices").get(0)
                .get("message").get("content").asText();
    }

    // 流式用 WebClient
    public Flux<String> callStream(String prompt) {
        return WebClient.create("https://api.deepseek.com")
            .post()
            .uri("/v1/chat/completions")
            .headers(h -> h.setBearerAuth(apiKey))
            .bodyValue(Map.of("model", "deepseek-chat",
                              "messages", List.of(Map.of("role", "user", "content", prompt)),
                              "stream", true))
            .retrieve()
            .bodyToFlux(String.class)
            .filter(line -> line.startsWith("data: "))
            .map(line -> {
                String data = line.substring(6);
                if ("[DONE]".equals(data)) return "";
                // 解析 delta.content
                return data;
            });
    }
}
```

## 常用模型 API 端点

| 模型 | 基础 URL | 鉴权方式 | 兼容性 |
|------|---------|---------|--------|
| DeepSeek | `https://api.deepseek.com/v1` | `Authorization: Bearer sk-xxx` | 兼容 OpenAI |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `Authorization: Bearer sk-xxx` | 兼容 OpenAI |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4` | `Authorization: Bearer sk-xxx` | 兼容 OpenAI |
| OpenAI | `https://api.openai.com/v1` | `Authorization: Bearer sk-xxx` | 标准 |

## 常见误区

- **误区1**: "调用 LLM API 一定需要框架" —— 不，90% 的场景只需要 HTTP POST + JSON 解析。框架帮你封装了重试、流式、Function Calling 的 JSON 解析逻辑，但底层就是 HTTP。
- **误区2**: "Java 不能流式输出" —— 可以。`WebClient` + SSE 完美支持。原理是逐行读取 HTTP 响应的 `data:` 事件。
- **误区3**: "Java AI 性能比 Python 差" —— Agent 的瓶颈永远在 LLM API 延迟上（2-5秒），和语言无关。Java 在并发处理和内存效率上反而有优势。

## 参考来源

- OpenAI API 文档: https://platform.openai.com/docs/api-reference
- DeepSeek API 文档: https://platform.deepseek.com/api-docs
- Java HttpClient 文档: https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html
- 相关笔记: `Java手册/06-AI与Agent/15-Spring AI实战.md`
