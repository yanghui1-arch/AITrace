package com.supertrace.aitrace.domain.core.step;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class StepOutput {
    /* Step function output */
    private Object funcOutput;
    /* LLM output used in step
    *  TODO: llm output type is temporary. Decided by python sdk.
    *        Now sdk will pass a string such as `<Object Stream xxx>` or Stream content only.
    */
    private Object llmOutputs;
}
