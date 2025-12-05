package com.supertrace.aitrace.dto.trace;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import com.supertrace.aitrace.domain.core.Track;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@Data
public class LogTraceRequest {
    @NotNull
    private String projectName;

    @NotNull
    private String traceId;

    @NotNull
    private String traceName;

    @NotNull
    private String conversationId;

    @NotNull
    private List<String> tags;

    private Map<String, Object> input;

    private Map<String, Object> output;

    private List<Track> tracks;

    private String errorInfo;

    private LocalDateTime startTime;

    private LocalDateTime lastUpdateTimestamp;

}
