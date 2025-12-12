package com.supertrace.aitrace.service.application.impl;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.service.domain.ProjectService;
import com.supertrace.aitrace.service.application.QueryService;
import com.supertrace.aitrace.service.domain.StepService;
import com.supertrace.aitrace.service.domain.TraceService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class QueryServiceImpl implements QueryService {
    private final StepService stepService;
    private final TraceService traceService;
    private final ProjectService projectService;

    /**
     * Get all steps of project which is owned by user uuid
     *
     * @param userId user uuid
     * @param projectName project name
     * @param page current page
     * @param pageSize page size
     * @return All steps
     */
    @Override
    public Page<Step> getSteps(UUID userId, String projectName, int page, int pageSize) {
        Project project = this.projectService.getProjectByUserIdAndName(userId, projectName)
            .orElseThrow(() -> new RuntimeException("Project not found: " + projectName));
        Long projectId = project.getId();
        return this.stepService.findStepsByProjectId(projectId, page, pageSize);
    }

    @Override
    public List<Trace> getTraces(UUID userId, String projectName) {
        Project project = this.projectService.getProjectByUserIdAndName(userId, projectName)
            .orElseThrow(() -> new RuntimeException("Project not found: " + projectName));
        Long projectId = project.getId();
        return this.traceService.getTracesByProjectId(projectId);
    }
}
