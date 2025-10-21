package com.supertrace.aitrace.response;

import lombok.Data;

@Data
public class APIResponse<T> {
    private int code;
    private String message;
    private T data;

    private APIResponse(int code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    public static <T> APIResponse<T> success(T data) {
        return new APIResponse<>(200, "Response successfully", data);
    }

    public static <T> APIResponse<T> success(T data, String message) {
        return new APIResponse<>(200, message, data);
    }

    public static <T> APIResponse<T> error(String message) {
        return new APIResponse<>(400, message, null);
    }
}
