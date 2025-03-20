package com.brunoxabreu.lead_enrichment.controller;

import com.brunoxabreu.lead_enrichment.domain.model.Lead;
import com.brunoxabreu.lead_enrichment.service.LeadEnrichmentService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/leads")
@RequiredArgsConstructor
public class LeadController {

    private final LeadEnrichmentService leadService;

    @PostMapping
    public ResponseEntity<Lead> criarLead(@RequestBody Lead lead) {
        return ResponseEntity.ok(leadService.iniciarProcesso(lead));
    }

    @PostMapping("/{id}/enriquecer")
    public ResponseEntity<Lead> enriquecerLead(@PathVariable Long id) {
        return ResponseEntity.ok(leadService.enriquecerLead(id));
    }
} 