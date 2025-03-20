package com.brunoxabreu.lead_enrichment.domain.repository;

import com.brunoxabreu.lead_enrichment.domain.model.Lead;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface LeadRepository extends JpaRepository<Lead, Long> {
    Optional<Lead> findByEmail(String email);
    Optional<Lead> findByProcessoInstanceId(String processoInstanceId);
} 