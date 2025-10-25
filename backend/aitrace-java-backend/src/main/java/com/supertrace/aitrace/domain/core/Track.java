package com.supertrace.aitrace.domain.core;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

import java.time.LocalDateTime;

@Builder
@Getter
@ToString
public class Track {
    private Step step;
    private LocalDateTime callTimestamp;
}
