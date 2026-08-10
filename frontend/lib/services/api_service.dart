import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';

  Future<Map<String, dynamic>> sendTask(
    String task,
    String token,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/agent/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
      },
      body: jsonEncode({
        'task': task,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    }

    throw Exception(
      'API error: ${response.statusCode} - ${response.body}',
    );
  }

  Future<List<dynamic>> getMemories(
    String token, {
    int limit = 10,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/memory/?limit=$limit'),
      headers: {
        'Authorization': 'Token $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as List<dynamic>;
    }

    throw Exception(
      'Memory API error: ${response.statusCode} - ${response.body}',
    );
  }

  Future<List<dynamic>> getConversations(
    String token, {
    int limit = 50,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/conversations/?limit=$limit'),
      headers: {
        'Authorization': 'Token $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as List<dynamic>;
    }

    throw Exception(
      'Conversation API error: '
      '${response.statusCode} - ${response.body}',
    );
  }
}