package com.supertrace.aitrace.vo;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AuthVO {
    private String token;
    private String userName;
    private String avatar;
}
