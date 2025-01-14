import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>?> fetchInstagramData(String username) async {
  final url = 'https://www.instagram.com/$username/?__a=1';

  try {
    // Fetch the Instagram page as JSON
    final response = await http.get(Uri.parse(url), headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    });

    // Check if the response status is OK (200)
    if (response.statusCode == 200) {
      // Remove the 'for (;;);' wrapper if it exists
      String responseBody = response.body;
      if (responseBody.startsWith('for (;;);')) {
        responseBody = responseBody.substring(8); // Remove 'for (;;);' part
      }

      // Parse the cleaned response body as JSON
      final jsonResponse = jsonDecode(responseBody);

      // Check if the response contains valid data
      if (jsonResponse['graphql'] != null) {
        final user = jsonResponse['graphql']['user'];

        // Return the required user data
        return {
          'username': user['username'],
          'full_name': user['full_name'],
          'biography': user['biography'],
          'followers': user['edge_followed_by']['count'],
          'following': user['edge_follow']['count'],
          'total_posts': user['edge_owner_to_timeline_media']['count'],
          'profile_pic_url': user['profile_pic_url_hd'],
        };
      } else {
        print('User data not found.');
        return null;
      }
    } else {
      print('Failed to fetch data. Status code: ${response.statusCode}');
      return null;
    }
  } catch (e) {
    print('Error fetching data: $e');
    return null;
  }
}
