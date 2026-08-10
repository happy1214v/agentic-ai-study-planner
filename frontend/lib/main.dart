import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

import 'services/api_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load();

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

  // Token is loaded from frontend/.env
  String get _token => dotenv.get('API_TOKEN', fallback: '');

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

    if (_token.isEmpty) {
      setState(() {
        _messages.add(
          ChatMessage(
            text: text,
            isUser: true,
          ),
        );

        _messages.add(
          const ChatMessage(
            text: 'API token is not configured.',
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

  // ------------------------------------------------------------
  // RESPONSE FORMATTER
  // ------------------------------------------------------------

  String _extractResponse(Map<String, dynamic> result) {
    // Direct response
    final directResponse = result['response'];

    if (directResponse != null) {
      return directResponse.toString();
    }

    final routes = result['routes'];

    final results = result['results'];

    if (results is List && results.isNotEmpty) {
      for (final item in results.reversed) {
        if (item is! Map) {
          continue;
        }

        final type = item['type']?.toString();

        // ------------------------------------------------------
        // LLM
        // ------------------------------------------------------

        if (type == 'llm') {
          final response = item['response'];

          if (response != null) {
            return response.toString();
          }

          final error = item['error'];

          if (error != null) {
            return error.toString();
          }
        }

        // ------------------------------------------------------
        // CALCULATOR
        // ------------------------------------------------------

        if (type == 'calculator') {
          final calculation = item['result'];

          if (calculation != null) {
            return '### 🧮 Result\n\n'
                '**$calculation**';
          }
        }

        // ------------------------------------------------------
        // DATETIME
        // ------------------------------------------------------

        if (type == 'datetime') {
          final dateTimeValue = item['result'];

          if (dateTimeValue != null) {
            return _formatDateTime(
              dateTimeValue.toString(),
            );
          }
        }

        // ------------------------------------------------------
        // PLANNER
        // ------------------------------------------------------

        if (type == 'planner') {
          final execution = item['execution'];

          if (execution != null) {
            return _formatPlanner(execution);
          }

          final plan = item['plan'];

          if (plan != null) {
            return _formatPlanner(plan);
          }
        }

        // Generic response
        final response = item['response'];

        if (response != null) {
          return response.toString();
        }

        final calculation = item['result'];

        if (calculation != null) {
          return calculation.toString();
        }

        final execution = item['execution'];

        if (execution != null) {
          return _formatPlanner(execution);
        }
      }
    }

    // Generic result
    final resultValue = result['result'];

    if (resultValue != null) {
      return resultValue.toString();
    }

    // Fallback
    if (routes is List && routes.isNotEmpty) {
      return 'Task completed successfully.';
    }

    return result.toString();
  }

  // ------------------------------------------------------------
  // DATETIME FORMATTER
  // ------------------------------------------------------------

  String _formatDateTime(String value) {
    try {
      final parsed = DateTime.parse(value);

      final day = parsed.day.toString().padLeft(2, '0');
      final month = _monthName(parsed.month);
      final year = parsed.year;

      final hour = parsed.hour % 12 == 0
          ? 12
          : parsed.hour % 12;

      final minute =
          parsed.minute.toString().padLeft(2, '0');

      final period = parsed.hour >= 12 ? 'PM' : 'AM';

      return '### 📅 Date & Time\n\n'
          '**$day $month $year**\n\n'
          '🕐 **$hour:$minute $period**';
    } catch (_) {
      return value;
    }
  }

  String _monthName(int month) {
    const months = [
      '',
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ];

    return months[month];
  }

  // ------------------------------------------------------------
  // PLANNER FORMATTER
  // ------------------------------------------------------------

  String _formatPlanner(dynamic execution) {
    final buffer = StringBuffer();

    buffer.writeln('### 📋 Study Plan');
    buffer.writeln();

    if (execution is List) {
      int number = 1;

      for (final item in execution) {
        if (item is Map) {
          final step = item['step']?.toString();

          final status =
              item['status']?.toString() ?? 'completed';

          final result =
              item['result']?.toString();

          if (step != null && step.isNotEmpty) {
            buffer.writeln(
              '**$number. $step**',
            );

            if (status.toLowerCase() == 'completed') {
              buffer.writeln('✅ Completed');
            } else {
              buffer.writeln('⏳ $status');
            }

            if (result != null &&
                result.isNotEmpty &&
                !result.startsWith('Executed:')) {
              buffer.writeln();
              buffer.writeln(result);
            }

            buffer.writeln();

            number++;
          }
        }
      }

      if (number > 1) {
        return buffer.toString().trim();
      }
    }

    // If planner data is not a List
    if (execution is Map) {
      final nestedResults = execution['results'];

      if (nestedResults is List) {
        return _formatPlanner(nestedResults);
      }
    }

    return execution.toString();
  }

  // ------------------------------------------------------------
  // AUTO SCROLL
  // ------------------------------------------------------------

  void _scrollToBottom() {
    Future.delayed(
      const Duration(milliseconds: 100),
      () {
        if (_scrollController.hasClients) {
          _scrollController.animateTo(
            _scrollController.position.maxScrollExtent,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      },
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  // ------------------------------------------------------------
  // MESSAGE UI
  // ------------------------------------------------------------

  Widget _buildMessage(ChatMessage message) {
    final isUser = message.isUser;

    return Align(
      alignment:
          isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: const BoxConstraints(
          maxWidth: 700,
        ),
        margin: const EdgeInsets.only(
          bottom: 12,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 12,
        ),
        decoration: BoxDecoration(
          color: isUser
              ? Theme.of(context)
                  .colorScheme
                  .primaryContainer
              : Theme.of(context)
                  .colorScheme
                  .surfaceContainerHighest,
          borderRadius: BorderRadius.circular(18),
        ),
        child: isUser
            ? Text(
                message.text,
                style: const TextStyle(
                  fontSize: 16,
                ),
              )
            : MarkdownBody(
                data: message.text,
                selectable: true,
                styleSheet: MarkdownStyleSheet(
                  p: const TextStyle(
                    fontSize: 16,
                    height: 1.5,
                  ),
                  h1: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                  h2: const TextStyle(
                    fontSize: 21,
                    fontWeight: FontWeight.bold,
                  ),
                  h3: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  strong: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                  code: const TextStyle(
                    fontSize: 14,
                    fontFamily: 'monospace',
                  ),
                  codeblockPadding:
                      const EdgeInsets.all(12),
                  codeblockDecoration:
                      const BoxDecoration(
                    color: Colors.black12,
                    borderRadius: BorderRadius.all(
                      Radius.circular(10),
                    ),
                  ),
                  listBullet: const TextStyle(
                    fontSize: 16,
                  ),
                ),
              ),
      ),
    );
  }

  // ------------------------------------------------------------
  // MAIN UI
  // ------------------------------------------------------------

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
                return _buildMessage(
                  _messages[index],
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
                    Text(
                      'Agentic AI is thinking...',
                    ),
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
                      textInputAction:
                          TextInputAction.send,
                      onSubmitted: (_) =>
                          _sendMessage(),
                      decoration: InputDecoration(
                        hintText:
                            'Ask Agentic AI...',
                        border: OutlineInputBorder(
                          borderRadius:
                              BorderRadius.circular(28),
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
                    onPressed:
                        _isLoading ? null : _sendMessage,
                    child: const Icon(
                      Icons.send,
                    ),
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