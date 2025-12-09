package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.exception.AuthenticationException;
import com.supertrace.aitrace.exception.UserIdNotFoundException;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.application.ApiKeyService;
import com.supertrace.aitrace.service.application.DeleteService;
import com.supertrace.aitrace.service.application.LogService;
import com.supertrace.aitrace.service.application.QueryService;
import com.supertrace.aitrace.utils.ApiKeyUtils;
import com.supertrace.aitrace.vo.trace.GetTraceVO;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v0")
public class TraceController {
    private final ApiKeyService apiKeyService;
    private final LogService logService;
    private final QueryService queryService;
    private final DeleteService deleteService;

    @PostMapping("/log/trace")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(
        @RequestHeader(value = "Authorization") String authorization,
        @RequestBody LogTraceRequest logTraceRequest
    ) {
        try {
            String apikey = ApiKeyUtils.extractApiKeyFromHttpHeader(authorization);
            boolean isExisted = this.apiKeyService.isApiKeyExist(apikey);
            if (!isExisted) {
                throw new AuthenticationException();
            }
            UUID userId = this.apiKeyService.resolveUserIdFromApiKey(apikey)
                .orElseThrow(UserIdNotFoundException::new);
            UUID traceId = this.logService.logTrace(userId, logTraceRequest);
            return ResponseEntity.ok(APIResponse.success(traceId));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/trace/{projectName}")
    public ResponseEntity<APIResponse<List<GetTraceVO>>> getTrace(HttpServletRequest request, @PathVariable("projectName") String projectName) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            List<Trace> traces = this.queryService.getTraces(userId, projectName);
            List<GetTraceVO> getTraceVOs = traces.stream()
                .map(trace -> GetTraceVO.builder()
                    .id(trace.getId())
                    .name(trace.getName())
                    .tags(trace.getTags())
                    .input(trace.getInput())
                    .output(trace.getOutput())
                    .tracks(trace.getTracks())
                    .errorInfo(trace.getErrorInfo())
                    .startTime(trace.getStartTime())
                    .lastUpdateTimestamp(trace.getLastUpdateTimestamp())
                    .build()
                )
                .toList();
            return ResponseEntity.ok(APIResponse.success(getTraceVOs));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/trace/delete")
    public ResponseEntity<APIResponse<List<UUID>>> deleteSteps(@RequestBody List<String> traceIds) {
        try {
            List<UUID> tracesUUIDToDelete = traceIds.stream().map(UUID::fromString).toList();
            List<UUID> tracesUUIDToDeleteSuccess = this.deleteService.deleteTracesAndRelatedStepsByTraceIds(tracesUUIDToDelete);
            return ResponseEntity.ok(APIResponse.success(tracesUUIDToDeleteSuccess));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(APIResponse.error("Please ensure trace id to delete is correct."));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
