package com.supertrace.aitrace.vo;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
public class AuthVO {
    private String token;
    private UUID userId;
}
