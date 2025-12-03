package com.supertrace.aitrace.repository;

import com.supertrace.aitrace.domain.core.Trace;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TraceRepository extends JpaRepository<Trace, UUID> {
    List<Trace> findTracesByProjectId(@NotNull Long projectId);
}
