package com.supertrace.aitrace.domain.auth;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "user_auth")
public class UserAuth {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotBlank
    @Column(name = "user_uuid")
    private UUID userId;

    @Enumerated(EnumType.STRING)
    @Column(name = "auth_type")
    private AuthPlatform authType;

    @NotBlank
    private String identifier;

    private String credential;

    @NotBlank
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}
