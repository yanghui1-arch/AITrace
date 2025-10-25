package com.supertrace.aitrace.repository;

import com.supertrace.aitrace.domain.core.Trace;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface TraceRepository extends JpaRepository<Trace, UUID> {
}
