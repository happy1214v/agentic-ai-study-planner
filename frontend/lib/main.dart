import 'package:flutter/material.dart';

import 'services/api_service.dart';

void main() {
  runApp(const AgenticAIApp());
}

class AgenticAIApp extends StatelessWidget {
  const AgenticAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Agentic AI',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.indigo,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const ChatPage(),
    );
  }
}

class ChatMessage {
  final String text;
  final bool isUser;

  const ChatMessage({
    required this.text,
    required this.isUser,
  });
}

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  final ApiService _apiService = ApiService();

  // Development token.
  // We will replace this with proper login/authentication later.
  final String _token =
    const String.fromEnvironment('API_TOKEN');

  bool _isLoading = false;

  final List<ChatMessage> _messages = [
    const ChatMessage(
      text: 'Hello! I am Agentic AI. How can I help you?',
      isUser: false,
    ),
  ];

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();

    if (text.isEmpty || _isLoading) {
      return;
    }

    if (_token == 'YOUR_TEST_API_TOKEN') {
      setState(() {
        _messages.add(
          ChatMessage(
            text: text,
            isUser: true,
          ),
        );

        _messages.add(
          const ChatMessage(
            text: 'API token is not configured yet.',
            isUser: false,
          ),
        );
      });

      _controller.clear();
      _scrollToBottom();
      return;
    }

    setState(() {
      _messages.add(
        ChatMessage(
          text: text,
          isUser: true,
        ),
      );

      _isLoading = true;
    });

    _controller.clear();
    _scrollToBottom();

    try {
      final result = await _apiService.sendTask(
        text,
        _token,
      );

      final responseText = _extractResponse(result);

      if (!mounted) {
        return;
      }

      setState(() {
        _messages.add(
          ChatMessage(
            text: responseText,
            isUser: false,
          ),
        );

        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) {
        return;
      }

      setState(() {
        _messages.add(
          ChatMessage(
            text: 'Error: $e',
            isUser: false,
          ),
        );

        _isLoading = false;
      });
    }

    _scrollToBottom();
  }

  String _extractResponse(Map<String, dynamic> result) {
    final directResponse = result['response'];

    if (directResponse != null) {
      return directResponse.toString();
    }

    final results = result['results'];

    if (results is List && results.isNotEmpty) {
      final lastResult = results.last;

      if (lastResult is Map<String, dynamic>) {
        final response = lastResult['response'];

        if (response != null) {
          return response.toString();
        }

        final calculation = lastResult['result'];

        if (calculation != null) {
          return calculation.toString();
        }
      }
    }

    final resultValue = result['result'];

    if (resultValue != null) {
      return resultValue.toString();
    }

    return result.toString();
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
            CircleAvatar(
              child: Icon(Icons.smart_toy),
            ),
            SizedBox(width: 12),
            Text(
              'Agentic AI',
              style: TextStyle(
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];

                return Align(
                  alignment: message.isUser
                      ? Alignment.centerRight
                      : Alignment.centerLeft,
                  child: Container(
                    constraints: const BoxConstraints(
                      maxWidth: 600,
                    ),
                    margin: const EdgeInsets.only(
                      bottom: 12,
                    ),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 12,
                    ),
                    decoration: BoxDecoration(
                      color: message.isUser
                          ? Theme.of(context)
                              .colorScheme
                              .primaryContainer
                          : Theme.of(context)
                              .colorScheme
                              .surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(18),
                    ),
                    child: Text(
                      message.text,
                      style: const TextStyle(
                        fontSize: 16,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),

          if (_isLoading)
            const Padding(
              padding: EdgeInsets.only(
                left: 16,
                bottom: 8,
              ),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Row(
                  children: [
                    SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                      ),
                    ),
                    SizedBox(width: 10),
                    Text('Agentic AI is thinking...'),
                  ],
                ),
              ),
            ),

          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(
                12,
                8,
                12,
                12,
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      textInputAction: TextInputAction.send,
                      onSubmitted: (_) => _sendMessage(),
                      decoration: InputDecoration(
                        hintText: 'Ask Agentic AI...',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(28),
                        ),
                        contentPadding:
                            const EdgeInsets.symmetric(
                          horizontal: 20,
                          vertical: 14,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  FloatingActionButton(
                    onPressed: _isLoading ? null : _sendMessage,
                    child: const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}