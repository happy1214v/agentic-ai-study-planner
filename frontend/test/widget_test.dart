import 'package:flutter_test/flutter_test.dart';

import 'package:frontend/main.dart';

void main() {
  testWidgets('Agentic AI chat screen loads', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const AgenticAIApp());

    expect(
      find.text('Agentic AI'),
      findsOneWidget,
    );

    expect(
      find.text('Hello! I am Agentic AI. How can I help you?'),
      findsOneWidget,
    );

    expect(
      find.text('Ask Agentic AI...'),
      findsOneWidget,
    );
  });
}