package com.supertrace.aitrace.utils;

public class ApiKeyUtils {

    public static String concealApiKey(String apiKey) {
        if (apiKey == null || apiKey.length() <= 6) {
            return apiKey;
        }

        int start = 6;
        int end = 32;

        StringBuilder sb = new StringBuilder(apiKey);
        for (int i = start; i <= end; i++) {
            sb.setCharAt(i, '*');
        }
        return sb.toString();
    }
}
