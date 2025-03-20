package com.brunoxabreu.lead_enrichment.service;

import com.brunoxabreu.lead_enrichment.domain.model.Lead;
import com.brunoxabreu.lead_enrichment.domain.repository.LeadRepository;
import com.brunoxabreu.lead_enrichment.integration.ClearbitClient;
import com.brunoxabreu.lead_enrichment.integration.HunterClient;
import com.brunoxabreu.lead_enrichment.integration.LinkedInClient;
import io.camunda.zeebe.client.ZeebeClient;
import io.camunda.zeebe.client.api.response.ProcessInstanceEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class LeadEnrichmentService {

    private final LeadRepository leadRepository;
    private final ZeebeClient zeebeClient;
    private final LinkedInClient linkedInClient;
    private final ClearbitClient clearbitClient;
    private final HunterClient hunterClient;

    @Value("${services.linkedin.api-key}")
    private String linkedinApiKey;

    @Value("${services.clearbit.api-key}")
    private String clearbitApiKey;

    @Value("${services.hunter.api-key}")
    private String hunterApiKey;

    @Transactional
    public Lead iniciarProcesso(Lead lead) {
        log.info("Iniciando processo de enriquecimento para lead: {}", lead.getNome());
        
        // Gera ID único para o lead
        lead.setStatus("EM_PROCESSAMENTO");
        
        // Salva o lead
        lead = leadRepository.save(lead);
        
        // Inicia o processo no Camunda
        ProcessInstanceEvent processInstance = zeebeClient.newCreateInstanceCommand()
                .bpmnProcessId("lead-enrichment")
                .latestVersion()
                .variables(Map.of(
                        "leadId", lead.getId(),
                        "nome", lead.getNome(),
                        "email", lead.getEmail(),
                        "empresa", lead.getEmpresa()
                ))
                .send()
                .join();
        
        // Atualiza o lead com o ID do processo
        lead.setProcessoInstanceId(processInstance.getProcessInstanceKey().toString());
        return leadRepository.save(lead);
    }

    @Transactional
    public Lead enriquecerLead(Long leadId) {
        log.info("Enriquecendo lead: {}", leadId);
        
        Lead lead = leadRepository.findById(leadId)
                .orElseThrow(() -> new RuntimeException("Lead não encontrado"));
        
        Map<String, Object> dadosEnriquecidos = new HashMap<>();
        
        try {
            // Busca dados no LinkedIn
            Map<String, Object> dadosLinkedIn = linkedInClient.buscarPessoa(
                    "Bearer " + linkedinApiKey,
                    lead.getNome() + " " + lead.getEmpresa()
            );
            dadosEnriquecidos.put("linkedin", dadosLinkedIn);
            
            // Busca dados no Clearbit
            Map<String, Object> dadosClearbit = clearbitClient.buscarPessoa(
                    "Bearer " + clearbitApiKey,
                    lead.getEmail()
            );
            dadosEnriquecidos.put("clearbit", dadosClearbit);
            
            // Busca dados no Hunter.io
            Map<String, Object> dadosHunter = hunterClient.buscarEmail(
                    "Bearer " + hunterApiKey,
                    lead.getNome(),
                    lead.getEmpresa()
            );
            dadosEnriquecidos.put("hunter", dadosHunter);
            
            // Atualiza o lead com os dados enriquecidos
            lead.setDadosEnriquecidos(dadosEnriquecidos);
            lead.setStatus("ENRIQUECIDO");
            lead.setDataEnriquecimento(java.time.LocalDateTime.now());
            
            // Completa a tarefa no processo
            zeebeClient.newPublishMessageCommand()
                    .messageName("lead-enriquecido")
                    .correlationKey(lead.getProcessoInstanceId())
                    .variables(Map.of("enriquecido", true))
                    .send()
                    .join();
            
        } catch (Exception e) {
            log.error("Erro ao enriquecer lead: {}", e.getMessage());
            lead.setStatus("ERRO");
            lead.setObservacoes("Erro ao enriquecer lead: " + e.getMessage());
            
            // Completa a tarefa com erro no processo
            zeebeClient.newPublishMessageCommand()
                    .messageName("lead-erro")
                    .correlationKey(lead.getProcessoInstanceId())
                    .variables(Map.of(
                            "enriquecido", false,
                            "erro", e.getMessage()
                    ))
                    .send()
                    .join();
        }
        
        return leadRepository.save(lead);
    }
} 