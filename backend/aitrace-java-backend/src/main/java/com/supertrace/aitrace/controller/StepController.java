package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.LogStepService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("/api/v0")
public class StepController {

    private final LogStepService logStepService;

    @Autowired
    public StepController(LogStepService logStepService) {
        this.logStepService = logStepService;
    }

    @PostMapping("/log/step")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(@RequestBody LogStepRequest logStepRequest) {
        try {
            System.out.println(logStepRequest);
            UUID stepId = this.logStepService.logStep(logStepRequest);
            return ResponseEntity.ok(APIResponse.success(stepId));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
