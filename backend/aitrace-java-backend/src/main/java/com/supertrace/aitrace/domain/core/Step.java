package com.supertrace.aitrace.domain.core;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "step")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Step {
    @Id
    // @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotNull
    private String name;

    @NotNull
    @Column(name = "trace_id")
    private UUID traceId;

    @Column(name = "parent_step_id")
    private UUID parentStepId;

    @NotBlank
    private String type;

    @JdbcTypeCode(SqlTypes.JSON)
    @NotNull
    @Column(columnDefinition = "jsonb")
    private List<String> tags;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> input;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> output;

    @Column(name = "error_info")
    private String errorInfo;

    private String model;

    private Integer usage;

    @NotBlank
    @Column(name = "project_name")
    private String projectName;

}
