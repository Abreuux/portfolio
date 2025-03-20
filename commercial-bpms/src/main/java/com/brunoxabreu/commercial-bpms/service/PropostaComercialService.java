package com.brunoxabreu.commercial_bpms.service;

import com.brunoxabreu.commercial_bpms.domain.model.PropostaComercial;
import com.brunoxabreu.commercial_bpms.domain.repository.PropostaComercialRepository;
import io.camunda.zeebe.client.ZeebeClient;
import io.camunda.zeebe.client.api.response.ProcessInstanceEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Map;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class PropostaComercialService {

    private final PropostaComercialRepository propostaRepository;
    private final ZeebeClient zeebeClient;

    @Transactional
    public PropostaComercial iniciarProcesso(PropostaComercial proposta) {
        log.info("Iniciando processo para proposta: {}", proposta.getNumeroProposta());
        
        // Gera ID único para a proposta
        proposta.setNumeroProposta("PROP-" + UUID.randomUUID().toString().substring(0, 8));
        proposta.setStatus("EM_ANALISE");
        
        // Salva a proposta
        proposta = propostaRepository.save(proposta);
        
        // Inicia o processo no Camunda
        ProcessInstanceEvent processInstance = zeebeClient.newCreateInstanceCommand()
                .bpmnProcessId("proposta-comercial")
                .latestVersion()
                .variables(Map.of(
                        "propostaId", proposta.getId(),
                        "numeroProposta", proposta.getNumeroProposta(),
                        "cliente", proposta.getCliente(),
                        "valorTotal", proposta.getValorTotal()
                ))
                .send()
                .join();
        
        // Atualiza a proposta com o ID do processo
        proposta.setProcessoInstanceId(processInstance.getProcessInstanceKey().toString());
        return propostaRepository.save(proposta);
    }

    @Transactional
    public PropostaComercial aprovarProposta(Long propostaId) {
        log.info("Aprovando proposta: {}", propostaId);
        
        PropostaComercial proposta = propostaRepository.findById(propostaId)
                .orElseThrow(() -> new RuntimeException("Proposta não encontrada"));
        
        // Atualiza status
        proposta.setStatus("APROVADA");
        proposta.setDataAprovacao(java.time.LocalDateTime.now());
        
        // Completa a tarefa no processo
        zeebeClient.newPublishMessageCommand()
                .messageName("proposta-aprovada")
                .correlationKey(proposta.getProcessoInstanceId())
                .variables(Map.of("aprovado", true))
                .send()
                .join();
        
        return propostaRepository.save(proposta);
    }

    @Transactional
    public PropostaComercial rejeitarProposta(Long propostaId, String observacoes) {
        log.info("Rejeitando proposta: {}", propostaId);
        
        PropostaComercial proposta = propostaRepository.findById(propostaId)
                .orElseThrow(() -> new RuntimeException("Proposta não encontrada"));
        
        // Atualiza status
        proposta.setStatus("REJEITADA");
        proposta.setObservacoes(observacoes);
        
        // Completa a tarefa no processo
        zeebeClient.newPublishMessageCommand()
                .messageName("proposta-rejeitada")
                .correlationKey(proposta.getProcessoInstanceId())
                .variables(Map.of(
                        "aprovado", false,
                        "observacoes", observacoes
                ))
                .send()
                .join();
        
        return propostaRepository.save(proposta);
    }
} 