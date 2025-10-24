package com.supertrace.aitrace.domain.core;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Builder
@Getter
public class Track {
    private Step step;
    private LocalDateTime callTimestamp;
}
