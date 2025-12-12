package com.supertrace.aitrace.vo;

import lombok.Builder;
import lombok.Data;

import java.util.List;

/**
 * Generate pagination search result response.
 *
 * @param <T> data type
 */
@Data
@Builder
public class PageVO<T> {
    private int pageCount;
    private List<T> data;
}
