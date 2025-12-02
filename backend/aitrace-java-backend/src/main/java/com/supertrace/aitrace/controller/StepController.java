package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.exception.AuthenticationException;
import com.supertrace.aitrace.exception.UserIdNotFoundException;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.ApiKeyService;
import com.supertrace.aitrace.service.StepService;
import com.supertrace.aitrace.utils.ApiKeyUtils;
import com.supertrace.aitrace.vo.step.GetStepVO;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v0")
@RequiredArgsConstructor
public class StepController {

    private final StepService stepService;
    private final ApiKeyService apiKeyService;

    @PostMapping("/log/step")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(
        @RequestHeader(value = "Authorization") String authorization,
        @RequestBody LogStepRequest logStepRequest
    ) {
        try {
            String apikey = ApiKeyUtils.extractApiKeyFromHttpHeader(authorization);
            boolean isExisted = this.apiKeyService.isApiKeyExist(apikey);
            if (!isExisted) {
                throw new AuthenticationException();
            }
            UUID userId = this.apiKeyService.resolveUserIdFromApiKey(apikey)
                .orElseThrow(UserIdNotFoundException::new);
            UUID stepId = this.stepService.logStep(userId, logStepRequest);
            return ResponseEntity.ok(APIResponse.success(stepId));
        } catch (AuthenticationException | UserIdNotFoundException e) {
            return ResponseEntity.badRequest().body(APIResponse.error("Invalid AITrace API key. Please ensure your API Key is valid and not expired."));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/step/{projectName}")
    public ResponseEntity<APIResponse<List<GetStepVO>>> getStep(HttpServletRequest request, @PathVariable String projectName) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            List<Step> steps = this.stepService.findStepsByUserIdAndProject(userId, projectName);
            List<GetStepVO> getStepVOs = steps.stream()
                .map(step -> GetStepVO.builder()
                    .id(step.getId())
                    .name(step.getName())
                    .type(step.getType())
                    .tags(step.getTags())
                    .input(step.getInput())
                    .output(step.getOutput())
                    .errorInfo(step.getErrorInfo())
                    .model(step.getModel())
                    .usage(step.getUsage())
                    .startTime(step.getStartTime())
                    .endTime(step.getEndTime())
                    .build()
                )
                .toList();
            return ResponseEntity.ok(APIResponse.success(getStepVOs));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
