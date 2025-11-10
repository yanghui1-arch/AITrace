package com.supertrace.aitrace.vo.trace;

import com.supertrace.aitrace.domain.core.Track;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Data
@Builder
public class GetTraceVO {
    private UUID id;

    @NotNull
    private String name;

    @NotNull
    private List<String> tags;

    private Map<String, Object> input;

    private Map<String, Object> output;

    @NotNull
    private List<Track> tracks;

    private String errorInfo;

    private LocalDateTime startTime;

    private LocalDateTime lastUpdateTimestamp;

}
