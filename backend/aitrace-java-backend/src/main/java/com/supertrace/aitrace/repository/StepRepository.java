package com.supertrace.aitrace.repository;

import com.supertrace.aitrace.domain.core.step.Step;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface StepRepository extends JpaRepository<Step, UUID> {
    List<Step> findStepsByProjectId(@NotNull Long projectId);

    List<Step> findStepsByTraceId(@NotNull UUID traceId);
}
