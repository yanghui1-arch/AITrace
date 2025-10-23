package com.supertrace.aitrace.response;

import lombok.Data;

/**
 * APIResponse is only responsible for returning backend result to web or client.
 * It only can be used in the controller.
 *
 * @author dass90
 * @since 2025-10-23
 *
 * @param <T> type of data
 */
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
