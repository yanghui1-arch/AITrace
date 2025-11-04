package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.core.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.StepService;
import com.supertrace.aitrace.vo.step.GetStepVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v0")
public class StepController {

    private final StepService stepService;

    @Autowired
    public StepController(StepService stepService) {
        this.stepService = stepService;
    }

    @PostMapping("/log/step")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(@RequestBody LogStepRequest logStepRequest) {
        try {
            UUID stepId = this.stepService.logStep(logStepRequest);
            return ResponseEntity.ok(APIResponse.success(stepId));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/step/{projectName}")
    public ResponseEntity<APIResponse<List<GetStepVO>>> getStep(@PathVariable String projectName) {
        try {
            List<Step> steps = this.stepService.getAllSteps(projectName);
            List<GetStepVO> getStepVOs = new ArrayList<>();
            for (Step step : steps) {
                getStepVOs.add(GetStepVO.builder()
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
                );
            }
            return ResponseEntity.ok(APIResponse.success(getStepVOs));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
